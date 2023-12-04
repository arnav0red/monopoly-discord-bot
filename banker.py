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
        pass
        playerList.append(playerClass(message.author))
    # ------------------
    if messageValue.startswith("game start"):
        gameMessage.clear()
        gameMessage.append(
            await message.channel.send(
                "Starting game.\nTo participate react with 🚩 to the game start message"
            )
        )
        await gameMessage[0].add_reaction("🚩")

    if len(gameMessage) != 1:
        return
    elif message.content == ("print"):
        playerList[0].map = -1
    elif message.content == ("com"):
        await message.channel.send(com()[0])
    elif message.content == ("cnc"):
        await message.channel.send(cnc()[0])
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
            toReturn = mapMovement(currPlayer, num)
            await message.channel.send(toReturn)
        else:
            choice = await message.channel.send(
                "Choose how you wish to get out of jail: \n1. By rolling a double \n2. Using a “Get out of jail free” card \n3.paying a $50 fine."
            )
            await choice.add_reaction("1️⃣")
            await choice.add_reaction("2️⃣")
            await choice.add_reaction("3️⃣")


def mapMovement(currPlayer, num):
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
    if action[1] == 0:
        comAct = com()
        toReturn += "\n" + comAct[0]

        if comAct[1] == 0:
            currPlayer.value += comAct[2]
            toReturn += (
                "\n" + str(currPlayer.user) + " now has $" + str(currPlayer.value)
            )
        elif comAct[1] == 1:
            currPlayer.properties.append(index(comAct[2]))
            toReturn += (
                "\n" + str(currPlayer.user) + " now has " + str(index(comAct[2]))
            )
        elif comAct[1] == 2:
            for i in playerList:
                if i.user == currPlayer:
                    continue
                i.user -= comAct[2]
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
    return toReturn


def resolveJail(currPlayer, resolveMethod):
    toReturn = ""
    if resolveMethod == 1:
        num = dice()
        if num[0] == num[1]:
            toReturn = "GOT OUT OF JAIL\n"
            currPlayer.map = 10
            toReturn += mapMovement(currPlayer, num)
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
    return toReturn


@client.event
async def on_reaction_add(reaction, user):
    global gameMessage, playerList
    if reaction.message == gameMessage[0] and user != client.user:
        playerList.append(playerClass(user))
        await gameMessage[0].channel.send("Added player " + str(user))
    currPlayer = None
    for val in playerList:
        if val.user == user:
            currPlayer = val
            break
    if currPlayer != None and currPlayer.map < 0:
        if reaction.emoji == "1️⃣":
            await reaction.message.channel.send(resolveJail(currPlayer, 1))
        elif reaction.emoji == "2️⃣":
            resolveJail(currPlayer, 2)
        elif reaction.emoji == "3️⃣":
            resolveJail(currPlayer, 3)


client.run(token)
