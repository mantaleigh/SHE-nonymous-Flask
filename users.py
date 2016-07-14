#!/usr/local/bin/python2.7
'''
Author: Samantha Voigt
signin.py

TODO: Write a description of the file

'''

import MySQLdb
import dbConnect

def checkInfo(username, password): 
	'''
	Checks that the given login information is correct - returns True or False
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) 
	statement = "SELECT login_id FROM login WHERE login_id = %s AND passhash = SHA1(%s);"
	curs.execute(statement, (username, password))
	row = curs.fetchone()
	return row # return whether or not the log in was successful


def addUser(username, password):
	''' 
	Adds login information to the database for the given username/password
	Adds a row to both the login table and the profile_info table

	Returns True if adding the user to the database was successful, false otherwise (e.g. username already taken)
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)

	if userExists(username): return False

	# if you get to this point, the username is good
	statement = "INSERT INTO login (login_id, passhash) VALUES (%s, SHA1(%s));"
	curs.execute(statement, (username, password))

	statement = "INSERT INTO profile_info (login_id) VALUES (%s);"
	curs.execute(statement, (username,))
	return True

def userExists(username):
	'''
	Returns True if a user exists in the database (checks for username), False otherwise
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
	statement = "SELECT login_id FROM login WHERE login_id = %s;"
	curs.execute(statement, (username,))
	return curs.fetchone()


