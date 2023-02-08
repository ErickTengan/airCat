#            _           _____           _                ___        __            #
#           (_)         / ____|         | |              / _ \      /_ |           #
#     __ _   _   _ __  | |        __ _  | |_    __   __ | | | |      | |           #
#    / _` | | | | '__| | |       / _` | | __|   \ \ / / | | | |      | |           #
#   | (_| | | | | |    | |____  | (_| | | |_     \ V /  | |_| |  _   | |           #
#    \__,_| |_| |_|     \_____|  \__,_|  \__|     \_/    \___/  (_)  |_|           #
#                                           _____________________________          # 
#                                                  github.com/ErickTengan          #
#                                           live on twitch.tv/elicktengan          #
#                                           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾          #
#  [Twitch and MySQL credentials are stored on envsetup.py]                        #

import aiomysql, asyncio
from twitchio.ext import commands
from datetime import datetime, timedelta
from envsetup import *

## Hard-coded ##
FLIGHT_DURATION = 75    

## Hard-coded ##
places = ["Viracopos (VCP-SBKP) Campinas - SP / Brazil",
          "Santos Dumont (SDU-SBRJ) Rio de Janeiro - RJ / Brazil"]


loop = asyncio.get_event_loop()     # Needed for using async methods

class Bot(commands.Bot):

    def __init__(self):
        # Start bot with credentials. Prefix is a symbol used to identify the user's message as a command #
        super().__init__(token=twitchToken, prefix='#', initial_channels=[channelName])
        print("Starting...")

    async def event_ready(self):    # Run when connected
        # Log into console that bot is connected #
        print(datetime.now())
        print(f'airCat Service Bot is now online 🐈 | {self.nick}')
        print(f'Your user ID is | {self.user_id}')

    # ---   Commands Section (menu options)  --- #

    # --     | Show main menu (#cat) |     -- # 
    @commands.command()
    async def cat(self, ctx: commands.Context):
        await ctx.send(f'✈️ Welcome to airCat Client v0.1 🐈 ✈️ | Commands: #cat #catfly #newcat #catstatus')

    # --   | Start a new flight (#catfly) |   -- #
    @commands.command()
    async def catfly(self, ctx: commands.Context):
        twitchUser = ctx.author.name
        newrank = False
        conn = await aiomysql.connect(host=dbHost, port=3306, user=dbUser, password=dbPass, db=dbName, loop=loop)
        ##  SQL connected  ##
        cur = await conn.cursor()
        await cur.execute(f'SELECT COUNT(*) FROM pilots WHERE twitchUsr = "{twitchUser}"')  # Check for existing twitch username on database
        verifyTwitch = await cur.fetchone()
        if verifyTwitch[0] == 0:            # Send deny message if not and quit function
            await ctx.send(f"Hey {twitchUser}, you're not a cat pilot yet! To become one, send #newcat so you will receive a unique member ID and can start flying! 🐱✈️")
            return
        await cur.execute(f'SELECT place, flightHrs, expectedArrival, rank FROM pilots WHERE twitchUsr = "{twitchUser}"')   # Build and execute SQL query
        profile = await cur.fetchone()      # Fetch user's data and store it into a list
        # Store values into individual variables to manipulate data #
        place = profile[0]
        flighthrsbefore = profile[1]
        expectedarrival = profile[2]
        rank = profile[3]
        now = datetime.now()
        flightduration = FLIGHT_DURATION    # Get value in minutes from global scope and set it to a local variable
        if expectedarrival == '0000-00-00 00:00:00':
            expectedarrival = now
        timeleft = expectedarrival - now
        if timedelta.total_seconds(timeleft) > 0:   # Detect if user's is already flying. If yes, send a message and quit function.  
            timeleft = str(timeleft)
            await ctx.send(f'Captain {twitchUser}, you are already flying! Time left: {timeleft[:7]}')
            await cur.close()
            conn.close() 
            return
        # Start a flight 🛫 #
        expectedarrival = now + timedelta(minutes=flightduration)
        if place == 0:                                                                  ##  [Hard-Coded] Destiny set-up  ##
            flightplan = 'Campinas/SP --> Rio de Janeiro/RJ (SBKP/VCP -> SBRJ/SDU)'     ## 
            destiny = 1                                                                 ##  'destiny' and 'place' are expected to be
        else:                                                                           ##  attributes from a 'route' object not yet developed.
            flightplan = 'Rio de Janeiro/RJ --> Campinas/SP  (SBRJ/SDU -> SBKP/VCP)'    ##  'flightplan' will also be system-generated.
            destiny = 0                                                                   
        flighthrsT = flighthrsbefore + (flightduration/60)  # Set user's final flight hours value to store it on database
        await cur.execute(f"SELECT hours FROM ranks WHERE id = {rank}")
        rankinfo = await cur.fetchone()
        hoursrank = rankinfo[0]
        rank = int(rank)
        if flighthrsT > hoursrank:      # Add rank if user's new flight hours is greater than the past rank. Only add 1 rank per flight.
            rank += 1
            newrank = True
        await cur.execute(f'UPDATE pilots SET tmspLastTakeoff = CURRENT_TIMESTAMP, place = {destiny}, flightHrs = {flighthrsT}, expectedArrival = ADDTIME(CURRENT_TIMESTAMP, "{timedelta(minutes=flightduration)}"), rank = {rank} WHERE pilots.twitchUsr = "{twitchUser}"')
        await conn.commit()
        await cur.close()
        conn.close()
        ##  /SQL  ##
        await ctx.send(f'Air Traffic Controller says: {twitchUser}, cleared to take-off! ...🛫...  | Flight Route: {flightplan} | ETE (Expected Time En Route) : {flightduration} minutes | Status: Flying ✈️☁️')
        if newrank:
            await ctx.send(f'{twitchUser} just got a new rank!!! Use #catstatus to see it on your profile.')
        print(datetime.now())       # Log activity on console
        print(f'Pilot {twitchUser} started a flight: {flightplan}')

    # --   | Check user status (#catstatus) |   -- #
    @commands.command()
    async def catstatus(self, ctx: commands.Context):
        conn = await aiomysql.connect(host=dbHost, port=3306, user=dbUser, password=dbPass, db=dbName, loop=loop)
        ## SQL connected ##
        cur = await conn.cursor()
        twitchUser = ctx.author.name
        await cur.execute(f"SELECT id, flightHrs, place, expectedArrival, rank, CURRENT_TIMESTAMP FROM pilots WHERE twitchUsr = '{twitchUser}'")
        profile = await cur.fetchone()
        if not profile:
            await ctx.send(f"Hey {twitchUser}, you're not yet an airCat pilot. To become one, just type #newcat on chat! 🐱✈️")
            return
        # Store user's data into local variables #
        idnum = profile[0]
        flighthrs = profile[1]
        place = places[profile[2]]
        expectedarrival = profile[3]
        rank = profile[4]
        now = profile[5]
        if expectedarrival == '0000-00-00 00:00:00':
            expectedarrival = now
        if expectedarrival > now:
            place = "Sky ✈️☁️"
            flighthrs = flighthrs - (timedelta.total_seconds(expectedarrival - now)/3600)
        await cur.execute(f"SELECT rankName FROM ranks WHERE id = {rank}")
        rankinfo = await cur.fetchone()
        userrank = rankinfo[0]
        await cur.close()
        conn.close()
        ##  /SQL  ##
        # Assemble full string and send it on chat #
        await ctx.send(f'airCat Pilot #{idnum} - Captain {ctx.author.name} 🐱✈️ |  Rank: {userrank}  |  Flight Hours: {round(flighthrs, 3)}  |  Location: {place} |')


    # --   | Register new user (#newcat) |   -- #
    @commands.command()
    async def newcat(self, ctx: commands.Context):
        twitchUser = ctx.author.name
        ## SQL connected ##
        conn = await aiomysql.connect(host=dbHost, port=3306, user=dbUser, password=dbPass, db=dbName, loop=loop)
        cur = await conn.cursor()
        await cur.execute(f"SELECT COUNT(*) FROM pilots WHERE twitchUsr = '{twitchUser}'")      # Check for existing twitch username on database
        verifyTwitch = await cur.fetchone()
        if verifyTwitch[0] != 0:
                await ctx.send(f'Hey Captain {twitchUser}, you are already a registered cat-pilot. Use #chatfly to start a flight or #catstatus to show your profile info. 🐈✈️')
                await cur.close()
                conn.close()
                return
        await cur.execute(f"INSERT INTO pilots (twitchUsr, tmspReg, place, rank) VALUES ('{twitchUser}', CURRENT_TIMESTAMP, 0, 1)")
        await conn.commit()
        await cur.execute(f"SELECT id FROM pilots WHERE twitchUsr = '{twitchUser}'")
        userid = await cur.fetchone()
        await cur.close()
        conn.close()
        ### /SQL ###
        # Send confirmation message and log activity into console # 
        await ctx.send(f'Congratulations {twitchUser}, you are the #{userid[0]} cat pilot at airCat! Use #catfly to start your first solo flight. 🐈✈️')
        print(datetime.now())
        print(f'New airCat player registered: {twitchUser}')
        return 

bot = Bot()
bot.run()