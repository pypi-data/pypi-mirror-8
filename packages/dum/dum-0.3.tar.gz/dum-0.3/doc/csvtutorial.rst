############
CSV tutorial
############

.. testsetup:: header

   import sys, io,csv
   sys.path.append("..")
   csvfile=io.StringIO("""city,population,country
   Shanghai,24150000,China
   Karachi,23500000,Pakistan
   Beijing,21150000,China
   Delhi,17838842,India
   Lagos,17060307,Nigeria
   Istanbul,14160467,Turkey""")
   csvcities = csv.reader(csvfile)

Supose you want to parse the following cities.csv file :

::

   city,population,country
   Shanghai,24150000,China
   Karachi,23500000,Pakistan
   Beijing,21150000,China
   Delhi,17838842,India
   Lagos,17060307,Nigeria
   Istanbul,14160467,Turkey

.. code::

    import csv
    csvfile = open('cities.csv')
    csvcities = csv.reader(csvfile)

.. testcode:: header

    import dum 
  
    # define our parser class and run it on our sample of XML
    class City:
        class dum:
            name = str,"city"
            country = str
            population = int
    
    for city in dum.csv(City, csvcities):
        print(city.name, city.country, city.population)
    
If you run this you get :

.. testoutput:: header
  
    Shanghai China 24150000
    Karachi Pakistan 23500000
    Beijing China 21150000
    Delhi India 17838842
    Lagos Nigeria 17060307
    Istanbul Turkey 14160467



Explicit column headers
-----------------------




.. testsetup:: noheader

   import sys, io,csv
   sys.path.append("..")
   import dum
   csvfile=io.StringIO("""Shanghai,24150000,China
   Karachi,23500000,Pakistan
   Beijing,21150000,China
   Delhi,17838842,India
   Lagos,17060307,Nigeria
   Istanbul,14160467,Turkey""")
   csvcities = csv.reader(csvfile)

If the cities.csv file hasn't a row header:

::

   Shanghai,24150000,China
   Karachi,23500000,Pakistan
   Beijing,21150000,China
   Delhi,17838842,India
   Lagos,17060307,Nigeria
   Istanbul,14160467,Turkey

You need to pass it to dum.csv

.. testcode:: noheader
  
    # define our parser class and run it on our sample of XML
    class City:
        class dum:
            name = str,"city"
            country = str
            population = int
    
    for city in dum.csv(City, csvcities, headers=["city", "population", "country"]):
        print(city.name, city.country, city.population)
    
If you run this you get also :

.. testoutput:: noheader
  
    Shanghai China 24150000
    Karachi Pakistan 23500000
    Beijing China 21150000
    Delhi India 17838842
    Lagos Nigeria 17060307
    Istanbul Turkey 14160467
