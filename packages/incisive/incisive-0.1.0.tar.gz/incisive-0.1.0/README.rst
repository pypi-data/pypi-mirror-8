incisive
========

**incisive** is a tiny library for handling CSV in Python. It's a wrapper for the csv module.


Usage
-----

* You can read a csv file like this::

    >>> iris = read_csv("data/iris.csv")
    >>> iris.next()
    {'petal_length': 1.4,
     'petal_width': 0.2,
     'sepal_length': 5.1,
     'sepal_width': 3.5,
     'species': 'setosa'}

`read_csv` returns a generator. Note that `incisive`, by default, tries to guess the type of the columns.


* Writing a CSV file can be done in two ways:
  
1. with a list of dictionaries::

    >>> data = [{'name': 'Lancelot', 'actor': 'John Cleese', 'color': 'blue'},
               {'name': 'Galahad', 'actor': 'Michael Palin', 'color': 'yellow'}]

    >>> write_csv('bridge.csv', ('name', 'actor', 'color'), data=data)

(the keys are the field names of the CSV file.)

2. or with just a list of rows::

    >>> rows = [('Lancelot', 'John Cleese', 'blue'),
            ('Galahad', 'Michael Palin', 'yellow')]

    >>> write_csv('bridge.csv', ('name', 'actor', 'color'), rows=rows)

Note that this second method requires that your field names correspond exactly
to the elements of your rows.


Features
--------

* Simple API
* Guess the types when it's possible 
* Accept functions to specify the types
