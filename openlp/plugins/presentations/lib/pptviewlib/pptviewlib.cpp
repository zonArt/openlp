/*
 *   PPTVIEWLIB - Control PowerPoint Viewer 2003/2007 (for openlp.org)
 *   Copyright (C) 2008 Jonathan Corwin
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


#define WIN32_LEAN_AND_MEAN  
#include <windows.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "pptviewlib.h"

// Because of the callbacks used by SetWindowsHookEx, the memory used needs to 
// be sharable across processes (callbacks are done from a different process)
// Therefore use data_seg with RWS memory.
//
// See http://msdn.microsoft.com/en-us/library/aa366551(VS.85).aspx for 
// alternative method of holding memory, removing fixed limits which would allow
// dynamic number of items, rather than a fixed number. Use a Local\ mapping, 
// since global has UAC issues in Vista.

#pragma data_seg(".PPTVIEWLIB")
PPTVIEW pptviews[MAX_PPTS] = {NULL};
HHOOK global_hook = NULL;
BOOL debug = FALSE;
#pragma data_seg()
#pragma comment(linker, "/SECTION:.PPTVIEWLIB,RWS")

HINSTANCE h_instance = NULL;

BOOL APIENTRY DllMain(HMODULE h_module, DWORD ul_reason_for_call, 
	LPVOID lp_reserved)
{
    h_instance = (HINSTANCE)h_module;
	switch (ul_reason_for_call)
	{
		case DLL_PROCESS_ATTACH:
			DEBUG("PROCESS_ATTACH\n");
			break;
		case DLL_THREAD_ATTACH:
			DEBUG("THREAD_ATTACH\n");
			break;
		case DLL_THREAD_DETACH:
			DEBUG("THREAD_DETACH\n");
			break;
		case DLL_PROCESS_DETACH:
			// Clean up... hopefully there is only the one process attached? 
			// We'll find out soon enough during tests!
			DEBUG("PROCESS_DETACH\n");
			for(int i = 0; i < MAX_PPTS; i++)
				ClosePPT(i);
			break;
	}
	return TRUE;
}
DllExport void SetDebug(BOOL on_off)
{
	printf("SetDebug\n");
	debug = on_off;
	DEBUG("enabled\n");
}

DllExport BOOL CheckInstalled()
{
	DEBUG("CheckInstalled\n");
	char cmd_line[MAX_PATH * 2];

	return GetPPTViewerPath(cmd_line, sizeof(cmd_line));
}

// Open the PointPoint, count the slides and take a snapshot of each slide
// for use in previews
// previewpath is a prefix for the location to put preview images of each slide.
// "<n>.bmp" will be appended to complete the path. E.g. "c:\temp\slide" would 
// create "c:\temp\slide1.bmp" slide2.bmp, slide3.bmp etc.
// It will also create a *info.txt containing information about the ppt
DllExport int OpenPPT(char *filename, HWND h_parent_wnd, RECT rect, 
	char *preview_path)
{
	int id;

	DEBUG("OpenPPT start: %s; %s\n", filename, preview_path);
	DEBUG("OpenPPT start: %u; %i, %i, %i, %i\n", h_parent_wnd, rect.top, 
		rect.left, rect.bottom, rect.right);
	id = -1;
	for(int i = 0; i < MAX_PPTS; i++)
	{
		if(pptviews[i].state == PPT_CLOSED)
		{
			id = i;
			break;
		}
	}
	if(id < 0)
	{
		DEBUG("OpenPPT: Too many PPTs\n");
		return -1;
	}
	BOOL got_info = InitPPTObject(id, filename, h_parent_wnd, rect, 
        preview_path);
	if(!StartPPTView(id))
	{
		ClosePPT(id);
		return -1;
	}
	if(!got_info)
	{
		DEBUG("OpenPPT: Get info\n");
		pptviews[id].steps = 0;
		int steps = 0;
		while(pptviews[id].state == PPT_OPENED)
		{
			if(steps <= pptviews[id].steps)
			{
				Sleep(20);
				DEBUG("OpenPPT: Step %d/%d\n", steps, pptviews[id].steps);
				steps++;
				NextStep(id);
			} 
			Sleep(10);
		}
		DEBUG("OpenPPT: Steps %d, first slide steps %d\n",
			pptviews[id].steps, pptviews[id].first_slide_steps);
		SavePPTInfo(id);
	    if(pptviews[id].state == PPT_CLOSING
            || pptviews[id].slide_count <= 0)
		{
			// We've gone off the end and pptview is closing. 
            // We'll need to start again
	        ClosePPT(id);
			got_info = InitPPTObject(id, filename, h_parent_wnd, rect, 
                preview_path);
			if(got_info) 
				got_info = StartPPTView(id);
			if(!got_info)
			{
				ClosePPT(id);
				return -1;
			}
	    }
		else
       		RestartShow(id);
	}
	if(got_info)
	{
		DEBUG("OpenPPT: Info loaded, no refresh\n");
		pptviews[id].state = PPT_LOADED;
		Resume(id);
	}
	if(pptviews[id].mhook != NULL)	
	    UnhookWindowsHookEx(pptviews[id].mhook);
    pptviews[id].mhook = NULL;
	DEBUG("OpenPPT: Exit: id=%i\n", id);
	return id;
}

BOOL InitPPTObject(int id, char *filename, HWND h_parent_wnd, 
	RECT rect, char *preview_path)
{
	DEBUG("InitPPTObject %d\n", id);
	memset(&pptviews[id], 0, sizeof(pptviews));
	strcpy_s(pptviews[id].filename, MAX_PATH, filename);
	strcpy_s(pptviews[id].preview_path, MAX_PATH, preview_path);
	pptviews[id].state = PPT_CLOSED;
	pptviews[id].slide_count = 0;
	pptviews[id].current_slide = 0;
	pptviews[id].first_slide_steps = 0;
	pptviews[id].guess = 1;
	for(int i = 0; i < MAX_SLIDES; i++)
		pptviews[id].slide_no[i] = 0;
	pptviews[id].h_parent_wnd = h_parent_wnd;
	pptviews[id].h_wnd = NULL;
	pptviews[id].h_wnd_input = NULL;
	if(h_parent_wnd != NULL && rect.top == 0 && rect.bottom == 0
		&& rect.left == 0 && rect.right == 0)
	{
		LPRECT wnd_rect = NULL;
		GetWindowRect(h_parent_wnd, wnd_rect);
		pptviews[id].rect.top = 0;
		pptviews[id].rect.left = 0;
		pptviews[id].rect.bottom = wnd_rect->bottom - wnd_rect->top;
		pptviews[id].rect.right = wnd_rect->right - wnd_rect->left;
	}
	else
	{
		pptviews[id].rect.top = rect.top;
		pptviews[id].rect.left = rect.left;
		pptviews[id].rect.bottom = rect.bottom;
		pptviews[id].rect.right = rect.right;
	}
	BOOL got_info = GetPPTInfo(id);
	return got_info;
}
BOOL StartPPTView(int id)
{
	/* 
	 * I'd really like to just hook on the new threadid. However this always gives
	 * error 87. Perhaps I'm hooking to soon? No idea... however can't wait
	 * since I need to ensure I pick up the WM_CREATE as this is the only
	 * time the window can be resized in such away the content scales correctly
	 *
	 * hook = SetWindowsHookEx(WH_CBT,CbtProc,hInstance,pi.dwThreadId);
	 */
	DEBUG("StartPPTView\n");
	STARTUPINFO si;
	PROCESS_INFORMATION pi;
	char cmd_line[MAX_PATH * 2];

	if(global_hook != NULL)
		UnhookWindowsHookEx(global_hook);
	global_hook = SetWindowsHookEx(WH_CBT, CbtProc, h_instance, NULL);
	if(global_hook == 0)
	{
		DEBUG("OpenPPT: SetWindowsHookEx failed\n");
		ClosePPT(id);
		return FALSE;
	}
	if(GetPPTViewerPath(cmd_line, sizeof(cmd_line)) == FALSE)
	{
		DEBUG("OpenPPT: GetPPTViewerPath failed\n");
		return FALSE;
	}
	pptviews[id].state = PPT_STARTED;
    Sleep(10); 
	strcat_s(cmd_line, MAX_PATH * 2, "/F /S \"");
	strcat_s(cmd_line, MAX_PATH * 2, pptviews[id].filename);
	strcat_s(cmd_line, MAX_PATH * 2, "\"");
	memset(&si, 0, sizeof(si));
	memset(&pi, 0, sizeof(pi));
    DEBUG("Command: %s\n", cmd_line);
	if(!CreateProcess(NULL, cmd_line, NULL, NULL, FALSE, 0, 0, NULL, &si, &pi))
	{
		DEBUG("OpenPPT: CreateProcess failed\n");
		ClosePPT(id);
		return FALSE;
	}
	pptviews[id].dw_process_id = pi.dwProcessId;
	pptviews[id].dw_thread_id = pi.dwThreadId;
	pptviews[id].h_thread = pi.hThread;
	pptviews[id].h_process = pi.hProcess;
	while(pptviews[id].state == PPT_STARTED)
		Sleep(10);
	return TRUE;
}

