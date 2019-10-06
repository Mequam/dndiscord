#this file is used to make sure that user data does not contain porly formated data for the sql database
#all sanitation checks for data should go through this file so WHEN there is a problem
#it can be changed globaly from here

#these variables control the connection to the database

import psycopg2 as ps


def checkStr(string,whitelist="abcdefghijklmnopqrstuvwxyz"):
	for char in string:	
		if char.lower() not in whitelist:
			return False	
	return True
def getConn(dbname='dnd',dbuser='dm',dbpass='JsGZb6ZFoWqtokQr5GCD',dbhost='localhost'):
	try:
		return ps.connect("dbname='" + dbname + "' user='" + dbuser + "' host='" + dbhost + "' password='" + dbpass +"'")
	except:
		return False	
