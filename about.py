# about.py

import MySQLdb
import dbConnect

def getSHEs(): 
	'''
	documentation needed
	'''
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	statement = "SELECT * FROM login;"
	curs.execute(statement)
	allSHEs = []
	while True:
		row = curs.fetchone()
		if row == None: 
			return allSHEs
		else:
			# try to get the name from the profile_info table, and display that. Otherwise display the username.
			info_curs = conn.cursor(MySQLdb.cursors.DictCursor)
			info_statement = "SELECT name FROM profile_info WHERE login_id = %s"
			info_curs.execute(info_statement, (row['login_id'],))
			info_row = info_curs.fetchone()
			name = info_row['name']
			if name: 
				allSHEs.append({'login_id': row['login_id'], 'name': name})
			else:
				allSHEs.append({'login_id': row['login_id']})


# TODO: Modify this to work for Flask
def getProfileContent(canEdit): 
	'''
	Returns the name to display in the "About X" string (username if there is no name in the database) as the 
	first element in a tuple, and the page content for the the person's profile page as the second element. 

	canEdit is a boolean that represents whether or not the logged in user is looking at their own page, and therefore
	should have editing capabilities.
	'''

	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	statement = "SELECT * FROM profile_info WHERE login_id=%s;"
	curs.execute(statement, (username,))
	row = curs.fetchone() # should only be one result
	name = row['name']
	about = row['about']
	class_year = row['class_yea r']

	if not name: name = row['login_id'] # if there is not a name in the database, treat the login_id as the name for displaying purposes

	if row: # double check, tho
		if canEdit: # make editable fields
			content += "<form method=post action='profile.cgi?user=" + row['login_id'] + "'><fieldset class='form-group'>"
			content += "<label for='name'>Name</label><input name='name' class='form-control' value='" + name + "'>"
			content += "<label for='class_year'>Class Year</label><input name='class_year' class='form-control' value='" + class_year_placeholder + "' maxlength='4'>"
			# content += "<label for='picfile'>Profile Image</label><input type='file' name='picfile'>"
			content += "<label for='about'>About</label><textarea class='form-control' name='about' rows='10'>"+about_placeholder+"</textarea>"
			content += "</fieldset><input type='submit' class='btn btn-primary' name='update' value='Update'></form>"
		else: # just display the content
			if class_year: 
				content += "<p><i>Class of " + class_year + "</i>"
			if about:
				content += "<p><b>About:</b><p>" + about
			else: 
				content += "<p>This user has no about at the moment."
	return (name, content)


def updateInfo(username, name, class_year, about):
	conn = dbConnect.connect()
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	statement = "UPDATE profile_info SET name=%s, about=%s, class_year=%s WHERE login_id=%s;"
	curs.execute(statement, (name, about, class_year, username))










