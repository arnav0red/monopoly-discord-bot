# community chest
import random


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
        com = "Advance token to the nearest Railroad and pay owner twice the rental to which he/she {he} is otherwise entitled. If Railroad is unowned, you may buy it from the Bank"
    elif cd == 6:
        com = "Advance token to the nearest Railroad and pay owner twice the rental to which he/she {he} is otherwise entitled. If Railroad is unowned, you may buy it from the Bank"
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
    elif cd == 11:
        com = "Make general repairs on all your property: For each house pay $25, For each hotel {pay} $100"
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
        file=("./resources/Marylebone Street.png")
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
        m = ":black_large_square: Park Lane- 36"
        toDoCode = 2
        file=("./resources/Park Lane.png")
    elif n == 38:
        m = "Super Tax"
    elif n == 39:
        m = ":black_large_square: Mayfair- 39"
        toDoCode = 2
        file=("./resources/Mayfair.png")
    elif n == 40:
        m = ":flag_white: Get out of Jail Free- 40"

    return m, toDoCode, file


def increase(pc, val):
    pc += val
    return pc


def decrease(pc, val):
    pc -= val
    return pc
