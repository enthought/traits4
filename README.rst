This package is no longer maintained, and no current projects should rely on it.
If you encounter projects that still depend on enthought/traits4, please open issues
against those projects.

----

Traits4
=======

This is concept code for the next generation of Traits, aka Traits4. 
Eventually, ctraits.py should be merged into this repo.

Some ideas being explored here:

- Simplifying the trait resolution order by implementing trait objects as descriptors.
- Porting the performance hacks of ctraits.c to Cython, so we don't take a performance hit.
- Eliminating magic integers and the generally convoluted code found in ctraits.c
- Making the code more maintainable so that a Cython and pure Python version of the backend can coexist easily.
- Giving traits a proper event system, and relying on that system for things like delegation, validation, notification, defaults, etc...
- Making the event system accessible, extensible, and easily usable by client code.
- Decouple everything.
