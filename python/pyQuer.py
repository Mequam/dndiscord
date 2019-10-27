import sanatize as san
import psycopg2 
import psycopg2.extras
def sqlStr(x):
	if type(x) == int:
		return str(x)
	else:
		return "'" + str(x) + "'"
def clearRightWhite(string):
	while string[-1] == ' ':
		string = string[0:-1]
	return string
class query:
	def __init__(self,mode,table,primary):
		self.mode = mode
		self.primary = primary
		self.table = table
	def sanitize(self):
		for key in self.__dict__:
			if k != 'mode':
				if not san.checkStr(str(self.__dict__[key])):
					return False
		return True
	def load(self):
		if 's' not in self.mode:
			return False
		conn = san.getConn()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		

		#run the sanatization checks
		if not (san.checkStr(self.table) and san.checkStr(self.primary[0]) and san.check(sqlStr(self.primary[1]))):
			return False
		
		cur.execute('SELECT * FROM ' + self.table + " WHERE " + self.primary[0] + "=" + sqlStr(self.primary[1]) + ' LIMIT 1')
		row = cur.fetchone()
		
		if row == None:
			print('[ERROR] primary key does not exist!')
			return False
	
		for key in row:
			if key in self.__dict__:
				if type(row[key]) == str:
					self.__dict__[key] = clearRightWhite(row[key]) # the whitespace to the right of values we read from the database is not
					#necicary for storage
				else:
					self.__dict__[key] = row[key]
		conn.close()

	def save(self):
		if not ('u' in self.mode or 'i' in self.mode):
			#they need to be able to write or creat enew information in order to use this fucntion
			return False
		conn = san.getConn()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		
		if not (san.checkStr(self.primary[0]) and san.checkStr(self.primary[1]) and san.checkStr(self.table)):
			return False
		cur.execute('SELECT ' + self.primary[0] + ' FROM ' + self.table + ' WHERE ' + self.primary[0] + '=' + sqlStr(self.primary[1]) + ' LIMIT 1')
		row = cur.fetchone()

		if len(row) < 1:
			print('[ERROR] invalid primary key!')
			return False


		#create the set clause of the sql statement
		sets = []
		for key in self.__dict__:
			#run the sanatization checks on the stats before appending them to our dictionary		
			if key != 'mode' and key != 'primary' and key != 'table' and san.checkStr(key) and san.checkStr(self.__dict__[key]):
				sets.append(key + '=' + sqlStr(self.__dict__[key]))
		
		sets = ",".join(sets)
	
		if not (san.checkStr(self.primary[0]) and san.checkStr(self.primary[1]) and san.checkStr(self.table)):
			return False
		
		cond = self.primary[0] + '=' + sqlStr(self.primary[1])

		cur.execute('UPDATE ' + self.table + ' SET ' + sets + ' WHERE ' + cond)	
		
		conn.commit()
		conn.close()
	def create(self):
		if not 'i' in self.mode:
			return False
		conn = san.getConn()
		cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		
		if not san.checkStr(self.primary[0]) and san.checkStr(self.primary[1]):
			return False

		col = []
		val = []
		for key in self.__dict__:
			if key != 'mode' and key != 'primary' and key != 'table' and san.checkStr(key) and san.checkStr(self.__dict__[key]):
				col.append(key)
				val.append(sqlStr(self.__dict__[key]))
		col = '(' + ",".join(col) + ')'
		val = '(' + ",".join(val) + ')'
	
		cur.execute('INSERT INTO ' + self.table + col + ' VALUES' + val)
		
		conn.commit()
		conn.close()
class stat(query):
	def __init__(self,staname):
		query.__init__(self,'siu','stat',('staname',staname))
		self.staname = staname
		self.stadesc = None
		self.staroll = None

if __name__ == '__main__':
	s = stat('hp')	
	s.staroll='1d100'
	s.stadesc='how close to death you have succumbed'
	s.create()

	print('printing stat description')
	print(clearRightWhite('this is a super secret message from the illuminati with spaces to teh right              '),end='')
	print('test')
	print(s.stadesc)
