#############
JSON tutorial
#############

.. testsetup:: *

   import sys
   sys.path.append("..")
   import dum
   data = {
    "title" : "Authors",
    "author" : [
        {"name":"Victor Hugo", "book":"Les Misérables", "lang":"fr",},
        {"name":"Mark Twain", "book":"The Adventures of Tom Sawyer", "lang":"en"},
        {"name":"Charles Dickens", "book":"Oliver Twist", "lang":"en"}]}


.. testcode::  

    import dum 
  
    # The json module will return something like
    data = {
      "title" : "novels",
      "author" :[
        {"name":"Victor Hugo", "book":"Les Misérables", "lang":"fr",},
        {"name":"Mark Twain", "book":"The Adventures of Tom Sawyer", "lang":"en"},
        {"name":"Charles Dickens", "book":"Oliver Twist", "lang":"en"}]}
    
    class Author:
        class dum:
            name = ""
            book = ""
    class Library:
        class dum:
            title = ""
            author = [Author]
        
    
    library =  dum.json(Library, data)
    print(library.title)
    for auth in library.author:
        print(auth.name, auth.book)
    
If you run this you get :

.. testoutput:: 
  
    novels
    Victor Hugo Les Misérables
    Mark Twain The Adventures of Tom Sawyer
    Charles Dickens Oliver Twist

Using expressions
-----------------
You can use an xPath like syntax to filter data

.. testcode::  

    class Library:
        class dum:
            enbooks = [str], "/author[@lang=en]/book"
 
    library =  dum.json(Library, data)
    for book in library.enbooks:
        print(book)
    
Then you get :

.. testoutput:: 
  
    The Adventures of Tom Sawyer
    Oliver Twist


