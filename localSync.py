from filecmp import cmp, dircmp
import mmap
from sys import platform
from os import O_RDONLY, path
from os.path import getsize
from shutil import copy, copytree
from errno import ENOTDIR
from ctypes import WinDLL, CDLL, c_size_t, c_uint32, c_void_p, c_char_p, c_wchar_p, c_long, memmove, string_at
from win32.win32file import GetFileSize
import win32file

if platform == 'win32':
    print('win')
    kernel32 = WinDLL('kernel32')
    
    # # Определение аргументов и возвращаемого значения функции CreateFileA
    # kernel32.CreateFileW.argtypes = [
    #     c_wchar_p,  # lpFileName
    #     c_uint32,  # dwDesiredAccess
    #     c_uint32,  # dwShareMode
    #     c_void_p,  # lpSecurityAttributes
    #     c_uint32,  # dwCreationDisposition
    #     c_uint32,  # dwFlagsAndAttributes
    #     c_void_p   # hTemplateFile
    # ]
    # kernel32.CreateFileW.restype = c_void_p

    # Определение аргументов и возвращаемого значения функции CreateFileMappingA
    kernel32.CreateFileMappingW.argtypes = [
        c_void_p,  # hFile
        c_void_p,  # lpFileMappingAttributes
        c_uint32,  # flProtect
        c_uint32,  # dwMaximumSizeHigh
        c_uint32,  # dwMaximumSizeLow
        c_wchar_p   # lpName
    ]
    kernel32.CreateFileMappingW.restype = c_void_p

    # Определение аргументов и возвращаемого значения функции MapViewOfFile
    kernel32.MapViewOfFile.argtypes = [
        c_void_p,  # hFileMappingObject
        c_uint32,  # dwDesiredAccess
        c_uint32,  # dwFileOffsetHigh
        c_uint32,  # dwFileOffsetLow
        c_size_t,  # dwNumberOfBytesToMap
    ]
    kernel32.MapViewOfFile.restype = c_void_p

    kernel32.UnmapViewOfFile.argtypes = (c_void_p,)
    kernel32.UnmapViewOfFile.restype = c_long
    
elif platform == 'linux':
    print('linux')
    libc = CDLL('libc.so.6')
else:
    print('others')

