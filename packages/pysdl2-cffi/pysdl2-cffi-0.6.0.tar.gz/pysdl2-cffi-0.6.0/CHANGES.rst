0.6.0
-----
- Windows is now supported! You must manually download the SDL2 dll's and
  place them on PATH `set PATH=%PATH%;C:\users\me\SDL2Dir` but pysdl2-cffi
  will attempt to load the Windows `.dll` as well as the Unix `.so` files.

0.5.1
-----
- Enums are no longer wrapped in (nonexistent) classes
- Python 2 can also pass Unicode where char* is required; automatically
  encoded to utf-8.
