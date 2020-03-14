import sanatize as san
import psycopg2 as ps
def clear_trailing_white(string):
	while(string[-1] == ' '):
		string = string[:-1]
	return string
def get_connection():
	try:
		con = ps.connect("dbname='dndiscord' user='dm' host='localhost' password='yellowSprk'")
		return con
	except:
		print('[ERROR] could not connect to the database :(')
		die()
#the following two classes represent the raw data from the database, each field in the classes corisponds to a name in the database
	
class character:
	def __init__(self,chanum):
		con = get_connection()
		cur = con.cursor()
		
		#figure out wether or not the given id exists
		cur.execute("SELECT chaname,planum,racname FROM charicter WHERE chaNum="+str(chanum))
		rows = cur.fetchall()
		
		if (len(rows) == 1):
			#set the values for the given character
			self.chaname = rows[0][0]
			self.planum = rows[0][1]
			self.racname = rows[0][2]
			self.chanum = chanum

			#create a dictionary of the characters stats
			self.stats = {}
			cur.execute("SELECT emoji,value FROM cha2sta WHERE chaNum="+str(chanum))
			rows = cur.fetchall()
			for i in range(0,len(rows)):
				self.stats[clear_trailing_white(rows[i][0])] = rows[i][1]
		con.close()
class stat:
	#the speedy variable determines wether or not we want our stat to contain information about the stat description
	def __init__(self,emoji,desc_info=False):
		
		#get a window into the database
		con = get_connection()
		cur = con.cursor()
		
		
		#query the db for a list of stats
		if (not desc_info):
			#we don not want to query the db for description information
			cur.execute("SELECT staname,stagen,staroll FROM stat WHERE emoji='"+emoji+"'")
		else:
			#we want to get the description of the stat
			cur.execute("SELECT staname,stagen,staroll,stadesc FROM stat WHERE emoji='"+emoji+"'")	
		rows = cur.fetchall()
		
		#store the info in a python freindly format
		self.emoji = emoji
		self.staname = rows[0][0]
		self.stagen = rows[0][1]
		self.staroll = rows[0][2]
		
		#only store the description if we were searching for it earlier
		if (desc_info):
			self.stadesc = rows[0][3]
		else:
			self.stadesc = None #there is no known description

class player:
	def __init__(self,planum):
		con = get_connection()
		cur = con.cursor()
		if (type(planum) is int):
			#figure out wether or not the given id exists	
			cur.execute("SELECT planame,platag FROM player WHERE plaNum="+str(planum))
			rows = cur.fetchall()	
			if (len(rows) == 1):
				self.planame = rows[0][0]
				self.platag = rows[0][1]
				self.planum = planum
		else: 
			if (type(planum) is str):
				#in this case planum represents the hash of the discord ID, not the player number
				if (san.checkStr(planum)):
					cur.execute("SELECT planum,planame FROM player WHERE platag='"+planum+"'")
					rows = cur.fetchall()
					if (len(rows) == 1):
						self.planame = rows[0][1]
						self.planum = rows[0][0]
						self.platag = planum
		con.close()
	
	#this function returns an array of charicter Ids that represent the characters owned by the player in the DB
	def list_characters(self):
		con = get_connection()
		cur = con.cursor()
		
		cur.execute("SELECT chanum FROM charicter WHERE planum="+str(self.planum))
		
		rows = cur.fetchall()
		
		#get the rows into a pleasent array format	
		ret_val = []
		for row in rows:
			#append the id to the id array
			ret_val.append(row[0])
		
		#return that array
		return ret_val
		
if __name__ == '__main__':
	bob = character(1)
	print(bob.chaname)	
	print(bob.stats['str'])
	print(player(bob.planum).planame)
	print(player('98156571031').planame)
	print(stat('str').stadesc)
	print(clear_trailing_white('a     ')+ 'b')
