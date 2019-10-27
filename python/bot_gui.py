import sys
sys.path.append('./DGui')
import DGui
import random
def rollDice(num,typ):
	if num <= 0 or num <= 0:
		return 0
	ret_val = 0
	for i in range(0,num):
		ret_val += random.randrange(1,typ+1)
	return ret_val

class addCharicter(DGui.gui):
	def __init__(self,uid,stats=['str','dex','con','int','wis','cha']):
		#the arrays used by DGui
		self.id=uid	
		self.windows = [addCharicter.showUser,addCharicter.showOptions]
		self.emojiL = []
		
		
		self.stats=stats
		
		#initilize the rolls and stats that the player will be rolling
		self.rolls = []
		self.setStats = {}
		for stat in self.stats:
			self.rolls.append(rollDice(3,6))
			self.setStats[stat]=0
			self.emojiL.append('\u0000')
	def showUser(self):
		return str(self.id) 
	def showOptions(self):
		ret_val = ''
		for stat in self.stats:
			ret_val += stat + '\n'
		return ret_val
	def update(self,reaction,user):
		print('[*] updating :D')
		return True	
