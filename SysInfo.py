import platform
import os
import sys

class SysInfo:
    def __init__(self):
        self.os_name = platform.system()

    # Название ОС
    def GetOSName(self) -> str:
        return self.os_name

    # Версия ОС
    def GetOSVersion(self) -> str:
        return platform.version()

    # Количество процессоров
    def GetProcessorCount(self) -> int:
        return os.cpu_count()

    # Общая память (байты)
    def GetTotalMemory(self) -> int:
        if self.os_name == "Windows":
            # Используем ctypes → WinAPI
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]

            mem = MEMORYSTATUSEX()
            mem.dwLength = ctypes.sizeof(mem)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
            return mem.ullTotalPhys

        else:
            # Linux → читаем /proc/meminfo
            try:
                with open("/proc/meminfo") as f:
                    for line in f:
                        if "MemTotal:" in line:
                            return int(line.split()[1]) * 1024  # kB -> bytes
            except:
                pass

    # Свободная память (байты)
    def GetFreeMemory(self) -> int:
        if self.os_name == "Windows":
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]

            mem = MEMORYSTATUSEX()
            mem.dwLength = ctypes.sizeof(mem)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
            return mem.ullAvailPhys

        else:
            # Linux
            try:
                with open("/proc/meminfo") as f:
                    for line in f:
                        if "MemAvailable:" in line:
                            return int(line.split()[1]) * 1024
            except:
                pass
