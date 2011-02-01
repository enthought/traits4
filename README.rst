Traits4
=======

This is concept code for the next generation of Traits, aka Traits4. 
Eventually, ctraits.py should be merged into this repo.

Some ideas being explored here:
- Simplifying the trait resolution order by implementing trait objects as descriptors.
- Porting the performance hacks of ctraits.c to Cython, so we don't take a performance hit.
- Eliminating magic integers and the generally convoluted code found in ctraits.c
- Making the code more maintainable so that a Cython and pure Python version of the backend can coexist easily.