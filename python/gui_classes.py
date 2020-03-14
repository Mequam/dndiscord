#this file contains all of the code to run the gui display with the DGUI code
import DGui
#this file contains all of the classes for sql interaction
import dndiscord_sql

#this gui is used to list all of the characters that a player has and allow them to interact with them
class charicter_list_gui(DGui.gui):
	def __init__(self,player):
		self.Id = 0
		self.player = player
		
		#this represents the index of the character that the user selected
		self.target_index = -1
		#this represents the index of the page that the user wants to view, each page contains at least 5 users from the db
		self.target_page = 0 

		self.characters = []
		#get a list of character ids that belong to the player
		char_id_list = player.list_characters()
		for chaid in char_id_list:
			self.characters.append(dndiscord_sql.character(chaid))
		
		self.windows = [charicter_list_gui.char_name_win,charicter_list_gui.focused_char_win]
		self.emojiL = ['⬅️','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','➡️']
	
	#this function displays a window of 5 character names starting
	#on the index represented by the target_page of the class
	def char_name_win(self):
		ret_val = ''	
		#we are printing 5 characters
		for i in range(0,5):
			#leave the loop if we run out of characters to print
			if (i+self.target_page >= len(self.characters)):
				break
			#append the characters to our return value
			ret_val += str(i+1) + ':' + self.characters[i+self.target_page].chaname	
			#seperate every name but the last name with a newline
			#we know the last name is target_window+4 because +5 brings us to a new window in base 5
			if (i != self.target_page+4):
				ret_val += '\n'	
		return ret_val
	#this function is a window function that returns more information about the character who is in focus in
	#the gui
	def focused_char_win(self):
		#the user has not yet selected a character
		if (self.target_index == -1):
			return 'select a character'
		ret_val = ''
		for stat in self.characters[self.target_index].stats:
			#append the stat name and stat value to the return string
			ret_val += stat + ':' + str(self.characters[self.target_index].stats[stat]) + '\n'
		return ret_val
	#this function is run whenever the user presses a button on our gui
	def update(self,reaction,user):
		#if the user has not yet selected a character
		if (self.target_index == -1):
			#this runs if we have not yet selected a character
			if (reaction.emoji=='1️⃣'):	
				self.target_index=self.target_page
			elif (reaction.emoji == '2️⃣'):
				if len(self.characters) > self.target_page+1:
					self.target_index=self.target_page+1
			elif (reaction.emoji == '3️⃣'):
				if len(self.characters) > self.target_page+2:
					self.target_index=self.target_page+2
			elif (reaction.emoji == '4️⃣'):
				if len(self.characters) > self.target_page+3:
					self.target_index=self.target_page+3
			elif (reaction.emoji == '5️⃣'):
				if len(self.characters) > self.target_page+4:
					self.target_index=self.target_page+4
			elif (reaction.emoji == '⬅️'):
				#the user wants to move the page back, this means subtract 5 from our window	
					self.target_page=self.target_page-5
					#this impliments the loop around feature and handles bounds checking for the array
					if (self.target_page < 0 or self.target_page >= len(self.characters)): #check if the array is out of bounds in the oppisit direction just in case

						#modulus 5 represents the number of characters in the last slot
						#if we remove that from the total length of the slot the remainding length
						#gives us the first index of the last slot 
						self.target_page = len(self.characters)-(len(self.characters)%5)
			elif (reaction.emoji == '➡️'):
				#the user wants to move onto the next page
				self.target_page+=5
				if (self.target_page >= len(self.characters) or self.target_page < 0):
					self.target_page = 0 #the first index of the first window is allways zero		
			return True
			
		else:
			#we have selected a character, now what will the user do with them?
			print('[DEBUG] selected ' + self.characters[self.target_index].chaname)

class charicter_gui(DGui.gui):
	#this function initilizes the gui to display a character
	#it sets up the window list (an array of functions stored in self.windows that render the gui as text)
	#sets up the emoji list (emojiL that stores a list of buttons to click on)
	#and stores the character to display, char, inside of it
	def __init__(self,char):
		#an id of zero indicates that we have not yet set our id and the driving code should set it for us
		self.Id = 0 
		self.char =  char
		self.test_text = 'blah'
		self.windows = [charicter_gui.header_display,charicter_gui.stat_display,charicter_gui.focused_stat_display]
		self.emojiL = []
		
		self.roll = 0

		#this variable is used to store the selected stat of the character 
		self.selected_stat = None
		for key in char.stats:
			#loop throught the keys and use their emojis in our buttons
			self.emojiL.append(dndiscord_sql.stat(key).emoji)
		self.emojiL.append('➕')
		self.emojiL.append('➖')
	#this function is run every time that someone clicks on one of the buttons on the gui and is used to update the
	#internal variables of the display before the windows render it
	def update(self,reaction,user):	
		if (reaction.emoji == '🎲'):
			print('[DEBUG] this feature is not yet implimented')			
		elif (reaction.emoji == '➕'):
			if (self.selected_stat != None):
				#incriment the selected stat
				self.char.stats[self.selected_stat]+=1
		elif (reaction.emoji == '➖'):
			if (self.selected_stat != None):
				#decriment the selected stat
				self.char.stats[self.selected_stat]-=1
		else:	
			#they have selected an emoji
			self.selected_stat = reaction.emoji
		return True
	#this window displays the name and race of the given charaicter
	def header_display(self):
		ret_val = '**name**:' + self.char.chaname + '\t' + '**race**:'+self.char.racname
		return ret_val
	#this window is in charge of displaying each stat for the user to see
	#it loops over the sats of our character and adds them to the output of the window
	def stat_display(self):
		ret_val = '**stats**\n\n'
		for key in self.char.stats:
			ret_val += key + ':' + str(self.char.stats[key]) + '\n'
		return ret_val
	
	#this display shows the user which stat they have slected
	def focused_stat_display(self):
		if (self.selected_stat == None):
			return 'no stat selected'
		else:
			return self.selected_stat + '\n' + str(self.char.stats[self.selected_stat])	
