from commands import *
import discord, random, string, asyncio, pickle, os


class playerClass:
    def __init__(self, user):
        self.user = user

    playerNum = -1
    value = 1500
    properties = []
    map = 0


playerList = []

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
        playerList.append(playerClass(message.author))
    # ------------------
    if messageValue.startswith("game start"):
        gameMessage.clear()
        gameMessage.append(message)
        await message.channel.send(
            "Starting game.\nTo participate react with [x] to the game start message"
        )
    if len(gameMessage) != 1:
        return
    elif message.content == ("print"):
        await message.channel.send(len(playerList))
    elif message.content == ("com"):
        await message.channel.send(com())
    elif message.content == ("cnc"):
        await message.channel.send(cnc())
    elif message.content == ("dice"):
        await message.channel.send(dice())
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

        num = dice()
        currPlayer.map = (currPlayer.map + num[2]) % 40
        action = index(currPlayer.map)

        toReturn = (
            "Player "
            + str(message.author)
            + " has rolled "
            + str(num[0])
            + "+"
            + str(num[1])
            + "="
            + str(num[2])
            + "\nPlayer has landed on "
            + action[0]
        )
        if action[1] == 0:
            comAct = com()
            toReturn += "\n" + comAct[0]

            if comAct[1] == 0:
                currPlayer.value += comAct[2]
                toReturn += "\nPlayer now has $" + str(currPlayer.value)
            elif comAct[1] == 2:
                for i in playerList:
                    if i.user == currPlayer:
                        continue
                    i.user -= comAct[2]
                currPlayer.value += comAct[2]
                toReturn += "\nPlayer now has $" + str(currPlayer.value)
            elif comAct[1] == 1:
                currPlayer.properties.append(index(40))
                toReturn += "\nPlayer now has " + str(index(40))

        elif action[1] == 1:
            cncAct=cnc()
            toReturn += "\n" + cncAct[0]
            if cncAct[1] == 0:
                currPlayer.value += cncAct[2]
                toReturn += "\nPlayer now has $" + str(currPlayer.value)
            

        await message.channel.send(toReturn)

    elif message.content.startswith("inc"):
        p = "p" + message.content[5]
        money = message.content[7 : len(message.content)]
        money = int(money)
        if p == "p1":
            p1cur = increase(p1cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p1cur)
            await message.channel.send(finale)
        elif p == "p2":
            p2cur = increase(p2cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p2cur)
            await message.channel.send(finale)
        elif p == "p3":
            p3cur = increase(p3cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p3cur)
            await message.channel.send(finale)
        elif p == "p4":
            p4cur = increase(p4cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p4cur)
            await message.channel.send(finale)
        elif p == "p5":
            p5cur = increase(p5cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p5cur)
            await message.channel.send(finale)
        elif p == "p6":
            p6cur = increase(p6cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p6cur)
            await message.channel.send(finale)
        elif p == "p7":
            p7cur = increase(p7cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p7cur)
            await message.channel.send(finale)
        elif p == "p8":
            p8cur = increase(p8cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p8cur)
            await message.channel.send(finale)
        elif p == "p9":
            p9cur = increase(p9cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p9cur)
            await message.channel.send(finale)
        elif p == "p10":
            p10cur = increase(p10cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p10cur)
            await message.channel.send(finale)
        elif p == "p11":
            p11cur = increase(p11cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p11cur)
            await message.channel.send(finale)

    elif message.content.startswith("dec"):
        p = "p" + message.content[5]
        money = message.content[7 : len(message.content)]
        money = int(money)
        if p == "p1":
            p1cur = decrease(p1cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p1cur)
            await message.channel.send(finale)
        elif p == "p2":
            p2cur = decrease(p2cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p2cur)
            await message.channel.send(finale)
        elif p == "p3":
            p3cur = decrease(p3cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p3cur)
            await message.channel.send(finale)
        elif p == "p4":
            p4cur = decrease(p4cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p4cur)
            await message.channel.send(finale)
        elif p == "p5":
            p5cur = decrease(p5cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p5cur)
            await message.channel.send(finale)
        elif p == "p6":
            p6cur = decrease(p6cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p6cur)
            await message.channel.send(finale)
        elif p == "p7":
            p7cur = decrease(p7cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p7cur)
            await message.channel.send(finale)
        elif p == "p8":
            p8cur = decrease(p8cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p8cur)
            await message.channel.send(finale)
        elif p == "p9":
            p9cur = decrease(p9cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p9cur)
            await message.channel.send(finale)
        elif p == "p10":
            p10cur = decrease(p10cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p10cur)
            await message.channel.send(finale)
        elif p == "p11":
            p11cur = decrease(p11cur, money)
            finale = "Player " + message.content[5] + " has $" + str(p11cur)
            await message.channel.send(finale)

    elif message.content.startswith("val"):
        p = "p" + message.content[5]
        if p == "p1":
            finale = "Player " + message.content[5] + " has $" + str(p1cur)
            await message.channel.send(finale)
        elif p == "p2":
            finale = "Player " + message.content[5] + " has $" + str(p2cur)
            await message.channel.send(finale)
        elif p == "p3":
            finale = "Player " + message.content[5] + " has $" + str(p3cur)
            await message.channel.send(finale)
        elif p == "p4":
            finale = "Player " + message.content[5] + " has $" + str(p4cur)
            await message.channel.send(finale)
        elif p == "p5":
            finale = "Player " + message.content[5] + " has $" + str(p5cur)
            await message.channel.send(finale)
        elif p == "p6":
            finale = "Player " + message.content[5] + " has $" + str(p6cur)
            await message.channel.send(finale)
        elif p == "p7":
            finale = "Player " + message.content[5] + " has $" + str(p7cur)
            await message.channel.send(finale)
        elif p == "p8":
            finale = "Player " + message.content[5] + " has $" + str(p8cur)
            await message.channel.send(finale)
        elif p == "p9":
            finale = "Player " + message.content[5] + " has $" + str(p9cur)
            await message.channel.send(finale)
        elif p == "p10":
            finale = "Player " + message.content[5] + " has $" + str(p10cur)
            await message.channel.send(finale)
        elif p == "p11":
            finale = "Player " + message.content[5] + " has $" + str(p11cur)
            await message.channel.send(finale)

    elif message.content.startswith("trans"):
        value = message.content[7]
        p = "p" + value
        trval = int(message.content[9 : len(message.content)])
        if p == "p1":
            # await message.channel.send("jusst after if"+str(p1map))
            p1map = map(p, trval)
            if p1map >= 40:
                p1map -= 40
            loc = index(p1map)
            # await message.channel.send("after if"+str(p1map))
            if p1map == 30:
                p1map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p2":
            p2map = map(p, trval)
            if p2map >= 40:
                p2map -= 40
            loc = index(p2map)
            if p2map == 30:
                p2map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p3":
            p3map = map(p, trval)
            if p3map >= 40:
                p3map -= 40
            loc = index(p3map)
            if p3map == 30:
                p3map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p4":
            p4map = map(p, trval)
            if p4map >= 40:
                p4map -= 40
            loc = index(p4map)
            if p4map == 30:
                p4map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p5":
            p5map = map(p, trval)
            if p5map >= 40:
                p5map -= 40
            loc = index(p5map)
            if p5map == 30:
                p5map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p6":
            p6map = map(p, trval)
            if p6map >= 40:
                p6map -= 40
            loc = index(p6map)
            if p6map == 30:
                p6map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p7":
            p7map = map(p, trval)
            if p7map >= 40:
                p7map -= 40
            loc = index(p7map)
            if p7map == 30:
                p7map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p8":
            p8map = map(p, trval)
            if p8map >= 40:
                p8map -= 40
            loc = index(p8map)
            if p8map == 30:
                p8map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p9":
            p9map = map(p, trval)
            if p9map >= 40:
                p9map -= 40
            loc = index(p9map)
            if p9map == 30:
                p9map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p10":
            p10map = map(p, trval)
            if p10map >= 40:
                p10map -= 40
            loc = index(p10map)
            if p10map == 30:
                p10map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        elif p == "p11":
            p11map = map(p, trval)
            if p11map >= 40:
                p11map -= 40
            loc = index(p11map)
            if p10map == 30:
                p10map = 10
                finale = "Player " + value + " is now in Jail"
                await message.channel.send(finale)
        loc1 = "Player " + value + " is at " + loc
        if loc != "Go to Jail":
            await message.channel.send(loc1)
            n = trval
            if n == 0:
                m = "GO"
            elif n == 1:
                m = "Old Kent Road"
                await message.channel.send(
                    file=discord.File("./resources/Old Kent Road.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 2:
                m = "Community Chest"
                await message.channel.send(com())
            elif n == 3:
                m = "Whitechapel Road"
                await message.channel.send(
                    file=discord.File("./resources/Whitechapel Road.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 4:
                m = "Income Tax"
            elif n == 5:
                m = "Kings Cross Station"
                await message.channel.send(
                    file=discord.File("./resources/Kings Cross Station.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 6:
                m = "The Angel Islington"
                await message.channel.send(
                    file=discord.File("./resources/The Angel Islington.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 7:
                m = "Chance"
                await message.channel.send(cnc())
            elif n == 8:
                m = "Euston Road"
                await message.channel.send(
                    file=discord.File("./resources/Euston Road.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 9:
                m = "Pentonville Road"
                await message.channel.send(
                    file=discord.File("./resources/Pentonville Road.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 10:
                m = "Just Visiting Jail"
            elif n == 11:
                m = "Pall Mall"
                await message.channel.send(
                    file=discord.File("./resources/Pall Mall.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 12:
                m = "Electric Company"
                await message.channel.send(
                    file=discord.File("./resources/electric company.jpg")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 13:
                m = "Whitehall"
                await message.channel.send(
                    file=discord.File("./resources/Whitehall.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 14:
                m = "Northumrl'd Avenue"
                await message.channel.send(
                    file=discord.File("./resources/Northumberland Avenue.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 15:
                m = "Marylbone Station"
                await message.channel.send(
                    file=discord.File("./resources/Marylebone Station.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 16:
                m = "Bow Street"
                await message.channel.send(
                    file=discord.File("./resources/Bow Street.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 17:
                m = "Community Chest"
                await message.channel.send(com())
            elif n == 18:
                m = "Marlborough Street"
                await message.channel.send(
                    file=discord.File("./resources/Marylebone Station.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 19:
                m = "Vine Street"
                await message.channel.send(
                    file=discord.File("./resources/Vine Street.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 20:
                m = "Free Parking"
            elif n == 21:
                m = "Strand"
                await message.channel.send(file=discord.File("./resources/Strand.png"))
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 22:
                m = "Chance"
                await message.channel.send(cnc())
            elif n == 23:
                m = "Fleet Street"
                await message.channel.send(
                    file=discord.File("./resources/Fleet Street.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 24:
                m = "Trafalgar Square"
                await message.channel.send(
                    file=discord.File("./resources/Trafalgar Square.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 25:
                m = "Fenchurch St Station"
                await message.channel.send(
                    file=discord.File("./resources/Fenchurch Street Station.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 26:
                m = "Leicester Square"
                await message.channel.send(
                    file=discord.File("./resources/Leicester Square.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 27:
                m = "Coventry Street"
                await message.channel.send(
                    file=discord.File("./resources/Coventry Street.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 28:
                m = "Water Works"
                await message.channel.send(
                    file=discord.File("./resources/water works.jpg")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 29:
                m = "Picadilly"
                await message.channel.send(
                    file=discord.File("./resources/Piccadilly.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 30:
                m = "Go to Jail"
            elif n == 31:
                m = "Regent Street"
                await message.channel.send(
                    file=discord.File("./resources/Regent Street.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 32:
                m = "Oxford Street"
                await message.channel.send(
                    file=discord.File("./resources/Oxford Street.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 33:
                m = "Community Chest"
                await message.channel.send(com())
            elif n == 34:
                m = "Bond Street"
                await message.channel.send(
                    file=discord.File("./resources/Bond Street.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 35:
                m = "Liverpool St.Station"
                await message.channel.send(
                    file=discord.File("./resources/Liverpool Street Station.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 36:
                m = "Chance"
                await message.channel.send(cnc())
            elif n == 37:
                m = "Park Lane"
                await message.channel.send(
                    file=discord.File("./resources/Park Lane.png")
                )
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)
            elif n == 38:
                m = "Super Tax"
            elif n == 39:
                m = "Mayfair"
                await message.channel.send(file=discord.File("./resources/Mayfair.png"))
                finale = "Do you want to buy or auction?"
                await message.channel.send(finale)

    # await message.channel.send(file=discord.File('Whitehall.png'))
    elif message.content.startswith("prop"):
        value = "p" + message.content[6]
        ap = message.content[(13) : len(message.content)]
        if message.content[8:12] == "gain":
            ap = int(ap)
            pp = index(ap)
            pop = "Player " + value + " gets " + pp

            if value == "p1":
                p1list.append(pp)
            elif value == "p2":
                p2list.append(pp)
            elif value == "p3":
                p3list.append(pp)
            elif value == "p4":
                p4list.append(pp)
            elif value == "p5":
                p5list.append(pp)
            elif value == "p6":
                p6list.append(pp)
            elif value == "p7":
                p7list.append(pp)
            elif value == "p8":
                p8list.append(pp)
            elif value == "p9":
                p9list.append(pp)
            elif value == "p10":
                p10list.append(pp)
            elif value == "p11":
                p11list.append(pp)
            await message.channel.send(pop)
        if message.content[8:12] == "loss":
            ap = int(ap)
            pp = index(ap)
            pop = "Player " + value + " loses " + pp
            await message.channel.send(pop)

            if value == "p1":
                p1list.remove(pp)
            elif value == "p2":
                p2list.remove = pp
            elif value == "p3":
                p3list.remove = pp
            elif value == "p4":
                p4list.remove = pp
            elif value == "p5":
                p5list.remove = pp
            elif value == "p6":
                p6list.remove = pp
            elif value == "p7":
                p7list.remove = pp
            elif value == "p8":
                p8list.remove = pp
            elif value == "p9":
                p9list.remove = pp
            elif value == "p10":
                p10list.remove = pp
            elif value == "p11":
                p11list.remove = pp

        if message.content[8:12] == "curr":
            pop = "Player " + value + " has"

            if value == "p1":
                await message.channel.send(p1list)
            elif value == "p2":
                await message.channel.send(p2list)
            elif value == "p3":
                await message.channel.send(p3list)
            elif value == "p4":
                await message.channel.send(p4list)
            elif value == "p5":
                await message.channel.send(p5list)
            elif value == "p6":
                await message.channel.send(p6list)
            elif value == "p7":
                await message.channel.send(p7list)
            elif value == "p8":
                await message.channel.send(p8list)
            elif value == "p9":
                await message.channel.send(p9list)
            elif value == "p10":
                await message.channel.send(p10list)
            elif value == "p11":
                await message.channel.send(p11list)


@client.event
async def on_reaction_add(reaction, user):
    global gameMessage, playerList
    if reaction.message == gameMessage[0]:
        playerList.append(playerClass(user))
        await gameMessage[0].channel.send("Added player " + str(user))


client.run(token)
