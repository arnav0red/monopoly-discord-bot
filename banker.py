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
    def __init__(
        self, gameMessage, jailMessage, propertySellorAuction, auctionMessage, timer
    ):
        self.gameMessage: discord.TextChannel = gameMessage
        self.jailMessage: discord.TextChannel = jailMessage
        self.propertySellorAuction = propertySellorAuction
        self.auctionMessage = auctionMessage
        self.timer: discord.TextChannel = timer


playerList: list[playerClass] = []
propertyList: list[propertyClass] = []

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
        gameMode.gameMessage = None
        gameMode.gameMessage = await message.channel.send(
            "Starting game.\nTo participate react with 🚩 to the game start message"
        )
        await gameMode.gameMessage.add_reaction("🚩")

    if gameMode.gameMessage == None:
        return
    elif message.content == ("print"):
        playerList[0].value = 1
    elif message.content.startswith("move"):
        await mapMovement(
            playerList[0],
            ["test", "test", int(message.content.split("move ")[1])],
            message.channel,
        )

    elif message.content.startswith("bid"):
        currPlayer = getUser(message.author)
        if currPlayer == None:
            await message.channel.send(
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
                gameMode.auctionMessage = [currentBid, prop, currPlayer.user]
                await message.channel.send(toReturn)
                if gameMode.timer != None and not gameMode.timer.done():
                    gameMode.timer.cancel()
                gameMode.timer: asyncio.Task = asyncio.create_task(
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
        toReturn = (
            str(currPlayer.user) + "'s Account\nBalance: $" + str(currPlayer.value)
        )
        toReturn += "\nProperties: "
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
        if currPlayer.value < 0:
            await message.channel.send(
                "It appears you are in debt. Either get some funds or declare bankruptcy."
            )
        elif currPlayer.map >= 0:
            num = dice()
            asyncio.create_task(mapMovement(currPlayer, num, message.channel))

        else:
            gameMode.jailMessage = await message.channel.send(
                "Choose how you wish to get out of jail: \n1. By rolling a double \n2. Using a “Get out of jail free” card \n3.paying a $50 fine."
            )
            await gameMode.jailMessage.add_reaction("1️⃣")
            await gameMode.jailMessage.add_reaction("2️⃣")
            await gameMode.jailMessage.add_reaction("3️⃣")


async def auctionTimer(channel: discord.TextChannel, countdown: int):
    if gameMode.auctionMessage == None:
        await channel.send("Auction has been concluded")
        return
    timer = await channel.send("CountDown:" + str(countdown))
    while countdown > 0:
        countdown -= 1
        await asyncio.sleep(1)
        await timer.edit(content=("CountDown:" + str(countdown)))
    currBid: int = gameMode.auctionMessage[0]
    prop: propertyClass = gameMode.auctionMessage[1]
    currPLayer: playerClass = getUser(gameMode.auctionMessage[2])
    gameMode.auctionMessage = None
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


async def mapMovement(
    currPlayer: playerClass, num: list[int], channel: discord.TextChannel
):
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
            gameMode.propertySellorAuction = [
                await channel.send(toReturn),
                currPlayer,
                prop,
            ]
            await gameMode.propertySellorAuction[0].add_reaction("1️⃣")
            await gameMode.propertySellorAuction[0].add_reaction("2️⃣")
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
        elif action[1] == 4:
            toReturn += (
                "\n"
                + str(currPlayer.user)
                + " pays $"
                + getProperty(currPlayer.map).Cost
            )
            currPlayer.value -= int(getProperty(currPlayer.map).Cost)

        await channel.send(toReturn)


@client.event
async def on_reaction_remove(reaction, user):
    currPlayer = getUser(user)
    if (
        currPlayer != None
        and reaction.message == gameMode.gameMessage
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        playerList.remove(currPlayer)
        await gameMode.gameMessage.channel.send("Removed player " + str(user))


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    global playerList
    if (
        reaction.message == gameMode.gameMessage
        and user != client.user
        and reaction.emoji == "🚩"
    ):
        playerList.append(playerClass(user))
        await gameMode.gameMessage.channel.send("Added player " + str(user))

    currPlayer = getUser(user)
    if currPlayer not in playerList:
        return
    if (
        gameMode.propertySellorAuction != None
        and reaction.message == gameMode.propertySellorAuction[0]
        and user == gameMode.propertySellorAuction[1].user
    ):
        if reaction.emoji == "1️⃣":
            channel = gameMode.propertySellorAuction[0].channel
            if currPlayer.value >= int(gameMode.propertySellorAuction[2].Cost):
                currPlayer.addProperty(gameMode.propertySellorAuction[2])
                currPlayer.value -= int(gameMode.propertySellorAuction[2].Cost)

                toReturn = (
                    str(currPlayer.user)
                    + " has bought "
                    + str(gameMode.propertySellorAuction[2].PropertyInternational)
                )
                gameMode.propertySellorAuction = None
            else:
                toReturn = "You do not have enough funds to purchase this property"
            await channel.send(toReturn)
        elif reaction.emoji == "2️⃣":
            channel: discord.TextChannel = gameMode.propertySellorAuction[0].channel
            prop: propertyClass = gameMode.propertySellorAuction[2]

            gameMode.propertySellorAuction = None
            gameMode.auctionMessage = [0, prop]
            await channel.send(
                "Starting auction for "
                + prop.PropertyInternational
                + ". Please place your bids by typing 'bid NUMBER'"
            )

    if (
        currPlayer != None
        and currPlayer.map < 0
        and reaction.message == gameMode.jailMessage
    ):
        gameMode.jailMessage = None
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
        action=3
    elif cd == 11:
        com = "Make general repairs on all your property: For each house pay $25, For each hotel pay $100"
    elif cd == 12:
        com = "Pay poor tax of $15"
        action = 0
        changeValue = -15
    elif cd == 13:
        com = "Take a ride to King's Cross Station] If you pass Go, collect $200"
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


def index(n):
    """
    -1: None
    0: Community Chest
    1: Chance
    2: Property
    3: Go to Jail
    4: Tax
    """
    toDoCode = -1
    file=None
    if n == 0:
        m = "GO"
    elif n == 1:
        m = ":brown_square: Old Kent Road- 1"
        toDoCode = 2
        file=("./resources/Old Kent Road.png")

    elif n == 2:
        m = "Community Chest"
        toDoCode = 0
    elif n == 3:
        m = ":brown_square: Whitechapel Road- 3"
        toDoCode = 2
        file=("./resources/Whitechapel Road.png")
    elif n == 4:
        m = "Income Tax"
        toDoCode=4
    elif n == 5:
        m = "Kings Cross Station- 5"
        file=("./resources/Kings Cross Station.png")
    elif n == 6:
        m = ":blue_square: The Angel Islington- 6"
        toDoCode = 2
        file=("./resources/The Angel Islington.png")
    elif n == 7:
        m = "Chance"
        toDoCode = 1
    elif n == 8:
        m = ":blue_square: Euston Road- 8"
        toDoCode = 2
        file=("./resources/Euston Road.png")
    elif n == 9:
        m = ":blue_square: Pentonville Road- 9"
        toDoCode = 2
        file=("./resources/Pentonville Road.png")
    elif n == 10:
        m = "Just Visiting Jail"
    elif n == 11:
        m = ":purple_square: Pall Mall- 11"
        toDoCode = 2
        file=("./resources/Pall Mall.png")
    elif n == 12:
        m = "Electric Company- 12"
        file=("./resources/electric company.jpg")
    elif n == 13:
        m = ":purple_square: Whitehall- 13"
        toDoCode = 2
        file=("./resources/Whitehall.png")
    elif n == 14:
        m = ":purple_square: Northumrl'd Avenue- 14"
        toDoCode = 2
        file=("./resources/Northumberland Avenue.png")
    elif n == 15:
        m = "Marylbone Station- 15"
        file=("./resources/Marylebone Station.png")
    elif n == 16:
        m = ":orange_square: Bow Street- 16"
        toDoCode = 2
        file=("./resources/Bow Street.png")
    elif n == 17:
        m = "Community Chest"
        toDoCode = 0
    elif n == 18:
        m = ":orange_square: Marlborough Street- 18"
        toDoCode = 2
        file=("./resources/Marlborough Street.png")
    elif n == 19:
        m = ":orange_square: Vine Street- 19"
        toDoCode = 2
        file=("./resources/Vine Street.png")
    elif n == 20:
        m = "Free Parking"
    elif n == 21:
        m = ":red_square: Strand- 21"
        toDoCode = 2
        file=("./resources/Strand.png")
    elif n == 22:
        m = "Chance"
        toDoCode = 1
    elif n == 23:
        m = ":red_square: Fleet Street- 23"
        toDoCode = 2
        file=("./resources/Fleet Street.png")
    elif n == 24:
        m = ":red_square: Trafalgar Square- 24"
        toDoCode = 2
        file=("./resources/Trafalgar Square.png")
    elif n == 25:
        m = "Fenchurch St Station- 25"
        file=("./resources/Fenchurch Street Station.png")
    elif n == 26:
        m = ":yellow_square: Leicester Square- 26"
        toDoCode = 2
        file=("./resources/Leicester Square.png")
    elif n == 27:
        m = ":yellow_square: Coventry Street- 27"
        toDoCode = 2
        file=("./resources/Coventry Street.png")
    elif n == 28:
        m = "Water Works- 28"
        file=("./resources/water works.jpg")
    elif n == 29:
        m = ":yellow_square: Picadilly- 29"
        toDoCode = 2
        file=("./resources/Piccadilly.png")
    elif n == 30:
        m = "Go to Jail"
        toDoCode = 3
    elif n == 31:
        m = ":green_square: Regent Street- 31"
        toDoCode = 2
        file=("./resources/Regent Street.png")
    elif n == 32:
        m = ":green_square: Oxford Street- 32"
        toDoCode = 2
        file=("./resources/Oxford Street.png")
    elif n == 33:
        m = "Community Chest"
        toDoCode = 0
    elif n == 34:
        m = ":green_square: Bond Street- 34"
        toDoCode = 2
        file=("./resources/Bond Street.png")
    elif n == 35:
        m = "Liverpool Street Station- 35"
        file=("./resources/Liverpool Street Station.png")
    elif n == 36:
        m = "Chance"
        toDoCode = 1
    elif n == 37:
        m = ":black_large_square: Park Lane- 37"
        toDoCode = 2
        file=("./resources/Park Lane.png")
    elif n == 38:
        m = "Super Tax"
        toDoCode=4
    elif n == 39:
        m = ":black_large_square: Mayfair- 39"
        toDoCode = 2
        file=("./resources/Mayfair.png")
    elif n == 40:
        m = ":flag_white: Get out of Jail Free- 40"

    return m, toDoCode, file

with open("./resources/info.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        propertyList.append(propertyClass(row))

client.run(token)
