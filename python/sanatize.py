#this file is used to make sure that user data does not contain porly formated data for the sql database
#all sanitation checks for data should go through this file so WHEN there is a problem
#it can be changed globaly from here

#these variables control the connection to the database

import psycopg2 as ps
import sys

def checkStr(string,whitelist="0123456789 abcdefghijklmnopqrstuvwxyz?"):
	for char in string:	
		if char.lower() not in whitelist:
			return False	
	return True
#JsGZb6ZFoWqtokQr5GCD
def getPass(var='dmPass'):
	try:
		return sys.env['dmPass']
	except:
		print('[ERROR] unable to get enviorment var dmPass!')
		quit()
def getConn(dbname='dnd',dbuser='dm',dbpass='',dbhost='localhost'):
	try:
		if dbpass == None:
			dbpass = getPass()	
		return ps.connect("dbname='" + dbname + "' user='" + dbuser + "' host='" + dbhost + "' password='" + dbpass +"'")
	except:
		return False	
