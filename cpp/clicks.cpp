#include <iostream>
#include <windows.h>

int main() {
    // Координаты клика
    int x = 100;
    int y = 200;

    // Количество кликов
    int clicks = 1000;

    // Задержка между кликами в миллисекундах
    int delay = 1;

    // Получаем дескриптор окна
    HWND hwnd = GetDesktopWindow();

    // Переводим координаты клика в экранные координаты
    POINT pt;
    pt.x = x;
    pt.y = y;
    ClientToScreen(hwnd, &pt);

    // Устанавливаем курсор на указанные координаты и кликаем
    SetCursorPos(pt.x, pt.y);
    for (int i = 0; i < clicks; i++) {
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
        Sleep(delay);
    }

    return 0;
}
