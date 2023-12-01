//
// Created by iext13 on 01.12.23.
//

#include "ckikers.h"
#include <iostream>
#include <Windows.h>

int main() {
    while (true) {
        // Координаты клика
        int x = 100;
        int y = 200;

        // Нажатие левой кнопки мыши
        mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0);

        // Ожидание некоторого времени
        Sleep(100);

        // Отпускание левой кнопки мыши
        mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0);

        // Ожидание перед следующим кликом
        Sleep(0.01);
    }

    return 0;
}
