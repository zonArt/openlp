
#define DllExport extern "C"  __declspec( dllexport ) 

enum PPTVIEWSTATE { PPT_CLOSED, PPT_STARTED, PPT_OPENED, PPT_LOADED, PPT_CLOSING};

DllExport int OpenPPT(char *filename, HWND hParentWnd, RECT rect, char *previewpath);
DllExport BOOL CheckInstalled();
DllExport void ClosePPT(int id);
DllExport int GetCurrentSlide(int id);
DllExport int GetSlideCount(int id);
DllExport void NextStep(int id);
DllExport void PrevStep(int id);
DllExport void GotoSlide(int id, int slideno);
DllExport void RestartShow(int id);
DllExport void Blank(int id);
DllExport void Unblank(int id);
DllExport void Stop(int id);
DllExport void Resume(int id);
DllExport void SetDebug(BOOL onoff);

LRESULT CALLBACK CbtProc(int nCode, WPARAM wParam, LPARAM lParam);
LRESULT CALLBACK CwpProc(int nCode, WPARAM wParam, LPARAM lParam);
LRESULT CALLBACK GetMsgProc(int nCode, WPARAM wParam, LPARAM lParam);
BOOL GetPPTViewerPath(char *pptviewerpath, int strsize);
HBITMAP CaptureWindow (HWND hWnd);
VOID SaveBitmap (CHAR* filename, HBITMAP hBmp) ;
VOID CaptureAndSaveWindow(HWND hWnd, CHAR* filename);
BOOL GetPPTInfo(int id);
BOOL SavePPTInfo(int id);


void Unhook(int id);

#define MAX_PPTOBJS 50

struct PPTVIEWOBJ 
{
	HHOOK hook;
	HHOOK mhook;
	HWND hWnd;
	HWND hWnd2;
	HWND hParentWnd;
	HANDLE hProcess;
	HANDLE hThread;
	DWORD dwProcessId;
	DWORD dwThreadId;
	RECT rect;
	int slideCount;
	int currentSlide;
	int firstSlideSteps;
	int steps;
	char filename[MAX_PATH];
	char previewpath[MAX_PATH];
	PPTVIEWSTATE state;
};
