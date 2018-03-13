#pragma comment(lib,"KeyCall.lib") 
extern "C" _declspec(dllimport) int _stdcall KeySendChar(char * AData);
extern "C" _declspec(dllimport) int _stdcall MouseDown(byte AKey);
extern "C" _declspec(dllimport) int _stdcall MouseMove(byte AKey, int AX, int AY);
extern "C" _declspec(dllimport) int _stdcall MouseMoveTo(byte AKey, int AX, int AY);
extern "C" _declspec(dllimport) int _stdcall MouseMoveToEx(byte AKey, int AX, int AY);
extern "C" _declspec(dllimport) int _stdcall MouseClick(byte AKey);
extern "C" _declspec(dllimport) int _stdcall MouseDbClick(byte AKey);
extern "C" _declspec(dllimport) int _stdcall KeyDown(byte KeyCtrl, char * AData);
extern "C" _declspec(dllimport) int _stdcall KeyDownEx(char * AData);
extern "C" _declspec(dllimport) int _stdcall KeyUp(void);
extern "C" _declspec(dllimport) int _stdcall KeyDownUp(byte KeyCtrl, char * AData);
extern "C" _declspec(dllimport) int _stdcall KeyDownUpEx(char * AData);
extern "C" _declspec(dllimport) int _stdcall MouseKeyDownEx(char * AData);
extern "C" _declspec(dllimport) int _stdcall MouseKeyDownUpEx(char * AData);
extern "C" _declspec(dllimport) int _stdcall GetKeyDev(void);
extern "C" _declspec(dllimport) int _stdcall KeybdEvent(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);
extern "C" _declspec(dllimport) int _stdcall MouseEvent(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);
