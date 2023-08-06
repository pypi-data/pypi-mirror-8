=====
myorm
=====
(Version 0.0.5)

*******
Purpose
*******
Provides a more or less simple ORM for MySQL, PostgreSQL and SQLite.

Usage
=====
To use the power of myorm you need to set up an adaptor and let your classed inherit from myorm.DbObject.

For example:
************
DbObject = myorm.DbObject
DbObject.adaptor = myorm.SQLiteAdaptor(database='/home/christian/Projekte/projectname/database.db')

class User(DbObject):
    tablename = 'users'
    fields = {'id': 'int',
              'name': 'char',
              'password': 'char',
              'describtion': 'text',
              'registered': 'date',
              'logins': 'int',
              'active': 'bool'}

User instances will provide classmethods to handle them.


Available operations:
*********************
    - .all()
        - Returns all objects, unordered
    - .get(key=value)
        - E.g.: User.get(id=2)
          Returns one object
    - .filter(key=value)
        - E.g.: User.filter(id=2)
          Returns a list of objects (like `get` but returns more than one).
          max_key and min_key can be used to limit the results. E.g.
          "max_logins=10". This will return all users with less than 10 logins.
          max_key and min_key can be combined: User.filter(min_logins=10, max_logins=50). (Does not work for dates at the moment.)

          A special filter is "order_by". E.g. "order_by='-name'".
          This will return a ordered descending (-) list of objects. For an ascending use "order_by='name'".
    - .create()
        - Used to create objects of the calling class. Takes fieldnames as kwargs. E.g. User.create(id=None, name='Christian', ..)
          It returns the just created object.
    - .save()
        - Simply saves the object. If it is new, it will be created, if it already exists, it will be updated.
    - .delete()
        - Deletes the objects from the database
    - .pure()
        - This function can be used for more complex (SELECT) queries. It handles pure SQL.
          E.g.: User.pure('SELECT something FROM users WHERE complex=query')
    - .raw()
        - The builtin SQL injection function. It simply executes queries (INSERTS aswell as SELECTS).
          It always returns what it fetches. Use it wisely.
    - .create_table()
        - Function to create tables based on their fieldnames and tablename.
          The class which calls this function will get a table in the database.
          It DOES NOT provide migrations, it simply creates a table with all defaults on NULL.
          If you change the fieldnames afterwards, you have to migrate the table in another way.
          If you change the tablename and the execute this function again, you will get a new table. The old one will not be deleted.


License
=======
myorm is avialable under the terms of the GPLv3.


Disclaimer
==========
This software comes without any warranty. You use it on your own risk. It may contain bugs, viruses or harm your hardware in another way. The developer is not responsible for any consequences which may occur because of using the software.
