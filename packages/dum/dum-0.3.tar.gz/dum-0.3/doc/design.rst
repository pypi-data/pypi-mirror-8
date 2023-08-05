################ 
Design rationals
################

A few words about principles that have driven dum development to the current state.

Design by convention
--------------------
This library has been created as an application of the `convention over configuration <https://en.wikipedia.org/wiki/Convention_over_configuration>`_ principle.

Basically this principle state that a module should have a default behavior. When the convention implemented by the module matches the desired behavior, it behaves as expected without requiring the programmer to write boilerplate code. Only when the desired behavior deviates from the implemented convention is explicit configuration required.

The objective is to provide default behavior for 'normal' objects, but to allow objects to override a given piece of default behavior by inheriting from some specific 

An implied, but even more important principle is that things should keep the same name between modules.

Names clashes
-------------
The early *dum*  prototypes didn't used the inner :class:`dum` class and even didn't required to define the field to project (anything not defined was projected as string). This was elegant and fluid but proved to be very fragile : 

Suppose you have defined the method

.. code-block:: python

    def compute(self)
        # do something ... 
    
When your xml evolve with a tag named <compute>, the dum module will fail suddenly on TypeError.


Misc
----         
When a node has several sub-elements, dum chose the first instead of directly create a list to keep all of them because this would be inconsistent : if one element has 2 the children, the other only one and the last 0 then client code will have yo check for a list or something else.

All dum methods are prefixed with *dum_* to avoid name clashes with applicative code. 

            