// Load information about the ppt from an info.txt file.
// Format:
// version
// filedate
// filesize
// slidecount
// first slide steps
BOOL GetPPTInfo(int id)
{
	struct _stat file_stats;
	char info[MAX_PATH];
	FILE* p_file;
	char buf[100];

	DEBUG("GetPPTInfo: start\n");
	if(_stat(pptviews[id].filename, &file_stats) != 0)
		return FALSE;
	sprintf_s(info, MAX_PATH, "%sinfo.txt", pptviews[id].preview_path);
	int err = fopen_s(&p_file, info, "r");
	if(err != 0)
	{
		DEBUG("GetPPTInfo: file open failed - %d\n", err);
		return FALSE;
	}
	fgets(buf, 100, p_file); // version == 1
	fgets(buf, 100, p_file); 
	if(file_stats.st_mtime != atoi(buf))
	{
		fclose (p_file);
		return FALSE;
	}
	fgets(buf, 100, p_file);	
	if(file_stats.st_size != atoi(buf))
	{
		fclose(p_file);
		return FALSE;
	}
	fgets(buf, 100, p_file); // slidecount
	int slide_count = atoi(buf);
	fgets(buf, 100, p_file); // first slide steps
	int first_slide_steps = atoi(buf);
	// check all the preview images still exist
	for(int i = 1; i <= slide_count; i++)
	{
		sprintf_s(info, MAX_PATH, "%s%i.bmp", 
			pptviews[id].preview_path, i);
		if(GetFileAttributes(info) == INVALID_FILE_ATTRIBUTES)
			return FALSE;
	}
	fclose(p_file);
	pptviews[id].slide_count = slide_count;
	pptviews[id].first_slide_steps = first_slide_steps;
	DEBUG("GetPPTInfo: exit ok\n");
	return TRUE;
}

