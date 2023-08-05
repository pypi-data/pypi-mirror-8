// python-gphoto2 - Python interface to libgphoto2
// http://github.com/jim-easterbrook/python-gphoto2
// Copyright (C) 2014  Jim Easterbrook  jim@jim-easterbrook.me.uk
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

%module(package="gphoto2.lib") gphoto2_file

%{
#include "gphoto2/gphoto2.h"
%}

%feature("autodoc", "2");

%include "typemaps.i"

%include "macros.i"

// gp_file_new() returns a pointer in an output parameter
PLAIN_ARGOUT(CameraFile **)

// Add default constructor and destructor to _CameraFile
DECLARE_GP_ERROR()
struct _CameraFile {};
DEFAULT_CTOR(_CameraFile, gp_file_new)
DEFAULT_DTOR(_CameraFile, gp_file_unref)
%ignore _CameraFile;

// These structures are private
%ignore _CameraFileHandler;

%include "gphoto2/gphoto2-file.h"
