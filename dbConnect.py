'''
    Module for connecting with the MySQL database

    Includes the DSN info

    Partially modified and adapted from Scott Anderson's dbconn2 
    module, used in Wellesley CS course 304.

'''

import MySQLdb

# this is essentially a static variable of this package. It caches the DB
# connection, so that it can be returned quickly without setting up a new
# connection, if the user tries to connect again.  

the_database_connection = False

DSN = {
    'user': 'SHE_admin', 
    'passwd': 'sexpositivity',
    'db': 'SHEnonymousdb'
}

def connect():
    '''Returns a database connection/handle given the dsn (a dictionary)

This function saves the database connection, so if you invoke this again,
it gives you the same one, rather than making a second connection.  This
is the so-called Singleton pattern.  In a more sophisticated
implementation, the DSN would be checked to see if it has the same data as
for the cached connection.'''
    global the_database_connection
    if not the_database_connection:
        try:
            the_database_connection = MySQLdb.connect( **DSN )
            # so each modification takes effect automatically
            the_database_connection.autocommit(True)
        except MySQLdb.Error, e:
            print ("Couldn't connect to database. MySQL error %d: %s" %
                   (e.args[0], e.args[1]))
            raise
    return the_database_connection


