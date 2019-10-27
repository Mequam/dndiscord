#!/bin/python3


import discord
from discord.ext import commands
import bot_gui

def get_token(env='token'):
	#this function is used to retrive information for the bot
	try:
		import os
		return os.environ[env]
	except:
		return None
if __name__ == '__main__':
	import sys
	sys.path.append('./DGui')
	import DGui	
	
	print('[*] using discord.py version ' + str(discord.version_info))	
	bot = commands.Bot(command_prefix='dndiscord ')
	bot.remove_command('help')
	token = get_token()
	clientId = get_token('clientId')

	@bot.command()
	async def test(ctx,*args):
		g = bot_gui.addCharicter(ctx.author)
		await g.add(ctx) 
	if token == None:
		print('[ERROR] unable to retrive the token')
		quit()
	else:
		try:
			bot.run(token)
		except:
			print('[ERROR] unable to connect to discord!')
			quit()
	
	@bot.event
	async def on_reaction_add(reaction,user):
		print('[*] a reaction was added!')
		await DGui.checkGui(clientId,reaction,user)
