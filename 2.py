import os              # Работа с ОС: пути, statvfs, файл системы
import platform        # Системная информация: ядро, архитектура
import getpass         # Получение имени пользователя
import socket          # Получение hostname
import psutil          # Информация о памяти, swap, CPU

def read_os_release():
    info = {}          # Словарь для хранения данных из /etc/os-release
    try:
        with open("/etc/os-release") as f:   # Открываем файл с информацией о дистрибутиве
            for line in f:                  # Читаем каждую строку
                if "=" in line:             # Пропускаем строки без ключ=значение
                    key, val = line.rstrip().split("=", 1)  # Разделяем на ключ и значение
                    info[key] = val.strip('"')              # Сохраняем, убирая кавычки
    except:
        pass            # Если файла нет — просто игнорируем
    return info         # Возвращаем словарь с данными

def read_loadavg():
    try:
        with open("/proc/loadavg") as f:     # Файл со средней загрузкой CPU
            load = f.read().split()[:3]      # Берём первые 3 значения
            return tuple(load)               # Возвращаем как кортеж
    except:
        return None

def read_mounts():
    mounts = []                               # Список точек монтирования
    try:
        with open("/proc/mounts") as f:        # Файл со всеми смонтированными FS
            for line in f:                     # Каждая строка — одна FS
                parts = line.split()           # Разбиваем строку
                if len(parts) >= 3:            # Проверяем, что есть путь и тип FS
                    mounts.append((parts[1], parts[2]))  # Добавляем (путь, тип)
    except:
        pass
    return mounts

def statvfs_info(path):
    try:
        st = os.statvfs(path)                 # Получаем статистику FS
        free = st.f_bavail * st.f_frsize      # Доступное пространство
        total = st.f_blocks * st.f_frsize     # Общее пространство
        return free, total
    except:
        return None, None                     # Если ошибка — вернуть пустые значения

def read_virtual_memory():
    try:
        with open("/proc/meminfo") as f:     # Файл с информацией о памяти
            for line in f:
                if line.startswith("VmallocTotal"):   # Ищем строку виртуальной памяти
                    parts = line.split()
                    kb = int(parts[1])       # Значение в килобайтах
                    return kb // 1024        # Переводим в мегабайты
    except:
        pass
    return None

def main():
    # OS and kernel
    os_info = read_os_release()                 # Данные о дистрибутиве
    kernel = platform.release()                 # Версия ядра Linux
    arch = platform.machine()                   # Архитектура CPU
    hostname = socket.gethostname()             # Имя компьютера
    user = getpass.getuser()                    # Имя текущего пользователя

    print(f"OS: {os_info.get('PRETTY_NAME', 'Unknown')}")     # Вывод ОС
    print(f"Kernel: Linux {kernel}")                           # Ядро
    print(f"Architecture: {arch}")                             # Архитектура
    print(f"Hostname: {hostname}")                             # Хостнейм
    print(f"User: {user}")                                     # Пользователь

    # RAM & swap (через psutil)
    vm = psutil.virtual_memory()                               # Информация о RAM
    swap = psutil.swap_memory()                                # Информация о swap
    print(f"RAM: {vm.available // (1024*1024)}MB free / {vm.total // (1024*1024)}MB total")
    print(f"Swap: {swap.free // (1024*1024)}MB free / {swap.total // (1024*1024)}MB total")

    # Virtual memory
    vmem = read_virtual_memory()                                # Читаем VmallocTotal
    if vmem:
        print(f"Virtual memory: {vmem} MB")

    # CPU
    print(f"Processors: {os.cpu_count()}")                      # Логические ядра

    # Load average
    load = read_loadavg()
    if load:
        print(f"Load average: {', '.join(load)}")               # Средняя загрузка CPU

    # Drives
    print("Drives:")
    for mount, fstype in read_mounts():                         # Для каждого mountpoint
        free, total = statvfs_info(mount)                       # Получить свободно/всего
        if free is None:
            continue                                             # Пропустить недоступные FS
        free_gb = round(free / (1024**3), 2)                    # Перевод в ГБ
        total_gb = round(total / (1024**3), 2)
        print(f"  {mount:10} {fstype:8} {free_gb}GB free / {total_gb}GB total")  # Вывод

if __name__ == "__main__":
    main()  # Запуск main()