BOOL SavePPTInfo(int id)
{
	struct _stat file_stats;
	char info[MAX_PATH];
	FILE* p_file;

	DEBUG("SavePPTInfo: start\n");
	if(_stat(pptviews[id].filename, &file_stats) != 0)
	{
		DEBUG("SavePPTInfo: stat of %s failed\n", pptviews[id].filename);
		return FALSE;
	}
	sprintf_s(info, MAX_PATH, "%sinfo.txt", pptviews[id].preview_path);
	int err = fopen_s(&p_file, info, "w");
	if(err != 0)
	{
		DEBUG("SavePPTInfo: fopen of %s failed%i\n", info, err);
		return FALSE;
	}
	else
	{
		DEBUG("SavePPTInfo: fopen of %s succeeded\n", info);
	}
	fprintf(p_file, "1\n");
	fprintf(p_file, "%u\n", file_stats.st_mtime);
	fprintf(p_file, "%u\n", file_stats.st_size);
	fprintf(p_file, "%u\n", pptviews[id].slide_count);
	fprintf(p_file, "%u\n", pptviews[id].first_slide_steps);
	fclose(p_file);
	DEBUG("SavePPTInfo: exit ok\n");
	return TRUE;
}

// Get the path of the PowerPoint viewer from the registry
BOOL GetPPTViewerPath(char *pptviewer_path, int str_size)
{
	HKEY h_key;
	DWORD dw_type, dw_size;
	LRESULT l_result;

	DEBUG("GetPPTViewerPath: start\n");
	if((RegOpenKeyEx(HKEY_CLASSES_ROOT, 
		"PowerPointViewer.Show.12\\shell\\Show\\command", 
		0, KEY_READ, &h_key) != ERROR_SUCCESS)
        && (RegOpenKeyEx(HKEY_CLASSES_ROOT, 
        "Applications\\PPTVIEW.EXE\\shell\\open\\command", 
        0, KEY_READ, &h_key) != ERROR_SUCCESS)
        && (RegOpenKeyEx(HKEY_CLASSES_ROOT, 
        "Applications\\PPTVIEW.EXE\\shell\\Show\\command", 
        0, KEY_READ, &h_key) != ERROR_SUCCESS))
    {
        return FALSE;
    }
	dw_type = REG_SZ;
	dw_size = (DWORD)str_size;
	l_result = RegQueryValueEx(h_key, NULL, NULL, &dw_type, 
		(LPBYTE)pptviewer_path, &dw_size);
	RegCloseKey(h_key);
	if(l_result != ERROR_SUCCESS)
		return FALSE;
    // remove "%1" from the end of the key value
	pptviewer_path[strlen(pptviewer_path) - 4] = '\0';	
	DEBUG("GetPPTViewerPath: exit ok\n");
	return TRUE;
}

