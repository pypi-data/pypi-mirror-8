/*-----------------------------------------------------------------------------
| Copyright (c) 2014, Nucleic Development Team.
|
| Distributed under the terms of the Modified BSD License.
|
| The full license is in the file COPYING.txt, distributed with this software.
|----------------------------------------------------------------------------*/
#pragma once

#include <Python.h>

#define CPPY_MAJOR_VERSION 1
#define CPPY_MINOR_VERSION 0
#define CPPY_PATCH_VERSION 1

#define CPPY_VERSION "1.0.1"

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif
