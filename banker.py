from commands import *
import discord, random, string, asyncio, pickle, os, csv, time


class propertyClass:
    def __init__(self, listVals):
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
        self.Index = listVals[13]

    def getRent(self) -> int:
        return int(self.Site)

    owner = None


class playerClass:
    def __init__(self, user):
        self.user = user

    def addProperty(self, property: propertyClass) -> None:
        property.owner = self
        self.properties.append(property)

    playerNum = -1
    value = 1500
    properties = []
    map = 0


class gameModeClass:
    def __innit__(
        self, gameMessage, jailMessage, propertySellorAuction, auctionMessage, timer
    ):
        self.gameMessage = gameMessage
        self.jailMessage = jailMessage
        self.propertySellorAuction = propertySellorAuction
        self.auctionMessage = auctionMessage
        self.timer = timer


playerList: list[playerClass] = []
propertyList = []

gameMode = gameModeClass(None, None, None, None, None)

# TODO: changing gameMessage for testing
gameMode.gameMessage = 1


def getUser(user: discord.Member) -> playerClass:
    currPlayer = None
    for val in playerList:
        if val.user == user:
            currPlayer = val
            break
    return currPlayer


def getProperty(num: int) -> propertyClass:
    prop = None
    for i in propertyList:
        if int(i.Index) == num:
            prop = i
            break
    return prop


client = discord.Client(intents=discord.Intents.all())

with open("config.txt", "r") as fileRead:
    token = fileRead.read()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message: discord.Message):
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
        playerList.append(playerClass(message.author))
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
        playerList[0].map = -1
    elif message.content == ("test"):
        playerList[1].addProperty(getProperty(1))

    elif message.content.startswith("bid"):
        currPlayer = getUser(message.author)
        if currPlayer == None:
            await message.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        if (
            gameMode["auctionMessage"] != None
            and message.content.split("bid ")[1].strip().isdigit()
        ):
            currentBid = int(message.content.split("bid ")[1].strip())
            oldBid = gameMode["auctionMessage"][0]
            prop = gameMode["auctionMessage"][1]
            if currentBid <= oldBid or currentBid < 1:
                await message.channel.send("Please bid more than " + str(oldBid))
            elif currentBid > currPlayer.value:
                await message.channel.send("Please do not bid more than what you have")
            else:
                toReturn = (
                    str(currPlayer.user)
                    + " has bid $"
                    + str(currentBid)
                    + " for "
                    + str(prop.PropertyInternational)
                )
                gameMode["auctionMessage"] = [currentBid, prop, currPlayer.user]
                await message.channel.send(toReturn)
                if gameMode["timer"] != None and not gameMode["timer"].done():
                    gameMode["timer"].cancel()
                gameMode["timer"]: asyncio.Task = asyncio.create_task(
                    auctionTimer(message.channel, 5)
                )

    elif message.content == ("sudo com"):
        await message.channel.send(com()[0])
    elif message.content == ("sudo cnc"):
        await message.channel.send(cnc()[0])
    elif message.content == ("list"):
        currPlayer = getUser(message.author)
        if currPlayer == None:
            await message.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        toReturn = str(currPlayer.user) + "'s Properties: "
        for i in currPlayer.properties:
            if i.ColorSet == "0":
                toReturn += ":brown_square:"
            elif i.ColorSet == "1":
                toReturn += ":blue_square:"
            elif i.ColorSet == "2":
                toReturn += ":purple_square:"
            elif i.ColorSet == "3":
                toReturn += ":orange_square:"
            elif i.ColorSet == "4":
                toReturn += ":red_square:"
            elif i.ColorSet == "5":
                toReturn += ":yellow_square:"
            elif i.ColorSet == "6":
                toReturn += ":green_square:"
            elif i.ColorSet == "7":
                toReturn += ":black_large_square:"

            toReturn += " " + str(i.PropertyInternational) + ", "
        await message.channel.send(toReturn)

    elif message.content == ("account"):
        currPlayer = getUser(message.author)
        if currPlayer == None:
            await message.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        toReturn = str(currPlayer.user) + " now has $" + str(currPlayer.value)
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
        currPlayer = getUser(message.author)
        if currPlayer == None:
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


async def auctionTimer(channel: discord.TextChannel, countdown: int):
    if gameMode["auctionMessage"] == None:
        await channel.send("Auction has been concluded")
        return
    timer = await channel.send("CountDown:" + str(countdown))
    while countdown > 0:
        countdown -= 1
        await asyncio.sleep(1)
        await timer.edit(content=("CountDown:" + str(countdown)))
    currBid: int = gameMode["auctionMessage"][0]
    prop: propertyClass = gameMode["auctionMessage"][1]
    currPLayer: playerClass = getUser(gameMode["auctionMessage"][2])
    gameMode["auctionMessage"] = None
    currPLayer.value -= currBid
    prop.owner = currPLayer
    currPLayer.addProperty(prop)
    await channel.send(
        str(currPLayer.user)
        + " has bought "
        + str(prop.PropertyInternational)
        + " for $"
        + str(currBid)
    )


