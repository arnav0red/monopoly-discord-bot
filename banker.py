import discord, random, string, asyncio, pickle, os, csv, time


class mapItemClass:
    """Action:
    -1: None
    0: Community Chest
    1: Chance
    2: Property
    3: Go to Jail
    4: Tax
    5: Station
    6: Company
    """

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
        self.Emoji = listVals[14]
        self.Action = listVals[15]

    def __str__(self) -> str:
        toReturn = self.Emoji + " "
        toReturn += self.PropertyInternational
        return toReturn


class propertyClass:
    def __init__(self, index: int, owner):
        self.index = index
        self.owner = owner
        self.houses = 0
        self.hotel = 0

    def __str__(self) -> str:
        return (
            getMapItem(self.index).Emoji
            + " "
            + getMapItem(self.index).PropertyInternational
        )

    def getColorSet(self) -> int:
        return int(getMapItem(self.index).ColorSet)

    def getRent(self) -> int:
        return int(getMapItem(self.index).Site)


class playerClass:
    def __init__(self, user):
        self.user: discord.Member = user
        self.value: int = 1500
        self.properties: list[propertyClass] = []
        self.map: int = 0

    def __str__(self) -> str:
        return str(self.user)

    def addProperty(self, mapItem: mapItemClass) -> propertyClass:
        self.properties.append(None)
        i = len(self.properties) - 2
        while i >= 0:
            if self.properties[i].getColorSet() > int(mapItem.ColorSet):
                self.properties[i + 1] = self.properties[i]
            else:
                break
            i -= 1
        self.properties[i + 1] = propertyClass(int(mapItem.Index), self)
        return self.properties[i + 1]

    def hasProperty(self, property: propertyClass) -> bool:
        for i in self.properties:
            if i == property:
                return True
        return False

    def removeProperty(self, property: propertyClass) -> propertyClass:
        toReturn: propertyClass = None
        i = 0
        while i < len(self.properties):
            if self.properties[i] == property:
                toReturn = property
                break
            i += 1
        size = len(self.properties)
        self.properties = self.properties[0:i] + self.properties[i + 1 : size]
        return toReturn

    def useGetOutOfJailCard(self) -> bool:
        if getMapItem(40):
            pass


class gameModeClass:
    def __init__(
        self,
        gameMessage,
        jailMessage,
        propertySellorAuction,
        auctionMessage,
        timer,
        tradeMessage,
    ):
        self.gameMessage: discord.Message = gameMessage
        self.jailMessage: discord.TextChannel = jailMessage
        self.propertySellorAuction = propertySellorAuction
        self.auctionMessage = auctionMessage
        self.timer: discord.TextChannel = timer
        self.tradeMessage: discord.Message = tradeMessage
        self.playerList: list[playerClass] = []
        self.propertiesOwned: list[propertyClass] = []

    def getUser(self, user: discord.Member) -> playerClass:
        currPlayer = None
        for val in self.playerList:
            if val.user == user:
                currPlayer = val
                break
        return currPlayer

    def getUserFromString(self, user: str) -> playerClass:
        currPlayer = None
        for val in self.playerList:
            if str(val.user) == user:
                currPlayer = val
                break
        return currPlayer

    def registerPropertyOwned(self, property: propertyClass) -> None:
        self.propertiesOwned.append(property)

    def getProperty(self, mapItem: mapItemClass) -> propertyClass:
        toReturn = None
        for i in self.propertiesOwned:
            if i.index == int(mapItem.Index):
                toReturn = i
                break
        return toReturn


def getMapItem(num: int) -> mapItemClass:
    prop = None
    for i in mapItemList:
        if int(i.Index) == num:
            prop = i
            break
    return prop


mapItemList: list[mapItemClass] = []
hostedGames: list[gameModeClass] = []


def getGame(channel: discord.TextChannel) -> gameModeClass:
    toReturn = None
    for i in hostedGames:
        if i.gameMessage.channel == channel:
            toReturn = i
            break
    return toReturn


# TODO: changing gameMessage for testing
debug = False


client = discord.Client(intents=discord.Intents.all())

