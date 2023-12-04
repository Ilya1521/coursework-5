#pragma once

#ifdef fileSync_EXPORTS
#define fileSync_API __declspec(dllexport)
#else
#define fileSync_API __declspec(dllimport)
#endif

//extern "C" fileSync_API class localSync;

//extern "C" fileSync_API class remoteSync;

extern "C" fileSync_API class interfaceSync;