// Unhook the Windows hook 
void Unhook(int id)
{
	DEBUG("Unhook: start %d\n", id);
	if(pptviews[id].hook != NULL)	
		UnhookWindowsHookEx(pptviews[id].hook);
	if(pptviews[id].mhook != NULL)	
		UnhookWindowsHookEx(pptviews[id].mhook);
	pptviews[id].hook = NULL;
	pptviews[id].mhook = NULL;
	DEBUG("Unhook: exit ok\n");
}

// Close the PowerPoint viewer, release resources
DllExport void ClosePPT(int id)
{
	DEBUG("ClosePPT: start%d\n", id);
	pptviews[id].state = PPT_CLOSED;
	Unhook(id);
	if(pptviews[id].h_wnd == 0)
		TerminateThread(pptviews[id].h_thread, 0);
	else
		PostMessage(pptviews[id].h_wnd, WM_CLOSE, 0, 0);
	CloseHandle(pptviews[id].h_thread);
	CloseHandle(pptviews[id].h_process);
	memset(&pptviews[id], 0, sizeof(pptviews));
	DEBUG("ClosePPT: exit ok\n");
	return;
}
// Moves the show back onto the display
DllExport void Resume(int id)
{
	DEBUG("Resume: %d\n", id);
	MoveWindow(pptviews[id].h_wnd, pptviews[id].rect.left, 
		pptviews[id].rect.top, 
		pptviews[id].rect.right - pptviews[id].rect.left, 
		pptviews[id].rect.bottom - pptviews[id].rect.top, TRUE);
	Unblank(id);								
}
// Moves the show off the screen so it can't be seen
DllExport void Stop(int id)
{
	DEBUG("Stop:%d\n", id);
	MoveWindow(pptviews[id].h_wnd, -32000, -32000, 
		pptviews[id].rect.right - pptviews[id].rect.left, 
		pptviews[id].rect.bottom - pptviews[id].rect.top, TRUE);
}

// Return the total number of slides
DllExport int GetSlideCount(int id)
{
	DEBUG("GetSlideCount:%d\n", id);
	if(pptviews[id].state == 0)
		return -1;
	else
		return pptviews[id].slide_count;
}

// Return the number of the slide currently viewing
DllExport int GetCurrentSlide(int id)
{
	DEBUG("GetCurrentSlide:%d\n", id);
	if(pptviews[id].state == 0)
		return -1;
	else
		return pptviews[id].current_slide;
}

// Take a step forwards through the show 
DllExport void NextStep(int id)
{
	DEBUG("NextStep:%d (%d)\n", id, pptviews[id].current_slide);
	if(pptviews[id].current_slide > pptviews[id].slide_count)
		return;
	pptviews[id].guess = pptviews[id].current_slide + 1;
	PostMessage(pptviews[id].h_wnd_input, WM_MOUSEWHEEL, 
		MAKEWPARAM(0, -WHEEL_DELTA), 0);
}