with open("config.txt", "r") as fileRead:
    token = fileRead.read()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message: discord.Message):
    messageValue = str(message.content.lower())
    gameMode=getGame(message.channel)
    if messageValue.startswith("game start"):
        if gameMode != None:
            await gameMode.gameMessage.channel.send(
                "There is already an existing game in this channel.\nPlease write ```game close``` to end it."
            )
            return
        
        for i in message.channel.threads:
            if i.name == "TRADE" and i.owner == client.user:
                await i.delete()
        gameMessage = await message.channel.send(
            "Starting game.\nTo participate react with 🚩 to the game start message"
        )
        gameMode=gameMode = gameModeClass(gameMessage, None, None, None, None, None)
        hostedGames.append(gameMode)
        
        await gameMode.gameMessage.add_reaction("🚩")

    if debug or gameMode==None:
        return
    
    # -------------------
    # TODO: Temp added
    notInList = debug
    for val in gameMode.playerList:
        if val.user == message.author:
            notInList = False
            break
    if notInList:
        pass
        gameMode.gameMessage = message
        gameMode.playerList.append(playerClass(message.author))
    # ------------------
    
    elif message.content == ("print"):
        pass

    elif message.content.startswith("move"):
        await mapMovement(
            gameMode.getUser(message.author),
            ["test", "test", int(message.content.split("move ")[1])],
            gameMode.gameMessage.channel,
        )
    elif message.content.startswith("test"):
        message.content = message.content.split("test ")[1]
        message.author = gameMode.playerList[1].user
        asyncio.create_task(on_message(message))
    elif message.content.startswith("bid"):
        currPlayer = gameMode.getUser(message.author)
        if currPlayer == None:
            await gameMode.gameMessage.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        if (
            gameMode.auctionMessage != None
            and message.content.split("bid ")[1].strip().isdigit()
        ):
            currentBid = int(message.content.split("bid ")[1].strip())
            oldBid = gameMode.auctionMessage[0]
            prop = gameMode.auctionMessage[1]
            if currentBid <= oldBid or currentBid < 1:
                await gameMode.gameMessage.channel.send(
                    "Please bid more than " + str(oldBid)
                )
            elif currentBid > currPlayer.value:
                await gameMode.gameMessage.channel.send(
                    "Please do not bid more than what you have"
                )
            else:
                toReturn = (
                    str(currPlayer.user)
                    + " has bid $"
                    + str(currentBid)
                    + " for "
                    + str(prop)
                )
                gameMode.auctionMessage = [currentBid, prop, currPlayer.user]
                await gameMode.gameMessage.channel.send(toReturn)
                if gameMode.timer != None and not gameMode.timer.done():
                    gameMode.timer.cancel()
                gameMode.timer: asyncio.Task = asyncio.create_task(
                    auctionTimer(gameMode.gameMessage.channel, 5)
                )
    elif message.content == ("sudo com"):
        await gameMode.gameMessage.channel.send(com()[0])
    elif message.content == ("sudo cnc"):
        await gameMode.gameMessage.channel.send(cnc()[0])
    elif message.content == ("list"):
        currPlayer = gameMode.getUser(message.author)
        if currPlayer == None:
            await gameMode.gameMessage.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        await listUser(gameMode.gameMessage.channel, currPlayer)
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
        await gameMode.gameMessage.channel.send(toReturn)
    elif message.content == ("roll"):
        await rollDice(gameMode.gameMessage.channel, gameMode.getUser(message.author))
    elif message.content.startswith("trade "):
        currPlayer = gameMode.getUser(message.author)
        if currPlayer == None:
            await gameMode.gameMessage.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        tradePlayer: playerClass = gameMode.getUserFromString(
            message.content.split("trade ")[1].strip()
        )

        if tradePlayer != None:
            if gameMode.tradeMessage != None:
                gameMode.tradeMessage = None
                await gameMode.gameMessage.channel.send(
                    "Starting a new trade. Terminating the last one in session."
                )
            thread = await gameMode.gameMessage.channel.create_thread(
                name="TRADE", type=discord.ChannelType.public_thread
            )
            await thread.add_user(currPlayer.user)
            await thread.add_user(tradePlayer.user)
            toReturn = (
                "Created trade group between "
                + str(currPlayer)
                + " and "
                + str(tradePlayer)
            )
            toReturn += "Write your offer in the format.\n```offer [USER] [AMOUNT] [PROPERTY1],[PROPERTY2],...```"

            await thread.send(toReturn)
        else:
            await gameMode.gameMessage.channel.send(
                "Can't find the user you're trying to trade with. Are you sure you've entered the correct name?"
            )
    elif message.content.startswith("offer "):
        currPlayer = gameMode.getUser(message.author)
        if currPlayer == None:
            await gameMode.gameMessage.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        tradePlayer: playerClass = gameMode.getUserFromString(
            message.content.split("offer ")[1].strip()
        )

        if tradePlayer != None:
            if gameMode.tradeMessage != None:
                gameMode.tradeMessage = None
                await gameMode.gameMessage.channel.send(
                    "Starting a new trade. Terminating the last one in session."
                )
            thread = await gameMode.gameMessage.channel.create_thread(
                name="TRADE", type=discord.ChannelType.public_thread
            )
            await thread.add_user(currPlayer.user)
            await thread.add_user(tradePlayer.user)
            toReturn = (
                "Created trade group between "
                + str(currPlayer)
                + " and "
                + str(tradePlayer)
            )
            toReturn += "Write your offer in the format.\n```offer [USER] [AMOUNT] [PROPERTY1],[PROPERTY2],...```"

            await thread.send(toReturn)
        else:
            await gameMode.gameMessage.channel.send(
                "Can't find the user you're trying to trade with. Are you sure you've entered the correct name?"
            )


