#!/bin/python3


#this file contains functions to interact with the psql database

import sanatize as san
import psycopg2 as ps

#this function adds a charicter to the database
def addCharicter(playerNum,raceName,play,parnum=None):
	
	#sanitize our data
	if not san.checkStr(raceName):
		#the race name or player num contain a sql injection
		return False
	values = str(playerNum) +',\'' + raceName + '\''	
	
	if parnum != None:
		columns += ',parnum'
		values += ',' + str(parnum)
	if play.name != None:
		if not san.checkStr(play.name):
			#check to make sure the name does not contain a sql injection
			return False
		columns += ',chaname'
		values += ',\'' + play.name + "'"
	
	conn = san.getConn() 	
	if not conn:
		#we were unable to get a valid connection to the database
		return False

	#get a cursor into the database
	cur = conn.cursor()

	#create the values for the query
	columns = 'plaNum,racName'
	#there is no need to check the playernum as python will check to make sure it is an intager, meaning we get to completly control what the data is

	
	
	cur.execute('INSERT INTO charicter(' + columns + ') VALUES('+values+')')

	#save the changes that we are adding to the database
	conn.commit()

#get the charicter number from the database for the charicter that we just created
	cur.execute('SELECT chanum FROM charicter ORDER BY chanum DESC LIMIT 1')

	rows = cur.fetchall()
	if len(rows) == 0:
		return False
	charnum=int(rows[0][0])	


#get all of the stats that are in the database
	cur.execute('SELECT staname FROM stat')
	rows = cur.fetchall()
	
#format the stats that we get from the database so that they do not contain trailing whitespace 
	rowstr = []
	for row in rows:
		append_val = ''
		for char in row[0]:
			if char == ' ':
				break	
			append_val += char
		rowstr.append(append_val)
#if the stat of the player that we recived is in the database, load that stat	
	for stat in p.permstats:
		if stat.lower() in rowstr:
			#the stat exists in the database, add it to the relation
			values = str(charnum) + ',\'' + stat + '\',' + str(p.permstats[stat])
			cur.execute('INSERT INTO cha2sta(chanum,staname,value) VALUES('+ values+')')	
	conn.commit()
	conn.close()	
	return True

def getPNum(playerName):
	try:
		conn = ps.connect("dbname='dnd' user='dm' host='localhost' password='JsGZb6ZFoWqtokQr5GCD'") 
	except:
		return False
	
	cur = conn.cursor()
	if san.checkStr(playerName):
		cur.execute('SELECT planum FROM player WHERE planame=\''+playerName+"'") 
	else:
		#were were given a string that we cannot use, return false
		return False
	rows = cur.fetchall()
	if len(rows) != 1:
		#there can be more than one player number for a given player name, so complain if we dont find one
		return False
	else:
		return rows[0][0] #return the name
	conn.close()

if __name__=='__main__':
	import sys
	sys.path.insert(1,'./networld/')
	from entity import Player

	from cdice import roll
	import argparse
	
	name = ''
	playername = ''
	race=None
	statdict = {}
	for arg in sys.argv:
		split_arg = arg.split('=')
		if len(split_arg) > 1:
			if split_arg[0] == 'name':
				name = split_arg[1]
			elif split_arg[0] == 'pname':
				playername = split_arg[1]
			elif split_arg[0] == 'race':
				race=split_arg[1]
			else:
				statdict[split_arg[0]] = int(split_arg[1])		
	p = Player(name)
	p.permstats = statdict
	playernum = getPNum(playername)
	if playernum == False:
		print('[ERROR] invalid player name!')
		quit()
	elif race == None:
		print('[ERROR] race required!')
		quit()
	if not addCharicter(playernum,race,p):
		print('[ERROR] mal formated data!')
	