// Take a step backwards through the show 
DllExport void PrevStep(int id)
{
	DEBUG("PrevStep:%d (%d)\n", id, pptviews[id].current_slide);
	if(pptviews[id].current_slide > 1)
		pptviews[id].guess = pptviews[id].current_slide - 1;
	PostMessage(pptviews[id].h_wnd_input, WM_MOUSEWHEEL, 
        MAKEWPARAM(0, WHEEL_DELTA), 0);
}

// Blank the show (black screen)
DllExport void Blank(int id)
{	
	// B just toggles blank on/off. However pressing any key unblanks.
	// So send random unmapped letter first (say 'A'), then we can 
	// better guarantee B will blank instead of trying to guess 
	// whether it was already blank or not.
	DEBUG("Blank:%d\n", id);
	HWND h1 = GetForegroundWindow();
	HWND h2 = GetFocus();
	SetForegroundWindow(pptviews[id].h_wnd);
	SetFocus(pptviews[id].h_wnd);
    // slight pause, otherwise event triggering this call may grab focus back!
	Sleep(50);	
	keybd_event((int)'A', 0, 0, 0);
	keybd_event((int)'A', 0, KEYEVENTF_KEYUP, 0);
	keybd_event((int)'B', 0, 0, 0);
	keybd_event((int)'B', 0, KEYEVENTF_KEYUP, 0);
	SetForegroundWindow(h1);
	SetFocus(h2);
    
    // This is the preferred method, but didn't work. Keep it here for
    // documentation if we revisit in the future    
	//PostMessage(pptviews[id].h_wnd_input, WM_KEYDOWN, 'B', 0x00300001);
	//PostMessage(pptviews[id].h_wnd_input, WM_CHAR, 'b', 0x00300001);
	//PostMessage(pptviews[id].h_wnd_input, WM_KEYUP, 'B', 0xC0300001);
}
// Unblank the show 
DllExport void Unblank(int id)
{	
	DEBUG("Unblank:%d\n", id);
	// Pressing any key resumes. 
	// For some reason SendMessage works for unblanking, but not blanking.
    // However keep the commented code for documentation in case we want
    // to revisit later.
    
    //SendMessage(pptviews[id].h_wnd_input, WM_KEYDOWN, 'A', 0);
	SendMessage(pptviews[id].h_wnd_input, WM_CHAR, 'A', 0);
    //SendMessage(pptviews[id].h_wnd_input, WM_KEYUP, 'A', 0);
    //HWND h1 = GetForegroundWindow();
    //HWND h2 = GetFocus();
    ////slight pause, otherwise event triggering this call may grab focus back!
    //Sleep(50);	
    //SetForegroundWindow(pptviews[id].h_wnd);
    //SetFocus(pptviews[id].h_wnd);
    //keybd_event((int)'A', 0, 0, 0);
    //SetForegroundWindow(h1);
    //SetFocus(h2);
}

// Go directly to a slide
DllExport void GotoSlide(int id, int slide_no)
{	
	DEBUG("GotoSlide %i %i:\n", id, slide_no);
	// Did try WM_KEYDOWN/WM_CHAR/WM_KEYUP with SendMessage but didn't work
	// perhaps I was sending to the wrong window? No idea. 
	// Anyway fall back to keybd_event, which is OK as long we makesure
	// the slideshow has focus first
	char ch[10];

	if(slide_no < 0) 
		return;
	pptviews[id].guess = slide_no;
	_itoa_s(slide_no, ch, 10, 10);
	HWND h1 = GetForegroundWindow();
	HWND h2 = GetFocus();
	SetForegroundWindow(pptviews[id].h_wnd);
	SetFocus(pptviews[id].h_wnd);
    // slight pause, otherwise event triggering this call may grab focus back!
	Sleep(50);	
	for(int i = 0; i < 10; i++)
	{
		if(ch[i] == '\0')
			break;
		keybd_event((BYTE)ch[i], 0, 0, 0);
		keybd_event((BYTE)ch[i], 0, KEYEVENTF_KEYUP, 0);
	}
	keybd_event(VK_RETURN, 0, 0, 0);
	keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0);
	SetForegroundWindow(h1);
	SetFocus(h2);

    // I don't know why the below didn't work.
    // Kept here as documentation in case we want to try again in the future
    //
	//for(int i=0;i<10;i++)
	//{
	//	if(ch[i]=='\0') break;
	//	SendMessage(pptviews[id].h_wnd_input, WM_KEYDOWN, ch[i], 0);
	//	SendMessage(pptviews[id].h_wnd_input, WM_CHAR, ch[i], 0);
	//	SendMessage(pptviews[id].h_wnd_input, WM_KEYUP, ch[i], 0);
	//}
	//SendMessage(pptviews[id].h_wnd_input, WM_KEYDOWN, VK_RETURN, 0);
	//SendMessage(pptviews[id].h_wnd_input, WM_CHAR, VK_RETURN, 0);
	//SendMessage(pptviews[id].h_wnd_input, WM_KEYUP, VK_RETURN, 0);
	//keybd_event(VK_RETURN, 0, 0, 0);
}