async def tradeMethod(
    responseMessage: discord.Message,
    currPlayer: playerClass,
    tradePlayer: playerClass,
) -> None:
    pass


async def listUser(channel: discord.TextChannel, currPlayer: playerClass) -> None:
    toReturn = str(currPlayer.user) + "'s Account\nBalance: $" + str(currPlayer.value)
    toReturn += "\nProperties: "
    for i in currPlayer.properties:
        toReturn += " " + str(i) + "-No" + str(i.index) + ", "
    await channel.send(toReturn)


async def rollDice(channel: discord.TextChannel, currPlayer: playerClass) -> None:
    gameMode=getGame(channel)

    if currPlayer == None:
        await channel.send(
            "Huh! Weird that you're not in the game. Please react to the game start message to be added."
        )
        return
    if currPlayer.value < 0:
        await channel.send(
            "It appears you are in debt. Either get some funds or declare bankruptcy."
        )
    elif currPlayer.map >= 0:
        num = dice()
        await mapMovement(currPlayer, num, channel)
    else:
        gameMode.jailMessage = await channel.send(
            "Choose how you wish to get out of jail: \n1. By rolling a double \n2. Using a “Get out of jail free” card \n3.paying a $50 fine."
        )
        await gameMode.jailMessage.add_reaction("1️⃣")
        await gameMode.jailMessage.add_reaction("2️⃣")
        await gameMode.jailMessage.add_reaction("3️⃣")


async def auctionTimer(channel: discord.TextChannel, countdown: int):
    gameMode=getGame(channel)

    if gameMode.auctionMessage == None:
        await channel.send("Auction has been concluded")
        return
    timer = await channel.send("CountDown:" + str(countdown))
    while countdown > 0:
        countdown -= 1
        await asyncio.sleep(1)
        await timer.edit(content=("CountDown:" + str(countdown)))
    currBid: int = gameMode.auctionMessage[0]
    prop: mapItemClass = gameMode.auctionMessage[1]
    currPLayer: playerClass = gameMode.getUser(gameMode.auctionMessage[2])
    gameMode.auctionMessage = None
    currPLayer.value -= currBid
    gameMode.registerPropertyOwned(currPLayer.addProperty(prop))

    await channel.send(
        str(currPLayer.user) + " has bought " + str(prop) + " for $" + str(currBid)
    )


async def mapMovement(
    currPlayer: playerClass, num: list[int], channel: discord.TextChannel
):
    gameMode=getGame(channel)

    toReturn = ""
    currPlayer.map = currPlayer.map + num[2]
    if currPlayer.map >= 40:
        toReturn += str(currPlayer.user) + " has crossed GO. They collect $200.\n"
        currPlayer.value += 200
        currPlayer.map = currPlayer.map % 40
    prop = getMapItem(currPlayer.map)
    action = [
        str(prop),
        int(prop.Action),
        "./resources/" + prop.PropertyInternational + ".png",
    ]

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
        if gameMode.getProperty(prop) == None:
            toReturn = (
                "\nCost: " + str(prop.Cost) + "\nWould you like to \n1.Buy\n2.Auction"
            )
            # 0:message, 1:player
            gameMode.propertySellorAuction = [
                await channel.send(toReturn),
                currPlayer,
                prop,
            ]
            await gameMode.propertySellorAuction[0].add_reaction("1️⃣")
            await gameMode.propertySellorAuction[0].add_reaction("2️⃣")
        elif gameMode.getProperty(prop).owner == currPlayer:
            toReturn = "Welcome to your property"
            await channel.send(toReturn)
        else:
            property = gameMode.getProperty(prop)
            toReturn = (
                "\nProperty: "
                + str(property)
                + "is owned by "
                + str(property.owner)
                + "\n"
                + str(currPlayer.user)
                + " pays "
                + str(property.owner)
                + " $"
                + str(property.getRent())
            )
            if currPlayer.value >= property.getRent():
                currPlayer.value -= property.getRent()
                property.owner.value += property.getRent()
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
                prop: mapItemClass = getMapItem(comAct[2])
                gameMode.registerPropertyOwned(currPlayer.addProperty(prop))

                toReturn += "\n" + str(currPlayer.user) + " now has " + str(prop)
            elif comAct[1] == 2:
                for i in gameMode.playerList:
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
        elif action[1] == 4:
            toReturn += (
                "\n"
                + str(currPlayer.user)
                + " pays $"
                + getMapItem(currPlayer.map).Cost
            )
            currPlayer.value -= int(getMapItem(currPlayer.map).Cost)

        await channel.send(toReturn)


