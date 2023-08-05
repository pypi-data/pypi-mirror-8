#### 
Todo
#### 

Bugs
====
The group function should preserve relative order of element from the input file. Fixing this will need to revrite the xPath runtime.

Extend json xPath (see dum.py) to match xPath support for xml.

Names harmonization between Array class and lister decorator

Deeper convention
=================
How to associate more `valid element name <http://www.xml.com/pub/a/2001/07/25/namingparts.html>`_ with python target identifiers. We should at least propose something for xml namespaces character ':'.

Maybe inferring type information from xml schema could make type declaration shorter ?

Better interpretation of xPath to specify when a value must be extracted only from an attribute or a child
  
Use dum fields definition for generating xml, json... from objects. Exploit info from the schema/DTD ?


API
===
optional strict projection : raise an error when a field with no defaults is not found in input.

allow to create custom list class in lister decorator?

Other data formats
==================
 * yaml
 * binary TLV
 * SQL ?
 * LR parser
 * python objects