class localSync(object):
    """description of class"""
    def __init__(self, arg1, arg2) -> None:
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self) -> str:
        return 0

    def localSyncData(self, arg1, arg2):
        print('sync')
        comp = dircmp(arg1, arg2)
        #comp.report()
        
        if platform == 'win32':
            # copy folder
            for newFile in comp.left_only:
                print('copy new file')
                try:
                    copytree(arg1 + '/' + newFile, arg2 + '/' + newFile)
                except OSError as err:
                    if err.errno == ENOTDIR:
                        copy(arg1 + '/' + newFile, arg2 + '/' + newFile)

            comp = dircmp(arg1, arg2)
            #comp.report()

            # copy files
            for commFile in comp.common_files:
                file1 = path.join(arg1, commFile)
                file2 = path.join(arg2, commFile)
        
                if cmp(file1, file2) == False:
                    print('copy file')
                    
                    # file_handle = kernel32.CreateFileW(
                    #     "qqq.txt",  # Имя файла
                    #     0x80000000,  # Режим доступа (GENERIC_READ)
                    #     0,  # Режим совместного доступа (SHARE_NONE)
                    #     None,  # lpSecurityAttributes
                    #     3,  # dwCreationDisposition (OPEN_EXISTING)
                    #     0,  # dwFlagsAndAttributes
                    #     None  # hTemplateFile
                    # )
                
                    # Open the file for reading
                    file1_handle = win32file.CreateFile(
                        file1,
                        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                        win32file.FILE_SHARE_READ,
                        None,
                        win32file.OPEN_EXISTING,
                        win32file.FILE_ATTRIBUTE_NORMAL,
                        None
                    )
                    
                    # Open the file for reading
                    file2_handle = win32file.CreateFile(
                        file2,
                        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                        win32file.FILE_SHARE_READ,
                        None,
                        win32file.OPEN_EXISTING,
                        win32file.FILE_ATTRIBUTE_NORMAL,
                        None
                    )
                    
                    # Get the size of the files
                    file1_size = win32file.GetFileSize(file1_handle)
                    file2_size = win32file.GetFileSize(file2_handle)
                    
                    if file1_handle != c_void_p(-1).value and file2_handle != c_void_p(-1).value:
                        # Вызов функции CreateFileMappingW для создания отображения файла
                        file1_mapping_handle = kernel32.CreateFileMappingW(
                            file1_handle.handle,
                            None,
                            0x04,  # Режим защиты (PAGE_READWRITE)
                            0,
                            file1_size,
                            "data1_mapping"
                        )
                        
                        # Вызов функции CreateFileMappingW для создания отображения файла
                        file2_mapping_handle = kernel32.CreateFileMappingW(
                            file2_handle.handle,
                            None,
                            0x04,  # Режим защиты (PAGE_READWRITE)
                            0,
                            file1_size,
                            "data2_mapping"
                        )
                        
                        # Close the file handle
                        #win32file.CloseHandle(file1_handle)
                        #win32file.CloseHandle(file2_handle)
                        
                        # Проверка успешного создания отображения файла
                        if file1_mapping_handle != 0 and file2_mapping_handle != 0:
                            print("Отображение файла успешно создано!")
                            
                            # Получение указателя на отображение файла
                            mapped_file1_ptr = kernel32.MapViewOfFile(
                                file1_mapping_handle,
                                0xF001F,  # Режим доступа (FILE_MAP_ALL_ACCESS)
                                0,
                                0,
                                0
                            )
                            
                            # Получение указателя на отображение файла
                            mapped_file2_ptr = kernel32.MapViewOfFile(
                                file2_mapping_handle,
                                0xF001F,  # Режим доступа (FILE_MAP_ALL_ACCESS)
                                0,
                                0,
                                0
                            )
                            
                            # Проверка успешного получения указателя на отображение файла
                            if mapped_file1_ptr != 0 and mapped_file2_ptr != 0:
                                print("Указатель на отображение файла успешно получен!")

                                # Чтение данных из отображенного файла
                                data1 = string_at(mapped_file1_ptr, file1_size)  # Чтение 100 байтов
                                data2 = string_at(mapped_file2_ptr, file1_size)  # Чтение 100 байтов
                                #new_data = b"This is the new data"
                                #memmove(mapped_file_ptr, new_data, len(new_data))

                                if file1_size >= file2_size and file2_size != 0:
                                    # заполнение таблицы
                                    bufEdit = [0]
                                    lengthEdit = 0
                                    indexEdit = 0
                                    flag = False
                                    for i in range(0, file1_size):
                                        if data1[i] != data2[i] and flag == False:
                                            bufEdit[0] += 1
                                            bufEdit.append(i)
                                            lengthEdit = i
                                            flag = True
                                        if data1[i] == data2[i] and flag == True:
                                            lengthEdit = i - lengthEdit
                                            bufEdit.append(indexEdit)
                                            indexEdit += lengthEdit
                                            bufEdit.append(lengthEdit)
                                            flag = False
                                        
                                    if flag == True:
                                        lengthEdit = i - lengthEdit + 1
                                        bufEdit.append(indexEdit)
                                        indexEdit += lengthEdit
                                        bufEdit.append(lengthEdit)
                                        flag = False
                                        
                                    # # заполнение необходимых данных
                                    # for i in range(0, bufEdit[0]):
                                    #     bufEdit.append(data1[bufEdit[1 + i * 3]:bufEdit[1 + i * 3] + bufEdit[3 + i * 3]])
                                
                                    # перенос изменений в конечный файл
                                    for i in range(0, bufEdit[0]):
                                        memmove(mapped_file2_ptr + bufEdit[1 + i * 3], data1[bufEdit[1 + i * 3]:bufEdit[1 + i * 3] + bufEdit[3 + i * 3]], bufEdit[3 + i * 3])

                                    # Очистка не нужных байтов
                                    #memmove(mapped_file2_ptr + file1_size, mapped_file2_ptr + file2_size, file2_size - file1_size - 2)
                                
                                    #print("Прочитанные данные:", data1)
                                
                                    # Отмена отображения файла
                                    kernel32.UnmapViewOfFile(mapped_file1_ptr)
                                    kernel32.UnmapViewOfFile(mapped_file2_ptr)
                                else:
                                    kernel32.UnmapViewOfFile(mapped_file2_ptr)
                                    kernel32.CloseHandle(file2_mapping_handle)
                                    win32file.CloseHandle(file2_handle)
                                    
                                    # Open the file for writing
                                    file2_handle = win32file.CreateFile(
                                        file2,
                                        win32file.GENERIC_WRITE,
                                        0,
                                        None,
                                        win32file.CREATE_ALWAYS,
                                        win32file.FILE_ATTRIBUTE_NORMAL,
                                        None
                                    )

                                    win32file.WriteFile(file2_handle, data1)
                            
                            else:
                                print("Не удалось получить указатель на отображение файла!")
                                
                            # Закрытие дескрипторов отображения
                            kernel32.CloseHandle(file1_mapping_handle)
                            kernel32.CloseHandle(file2_mapping_handle)
                            
                            # Close the file handle
                            win32file.CloseHandle(file1_handle)
                            win32file.CloseHandle(file2_handle)
                            
                        else:
                            print("Не удалось создать отображение файла!")
                            
                    else:
                        print("Не удалось открыть файл!")
        
        elif platform == 'linux':
            # copy folder
            for newFile in comp.left_only:
                print('copy new file')
                try:
                    copytree(arg1 + '/' + newFile, arg2 + '/' + newFile)
                except OSError as err:
                    if err.errno == ENOTDIR:
                        copy(arg1 + '/' + newFile, arg2 + '/' + newFile)

            comp = dircmp(arg1, arg2)
            #comp.report()
            
            # copy files
            for commFile in comp.common_files:
                file1 = path.join(arg1, commFile)
                file2 = path.join(arg2, commFile)
        
                if cmp(file1, file2) == False:
                    print('copy file')
                    
                    # Open the file for reading
                    file1_handle = open(file1, O_RDONLY)
                    file2_handle = open(file2, O_RDONLY)

                    file1_size = getsize(file1)
                    file2_size = getsize(file2)
                    
                    data1 = mmap.mmap(file1_handle, file1_size, mmap.MAP_SHARED, mmap.PROT_READ)
                    data2 = mmap.mmap(file2_handle, file2_size, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)
            
        else:
            # copy folder
            for newFile in comp.left_only:
                print('copy new file')
                try:
                    copytree(arg1 + '/' + newFile, arg2 + '/' + newFile)
                except OSError as err:
                    if err.errno == ENOTDIR:
                        copy(arg1 + '/' + newFile, arg2 + '/' + newFile)

            comp = dircmp(arg1, arg2)
            #comp.report()

            # copy files
            for commFile in comp.common_files:
                file1 = path.join(arg1, commFile)
                file2 = path.join(arg2, commFile)
        
                if cmp(file1, file2) == False:
                    print('copy file')
                    copy(file1, file2)
    
        for subDir in comp.common_dirs:
            subDir1 = path.join(arg1, subDir)
            subDir2 = path.join(arg2, subDir)
            self.localSyncData(subDir1, subDir2)