async def escapeJail(
    currPlayer: playerClass, channel: discord.TextChannel, output: str, num: list[int]
) -> None:
    output += "\nGOT OUT OF JAIL"
    await channel.send(output)
    currPlayer.map = 10
    await mapMovement(currPlayer, num, channel)


@client.event
async def on_reaction_remove(reaction:discord.Reaction, user):
    gameMode=getGame(reaction.message.channel)
    currPlayer = gameMode.getUser(user)
    if (
        currPlayer != None
        and reaction.message == gameMode.gameMessage
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        gameMode.playerList.remove(currPlayer)
        await gameMode.gameMessage.channel.send("Removed player " + str(user))


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    gameMode=getGame(reaction.message.channel)
    if (
        reaction.message == gameMode.gameMessage
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        gameMode.playerList.append(playerClass(user))
        await gameMode.gameMessage.channel.send("Added player " + str(user))

    currPlayer = gameMode.getUser(user)
    if (
        currPlayer not in gameMode.playerList
        or gameMode.gameMessage.channel != reaction.message.channel
    ):
        return
    if (
        gameMode.propertySellorAuction != None
        and reaction.message == gameMode.propertySellorAuction[0]
        and user == gameMode.propertySellorAuction[1].user
    ):
        if reaction.emoji == "1️⃣":
            channel = gameMode.propertySellorAuction[0].channel
            if currPlayer.value >= int(gameMode.propertySellorAuction[2].Cost):
                gameMode.registerPropertyOwned(
                    currPlayer.addProperty(gameMode.propertySellorAuction[2])
                )
                currPlayer.value -= int(gameMode.propertySellorAuction[2].Cost)

                toReturn = (
                    str(currPlayer.user)
                    + " has bought "
                    + str(gameMode.propertySellorAuction[2])
                )
                gameMode.propertySellorAuction = None
            else:
                toReturn = "You do not have enough funds to purchase this property"
            await channel.send(toReturn)
        elif reaction.emoji == "2️⃣":
            channel: discord.TextChannel = gameMode.propertySellorAuction[0].channel
            prop: mapItemClass = gameMode.propertySellorAuction[2]

            gameMode.propertySellorAuction = None
            gameMode.auctionMessage = [0, prop]
            await channel.send(
                "Starting auction for "
                + str(prop)
                + ". Please place your bids by typing 'bid NUMBER'"
            )

    if (
        currPlayer != None
        and currPlayer.map < 0
        and reaction.message == gameMode.jailMessage
    ):
        num = dice()
        if reaction.emoji == "1️⃣":
            if num[0] != num[1]:
                toReturn = (
                    str(currPlayer.user)
                    + " has rolled "
                    + str(num[0])
                    + "+"
                    + str(num[1])
                    + "="
                    + str(num[2])
                )
                currPlayer.map -= 1
                if currPlayer.map > -4:
                    toReturn += "\nNot a double, so still stuck in jail"
                    await gameMode.gameMessage.channel.send(toReturn)
                    return
                else:
                    toReturn = (
                        "Since "
                        + str(currPlayer)
                        + " has been stuck in jail for three turns, they must now pay the $50 fine."
                    )
                    currPlayer.value -= 50
            else:
                toReturn = str(currPlayer) + " has rolled a double"

        elif reaction.emoji == "2️⃣":
            card: mapItemClass = getMapItem(40)
            if currPlayer.hasProperty(card):
                currPlayer.removeProperty(card)
                toReturn = str(currPlayer) + " has used their " + str(card)
            else:
                await gameMode.gameMessage.channel.send(
                    "You do not have a " + str(card)
                )
                return
        elif reaction.emoji == "3️⃣":
            currPlayer.value -= 50
            toReturn = str(currPlayer.user) + " has payed the $50 fine."
        gameMode.jailMessage = None
        await escapeJail(currPlayer, gameMode.gameMessage.channel, toReturn, num)


def com():
    """
    To keep track of actions:
    -1: None
    0: Change currency
    1: Gain Property changeValue
    2: Collect changeValue from each player
    3: Go to Jail
    """
    action = -1
    # toTrackChangeInCurrency
    changeValue = 0
    cd = random.randint(1, 17)
    if cd == 1:
        com = "Advance to 'Go'. (Collect $200)"
        action = 0
        changeValue = 200
    elif cd == 2:
        com = "Bank error in your favor. Collect $200"
        action = 0
        changeValue = 200
    elif cd == 3:
        com = "Doctor's fees. Pay $50"
        action = 0
        changeValue = -50
    elif cd == 4:
        com = "From sale of stock you get $50"
        action = 0
        changeValue = 50
    elif cd == 5:
        com = "Get Out of Jail Free. This card may be kept until needed or sold/traded."
        action = 1
        changeValue = 40
    elif cd == 6:
        com = "Go to Jail. Go directly to jail. Do not pass Go, Do not collect $200"
        action = 3
    elif cd == 7:
        com = (
            "Grand Opera Night. Collect $50 from every player for opening night seats."
        )
        action = 2
        changeValue = 50
    elif cd == 8:
        com = "Holiday Fund matures. Receive $100"
        action = 0
        changeValue = 100
    elif cd == 9:
        com = "Income tax refund. Collect $20"
        action = 0
        changeValue = 20
    elif cd == 10:
        com = "It is your birthday. Collect $10 from every player"
        action = 0
        changeValue = 10
    elif cd == 11:
        com = "Life insurance matures - Collect $100"
        action = 0
        changeValue = 100
    elif cd == 12:
        com = "Hospital Fees. Pay $50"
        action = 0
        changeValue = -50
    elif cd == 13:
        com = "School fees. Pay $50"
        action = 0
        changeValue = -50
    elif cd == 14:
        com = "Receive $25 consultancy fee"
        action = 0
        changeValue = 25
    elif cd == 15:
        com = "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own."
    elif cd == 16:
        com = "You have won second prize in a beauty contest. Collect $10"
        action = 0
        changeValue = 10
    elif cd == 17:
        com = "You inherit $100"
        action = 0
        changeValue = 100
    return com, action, changeValue


def cnc():
    """
    To keep track of actions:
    -1: None
    0: Change currency
    1: Gain Property
    2: Collect changeValue from each player
    3: Go to Jail
    """
    action = -1
    # toTrackChangeInCurrency
    changeValue = 0
    cd = random.randint(1, 17)
    if cd == 1:
        com = "Advance to 'Go'. (Collect $200)"
        action = 0
        changeValue = 200
    elif cd == 2:
        com = "Advance to Trafalgar Square. If you pass Go, collect $200"
    elif cd == 3:
        com = "Advance to Pall Mall. If you pass Go, collect $200"
    elif cd == 4:
        com = "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total 10 (ten) times the amount thrown"
    elif cd == 5:
        com = "Advance token to the nearest Railroad and pay owner twice the rental to which he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank"
    elif cd == 6:
        com = "Advance token to the nearest Railroad and pay owner twice the rental to which he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank"
    elif cd == 7:
        com = "Bank pays you dividend of $50."
        action = 0
        changeValue = 50
    elif cd == 8:
        com = "Get out of Jail Free. This card may be kept until needed, or traded/sold.{This card may be kept until needed or sold/traded.)"
    elif cd == 9:
        com = "Go Back Three {3} Spaces"
    elif cd == 10:
        com = "Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200."
        action = 3
    elif cd == 11:
        com = "Make general repairs on all your property: For each house pay $25, For each hotel pay $100"
    elif cd == 12:
        com = "Pay poor tax of $15"
        action = 0
        changeValue = -15
    elif cd == 13:
        com = "Take a ride to King's Cross Station. If you pass Go, collect $200"
    elif cd == 14:
        com = "Take a walk on the board walk. Advance token to Mayfair"
    elif cd == 15:
        com = "You have been elected Chairman of the Board. Pay each player $50."
    elif cd == 16:
        com = "Your building loan matures. Receive $150"
        action = 0
        changeValue = 150
    elif cd == 17:
        com = "You have won a crossword competition. Collect $100"
        action = 0
        changeValue = 100
    return com, action, changeValue


def dice():
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    com = roll1 + roll2
    return roll1, roll2, com


with open("./resources/info.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        mapItemList.append(mapItemClass(row))

client.run(token)
