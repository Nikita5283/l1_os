import ctypes  # модуль для вызова функций из DLL
import platform  # модуль для информации о платформе
from ctypes import wintypes  # импорт типов данных Windows API (DWORD, WCHAR, HANDLE и т.д.)

# 1. Получение версии Windows через RtlGetVersion

# Определяем структуру RTL_OSVERSIONINFOW, как в C
class RTL_OSVERSIONINFOW(ctypes.Structure):
    _fields_ = [
        ("dwOSVersionInfoSize", wintypes.DWORD), # размер структуры (нужно заполнить перед вызовом)
        ("dwMajorVersion", wintypes.DWORD),  # основная версия ОС (например 10 для Windows 10)
        ("dwMinorVersion", wintypes.DWORD), # минорная версия ОС
        ("dwBuildNumber", wintypes.DWORD), # номер сборки Windows
        ("szCSDVersion", wintypes.WCHAR * 128) # строка CSD (Service Pack или доп.инфо)
    ]

RtlGetVersion = ctypes.WinDLL("ntdll").RtlGetVersion  # получаем функцию RtlGetVersion из библиотеки ntdll.dll
RtlGetVersion.argtypes = [ctypes.POINTER(RTL_OSVERSIONINFOW)]  # функция принимает указатель на нашу структуру
RtlGetVersion.restype = wintypes.DWORD  # указываем возвращаемый тип — DWORD (32-битное целое)

def get_windows_version():
    """Возвращает строку с версией ОС"""
    info = RTL_OSVERSIONINFOW()  # создаём экземпляр структуры для заполнения
    info.dwOSVersionInfoSize = ctypes.sizeof(info)  # записываем размер структуры (требование API)
    RtlGetVersion(ctypes.byref(info))  # вызываем функцию, которая заполнит структуру info
    return f"Windows {info.dwMajorVersion}.{info.dwMinorVersion} (Build {info.dwBuildNumber})"  # форматируем строку версии


# 2. Информация о памяти через GlobalMemoryStatusEx

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", wintypes.DWORD),  # длина структуры в байтах
        ("dwMemoryLoad", wintypes.DWORD),  # процент использования физической памяти
        ("ullTotalPhys", ctypes.c_ulonglong),  # общий объём физической памяти (байты)
        ("ullAvailPhys", ctypes.c_ulonglong),  # доступная физическая память (байты)
        ("ullTotalPageFile", ctypes.c_ulonglong),  # общий объём файла подкачки (байты)
        ("ullAvailPageFile", ctypes.c_ulonglong),  # доступная часть файла подкачки (байты)
        ("ullTotalVirtual", ctypes.c_ulonglong),  # общий объём виртуальной памяти (байты)
        ("ullAvailVirtual", ctypes.c_ulonglong),  # доступная виртуальная память (байты)
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),  # зарезервировано (обычно 0)
    ]


GlobalMemoryStatusEx = ctypes.windll.kernel32.GlobalMemoryStatusEx # Получаем ссылку на функцию WinAPI GlobalMemoryStatusEx из библиотеки kernel32.dll

'''
Устанавливаем атрибут argtypes — это список типов аргументов, которые ожидает функция.
В данном случае указываем, что функция принимает один аргумент: указатель на структуру MEMORYSTATUSEX. ctypes.POINTER(MEMORYSTATUSEX) даёт ctypes информацию о том, как конвертировать/проверять передаваемый аргумент при вызове из Python (например, при вызове GlobalMemoryStatusEx(ctypes.byref(mem))).
Правильная настройка argtypes помогает избежать ошибок маршалинга данных и позволяет ctypes автоматически преобразовать переданные объекты в нужный C-тип.
'''
GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(MEMORYSTATUSEX)]

'''
Устанавливаем restype — тип возвращаемого значения функции. Здесь это wintypes.BOOL (обычно 0 — FALSE, ненулевое — TRUE).
По умолчанию ctypes трактует возвращаемое значение как C int. Явное указание restype гарантирует, что возвращаемое значение будет правильно интерпретировано (и, при необходимости, преобразовано в Python-тип).
Это важно, если вы планируете проверять успешность вызова (например, if not GlobalMemoryStatusEx(...):), или если функция возвращает указатель/структуру — тогда restype должен быть соответствующим (например, ctypes.c_void_p или указатель на структуру).
'''
GlobalMemoryStatusEx.restype = wintypes.BOOL


def get_memory_info():
    """Возвращает информацию о памяти (RAM и виртуальная память)"""
    mem = MEMORYSTATUSEX()  # создаём структуру для заполнения
    mem.dwLength = ctypes.sizeof(mem)  # указываем её размер
    GlobalMemoryStatusEx(ctypes.byref(mem))  # вызываем WinAPI для заполнения полей структуры
    return mem  # возвращаем заполненную структуру


# 3. Информация о файле подкачки через GetPerformanceInfo

class PERFORMANCE_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("cb", wintypes.DWORD),  # размер структуры в байтах
        ("CommitTotal", ctypes.c_size_t),  # общее использование commit (в страницах)
        ("CommitLimit", ctypes.c_size_t),  # лимит commit (в страницах)
        ("CommitPeak", ctypes.c_size_t),  # пиковое значение commit
        ("PhysicalTotal", ctypes.c_size_t),  # общее число физических страниц
        ("PhysicalAvailable", ctypes.c_size_t),  # доступные физические страницы
        ("SystemCache", ctypes.c_size_t),  # кэш системы
        ("KernelTotal", ctypes.c_size_t),  # ядро: всего
        ("KernelPaged", ctypes.c_size_t),  # ядро: paged
        ("KernelNonPaged", ctypes.c_size_t),  # ядро: non-paged
        ("PageSize", ctypes.c_size_t),  # размер страниц в байтах
        ("HandleCount", wintypes.DWORD),  # количество дескрипторов
        ("ProcessCount", wintypes.DWORD),  # количество процессов
        ("ThreadCount", wintypes.DWORD),  # количество потоков
    ]

