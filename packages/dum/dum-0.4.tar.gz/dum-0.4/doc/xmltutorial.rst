############
XML tutorial
############

.. testsetup:: *

   import sys
   sys.path.append("..")
   body="""<team name="The champions" founded="2012">
                <mascot>Fido</mascot>
        
                <member email='p.martin@sample.net'>Paul Martin</member>
                <member>Luce Whight</member>
                <member email='mfield78@sample.net'>Martin Field</member>
                <member>Kim Peng</member>
            </team>"""

Let's start by creating a short script :

.. testcode::

    import dum 
    
    # a sample of XML string to parse
    body="""<team name="The champions" founded="2012">
                <mascot>Fido</mascot>
        
                <member email='p.martin@sample.net'>Paul Martin</member>
                <member>Luce Whight</member>
                <member email='mfield78@sample.net'>Martin Field</member>
                <member>Kim Peng</member>
            </team>"""

    # define our parser class and run it on our sample of XML
    class Team:
        class dum:
            name = ""
            mascot = ""
            member = ""
    team=dum.xmls(Team, body)
    # inspect content
    print("name:", team.name)
    print("mascot:", team.mascot)
    print("member:", team.member)
    
If you run this you get :

.. testoutput:: 
  
    name: The champions
    mascot: Fido
    member: Paul Martin

We have used :func:`dum.xmls` to parse a string (there is also :func:`dum.xml` to parse a file object)
and we have been able to get information back from attributes and child nodes content.


Projecting collections 
----------------------
    
Fantastic ! But wait ... where are Luce, Martin and Kim ? 
By default *dum* only keep the first value, if you want all you will have to tell it . Let's redefine our Team class

.. testcode::
    
    class Team:
        class dum:
             member = [str]
    team=dum.xmls(Team, body) 
    print(team.member)

Run the script :
    
.. testoutput::   
  
    ['Paul Martin', 'Luce Whight', 'Martin Field', 'Kim Peng']   


Value's types 
-------------

Because the 'founded' attribute is a number, we don't want to have it returned as a string  :

.. testcode::
    
    class Team:
        class dum:
             founded = int
    team=dum.xmls(Team, body) 
    print("It was founded %d years after the beginning of the 21th century"% (team.founded-2000))
    
.. testoutput::   
  
    It was founded 12 years after the beginning of the 21th century       
    

Alternatively you can also define a default value as prototype. This is usefull when the attribute may be ommited in the input file.

.. code-block:: python
    
    class Team:
        class dum:
             founded = 42



Don't stay alone 
----------------

Ok, but now we need member email. For that we will instruct *dum* that member are nodes : 

.. testcode::

    class Member:
        class dum:
             name =  str, "dum_content"
             email = "none"
    class Team:
        class dum:
             member = [Member]
        
    team=dum.xmls(Team, body)  
    for member in team.member:
        print(member.name,":",member.email)

.. testoutput::

    Paul Martin : p.martin@sample.net
    Luce Whight : none
    Martin Field : mfield78@sample.net
    Kim Peng : none


        
Natively dum map textual content of xml elements to the *dum_content* attribute. Here we have said
to *dum* that we want to to go to the *name* attribute instead.


Path globing
------------

More formally, each field from the dum class can be split into 3 segments: 

        *target = converter[, source]*

* *target* is the name of the python's object attribute 
* *converter* is the function  used to convert input data from to python attribute value. It may be replaced by a default value which will be used as prototype.
* *source* is the localization of the data in the input document. 

The source segment is a string which must conform to a subset of `xPath <https://en.wikipedia.org/wiki/XPath>`_. 
Current implementation use `ElementTree syntax <https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax>`_  for xml and support a partial syntax with json.

This source segment is optional, by default *dum* will look for a node or an attribute with the same name than the target.

The following sample use an xPath expression to collect all the member's emails

.. testcode::

    class Team:
        class dum:
             emails = [str], "member/@email"
        
    team=dum.xmls(Team, body)  
    print(team.emails)

.. testoutput::

    ['p.martin@sample.net', 'mfield78@sample.net']


Customized data conversion
--------------------------
When a type default constructor doesn't accept string, you will have to define your own converter. For sample let's say we want to convert the *founded* attribute into a datetime.date object

You can define a function in *dum* class :

