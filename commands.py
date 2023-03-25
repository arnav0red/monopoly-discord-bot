#community chest
import random
global n,m
def com():
    cd=random.randint(1,17)
    if cd==1:
        com="Advance to 'Go'. (Collect $200)"
    elif cd==2:
        com="Bank error in your favor. Collect $200"
    elif cd==3:
        com="Doctor's fees. Pay $50"
    elif cd==4:
        com="From sale of stock you get $50"
    elif cd==5:
        com="Get Out of Jail Free. This card may be kept until needed or sold/traded."
    elif cd==6:
        com="Go to Jail. Go directly to jail. Do not pass Go, Do not collect $200"
    elif cd==7:
        com="Grand Opera Night. Collect $50 from every player for opening night seats."
    elif cd==8:
        com="Holiday Fund matures. Receive $100"
    elif cd==9:
        com="Income tax refund. Collect $20"
    elif cd==10:
        com="It is your birthday. Collect $10 from every player"
    elif cd==11:
        com="Life insurance matures – Collect $100"
    elif cd==12:
        com="Hospital Fees. Pay $50"
    elif cd==13:
        com="School fees. Pay $50"
    elif cd==14:
        com="Receive $25 consultancy fee"
    elif cd==15:
        com="You are assessed for street repairs: Pay $40 per house and $115 per hotel you own."
    elif cd==16:
        com="You have won second prize in a beauty contest. Collect $10"
    elif cd==17:
        com="You inherit $100"
    return com

def cnc():
    cd=random.randint(1,17)
    if cd==1:
        com="Advance to 'Go'. (Collect $200)"
    elif cd==2:
        com="Advance to Trafalgar Square. If you pass Go, collect $200"
    elif cd==3:
        com="Advance to Pall Mall. If you pass Go, collect $200"
    elif cd==4:
        com="Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total 10 (ten) times the amount thrown"
    elif cd==5:
        com="Advance token to the nearest Railroad and pay owner twice the rental to which he/she {he} is otherwise entitled. If Railroad is unowned, you may buy it from the Bank"
    elif cd==6:
        com="Advance token to the nearest Railroad and pay owner twice the rental to which he/she {he} is otherwise entitled. If Railroad is unowned, you may buy it from the Bank"
    elif cd==7:
        com="Bank pays you dividend of $50."
    elif cd==8:
        com="Get out of Jail Free. This card may be kept until needed, or traded/sold.{This card may be kept until needed or sold/traded.)"
    elif cd==9:
        com="Go Back Three {3} Spaces"
    elif cd==10:
        com="Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200."
    elif cd==11:
        com="Make general repairs on all your property: For each house pay $25, For each hotel {pay} $100"
    elif cd==12:
        com="Pay poor tax of $15"
    elif cd==13:
        com="Take a ride to King’s Cross Station] If you pass Go, collect $200"
    elif cd==14:
        com="Take a walk on the board walk. Advance token to Mayfair"
    elif cd==15:
        com="You have been elected Chairman of the Board. Pay each player $50."
    elif cd==16:
        com="Your building loan matures. Receive $150"
    elif cd==17:
        com="You have won a crossword competition. Collect $100"
    return com

def dice():
    global n
    a=1
    com=0
    while a<=2:
        cd=random.randint(1,6)
        if com==0:
            n1=cd
        n2=cd
        com=com+cd
        a+=1
    n="You've rolled a "+str(n1)+"+"+str(n2)+"="+str(com)
    return n,com

def map(p,num):
    pmap=0
    if p=="p1":
        pmap+=num
    elif p=="p2":
        pmap+=num
    elif p=="p3":
        pmap+=num
    elif p=="p4":
        pmap+=num
    elif p=="p5":
        pmap+=num
    elif p=="p6":
        pmap+=num
    elif p=="p7":
        pmap+=num
    elif p=="p8":
        pmap+=num
    elif p=="p9":
        pmap+=num
    elif p=="p10":
        pmap+=num
    elif p=="p11":
        pmap+=num
    return pmap

def index(n):
    if n==0:
        m="GO"
    elif n==1:
        m=":brown_square: Old Kent Road- 1"
    elif n==2:
        m="Community Chest"
    elif n==3:
        m=":brown_square: Whitechapel Road- 3"
    elif n==4:
        m="Income Tax"
    elif n==5:
        m="Kings Cross Station- 5"
    elif n==6:
        m=":blue_square: The Angel Islington- 6"
    elif n==7:
        m="Chance"
    elif n==8:
        m=":blue_square: Euston Road- 8"
    elif n==9:
        m=":blue_square: Pentonville Road- 9"
    elif n==10:
        m="Just Visiting Jail"
    elif n==11:
        m=":purple_square: Pall Mall- 11"
    elif n==12:
        m="Electric Company- 12"
    elif n==13:
        m=":purple_square: Whitehall- 13"
    elif n==14:
        m=":purple_square: Northumrl'd Avenue- 14"
    elif n==15:
        m="Marylbone Station- 15"
    elif n==16:
        m=":orange_square: Bow Street- 16"
    elif n==17:
        m="Community Chest"
    elif n==18:
        m=":orange_square: Marlborough Street- 18"
    elif n==19:
        m=":orange_square: Vine Street- 19"
    elif n == 20:
        m = "Free Parking"
    elif n == 21:
        m = ":red_square: Strand- 21"
    elif n == 22:
        m = "Chance"
    elif n == 23:
        m = ":red_square: Fleet Street- 23"
    elif n == 24:
        m = ":red_square: Trafalgar Square- 24"
    elif n == 25:
        m = "Fenchurch St Station- 25"
    elif n == 26:
        m = ":yellow_square: Leicester Square- 26"
    elif n == 27:
        m = ":yellow_square: Coventry Street- 27"
    elif n == 28:
          m = "Water Works- 28"
    elif n == 29:
         m = ":yellow_square: Picadilly- 29"
    elif n==30:
         m="Go to Jail"
    elif n==31:
         m=":green_square: Regent Street- 31"
    elif n==32:
         m=":green_square: Oxford Street- 32"
    elif n==33:
         m="Community Chest"
    elif n==34:
         m=":green_square: Bond Street- 34"
    elif n==35:
         m="Liverpool Street Station- 35"
    elif n==36:
         m="Chance"
    elif n==37:
         m=":black_large_square: Park Lane- 36"
    elif n==38:
         m="Super Tax"
    elif n==39:
         m=":black_large_square: Mayfair- 39"
    return m

def increase(pc,val):
    pc+=val
    return pc
def decrease(pc,val):
    pc-=val
    return pc


    
    

        
    
    
