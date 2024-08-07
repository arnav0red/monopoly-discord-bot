import discord, random, string, asyncio, pandas, math, json, os


# classes
class mapItemClass:
    """
    Class storing information about each tile. Corresponds to extra/info.xlsx
    Action:
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
        self.Emoji = listVals[14]

        def ifNotNan(val: float):
            if math.isnan(val):
                return None
            else:
                return int(val)

        self.Cost = ifNotNan(listVals[2])
        self.Site = ifNotNan(listVals[3])
        self.ColorSet = ifNotNan(listVals[4])
        self.H1 = ifNotNan(listVals[5])
        self.H2 = ifNotNan(listVals[6])
        self.H3 = ifNotNan(listVals[7])
        self.H4 = ifNotNan(listVals[8])
        self.Hotel = ifNotNan(listVals[9])
        self.BuildingCost = ifNotNan(listVals[10])
        self.Mortgage = ifNotNan(listVals[11])
        self.UnmortgageCost = ifNotNan(listVals[12])
        self.Index = ifNotNan(listVals[13])
        self.Action = ifNotNan(listVals[15])

    """
asd
"""

    def __str__(self) -> str:
        toReturn = str(self.Emoji) + " "
        toReturn += self.PropertyInternational
        return toReturn

    def printAll(self):
        toReturn = ""
        toReturn += str(self.PropertyUS) + " "
        toReturn += str(self.PropertyInternational) + " "
        toReturn += str(self.Cost) + " "
        toReturn += str(self.Site) + " "
        toReturn += str(self.ColorSet) + " "
        toReturn += str(self.H1) + " "
        toReturn += str(self.H2) + " "
        toReturn += str(self.H3) + " "
        toReturn += str(self.H4) + " "
        toReturn += str(self.Hotel) + " "
        toReturn += str(self.BuildingCost) + " "
        toReturn += str(self.Mortgage) + " "
        toReturn += str(self.UnmortgageCost) + " "
        toReturn += str(self.Index) + " "
        toReturn += str(self.Emoji) + " "
        toReturn += str(self.Action) + " "
        return toReturn


class propertyClass:
    """
    Class storing information about each property owned by a user
    """

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

    def getRent(self, diceVal: int) -> int:
        if getMapItem(self.index).Action == 6:
            return 4 * diceVal
        return int(getMapItem(self.index).Site)


class playerClass:
    """
    Class storing information about each player
    """

    def __init__(self, user):
        self.user: discord.Member = user
        self.value: int = 1500
        self.properties: list[propertyClass] = []
        self.map: int = 0

    def __str__(self) -> str:
        return str(self.user)

    def addProperty(self, mapItem: mapItemClass, gameMode) -> propertyClass:
        toReturn: propertyClass = propertyClass(int(mapItem.Index), self)
        self.properties.append(toReturn)
        self.properties = sorted(self.properties, key=lambda x: x.getColorSet())
        gameMode.propertiesOwned.append(toReturn)
        return toReturn

    def hasProperty(self, property: propertyClass) -> bool:
        for i in self.properties:
            if i == property:
                return True
        return False

    def removeProperty(self, property: propertyClass, gameMode) -> propertyClass:
        toReturn: propertyClass = None
        for i in self.properties:
            if i == property:
                toReturn = property
                break
        self.properties.remove(toReturn)
        gameMode.propertiesOwned.remove(toReturn)
        return toReturn


class gameModeClass:
    """
    Class where each instance is an ongoing game
    """

    def __init__(
        self,
        gameMessage,
    ):
        self.gameMessage: discord.Message = gameMessage
        self.jailMessage: discord.TextChannel = None
        self.propertySellorAuction = None
        self.auctionMessage = None
        self.timer: asyncio.Task = None
        self.playerList: list[playerClass] = []
        self.propertiesOwned: list[propertyClass] = []
        self.tradeInfo = {}
        """
        tradeMessage: Countdown coroutine
        player1: playerClass object 1
        player2: playerClass object 
        prop1: list[propertyClass] 1
        prop2: list[propertyClass] 2
        confirm: confirmation message object
        """

    def getUser(self, user: discord.Member) -> playerClass:
        currPlayer = None
        for val in self.playerList:
            if val.user == user:
                currPlayer = val
                break
        return currPlayer

    def exchange(
        self,
        player1: playerClass,
        player2: playerClass,
        curr1: int,
        curr2: int,
        prop1: list[propertyClass],
        prop2: list[propertyClass],
    ):
        player1.value += curr2 - curr1
        player2.value += curr1 - curr2

        for i in prop2:
            player1.addProperty(getMapItem(player2.removeProperty(i, self).index), self)
        for i in prop1:
            player2.addProperty(getMapItem(player1.removeProperty(i, self).index), self)

    def getUserFromString(self, user: str) -> playerClass:
        currPlayer = None
        for val in self.playerList:
            if str(val.user) == user:
                currPlayer = val
                break
        return currPlayer

    def getProperty(self, mapItem: mapItemClass) -> propertyClass:
        toReturn = None
        for i in self.propertiesOwned:
            if i.index == int(mapItem.Index):
                toReturn = i
                break
        return toReturn


# variable
hostedGames: set[gameModeClass] = set()
"""set of all ongoing games"""
mapItemList: list[mapItemClass] = []
"""all the stored map information from info.xlsx"""
client = discord.Client(intents=discord.Intents.all())
debug = False


# regular methods
def main():
    # TODO: changing gameMessage for testing
    if os.path.isfile("debug"):
        debug = True
    if not os.path.isfile("config.txt"):
        print("enter token for bot")
        with open("config.txt", "w") as file:
            file.write(input())

    with open("config.txt", "r") as fileRead:
        token = fileRead.read()

    reader = pandas.read_excel("./resources/info.xlsx")
    for row in reader.values:
        mapItemList.append(mapItemClass(row))

    client.run(token)


def getMapItem(num: int) -> mapItemClass:
    """Matches the index number for its corresponding tile information
    Returns: mapItemClass with matching index. If match isn't found, returns None
    """
    prop = None
    for i in mapItemList:
        if int(i.Index) == num:
            prop = i
            break
    return prop


def getGame(channel: discord.TextChannel) -> gameModeClass:
    """Returns the ongoing game for a given discord text channel
    Returns: gameModeClass, or None if not matched
    """
    toReturn = None
    for i in hostedGames:
        if i.gameMessage.channel == channel:
            toReturn = i
            break
    return toReturn


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
        action = 2
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
    """Simulates dice roll
    Returns: Tuple of order (First roll, Second roll, Sum of the rolls)"""
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    com = roll1 + roll2
    return roll1, roll2, com


# async methods


@client.event
async def on_ready():
    """
    Sends command when bot is ready. In debugging mode also sends a command to the relevant channel
    """
    print("We have logged in as {0.user}".format(client))
    if debug:
        await client.get_channel(1089298595905274016).send("DEBUGGING")


@client.event
async def on_message(message: discord.Message):
    """
    Executes on recieving specific messages.
    """
    messageValue = str(message.content.lower())
    gameMode = getGame(message.channel)
    if messageValue.startswith("game start"):
        if gameMode != None:
            await gameMode.gameMessage.channel.send(
                "There is already an existing game in this channel.\nPlease write ```game close``` to end it."
            )
            return

        gameMessage = await message.channel.send(
            "Starting game.\nTo participate react with 🚩 to the game start message"
        )
        gameMode = gameMode = gameModeClass(gameMessage)
        hostedGames.add(gameMode)

        await gameMode.gameMessage.add_reaction("🚩")

    if not debug and gameMode == None:
        return
    # -------------------
    # TODO: Temp added
    notInList = debug
    if debug and gameMode == None:
        gameMode = gameModeClass(message)
        hostedGames.add(gameMode)

    for val in gameMode.playerList:
        if val.user == message.author:
            notInList = False
            break
    if notInList:
        pass
        gameMode.playerList.append(playerClass(message.author))
    # ------------------
    if gameMode.tradeInfo.get("tradeMessage") != None and messageValue.startswith(
        "offer "
    ):
        currPlayer = gameMode.getUser(message.author)
        values = messageValue.split("offer ")[1].strip().split(" ")
        toReturn = ""
        playerNum = 0
        if currPlayer == gameMode.tradeInfo.get("player1"):
            playerNum = 1
        elif currPlayer == gameMode.tradeInfo.get("player2"):
            playerNum = 2
        if playerNum != 0:
            validFormat = True
            if not values[0].isdigit():
                validFormat = False
            for i in range(1, len(values)):
                if values[i][0] != "p":
                    validFormat = False
                    break
                if not values[i][1 : len(values[i])].isdigit():
                    validFormat = False
                    break
        if not validFormat:
            toReturn = (
                "Please write your offer in the valid format.\nEg:```offer 120 P1 P2```"
            )
        else:
            listProperties = []
            if currPlayer.value < int(values[0]):
                toReturn = "Please only offer the amount you have"
            else:
                listProperties.append(int(values[0]))
                ownsProperties = True
                for i in range(1, len(values)):
                    if not currPlayer.hasProperty(
                        gameMode.getProperty(
                            getMapItem(int(values[i][1 : len(values[i])]))
                        )
                    ):
                        ownsProperties = False
                        break
                    listProperties.append(
                        gameMode.getProperty(
                            getMapItem(int(values[i][1 : len(values[i])]))
                        )
                    )
                if not ownsProperties:
                    toReturn = "Please only offer properties you own"
                else:
                    gameMode.tradeInfo["prop" + str(playerNum)] = listProperties
                    toReturn = (
                        str(currPlayer) + " is offering $" + str(listProperties[0])
                    )
                    for i in range(1, len(listProperties)):
                        toReturn += ", " + str(listProperties[i])
        await gameMode.gameMessage.channel.send(toReturn)
        if (
            gameMode.tradeInfo.get("prop1") != None
            and gameMode.tradeInfo.get("prop2") != None
        ):
            toReturn = (
                "Does this deal work for both parties? React with ✔ to finalize it.\n"
            )
            for i in range(1, 3):
                listProperties = gameMode.tradeInfo.get("prop" + str(i))
                toReturn += (
                    str(gameMode.tradeInfo.get("player" + str(i)))
                    + " is offering $"
                    + str(listProperties[0])
                )
                for j in range(1, len(listProperties)):
                    toReturn += ", " + str(listProperties[j])
                toReturn += "\n"
            gameMode.tradeInfo["confirm"] = await gameMode.gameMessage.channel.send(
                toReturn
            )
            await gameMode.tradeInfo.get("confirm").add_reaction("✅")

    elif messageValue == ("print"):
        for i in range(10):
            print(com())

    elif messageValue.startswith("printer"):
        print(gameMode.playerList[1].hasProperty(gameMode.getProperty(getMapItem(6))))

    elif messageValue.startswith("move "):
        await mapMovement(
            gameMode.getUser(message.author),
            ["test", "test", int(messageValue.split("move ")[1])],
            gameMode.gameMessage.channel,
        )
    elif messageValue.startswith("test"):
        message.content = messageValue.split("test ")[1]
        message.author = gameMode.playerList[0].user
        asyncio.create_task(on_message(message))
    elif messageValue.startswith("bid"):
        currPlayer = gameMode.getUser(message.author)
        if currPlayer == None:
            await gameMode.gameMessage.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        if (
            gameMode.auctionMessage != None
            and messageValue.split("bid ")[1].strip().isdigit()
        ):
            currentBid = int(messageValue.split("bid ")[1].strip())
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
                gameMode.timer = asyncio.create_task(
                    auctionTimer(gameMode.gameMessage.channel, 5)
                )
    elif messageValue == ("sudo com"):
        await gameMode.gameMessage.channel.send(com()[0])
    elif messageValue == ("sudo cnc"):
        await gameMode.gameMessage.channel.send(cnc()[0])
    elif messageValue == ("list"):
        currPlayer = gameMode.getUser(message.author)
        if currPlayer == None:
            await gameMode.gameMessage.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        await listUser(gameMode.gameMessage.channel, currPlayer)
    elif messageValue == ("list all"):
        for i in gameMode.playerList:
            await listUser(gameMode.gameMessage.channel, i)

    elif messageValue == ("dice"):
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
    elif messageValue == ("roll"):
        await rollDice(gameMode.gameMessage.channel, gameMode.getUser(message.author))
    elif messageValue.startswith("trade"):
        currPlayer = gameMode.getUser(message.author)
        if currPlayer == None:
            await gameMode.gameMessage.channel.send(
                "Huh! Weird that you're not in the game. Please react to the game start message to be added."
            )
            return
        elif len(messageValue.split(" ")) < 2:
            await gameMode.gameMessage.channel.send(
                "If you're trying to trade with another player, the command is ```trade JohnDoe```"
            )
            return
        tradePlayer = gameMode.getUserFromString(message.content.split(" ", 1)[1])
        if tradePlayer == None:
            await gameMode.gameMessage.channel.send(
                "If you're trying to trade with another player, please make sure you're entering the correct name."
            )
            return
        if gameMode.tradeInfo.get("tradeMessage") != None:
            await gameMode.gameMessage.channel.send("Closing previous trade")
            gameMode.tradeInfo["tradeMessage"].cancel()
            gameMode.tradeInfo.clear()
        gameMode.tradeInfo["player1"] = currPlayer
        gameMode.tradeInfo["player2"] = tradePlayer
        gameMode.tradeInfo["tradeMessage"] = asyncio.create_task(
            tradeTimer(message, 120)
        )
    elif messageValue == ("game close"):
        hostedGames.remove(gameMode)
        await message.channel.send("Closing Game")


async def tradeTimer(message: discord.Message, countdown: int) -> None:
    """Creates an asynchronous timer for trade for a given message and countdown length"""
    gameMode = getGame(message.channel)
    if gameMode.tradeInfo["tradeMessage"] == None:
        return
    toReturn = "Starting trade.\nWrite your offer in the format.\n```offer [AMOUNT] P[index1] P[index2],...```"
    timer = await gameMode.gameMessage.channel.send(
        toReturn + "\nCountDown:" + str(countdown)
    )
    while countdown > 0:
        countdown -= 1
        await asyncio.sleep(1)
        await timer.edit(content=(toReturn + "\nCountDown:" + str(countdown)))
    toReturn = "The Trade has been Closed"
    await gameMode.gameMessage.channel.send(toReturn)
    gameMode.tradeInfo.clear()


async def listUser(channel: discord.TextChannel, currPlayer: playerClass) -> None:
    """Sends information in the given channel about currPlayer"""
    toReturn = str(currPlayer.user) + "'s Account\nBalance: $" + str(currPlayer.value)
    toReturn += "\nProperties: "
    for i in currPlayer.properties:
        toReturn += " " + str(i) + "-No" + str(i.index) + ", "
    await channel.send(toReturn)


async def rollDice(channel: discord.TextChannel, currPlayer: playerClass) -> None:
    """
    Rolls dice and runs the command based on where player lands"""
    gameMode = getGame(channel)

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
    """Creates an asynchronous timer for an auction"""
    gameMode = getGame(channel)

    if gameMode.auctionMessage == None:
        await gameMode.gameMessage.channel.send("Auction has been concluded")
        return
    timer = await gameMode.gameMessage.channel.send("CountDown:" + str(countdown))
    while countdown > 0:
        countdown -= 1
        await asyncio.sleep(1)
        await timer.edit(content=("CountDown:" + str(countdown)))
    currBid: int = gameMode.auctionMessage[0]
    prop: mapItemClass = gameMode.auctionMessage[1]
    currPLayer: playerClass = gameMode.getUser(gameMode.auctionMessage[2])
    gameMode.auctionMessage = None
    currPLayer.value -= currBid
    currPLayer.addProperty(prop, gameMode)

    await gameMode.gameMessage.channel.send(
        str(currPLayer.user) + " has bought " + str(prop) + " for $" + str(currBid)
    )


async def mapMovement(
    currPlayer: playerClass, num: list[int], channel: discord.TextChannel
):
    """Executes command based on landing location"""
    gameMode = getGame(channel)

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
    if action[1] == 2 or action[1] == 5 or action[1] == 6:
        await channel.send(toReturn)
        await channel.send(file=discord.File(action[2]))
        if gameMode.getProperty(prop) == None:
            toReturn = "\nCost: " + str(prop.Cost) + "\nWould you like to \n1.Buy"
            if action[1] == 2:
                toReturn += "\n2.Auction"

            # 0:message, 1:player
            gameMode.propertySellorAuction = [
                await channel.send(toReturn),
                currPlayer,
                prop,
            ]
            await gameMode.propertySellorAuction[0].add_reaction("1️⃣")
            if action[1] == 2:
                await gameMode.propertySellorAuction[0].add_reaction("2️⃣")
        elif gameMode.getProperty(prop).owner == currPlayer:
            toReturn = "Welcome to your property"
            await channel.send(toReturn)
        else:
            property = gameMode.getProperty(prop)
            toReturn = (
                "\nProperty: "
                + str(property)
                + " is owned by "
                + str(property.owner)
                + "\n"
                + str(currPlayer.user)
                + " pays "
                + str(property.owner)
                + " $"
                + str(property.getRent(num[2]))
            )
            if currPlayer.value >= property.getRent(num[2]):
                currPlayer.value -= property.getRent(num[2])
                property.owner.value += property.getRent(num[2])
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
                currPlayer.addProperty(prop, gameMode)

                toReturn += "\n" + str(currPlayer.user) + " now has " + str(prop)
            elif comAct[1] == 2:
                for i in gameMode.playerList:
                    if i == currPlayer:
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
                + str(getMapItem(currPlayer.map).Cost)
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
async def on_reaction_remove(reaction: discord.Reaction, user):
    gameMode = getGame(reaction.message.channel)
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
    gameMode = getGame(reaction.message.channel)
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
                currPlayer.addProperty(gameMode.propertySellorAuction[2], gameMode)

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
    if gameMode.tradeInfo.get("confirm") == reaction.message and reaction.emoji == "✅":
        player1 = None
        player2 = None
        for reaction in reaction.message.reactions:
            if reaction.emoji != "✅":
                continue
            async for user in reaction.users():
                if gameMode.getUser(user) == gameMode.tradeInfo.get("player1"):
                    player1 = gameMode.tradeInfo.get("player1")
                elif gameMode.getUser(user) == gameMode.tradeInfo.get("player2"):
                    player2 = gameMode.tradeInfo.get("player2")
                if player1 != None and player2 != None:
                    break
        if player1 != None and player2 != None:
            gameMode.tradeInfo["tradeMessage"].cancel()
            gameMode.exchange(
                player1,
                player2,
                gameMode.tradeInfo.get("prop1")[0],
                gameMode.tradeInfo.get("prop2")[0],
                gameMode.tradeInfo.get("prop1")[1:],
                gameMode.tradeInfo.get("prop2")[1:],
            )
            await gameMode.gameMessage.channel.send("The Trade has been concluded")
            gameMode.tradeInfo.clear()

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
                currPlayer.removeProperty(card, gameMode)
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


if __name__ == "__main__":
    main()