async def mapMovement(currPlayer: playerClass, num: int, channel: discord.TextChannel):
    toReturn = ""
    currPlayer.map = currPlayer.map + num[2]
    if currPlayer.map >= 40:
        toReturn += str(currPlayer.user) + " has crossed GO. They collect $200.\n"
        currPlayer.value += 200
        currPlayer.map = currPlayer.map % 40
    action = index(currPlayer.map)

    toReturn += (
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
        prop = getProperty(currPlayer.map)
        if prop.owner == None:
            toReturn = (
                "\nCost: " + str(prop.Cost) + "\nWould you like to \n1.Buy\n2.Auction"
            )
            # 0:message, 1:player
            gameMode["propertySellorAuction"] = [
                await channel.send(toReturn),
                currPlayer,
                prop,
            ]
            await gameMode["propertySellorAuction"][0].add_reaction("1️⃣")
            await gameMode["propertySellorAuction"][0].add_reaction("2️⃣")
        elif prop.owner == currPlayer:
            toReturn = "Welcome to your property"
            await channel.send(toReturn)
        else:
            toReturn = (
                "\nProperty: "
                + str(prop.PropertyInternational)
                + "is owned by "
                + str(prop.owner.user)
                + "\n"
                + str(currPlayer.user)
                + " pays "
                + str(prop.owner.user)
                + " $"
                + str(prop.getRent())
            )
            if currPlayer.value >= prop.getRent():
                currPlayer.value -= prop.getRent()
                prop.owner.value += prop.getRent()
            else:
                toReturn += (
                    str(currPlayer.user)
                    + " does not have enough. What would you like to do?"
                )
            await channel.send(toReturn)
    else:
        if action[1] == 0:
            comAct = com()
            toReturn += "\n" + comAct[0]

            if comAct[1] == 0:
                currPlayer.value += comAct[2]

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

            elif comAct[1] == 3:
                currPlayer.map = -1
        elif action[1] == 1:
            cncAct = cnc()
            toReturn += "\n" + cncAct[0]
            if cncAct[1] == 0:
                currPlayer.value += cncAct[2]

            elif cncAct[1] == 3:
                currPlayer.map = -1

        elif action[1] == 3:
            currPlayer.map = -1
        await channel.send(toReturn)


@client.event
async def on_reaction_remove(reaction, user):
    currPlayer = getUser(user)
    if (
        currPlayer != None
        and reaction.message == gameMode["gameMessage"]
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        playerList.remove(currPlayer)
        await gameMode["gameMessage"].channel.send("Removed player " + str(user))


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    global playerList
    if (
        reaction.message == gameMode["gameMessage"]
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        playerList.append(playerClass(user))
        await gameMode["gameMessage"].channel.send("Added player " + str(user))

    currPlayer = getUser(user)
    if currPlayer not in playerList:
        return
    if (
        gameMode["propertySellorAuction"] != None
        and reaction.message == gameMode["propertySellorAuction"][0]
        and user == gameMode["propertySellorAuction"][1].user
    ):
        if reaction.emoji == "1️⃣":
            channel = gameMode["propertySellorAuction"][0].channel
            if currPlayer.value >= int(gameMode["propertySellorAuction"][2].Cost):
                currPlayer.addProperty(gameMode["propertySellorAuction"][2])
                currPlayer.value -= int(gameMode["propertySellorAuction"][2].Cost)

                toReturn = (
                    str(currPlayer.user)
                    + " has bought "
                    + str(gameMode["propertySellorAuction"][2].PropertyInternational)
                )
                gameMode["propertySellorAuction"] = None
            else:
                toReturn = "You do not have enough funds to purchase this property"
            await channel.send(toReturn)
        elif reaction.emoji == "2️⃣":
            channel: discord.TextChannel = gameMode["propertySellorAuction"][0].channel
            prop: propertyClass = gameMode["propertySellorAuction"][2]

            gameMode["propertySellorAuction"] = None
            gameMode["auctionMessage"] = [0, prop]
            await channel.send(
                "Starting auction for "
                + prop.PropertyInternational
                + ". Please place your bids by typing 'bid NUMBER'"
            )

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
            currPlayer.value -= 50
            await reaction.message.channel.send(
                str(currPlayer.user)
                + " has payed the $50 fine. They are now out of jail"
            )
            currPlayer.map = 10
            asyncio.create_task(
                mapMovement(currPlayer, dice(), reaction.message.channel)
            )


with open("./resources/info.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        propertyList.append(propertyClass(row))

client.run(token)
