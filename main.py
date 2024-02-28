from datetime import datetime
from time import sleep 
import threading

from interactions.models.internal.annotations import slash

from server import Server
from os import getcwd
# from subprocess import capture_output

import interactions
from interactions import Embed, SlashContext, listen, Intents, slash_command

from mcstatus import JavaServer
from rcon import Client

bot = interactions.Client(intents=Intents.DEFAULT)

def shutdownTimer():
    def bossbar():

        def map_value(value, from_low, from_high, to_low, to_high):
            return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

        for x in range(7200, 0, -1):
            y = round(map_value(x, 0, 7200, 0, 100))
            s.sendCommand(f'bossbar set server:shutdownin value {y}')
            sleep(0.01)

        s.sendCommand('bossbar remove server:shutdownin')
        s.stop(True, 10)


    
    s.sendCommand('bossbar add server:shutdownin "Server Shut Down"')
    s.sendCommand('bossbar set server:shutdownin players @a')
    s.sendCommand('bossbar set server:shutdownin value 100')

    t = threading.Thread(target=bossbar())
    t.daemon = True
    t.start()

def Main():
    def main():
        while True:
            if datetime.now().time().hour == 18:
                print('yes')
                shutdownTimer()
            sleep(2)

    t = threading.Thread(target=main)
    t.start()

    pass

root = getcwd()
remoteIP = "147.185.221.18"
remotePort = 32681

s = Server(
    jar=root + "/server/paper-1.20.4-423.jar",
    path=root + "/server",
    minimumRAM="1G",
    maximumRAM="8G",
)

@listen()
async def on_startup():
    print("Bot init")

@slash_command(name="start", description="UnU")
async def start(ctx: SlashContext):
    await ctx.send(embed=Embed("Starting Server", "Please wait"), ephemeral=True)
    s.start()
    pass

@slash_command(name="stop", description="Stop")
async def stop(ctx: SlashContext):
    await ctx.send(embed=Embed("Stopping Server", "Please wait"), ephemeral=True)
    s.stop()

@slash_command(name="status", description="Get information about the server")
async def status(ctx: SlashContext):
    e = Embed(title="Status", 
              description="Information about the server",
              color=16711680,
              )
    await ctx.send(embed=Embed(title="Loading", description="Pinging server")) 
    
    localhost = ":ballot_box_with_check:" if s.isOnline() else ":x:"
    portforward = ""

    try:
        JavaServer(remoteIP, remotePort).status()
    except :
        portforward = ":x:"
        e.add_field("Port Forward", portforward, True)
        e.add_field("localhost", localhost,True)
    else:
        portforward = ":ballot_box_with_check:"
        # memory = capture_output()
        e.add_field("Port Forward", portforward, True)
        e.add_field("localhost", localhost,True)

        e.add_field("Memory Stats", "NaN")
        e.add_field("Online Players", JavaServer.lookup('localhost').status().players.online, True)
        e.add_field("Up Time", "5 Hours, 12 mins", True)
    
    await ctx.edit(embed=e)
    pass

bot.load_extension("interactions.ext.jurigged")

with open('token') as f:
    bot.start(f.read())

