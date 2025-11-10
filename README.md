# Задание 1 — sys-info-win

## Формулировка

*Примеры приведены для С++, но вы можете использовать любой другой язык, где можно использовать Win32 API.*

Научиться работать с Windows API для получения системной информации, реализовать структурированный и надёжный код, который:

- Обрабатывает все возможные ошибки корректно,
- Даёт студенту понимание, как устроена система "под капотом".

Напишите программу sys-info-win для ОС Windows, которая бы выводила в консоль информацию о компьютере на котором она запущена:

- Версия операционной системы.
  - Используйте IsWindows10OrGreater() и аналоги из VersionHelpers.h
- Размер виртуальной и физической памяти, а также использование памяти в процентах.
- Количество ядер процессора
- Имя компьютера и имя пользователя
- Архитектура процессора (x86, x64, ARM)
- Размер файла подкачки (функция `GetPerformanceInfo`)
- Список логических дисков + их объёмы

#### Пример выводимой информации

```txt
OS: Windows 10 or Greater
Computer Name: DESKTOP-12345
User: Ivan Ivanov
Architecture: x64 (AMD64)
RAM: 6417MB / 7796MB
Virtual Memory: 16000MB
Memory Load: 47%
Pagefile: 20480MB / 32000MB

Processors: 16
Drives:
  - C:\  (NTFS): 114 GB free / 237 GB total
  - D:\  (NTFS): 80 GB free / 100 GB total
```

#### Подсказки

Начиная с Windows 8.1 Microsoft не рекомендует приложениям привязываться к версии операционной системы,
поэтому функции вроде [`GetVersionEx`](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getversionexw)
могут возвращать недостоверную информацию о версии операционной системы.

Используйте [вспомогательные функции Windows](https://learn.microsoft.com/en-us/windows/win32/sysinfo/version-helper-apis),
чтобы узнать информации о версии ОС.
Для получения актуальной информации используйте функцию [RtlGetVersion](https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-rtlgetversion?redirectedfrom=MSDN).

Узнать количество процессоров можно функцией [`GetSystemInfo`](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getsysteminfo)
и [`GetNativeSystemInfo`](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getnativesysteminfo).

Узнать информацию о памяти компьютера можно функций [`GlobalMemoryStatusEx`](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-globalmemorystatusex).

Размер файла подкачки можно получить функцией [GetPerformanceInfo](https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getperformanceinfo).

Информацию о дисках можно получить функциями `GetLogicalDriveStrings` и `GetDiskFreeSpaceEx`.

## Алгоритм решения

1. Импортировать встроенный модуль для вызова функций из DLL (WinAPI)
1. Импортировать модуль для информации о платформе
1. Импортировать типы данных Windows API (DWORD, WCHAR, HANDLE и т.д.)
1. Определить структуру RTL_OSVERSIONINFOW, как в C (LayoutKind.Sequential)
1. Загрузить библиотеку ntdll.dll и объявить RtlGetVersion
1. Написать функцию для возвращения строки с версией ОС
1. Получить информация о памяти через GlobalMemoryStatusEx
1. Написать метод для заполнения и возвращения структуры памяти
1. 