GetPerformanceInfo = ctypes.windll.psapi.GetPerformanceInfo
GetPerformanceInfo.argtypes = [ctypes.POINTER(PERFORMANCE_INFORMATION), wintypes.DWORD]
GetPerformanceInfo.restype = wintypes.BOOL

def get_pagefile_info():
    """Возвращает информацию о файле подкачки"""
    perf = PERFORMANCE_INFORMATION()  # создаём структуру для заполнения
    perf.cb = ctypes.sizeof(perf)  # указываем её размер
    GetPerformanceInfo(ctypes.byref(perf), perf.cb)  # заполняем структуру данными производительности
    used_mb = (perf.CommitTotal * perf.PageSize) // (1024 * 1024)  # пересчёт использованных байт в мегабайты
    limit_mb = (perf.CommitLimit * perf.PageSize) // (1024 * 1024)  # пересчёт лимита в мегабайты
    return used_mb, limit_mb  # возвращаем кортеж (использовано, лимит) в МБ


# 4. Информация о логических дисках через GetLogicalDriveStrings и GetDiskFreeSpaceEx

GetLogicalDriveStringsW = ctypes.windll.kernel32.GetLogicalDriveStringsW
GetLogicalDriveStringsW.argtypes = [wintypes.DWORD, wintypes.LPWSTR]
GetLogicalDriveStringsW.restype = wintypes.DWORD

GetDiskFreeSpaceExW = ctypes.windll.kernel32.GetDiskFreeSpaceExW
GetDiskFreeSpaceExW.argtypes = [
    wintypes.LPCWSTR,
    ctypes.POINTER(ctypes.c_ulonglong),
    ctypes.POINTER(ctypes.c_ulonglong),
    ctypes.POINTER(ctypes.c_ulonglong)
]
GetDiskFreeSpaceExW.restype = wintypes.BOOL

def get_drives():
    """Возвращает список кортежей (буква, свободно, всего)"""
    buf = ctypes.create_unicode_buffer(256)  # создаём буфер для строк с буквами дисков
    GetLogicalDriveStringsW(len(buf), buf)  # заполняем буфер списком дисков через нулевой разделитель
    drives = buf.value.split('\x00')  # разбиваем строку на отдельные пути дисков
    result = []  # список результатов
    for d in drives:  # проходим по всем найденным строкам
        if not d:  # пропускаем пустые строки от разделителя
            continue
        free = ctypes.c_ulonglong(0)  # переменная для свободного пространства
        total = ctypes.c_ulonglong(0)  # переменная для общего пространства
        GetDiskFreeSpaceExW(d, ctypes.byref(free), ctypes.byref(total), None)  # получаем размеры диска
        result.append((d, free.value, total.value))  # добавляем кортеж (буква, свободно, всего) в байтах
    return result  # возвращаем список дисков

# 5. Информация о процессорах

class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
        ("wProcessorArchitecture", wintypes.WORD),
        ("wReserved", wintypes.WORD),
        ("dwPageSize", wintypes.DWORD),
        ("lpMinimumApplicationAddress", wintypes.LPVOID),
        ("lpMaximumApplicationAddress", wintypes.LPVOID),
        ("dwActiveProcessorMask", ctypes.POINTER(ctypes.c_ulong)),
        ("dwNumberOfProcessors", wintypes.DWORD),
        ("dwProcessorType", wintypes.DWORD),
        ("dwAllocationGranularity", wintypes.DWORD),
        ("wProcessorLevel", wintypes.WORD),
        ("wProcessorRevision", wintypes.WORD)
    ]

GetSystemInfo = ctypes.windll.kernel32.GetSystemInfo
GetSystemInfo.argtypes = [ctypes.POINTER(SYSTEM_INFO)]

def get_cpu_count():
    info = SYSTEM_INFO()
    GetSystemInfo(ctypes.byref(info))
    return info.dwNumberOfProcessors


# 5. Основная функция

def main():

    # ОС
    print("OS:", get_windows_version())  # печатаем строку версии ОС
    print("Computer Name:", platform.node())  # имя хоста/компьютера
    print("User:", platform.os.getenv('USERNAME'))  # имя текущего пользователя (через platform.os -> os)
    print("Architecture:", platform.machine())  # архитектура процессора

    # Память
    mem = get_memory_info()  # получаем структуру с информацией о памяти
    print(f"RAM: {(mem.ullTotalPhys - mem.ullAvailPhys)//(1024*1024)}MB used / {mem.ullTotalPhys//(1024*1024)}MB total")  # вывод используемой и общей RAM в МБ
    print(f"Virtual Memory: {mem.ullTotalVirtual//(1024*1024)}MB")  # размер виртуальной памяти в МБ
    print(f"Memory Load: {mem.dwMemoryLoad}%")  # процент загрузки памяти

    # Файл подкачки
    used_pf, limit_pf = get_pagefile_info()  # получаем использованный и лимит файла подкачки (в МБ)
    print(f"Pagefile: {used_pf}MB used / {limit_pf}MB limit")  # вывод информации о файле подкачки

    # Кол-во логических процессоров
    print("Processors:", get_cpu_count())

    # Диски
    print("Drives:")
    for d, free, total in get_drives():  # перебираем найденные диски
        print(f"  - {d}: {free // (1024**3)} GB free / {total // (1024**3)} GB total")  # выводим свободное/общее место в ГБ

if __name__ == "__main__":
    main()  # запускаем main при прямом запуске скрипта
