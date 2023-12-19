from filecmp import cmp, dircmp
from sys import platform
from os import path
from shutil import copy, copytree
import errno
from ctypes import WinDLL, CDLL, WinError, c_size_t, c_uint32, c_void_p, c_char_p, memmove, string_at
from ctypes.wintypes import BOOL, HANDLE, DWORD, LPCSTR, LPCVOID, LPCWSTR, LPVOID
import win32file

from sys import argv
import localSync

def main():
    #print("запуск")
    #print("родительская папка: ")
    #inputPath = input()
    #print("дочерняя папка: ")
    #outputPath = input()
    #localSync(inputPath, outputPath)
    arg1 = argv[1]
    arg2 = argv[2]
    sync_files = localSync.localSync(arg1, arg2)
    sync_files.localSyncData(arg1, arg2)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()