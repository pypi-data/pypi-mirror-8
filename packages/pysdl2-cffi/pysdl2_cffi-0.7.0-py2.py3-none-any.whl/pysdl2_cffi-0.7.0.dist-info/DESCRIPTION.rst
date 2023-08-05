pysdl2-cffi is a Python wrapper for SDL2 written using cffi, featuring:

- A cffi + dlopen interface to the underlying SDL2 libraries.
- Automatically generated, consistent helper functions for SDL2, SDL_image,
  SDL_mixer, and SDL_ttf that hide most allocation and dereferencing.
- Useful docstrings on every function, including the C function signature and
  (for SDL2 only) the library's original doxygen documentation reformatted as
  Sphinx restructured text.
- A small collection of libSDL2's original example / test programs converted
  to Python using Eric S. Raymond's ctopy.

The goal is to provide a flat, consistent, faithful-to-C binding with some
more-Pythonic renaming and conveniences.

This wrapper won't contain anything that doesn't directly translate to part of
the library's API. The goal is to be a dependency for something like pygame,
not a replacement.

This library should be compatible with Linux, OSX and Windows.

This library is licensed under the GPLv2 or (at your option) any later
version. Alternatively a commercial license can be purchased from the 
author for a nominal fee.

Install with pip, or download from https://pypi.python.org/pypi/pysdl2-cffi

Source hosted at https://bitbucket.org/dholth/pysdl2-cffi

Documentation hosted at https://pythonhosted.org/pysdl2-cffi

0.7.0
-----
- Struct wrappers now expose all the attributes of the C-level struct as 
  properties. Great for tinkering, as the property names can now be 
  inspected interactively.
- Struct wrappers no longer pass all attribute access through
  getattr/setattr. Arbitrary data can be attached to the struct wrappers
  as is customary in Python.
- Fix a capitalization error for the "classy" API to conform to the general
  binding rules. ``ob.gL_Function`` is now ``ob.GL_Function``.

0.6.0
-----
- Windows is now supported! You must manually download the SDL2 dll's and
  place them on PATH ``set PATH=%PATH%;C:\users\me\SDL2Dir`` but pysdl2-cffi
  will attempt to load the Windows ``.dll`` as well as the Unix ``.so``.

0.5.1
-----
- Enums are no longer wrapped in (nonexistent) classes
- Python 2 can also pass Unicode where char* is required; automatically
  encoded to utf-8.