// Restart the show from the beginning
DllExport void RestartShow(int id)
{
	// If we just go direct to slide one, then it remembers that all other 
	// slides have been animated, so ends up just showing the completed slides 
	// of those slides that have been animated next time we advance. 
	// Only way I've found to get around this is to step backwards all the way 
	// through. Lets move the window out of the way first so the audience 
    // doesn't see this.
	DEBUG("RestartShow:%d\n", id);
	Stop(id);
	GotoSlide(id, pptviews[id].slide_count);
	while(pptviews[id].current_slide > 1)
	{
		PrevStep(id);
		Sleep(10);
	}
	for(int i = 0; i <= pptviews[id].first_slide_steps; i++)
	{
		PrevStep(id);
		Sleep(10);
	}
	Resume(id);
}

// This hook is started with the PPTVIEW.EXE process and waits for the
// WM_CREATEWND message. At this point (and only this point) can the
// window be resized to the correct size.
// Release the hook as soon as we're complete to free up resources
LRESULT CALLBACK CbtProc(int n_code, WPARAM w_param, LPARAM l_param)
{
	HHOOK hook = global_hook;
    if(n_code == HCBT_CREATEWND)
    {
	    char cs_class_name[16];
        HWND h_curr_wnd = (HWND)w_param;
		DWORD ret_proc_id = NULL;
		GetClassName(h_curr_wnd, cs_class_name, sizeof(cs_class_name));
		if((strcmp(cs_class_name, "paneClassDC") == 0)
		  ||(strcmp(cs_class_name, "screenClass") == 0))
		{
			int id = -1;
			DWORD window_thread = GetWindowThreadProcessId(h_curr_wnd,NULL);
			for(int i = 0; i < MAX_PPTS; i++)
			{
				if(pptviews[i].dw_thread_id == window_thread)
				{
					id = i;
					break;
				}
			}
			if(id >= 0)
			{
				if(strcmp(cs_class_name, "paneClassDC") == 0)
					pptviews[id].h_wnd_input = h_curr_wnd;
				else		
				{
					pptviews[id].h_wnd = h_curr_wnd;
					CBT_CREATEWND* cw = (CBT_CREATEWND*)l_param;
					if(pptviews[id].h_parent_wnd != NULL) 
						cw->lpcs->hwndParent = pptviews[id].h_parent_wnd;
					cw->lpcs->cy = pptviews[id].rect.bottom 
                        - pptviews[id].rect.top;
					cw->lpcs->cx = pptviews[id].rect.right
                        - pptviews[id].rect.left;
					cw->lpcs->y = -32000; 
					cw->lpcs->x = -32000; 
				}
				if((pptviews[id].h_wnd != NULL) 
                    && (pptviews[id].h_wnd_input != NULL))
				{
					UnhookWindowsHookEx(global_hook);
					global_hook = NULL;
					pptviews[id].hook = SetWindowsHookEx(WH_CALLWNDPROC,
						CwpProc, h_instance, pptviews[id].dw_thread_id);
					pptviews[id].mhook = SetWindowsHookEx(WH_GETMESSAGE,
						GetMsgProc, h_instance, pptviews[id].dw_thread_id);
					Sleep(10);
					pptviews[id].state = PPT_OPENED;
				}
			}
		}
    }
	return CallNextHookEx(hook, n_code, w_param, l_param); 
}

