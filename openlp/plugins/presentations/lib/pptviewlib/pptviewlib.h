
#define DllExport extern "C"  __declspec(dllexport) 
#define DEBUG(...)  if(debug) printf(__VA_ARGS__)

enum PPTVIEWSTATE {PPT_CLOSED, PPT_STARTED, PPT_OPENED, 
    PPT_LOADED, PPT_CLOSING};

DllExport int OpenPPT(char *filename, HWND h_parent_wnd, RECT rect, 
    char *preview_path);
DllExport BOOL CheckInstalled();
DllExport void ClosePPT(int id);
DllExport int GetCurrentSlide(int id);
DllExport int GetSlideCount(int id);
DllExport void NextStep(int id);
DllExport void PrevStep(int id);
DllExport void GotoSlide(int id, int slide_no);
DllExport void RestartShow(int id);
DllExport void Blank(int id);
DllExport void Unblank(int id);
DllExport void Stop(int id);
DllExport void Resume(int id);
DllExport void SetDebug(BOOL on_off);

LRESULT CALLBACK CbtProc(int n_code, WPARAM w_param, LPARAM l_param);
LRESULT CALLBACK CwpProc(int n_code, WPARAM w_param, LPARAM l_param);
LRESULT CALLBACK GetMsgProc(int n_code, WPARAM w_param, LPARAM l_param);
BOOL GetPPTViewerPath(char *pptviewer_path, int str_size);
HBITMAP CaptureWindow (HWND h_wnd);
VOID SaveBitmap (CHAR* filename, HBITMAP h_bmp);
VOID CaptureAndSaveWindow(HWND h_wnd, CHAR* filename);
BOOL GetPPTInfo(int id);
BOOL SavePPTInfo(int id);
BOOL InitPPTObject(int id, char *filename, HWND h_parent_wnd, 
	RECT rect, char *preview_path);
BOOL StartPPTView(int id);

void Unhook(int id);

#define MAX_PPTS 16
#define MAX_SLIDES 256

struct PPTVIEW 
{
	HHOOK hook;
	HHOOK mhook;
	HWND h_wnd;         // The main pptview window 
	HWND h_wnd_input;   // A child pptview window which takes windows messages
	HWND h_parent_wnd;
	HANDLE h_process;
	HANDLE h_thread;
	DWORD dw_process_id;
	DWORD dw_thread_id;
	RECT rect;
	int slide_count;
	int current_slide;
	int first_slide_steps;
	int steps;
	int guess;  // What the current slide might be, based on the last action
	char filename[MAX_PATH];
	char preview_path[MAX_PATH];
	int slide_no[MAX_SLIDES];
	PPTVIEWSTATE state;
};
