#ifndef OPENMM_HARDWARE_H_
#define OPENMM_HARDWARE_H_

/* -------------------------------------------------------------------------- *
 *                                   OpenMM                                   *
 * -------------------------------------------------------------------------- *
 * This is part of the OpenMM molecular simulation toolkit originating from   *
 * Simbios, the NIH National Center for Physics-Based Simulation of           *
 * Biological Structures at Stanford, funded under the NIH Roadmap for        *
 * Medical Research, grant U54 GM072970. See https://simtk.org.               *
 *                                                                            *
 * Portions copyright (c) 2013 Stanford University and the Authors.           *
 * Authors: Peter Eastman                                                     *
 * Contributors:                                                              *
 *                                                                            *
 * Permission is hereby granted, free of charge, to any person obtaining a    *
 * copy of this software and associated documentation files (the "Software"), *
 * to deal in the Software without restriction, including without limitation  *
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,   *
 * and/or sell copies of the Software, and to permit persons to whom the      *
 * Software is furnished to do so, subject to the following conditions:       *
 *                                                                            *
 * The above copyright notice and this permission notice shall be included in *
 * all copies or substantial portions of the Software.                        *
 *                                                                            *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR *
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,   *
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL    *
 * THE AUTHORS, CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,    *
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR      *
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE  *
 * USE OR OTHER DEALINGS IN THE SOFTWARE.                                     *
 * -------------------------------------------------------------------------- */

#ifndef __SSE4_1__
static int processorSupportsSSE41(void) {
  return 0;
}
#else

/**
 * This file defines a collection of functions for querying the specific hardware being used.
 */

/**
 * Get the number of CPU cores available.
 */
#ifdef __APPLE__
   #include <sys/sysctl.h>
   #include <dlfcn.h>
#else
   #ifdef _WIN32
      #define NOMINMAX
      #include <windows.h>
      #include <intrin.h>
   #else
      #include <dlfcn.h>
      #include <unistd.h>
   #endif
#endif


/**
 * Get a description of the CPU's capabilities.
 */
#ifdef _WIN32
#define cpuid __cpuid
#else
static void cpuid(int cpuInfo[4], int infoType){
#ifdef __LP64__
    __asm__ __volatile__ (
        "cpuid":
        "=a" (cpuInfo[0]),
        "=b" (cpuInfo[1]),
        "=c" (cpuInfo[2]),
        "=d" (cpuInfo[3]) :
        "a" (infoType)
    );
#else
    __asm__ __volatile__ (
        "pushl %%ebx\n"
        "cpuid\n"
        "movl %%ebx, %1\n"
        "popl %%ebx\n" :
        "=a" (cpuInfo[0]),
        "=r" (cpuInfo[1]),
        "=c" (cpuInfo[2]),
        "=d" (cpuInfo[3]) :
        "a" (infoType)
    );
#endif
}
#endif


static int processorSupportsSSE41(void) {
    /* Make sure the CPU supports SSE 4.1. */
    int cpuInfo[4];
    cpuid(cpuInfo, 0);
    if (cpuInfo[0] >= 1) {
        cpuid(cpuInfo, 1);
        return ((cpuInfo[2] & ((int) 1 << 19)) != 0);
    }
    return 0;
}

#endif /* SSE 4.1 */
#endif /* OPENMM_HARDWARE_H_ */
