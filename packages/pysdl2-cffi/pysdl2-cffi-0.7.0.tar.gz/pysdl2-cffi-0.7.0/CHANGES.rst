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
