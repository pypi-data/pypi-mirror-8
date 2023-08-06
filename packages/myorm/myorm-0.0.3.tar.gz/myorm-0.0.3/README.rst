myorm
=====
(Version 0.0.3)


Purpose
-------

Provides a more or less simple ORM for MySQL, PostgreSQL and SQLite.


Usage
-----

To use the power of myorm you need to set up an adaptor and let your classed inherit from myorm.DbObject.

For example:

DbObject = myorm.DbObject
DbObject.adaptor = myorm.SQLiteAdaptor(database='/home/christian/Projekte/five/test.db')

class User(DbObject):
    tablename = 'users'
    fieldnames = ['id', 'name', 'password']
    pass

User instances will provide classmethods to handle them.

Currently available operations:
    - all()
    - get(key=value)
    - filter(key=value)
    - ordered(criteria, direction) # eg: "date", "DESC"
    - create()
    - save()

Currently not implemented (because I forgot it and now it is too late for today)
    - delete()


License
-------

myorm is avialable under the terms of the GPLv3.


Disclaimer
-----------

This software comes without any warranty. You use it on your own risk. It may contain bugs, viruses or harm your hardware in another way. The developer is not responsible for any consequences which may occur because of using the software.