// This hook exists whilst the slideshow is loading but only listens on the
// slideshows thread. It listens out for mousewheel events
LRESULT CALLBACK GetMsgProc(int n_code, WPARAM w_param, LPARAM l_param) 
{
	HHOOK hook = NULL;
	MSG *p_msg = (MSG *)l_param;
	DWORD window_thread = GetWindowThreadProcessId(p_msg->hwnd, NULL);
	int id = -1;
	for(int i = 0; i < MAX_PPTS; i++)
	{
		if(pptviews[i].dw_thread_id == window_thread)
		{
			id = i;
			hook = pptviews[id].mhook;
			break;
		}
	}
	if(id >= 0 && n_code == HC_ACTION && w_param == PM_REMOVE 
		&& p_msg->message == WM_MOUSEWHEEL)
    {
		if(pptviews[id].state != PPT_LOADED)
		{
			if(pptviews[id].current_slide == 1)
				pptviews[id].first_slide_steps++;
			pptviews[id].steps++;
		}
    }
    return CallNextHookEx(hook, n_code, w_param, l_param);
}

// This hook exists whilst the slideshow is running but only listens on the
// slideshows thread. It listens out for slide changes, message WM_USER+22.
LRESULT CALLBACK CwpProc(int n_code, WPARAM w_param, LPARAM l_param)
{
	CWPSTRUCT *cwp;
	cwp = (CWPSTRUCT *)l_param;
	HHOOK hook = NULL;
	char filename[MAX_PATH];

	DWORD window_thread = GetWindowThreadProcessId(cwp->hwnd, NULL);
	int id = -1;
	for(int i = 0; i < MAX_PPTS; i++)
	{
		if(pptviews[i].dw_thread_id == window_thread)
		{
			id = i;
			hook = pptviews[id].hook;
			break;
		}
	}
	if((id >= 0) && (n_code == HC_ACTION))
	{
		if(cwp->message == WM_USER + 22)
		{
			if(pptviews[id].state != PPT_LOADED)
			{
				if((pptviews[id].current_slide > 0)
					&& (pptviews[id].preview_path != NULL 
					&& strlen(pptviews[id].preview_path) > 0))
				{
					sprintf_s(filename, MAX_PATH, "%s%i.bmp", 
                        pptviews[id].preview_path, 
						pptviews[id].current_slide);
					CaptureAndSaveWindow(cwp->hwnd, filename);
				}
			}
			if(cwp->wParam == 0)
			{
				if(pptviews[id].current_slide > 0) 
				{
					pptviews[id].state = PPT_LOADED;
					pptviews[id].current_slide = pptviews[id].slide_count + 1;
				}
			} 
			else
			{
				if(pptviews[id].state != PPT_LOADED) 
				{
					if((pptviews[id].current_slide == 0)
						||(pptviews[id].slide_no[pptviews[id].current_slide] 
                        != cwp->wParam))
					{
						if(pptviews[id].slide_no[1] == cwp->wParam)
						{
							pptviews[id].state = PPT_LOADED;
						}
						else
						{
							pptviews[id].current_slide++;
							pptviews[id].slide_count 
                                = pptviews[id].current_slide;
							pptviews[id].slide_no[pptviews[id].current_slide] 
                                = cwp->wParam;
						}
					}
				}
				else 
				{
					if(pptviews[id].guess > 0 
						&& pptviews[id].slide_no[pptviews[id].guess] == 0)
					{
						pptviews[id].current_slide = 0;
					}
					for(int i = 1; i < pptviews[id].slide_count; i++)
					{
						if(pptviews[id].slide_no[i] == cwp->wParam)
						{
							pptviews[id].current_slide = i;
							break;
						}
					}
					if(pptviews[id].current_slide == 0)
					{
						pptviews[id].slide_no[pptviews[id].guess] = cwp->wParam;
						pptviews[id].current_slide = pptviews[id].guess;
					}
				}
			}
		}
		if((pptviews[id].state != PPT_CLOSED) 
			&& (cwp->message == WM_CLOSE || cwp->message == WM_QUIT))
		{
			pptviews[id].state = PPT_CLOSING;
		}
	}
	return CallNextHookEx(hook, n_code, w_param, l_param); 
}

