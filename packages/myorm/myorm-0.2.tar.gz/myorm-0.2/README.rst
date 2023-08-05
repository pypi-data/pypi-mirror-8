
myorm
=====
(Version 0.0.1)


Purpose
-------

Provides a more or less simple ORM for MySQL and SQLite (PostgreSQL support is planned).


Usage
-----

To use the power of myorm you need to make your classes inherit from the myorm classes.

For example:

class User(myorm.SQLiteObject):
    tablename = 'users'
    fieldnames = ['id', 'name', 'password']
    pass

User instances will provide classmethods to handle them.

Currently available operations:
    - get_all()
    - get_by_id(id)
    - get_by_filter("name=%s", name)
    - get_ordered(criteria, direction) # eg: "date", "DESC"
    - create()
    - save()
    - insert()
    - update
    - delete()


License
-------

myorm is avialable under the terms of the GPLv3.


Disclaimer
-----------

This software comes without any warranty. You use it on your own risk. It may contain bugs, viruses or harm your hardware in another way. The developer is not responsible for any consequences which may occur because of using the software.
