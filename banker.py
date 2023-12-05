from commands import *
import discord, random, string, asyncio, pickle, os, csv


class propertyClass:
    def __init__(
        self,
        listVals
    ):
        self.PropertyUS = listVals[0]
        self.PropertyInternational = listVals[1]
        self.Cost = listVals[2]
        self.Site = listVals[3]
        self.ColorSet = listVals[4]
        self.H1 = listVals[5]
        self.H2 = listVals[6]
        self.H3 = listVals[7]
        self.H4 = listVals[8]
        self.Hotel = listVals[9]
        self.BuildingCost = listVals[10]
        self.Mortgage = listVals[11]
        self.UnmortgageCost = listVals[12]
        self.Index=listVals[13]


class playerClass:
    def __init__(self, user):
        self.user = user

    playerNum = -1
    value = 1500
    properties = []
    map = 0


playerList = []
propertyList=[]
gameMode = {"gameMessage": None, "jailMessage": None, "propertySellAuction": None}
# TODO: changing gameMessage for testing
gameMessage = [1]


client = discord.Client(intents=discord.Intents.all())

with open("config.txt", "r") as fileRead:
    token = fileRead.read()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global globalMessage
    messageValue = str(message.content.lower())
    # -------------------
    # TODO: Temp added
    notInList = True
    for val in playerList:
        if val.user == message.author:
            notInList = False
            break
    if notInList:
        pass
        #playerList.append(playerClass(message.author))
    # ------------------
    if messageValue.startswith("game start"):
        gameMode["gameMessage"] = None
        gameMode["gameMessage"] = await message.channel.send(
            "Starting game.\nTo participate react with 🚩 to the game start message"
        )
        await gameMode["gameMessage"].add_reaction("🚩")

    if len(gameMessage) != 1:
        return
    elif message.content == ("print"):
        for i in propertyList:
            print(i.PropertyInternational)
    elif message.content == ("com"):
        await message.channel.send(com()[0])
    elif message.content == ("cnc"):
        await message.channel.send(cnc()[0])
    elif message.content == ("list"):
        currPlayer = None
        for val in playerList:
            if val.user == message.author:
                currPlayer = val
                break
        else:
            await message.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        toReturn = "Properties: "
        for i in currPlayer.properties:
            toReturn += str(index(i)[0]) + ","
        await message.channel.send(toReturn)
    
    elif message.content == ("account"):
        currPlayer = None
        for val in playerList:
            if val.user == message.author:
                currPlayer = val
                break
        else:
            await message.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        toReturn = str(currPlayer.user)+" now has $"+str(currPlayer.value)
        await message.channel.send(toReturn)
    
    elif message.content == ("dice"):
        num = dice()
        toReturn = (
            str(currPlayer.user)
            + str(message.author)
            + " has rolled "
            + str(num[0])
            + "+"
            + str(num[1])
            + "="
            + str(num[2])
        )
        await message.channel.send(toReturn)
    elif message.content == ("roll"):
        currPlayer = None
        for val in playerList:
            if val.user == message.author:
                currPlayer = val
                break
        else:
            await message.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        if currPlayer.map >= 0:
            num = dice()
            asyncio.create_task(mapMovement(currPlayer, num, message.channel))

        else:
            gameMode["jailMessage"] = await message.channel.send(
                "Choose how you wish to get out of jail: \n1. By rolling a double \n2. Using a “Get out of jail free” card \n3.paying a $50 fine."
            )
            await gameMode["jailMessage"].add_reaction("1️⃣")
            await gameMode["jailMessage"].add_reaction("2️⃣")
            await gameMode["jailMessage"].add_reaction("3️⃣")