// Take a screenshot of the current slide, and create a .bmp
VOID CaptureAndSaveWindow(HWND h_wnd, CHAR* filename)
{
	HBITMAP h_bmp;
	if ((h_bmp = CaptureWindow(h_wnd)) == NULL) 
		return;

	RECT client;
	GetClientRect(h_wnd, &client);
	UINT ui_bytes_per_row = 3 * client.right; // RGB takes 24 bits
	UINT ui_remainder_for_padding;

	if ((ui_remainder_for_padding = ui_bytes_per_row % sizeof (DWORD)) > 0) 
		ui_bytes_per_row += (sizeof(DWORD) - ui_remainder_for_padding);

	UINT ui_bytes_per_all_rows = ui_bytes_per_row * client.bottom;
	PBYTE p_data_bits;

	if ((p_data_bits = new BYTE[ui_bytes_per_all_rows]) != NULL) 
	{
		BITMAPINFOHEADER bmi = {0};
		BITMAPFILEHEADER bmf = {0};

		// Prepare to get the data out of HBITMAP:
		bmi.biSize = sizeof(bmi);
		bmi.biPlanes = 1;
		bmi.biBitCount = 24;
		bmi.biHeight = client.bottom;
		bmi.biWidth = client.right;

		// Get it:
		HDC h_dc = GetDC(h_wnd);
		GetDIBits(h_dc, h_bmp, 0, client.bottom, p_data_bits, 
			(BITMAPINFO*) &bmi, DIB_RGB_COLORS);
		ReleaseDC(h_wnd, h_dc);

		// Fill the file header:
		bmf.bfOffBits = sizeof(bmf) + sizeof(bmi);
		bmf.bfSize = bmf.bfOffBits + ui_bytes_per_all_rows;
		bmf.bfType = 0x4D42;

		// Writing:
		FILE* p_file;
		int err = fopen_s(&p_file, filename, "wb");
		if (err == 0) 
		{
			fwrite(&bmf, sizeof(bmf), 1, p_file);
			fwrite(&bmi, sizeof(bmi), 1, p_file);
			fwrite(p_data_bits, sizeof(BYTE), ui_bytes_per_all_rows, p_file);
			fclose(p_file);
		} 
		delete [] p_data_bits;
	}
	DeleteObject(h_bmp);
}
HBITMAP CaptureWindow(HWND h_wnd)
{
	HDC h_dc;
	BOOL b_ok = FALSE;
	HBITMAP h_image = NULL;

	h_dc = GetDC(h_wnd);
	RECT rc_client;
	GetClientRect(h_wnd, &rc_client);
	if((h_image = CreateCompatibleBitmap(h_dc, rc_client.right, 
        rc_client.bottom)) != NULL)
	{
		HDC h_mem_dc;
		HBITMAP h_dc_bmp;

		if((h_mem_dc = CreateCompatibleDC (h_dc)) != NULL) 
		{
			h_dc_bmp = (HBITMAP)SelectObject(h_mem_dc, h_image);
			HMODULE h_lib = LoadLibrary("User32");
			// PrintWindow works for windows outside displayable area
			// but was only introduced in WinXP. BitBlt requires the window  
			// to be topmost and within the viewable area of the display
			if(GetProcAddress(h_lib, "PrintWindow") == NULL)
			{
				SetWindowPos(h_wnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOSIZE); 
				BitBlt (h_mem_dc, 0, 0, rc_client.right, rc_client.bottom, 
                    h_dc, 0, 0, SRCCOPY);
				SetWindowPos(h_wnd, HWND_NOTOPMOST, -32000, -32000, 0, 0, 
                    SWP_NOSIZE); 
			}
			else
			{
				PrintWindow(h_wnd, h_mem_dc, 0);
			}
			SelectObject(h_mem_dc, h_dc_bmp);
			DeleteDC(h_mem_dc);
			b_ok = TRUE;
		}
	}
	ReleaseDC(h_wnd, h_dc);
	if(!b_ok) 
	{
		if (h_image) 
		{
			DeleteObject(h_image);
			h_image = NULL;
		}
	}
	return h_image;
}