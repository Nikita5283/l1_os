from SysInfo import SysInfo

def bytes_to_mb(b):
    return b // (1024 * 1024)

def main():
    info = SysInfo()

    print("OS:", info.GetOSName())
    print("Version:", info.GetOSVersion())
    print("Processors:", info.GetProcessorCount())

    total = info.GetTotalMemory()
    free = info.GetFreeMemory()

    print(f"Total Memory: {bytes_to_mb(total)} MB")
    print(f"Free Memory:  {bytes_to_mb(free)} MB")

if __name__ == "__main__":
    main()