async def mapMovement(currPlayer, num, channel):
    currPlayer.map = (currPlayer.map + num[2]) % 40
    action = index(currPlayer.map)

    toReturn = (
        str(currPlayer.user)
        + " has rolled "
        + str(num[0])
        + "+"
        + str(num[1])
        + "="
        + str(num[2])
        + "\n"
        + str(currPlayer.user)
        + " has landed on "
        + action[0]
    )
    if action[1] == 2:
        await channel.send(toReturn)
        await channel.send(file=discord.File(action[2]))
        prop=None
        for i in propertyList:
            if int(i.Index)==currPlayer.map:
                prop=i
                break
        toReturn = "\nCost: "+str(prop.Cost)+"\nWould you like to \n1.Buy\n2.Auction"
        # 0:message, 1:player
        gameMode["propertySellAuction"] = [await channel.send(toReturn), currPlayer, prop]
        await gameMode["propertySellAuction"][0].add_reaction("1️⃣")
        await gameMode["propertySellAuction"][0].add_reaction("2️⃣")
    else:
        if action[1] == 0:
            comAct = com()
            toReturn += "\n" + comAct[0]

            if comAct[1] == 0:
                currPlayer.value += comAct[2]
                toReturn += (
                    "\n" + str(currPlayer.user) + " now has $" + str(currPlayer.value)
                )
            elif comAct[1] == 1:
                currPlayer.properties.append(comAct[2])
                toReturn += (
                    "\n" + str(currPlayer.user) + " now has " + str(index(comAct[2])[0])
                )
            elif comAct[1] == 2:
                for i in playerList:
                    if i.user == currPlayer:
                        continue
                    i.value -= comAct[2]
                currPlayer.value += comAct[2]
                toReturn += (
                    "\n" + str(currPlayer.user) + " now has $" + str(currPlayer.value)
                )
            elif comAct[1] == 3:
                currPlayer.map = -1
        elif action[1] == 1:
            cncAct = cnc()
            toReturn += "\n" + cncAct[0]
            if cncAct[1] == 0:
                currPlayer.value += cncAct[2]
                toReturn += (
                    "\n" + str(currPlayer.user) + " now has $" + str(currPlayer.value)
                )

        elif action[1] == 3:
            currPlayer.map = -1
        await channel.send(toReturn)


@client.event
async def on_reaction_remove(reaction, user):
    currPlayer = None
    for val in playerList:
        if val.user == user:
            currPlayer = val
            break
    if (
        currPlayer != None
        and reaction.message == gameMode["gameMessage"]
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        playerList.remove(currPlayer)
        await gameMode["gameMessage"].channel.send("Removed player " + str(user))


@client.event
async def on_reaction_add(reaction, user):
    global playerList
    if (
        reaction.message == gameMode["gameMessage"]
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        playerList.append(playerClass(user))
        await gameMode["gameMessage"].channel.send("Added player " + str(user))
    if (
        reaction.message == gameMode["propertySellAuction"][0]
        and user == gameMode["propertySellAuction"][1].user
    ):
        currPlayer = None
        for val in playerList:
            if val.user == user:
                currPlayer = val
                break
        if reaction.emoji == "1️⃣":
            currPlayer.value-=int(gameMode["propertySellAuction"][2].Cost)
            await gameMode["propertySellAuction"][0].channel.send(str(currPlayer.user)+" has bought "+str(gameMode["propertySellAuction"][2].PropertyInternational))
        elif reaction.message == "2️⃣":
            await gameMode["propertySellAuction"][0].channel.send("Auction")

    currPlayer = None
    for val in playerList:
        if val.user == user:
            currPlayer = val
            break
    if (
        currPlayer != None
        and currPlayer.map < 0
        and reaction.message == gameMode["jailMessage"]
    ):
        gameMode["jailMessage"] = None
        if reaction.emoji == "1️⃣":
            num = dice()
            if num[0] == num[1]:
                await reaction.message.channel.send("GOT OUT OF JAIL")
                currPlayer.map = 10
                asyncio.create_task(
                    mapMovement(currPlayer, num, reaction.message.channel)
                )
            else:
                toReturn = (
                    str(currPlayer.user)
                    + " has rolled "
                    + str(num[0])
                    + "+"
                    + str(num[1])
                    + "="
                    + str(num[2])
                    + "\nNot a double, so still stuck in jail"
                )
                await reaction.message.channel.send(toReturn)
        elif reaction.emoji == "2️⃣":
            pass
        elif reaction.emoji == "3️⃣":
            pass
with open("./resources/info.csv","r") as file:
    reader=csv.reader(file)
    next(reader)
    for row in reader:
        propertyList.append(propertyClass(row))

client.run(token)
