import os
import subprocess
import sys
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

import asyncio
import threading

from concurrent.futures import ThreadPoolExecutor

import io

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WOLFRAM_API_KEY = os.getenv('WOLFRAM_API_KEY')

server_process = 0
ngrok_process = 0
addr = ''
waiting_command_response = False
cmd_ctx = None
waiting_for_start = False
ssh_channel_id = 0

bot = commands.Bot(command_prefix='!')
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([str(member.id) + ' ' + member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    game = discord.Game('ssh')
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    print(message.content)
    #if message.channel.id == 789625114769621003:
    if message.channel.id == ssh_channel_id:
        # send a line to the process
        if ssh_channel_id != 0:
            server_process.stdin.write((message.content).encode())
            server_process.stdin.flush()

@bot.command(name='ping', help='pong!')
async def ping(ctx):
    await ctx.send('pong!')

async def output_reader(proc, loop):
    global current_players
    global waiting_command_response
    global cmd_ctx
    global waiting_for_start

    message = None
    io_pool_exc = ThreadPoolExecutor()

    while True:
        line = await loop.run_in_executor(io_pool_exc, proc.stdout.readline)

        current = line.decode('utf-8')

        if not bot.is_closed():
            '''
            player_message = re.search(r'^\[.*\] \[.*\]: (<.*>.*)$', current)
            if player_message != None:
                #await bot.get_channel(789625114769621003).send(player_message.groups()[0])
                await bot.get_channel(761382066360680448).send(player_message.groups()[0])

            player_joined = re.search(r': (.*) joined the game', current)
            if player_joined != None:
                #await bot.get_channel(789625114769621003).send(player_joined.groups()[0] + ' joined the game')
                await bot.get_channel(761382066360680448).send(player_joined.groups()[0] + ' joined the game')            
                try:
                    current_players.add(player_joined.groups()[0])
                except:
                    pass

            player_left = re.search(r': (.*) left the game', current)
            if player_left != None:
                #await bot.get_channel(789625114769621003).send(player_left.groups()[0] + ' left the game')
                await bot.get_channel(761382066360680448).send(player_left.groups()[0] + ' left the game')
                try:
                    current_players.remove(player_left.groups()[0])
                except:
                    pass
            '''

            await cmd_ctx.send(current)

            '''
            if waiting_for_start and message == None:
                message = await cmd_ctx.send('```m\n' + current + '```')
            elif waiting_for_start:
                await message.edit(content=('```m\n' + current + '```'))
                if re.search(r'Done \(.*\)!', current):
                    waiting_for_start = False
                    message = None
                    await cmd_ctx.send('Success! Server address: ' + addr + '\n\nIf you are at Austin\'s house, use 192.168.0.113:25566')
             '''   

        print(current, end='')

def input_handler(proc):
    while True:
        try:
            proc.stdin.write((input() + '\n').encode())
            proc.stdin.flush()
        except:
            return

@bot.command(name='ssh', help='Starts an ssh client')
async def startserver(ctx, *args):
    global server_process
    global ngrok_process
    global addr
    global waiting_for_start
    global cmd_ctx

    if ssh_channel_id != 0:
        await ctx.send('An ssh client is already running and I haven\'t set up multiprocessing yet, try again later.')
        return
        
    server_process = subprocess.Popen(['ssh'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    bot.loop.create_task(output_reader(server_process, bot.loop))
    #bot.loop.create_task(my_background_task(ctx, server_process))
    input_thread = threading.Thread(target=input_handler, args=(server_process,))
    input_thread.start()

    channel = await ctx.message.guild.create_text_channel('-'.join(['ssh'] + args))
    ssh_channel_id = channel.id
    cmd_ctx = ctx

for i in range(1000):
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(e)
        time.sleep(5)
        print('\nBot crashed, restarting...')

print('Reached maximum number of retries. Something went wrong.')
