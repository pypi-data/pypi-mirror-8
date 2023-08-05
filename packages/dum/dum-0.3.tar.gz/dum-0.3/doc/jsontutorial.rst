#############
JSON tutorial
#############

.. testsetup:: *

   import sys
   sys.path.append("..")
   data = {
    "title" : "Authors",
    "author" : [
        {
            "name":"Victor Hugo",
            "book":"Les Misérables",
        },{
            "name":"Mark Twain",
            "book":"The Adventures of Tom Sawyer", 
        }
    ]
   }


.. testcode::  

    import dum 
  
    # The json module will return something like
    data = {
      "title" : "novels",
      "author" : [{
            "name":"Victor Hugo",
            "book":"Les Misérables",
        },{
            "name":"Mark Twain",
            "book":"The Adventures of Tom Sawyer", 
        }]}
    
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


