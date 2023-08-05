#########
dumxpath
#########

The **dumxpath** module run xPath like syntax on Json data.

If the current element is a dictionary, the module will use the element itself. But if the current element is an array, the  module will look into each element of this array

Syntax
======
Element are separated by a slash (/)

**key** : select all values associated to the key  *key*

**.**  : Select the current element. 

**..**  : Select the parent element

**[@key]** or **[key]**  : Select the current element if it contains the key *key*

**[@key=value]**  : Select the current element if the value associated to the key *key* is equal to *value*

**[index]**  : If current element is an array, select child at *index* (1 is the first position). Note that  *last()-n* expressions are supported.


Unsuported syntax
-----------------

*****  : Select all child elements. 

**//**  : Select all sub-elements



.. module:: dumxpath   
   
Module content
==============

.. class:: JsPath(path)

        Compile an object that can be called with the json data as argument. It will return an iterator on
        all matching objects.
