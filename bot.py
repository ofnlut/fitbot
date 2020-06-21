#imports 
import challonge
import config
import discord
from discord.ext import commands
import asyncio


# Enter your API keys here. Its recommended you use something else to hide
# the keys rather than placing them into file.

# Todo: hide API keys

challonge.set_credentials(config.challgone_api_name, config.challgone_api_key)
DISCORD_TOKEN = config.discord_api_token

BOT_PREFIX = ("!")
bot = commands.Bot(command_prefix=BOT_PREFIX)

#global bracket 
battle_queue = {
    "active": False,
    "queued": 0,
    "slots": 0,
    "players": [],
}


def start_queue(leader, leaderId):
    """figure out if a fit battle can happen"""
    global battle_queue
    if battle_queue.get("active"):
        return False
    else:
        new_queue = {
            "active": True,
            "leader": leader,
            "leaderId": leaderId,
            "queued": 1,
            "slots": 2,
            "players":[leader],
            "playerIds":[leaderId],
            "round": 0,
        }
        battle_queue = new_queue.copy()
        print(battle_queue)
        return True

#say hi
@bot.command()
async def hello(ctx):
    msg = "hi!"
    await ctx.send(msg)

#check whos waiting
@bot.command()
async def queue(ctx):
    if battle_queue.get("active") == False:
        msg = 'There currently isn''t a battle queued! ''!battle'' to start one.' 
    else:
        msg = 'there are currently ' + ' (' + str(battle_queue.get("queued"))+ '/' + str(battle_queue.get("slots")) +')' + ' members waiting to start!'
    await ctx.send(msg)




#start a new bracket
@bot.command()
async def battle(ctx):
    leader = ctx.message.author.name
    leaderId = ctx.message.author.id
    if(start_queue(leader, leaderId)):
        msg = '{0.author.mention} started a fit battle!'.format(ctx) + ' (' + str(battle_queue.get("queued"))+ '/' + str(battle_queue.get("slots")) +')'
        await ctx.send(msg)
    else:
        msg = 'Sorry a fit battle is currently active please wait for the current battle to conclude.'
        await ctx.send(msg)


#add to the queue
@bot.command()
async def add(ctx):
    if ctx.message.author.name in battle_queue.values():
        msg = '{0.author.mention} you are already in queue...dumbass'.format(ctx) + ' (' + str(battle_queue.get("queued"))+ '/' + str(battle_queue.get("slots")) +')'
    else:
        battle_queue["queued"] = battle_queue.get("queued") + 1
        battle_queue["players"].append(ctx.message.author.name)
        battle_queue["playerIds"].append(ctx.message.author.id)
        #if the queue matches the current slots remind the leader to
        # start the game if they want 
        if(battle_queue.get("queued") == battle_queue.get("slots")):
            msg = '{0.author.mention} added to the queue!'.format(ctx) + ' <@'+str(battle_queue.get("leaderId")) + '> you can start or wait for more players!' + ' (' + str(battle_queue.get("queued"))+ '/' + str(battle_queue.get("slots")) +')'
        elif (battle_queue.get("queued") > battle_queue.get("slots")):
            battle_queue["slots"] = battle_queue.get("slots") * 2
            msg = '{0.author.mention} added to the queue!'.format(ctx) + ' (' + str(battle_queue.get("queued"))+ '/' + str(battle_queue.get("slots")) +')'
        else:
            msg = '{0.author.mention} added to the queue!'.format(ctx) + ' (' + str(battle_queue.get("queued"))+ '/' + str(battle_queue.get("slots")) +')'
    print(battle_queue)        
    await ctx.send(msg)


#start
#take the current playerlist and find their id
#DM them and tell them to send a photo for the first round
#once everyone has sent a photo run the routine to create the challong bracket
#this is the hard part i think
@bot.group()
async def start(ctx):
    #check if the person who invoked is the leader
    if ctx.author.id != battle_queue.get("leaderId"):
        msg = 'Sorry <@'+str(battle_queue.get("leaderId")) + '> must start the battle.'
        await ctx.send(msg)
    else:
        #increment the round 
        battle_queue["round"] = battle_queue.get("round") + 1
        #roll call and send out DM
        for i in battle_queue.get("playerIds"):
            msg = 'You queued for ' + str(battle_queue.get("leader")) + "'s fit battle. Please upload a fit for Round " + str(battle_queue["round"])
            user = bot.get_user(i)
            await user.send(msg) 
            





bot.run(DISCORD_TOKEN)