.. testcode::

    import datetime
    class Team:
        class dum:
             def founded(foundedstr):
                return datetime.date(int(foundedstr), 1, 1)
    team=dum.xmls(Team, body)    
    print(team.founded)
    
.. testoutput::    

    2012-01-01


Use the :func:`dum.converter` decorator to provide default and/or source 

.. testcode::

    class Team:
        class dum:
            @dum.converter(default=datetime.date(1900,1,1))
            def founded(foundedstr):
                return datetime.date(int(foundedstr), 1, 1)
    team=dum.xmls(Team, body)       
    print(team.founded)


.. testoutput::    

    2012-01-01
    
There is also a :func:`dum.lister` decorator for collecting multiple values into one list


Grouping child nodes
--------------------
Because we're all against discrimination, Fido should be a member of the team. The :func:`dum.group` function can put several node types on the same list. Just tell it which nodes to group and how to convert them with named arguments :  
 
.. testcode::

    class Team:
        class dum:
             allmembers = dum.group(member=str, mascot=str)
    team=dum.xmls(Team, body)
    team.allmembers.sort()
    print(", " .join(team.allmembers))
   
.. testoutput::

    Fido, Kim Peng, Luce Whight, Martin Field, Paul Martin


Mascarade
---------
Mascarade are node class wich create an other object : simply define the dum_projection method to return this object

.. testcode::

    class Team:
        class dum:
            name = u""
            founded = 0
        def dum_projection(self):
            return (self.name, self.founded)
    team=dum.xmls(Team, body)  
    print(team)


Here we create a tuple

.. testoutput::    

    ('The champions', 2012)

        


The method can also be used to do post-parsing initalization, but don't forget to return self.

.. testcode::

    class Team:
        class dum:
            name = ""
            founded = 0
        def dum_projection(self):
            self.title = "%s team, since %s !"%(self.name, self.founded)
            return self
    team=dum.xmls(Team, body)  
    print(team.title)

.. testoutput::    

    The champions team, since 2012 !


Namespaces
----------


.. testsetup:: *

  
   body="""<h:team name="The champions" founded="2012" xmlns:h="http://example.com/nsp">
                <h:mascot>Fido</h:mascot>
        
                <h:member email='p.martin@sample.net'>Paul Martin</h:member>
                <h:member>Luce Whight</h:member>
                <h:member email='mfield78@sample.net'>Martin Field</h:member>
                <h:member>Kim Peng</h:member>
            </h:team>"""

XML Namespaces are often used  to avoid element name conflicts. 
This chapter show how to process a document with a single namespace
 using the *__default_namespace__* directive.

.. testcode::

    import dum 
    
    # a sample of XML string to parse
    body="""<h:team name="The champions" founded="2012" xmlns:h="http://example.com/nsp">
                <h:mascot>Fido</h:mascot>
        
                <h:member email='p.martin@sample.net'>Paul Martin</h:member>
                <h:member>Luce Whight</h:member>
                <h:member email='mfield78@sample.net'>Martin Field</h:member>
                <h:member>Kim Peng</h:member>
            </h:team>"""

    # define __default_namespace__ in our parser class 
    class Team:
        class dum:
            __default_namespace__ = "http://example.com/nsp"
            name = ""
            mascot = ""
            member = [""]
    team=dum.xmls(Team, body)
    # inspect content
    print("name:", team.name)
    print("mascot:", team.mascot)
    print("member:", team.member)
    
Then you retrieve :

.. testoutput:: 
  
    name: The champions
    mascot: Fido
    member: ['Paul Martin', 'Luce Whight', 'Martin Field', 'Kim Peng'] 

If your document use several namespaces, you can still use *__default_namespace__* for one of
them, but you will have to be explicit with the others.

.. testcode::

    # use __namespaces__ in our parser class 
    class Team:
        class dum:
            __namespaces__ = {"nsp":"http://example.com/nsp"}
            name = "", "name" # attribute without namespace
            mascot = "", "nsp:mascot"
            member = [""], "nsp:member"
    team=dum.xmls(Team, body)
    # inspect content
    print("name:", team.name)
    print("mascot:", team.mascot)
    print("member:", team.member)
    
And again :

.. testoutput:: 
  
    name: The champions
    mascot: Fido
    member: ['Paul Martin', 'Luce Whight', 'Martin Field', 'Kim Peng'] 
        
