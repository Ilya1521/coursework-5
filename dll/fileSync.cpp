#include <stdio.h>
#include "pch.h"
#include "fileSync.h"

#include <iostream>
#include <string>
#include <windows.h>
#include <vector>

class localSync
{
public:
	int localSyncData()
	{
		#ifdef _WIN32
			std::cout << "Windows" << std::endl;



		#elif __APPLE__
			std::cout << "Mac OS" << std::endl;
		#elif __linux__
			std::cout << "Linux" << std::endl;
		#else
			std::cout << "Unknown OS" << std::endl;
		#endif

		return 0;
	}

private:

};

class remoteSync
{
public:
	int remoteSyncData()
	{
		#ifdef _WIN32
			std::cout << "Windows" << std::endl;
		#elif __APPLE__
			std::cout << "Mac OS" << std::endl;
		#elif __linux__
			std::cout << "Linux" << std::endl;
		#else
			std::cout << "Unknown OS" << std::endl;
		#endif

		return 0;
	}

private:

};

class interfaceSync: public localSync, public remoteSync
{
public:
	interfaceSync(std::string oper, std::string arg1, std::string arg2)
	{
		_oper = oper;
		_arg1 = arg1;
		_arg2 = arg2;
	}

	int initSync(std::string oper, std::string arg1, std::string arg2)
	{
		_oper = oper;
		_arg1 = arg1;
		_arg2 = arg2;
		
		return 0;
	}

private:
	std::string _oper, _arg1, _arg2;
};