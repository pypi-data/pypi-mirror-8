#########
Reference
#########

The **dum** module define a set of function to generate python objects from the projection of
data structured in xml, json or csv.


Node protocol
-------------
The *Node* protocol must be defined by the classes that host the result of the data projection.   


.. class:: Node
   :noindex:
   
   A class complying to the *Node* protocol must accept an **empty constructor** and define : 
   
    .. class:: dum
       :noindex:
   
    This static class is used as a namespace to store the projection fields.
    
    The dum class can also define the following attributes:
    
        .. data:: __namespaces__ 
        
        a mapping from namespace prefix to full name

        .. data:: __default_namespaces__ 
        
        a string with the full name of the element hierarchy
        
   
    .. method:: dum_projection()   
        
    This optional method is called when the closing tag is parsed. 
    Define it to return an alternative object (masquerade) or to perform some post parsing process. 
    In the second case the method should return self.


Each projection field is a **dum** class member with the form :
        *target = converter[, source]*
  
* *target* is the name of the python's object attribute 
* *converter* is the function  used to convert input data to python value. It may be replaced  by a default value which will be used as prototype. Conveter may be but inside a list to denote that value must me collected as list.
* *source* is the localization of the data in the input document. It is a string which must conform to a subset of `xPath <https://en.wikipedia.org/wiki/XPath>`_.  This source segment is optional, by default *dum* will look for a child with the same name than the target.






.. module:: dum   
   
Module content
--------------

.. data:: DUM_NONE 

   returned by converter functions when a value should be ignored


   
.. function:: group(name1=type1 [,name2=type2...])

   All child elements corresponding to name1,name2... should be collected in the same list
   after being interpreted by type1, type2... converter.
   You can give a dictionary as first argument if some child name are not valid Python
   identifiers.
   The group fields are only used for Xml parsing.


.. decorator:: converter
.. decorator:: converter(source, default)

   Use these decorator when you need to define a function to convert values.
   The form without argument is optional : you can use raw function as well.

   :param source: xPath string for locating value in input data 
   :param default: value to use if nothing is found in input data

    


.. decorator:: lister
.. decorator:: lister(source)

   When you need converter to be applied on a collection of values
    
   :param source: xPath string for locating value in input data 


.. function:: xml(Node, fd)
    
   Parse the xml file stored in the file descriptor fd, an project it's root element into the Node class.

   :param Node: class conforming to the *Node* protocol 
   :param fd: file descriptor opened for reading at the start of the xml data. 
   :returns: Node instance initialized from xml root element.


.. function:: xmls(Node, text)
    
   Parse the xml present in text string.
   
   :param Node: class conforming to the *Node* protocol 
   :param text: string containing the xml data. 
   :returns: Node instance initialized from xml root element.
   
.. function:: json(Node, object)
    
   Project *object* root element into the Node class; *object* may come from  
   `json.load <https://docs.python.org/3/library/json.html>`_ function.

   :param Node: class conforming to the *Node* protocol 
   :param object: dictionary corresponding of the root of json data. 
   :returns: Node instance initialized from *object*.
   
   
.. function:: csv(Node, iterator[, header])   

    Parse and project tabulated data from iterator into the Node class. The iterator object may come from  
    `csv.reader <https://docs.python.org/3/library/csv.html>`_ 

   :param Node: class conforming to the *Node* protocol 
   :param iterator: iterator yielding fixed length rows in the form of list of strings
   :param header: column name are used to interpret dum field source. If the header list it present it will be used
    for column names, else the first row of the iterator will be used.
   :returns: a generator of Node instances initialized from input rows values.
   



