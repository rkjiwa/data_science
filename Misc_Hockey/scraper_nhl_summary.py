# This was written in 2017 and may be out of date.

# This script has been written to take whether a game is a Regular Season game
# and the game number in order to generate a excel file of the scraped data

# inputs: regular season or playoffs, game number
# output: excel file in cwd

# TODO: There is an error that occurs when a team takes a team penalty in a game,
#       there is an additional row that is unaccounted for. Find a way to detect,
#       if this is the case and work around it so you can still get the event data.
#       Fix this error.


# imports
import lxml
from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys

# find out whether regular season or playoffs and get a game number
print('Would you like the event summary for the regular season or playoffs? Enter r for season or p for playoffs.')
RSoP = input()
if RSoP == 'r':
    RSoP = 'ES02'
elif RSoP == 'p':
    RSoP = 'ES03'
else:
    sys.exit('Error')

print('What game number would you like the data for? Please enter 4 digits. So game 1 would be 0001, game 10 would be 0010, game 100 would be 0100, and game 1000 would be 1000.')
GameNumber = input()
if len(GameNumber) != 4:
    sys.exit('Error')
elif int(GameNumber) > 1230:
    sys.exit('Error')
else:
    print('Thank you')
# set url
url = 'http://www.nhl.com/scores/htmlreports/20162017/' + RSoP + GameNumber + '.HTM'
# get data from url
r = requests.get(url)

# use beautiful soup and lxml to help parse data
soup = BeautifulSoup(r.text, 'lxml')

#print to verify
# print(soup)

# get data from beautiful soup, based off of the row class
# table = soup.findAll('table', attrs={'border':'0', 'cellpadding':'0','cellspacing':'0', 'width':'100%'})

# To eliminate team penalty problem


# create variables for data
Num = []
Pos = []
Name = []
G = []
A = []
P = []
PlMns = []
PN = []
PIM = []
TOT = []
Shifts = []
AvgSh = []
PP = []
SH = []
EV = []
S = []
AttBlk = []
MissShot = []
Hits = []
GV = []
TK = []
BS = []
FW = []
FL = []
FOpercentage = []

# create list with all instances of player numbers, then strip and create a new list with isolated numbers
table2 = soup.findAll('td', attrs = {'class':'lborder + bborder + rborder', 'align':'center'})
test1 = table2[0].string.strip()
for i in range(len(table2)):
    plnu = table2[i].string.strip()
    Num.append(int(plnu))

# create list w/ instances of player position, strip, create new list with isolate position
table3 = soup.findAll('td', attrs = {'class':'bborder + rborder', 'align':'center'})
test2 = table3[0].string.strip()
for i in range(len(table3)):
    plpos = table3[i].string.strip()
    Pos.append(plpos)

# create list with player name, strip and create new list to isolate
table4 = soup.findAll('td', attrs = {'class':'bborder + rborder'})
test3 = table4[1].string.strip()
for i in range(1,(len(table4)),2):
    plnam = table4[i].string.strip()
    Name.append(plnam)



# isolate the actual player stats, split into teams and merge again to eliminate the team total rows
table5 = soup.findAll('td', attrs = {'class':'rborder + bborder', 'align':'center'})
team1 = table5[0:440]
team2 = table5[458:897]
bothteams = team1 + team2

# TODO: This can be shortened by creating a function. So write said function.
#create a list for the goals
for i in range(0,(len(bothteams)),22):
    col1 = bothteams[i].string.strip()
    if col1 == '':
        col1 = 0
    else:
        col1 = int(col1)
    G.append(col1)

#create a list for the assists
for i in range(1,(len(bothteams)),22):
    col2 = bothteams[i].string.strip()
    if col2 == '':
        col2 = 0
    else:
        col2 = int(col2)
    A.append(col2)

#create a list for points
for i in range(2,(len(bothteams)), 22):
    col3 = bothteams[i].string.strip()
    if col3 == '':
        col3 = 0
    else:
        col3 = int(col3)
    P.append(col3)

# create a list for Plus Minus
for i in range(3, (len(bothteams)), 22):
    col4 = bothteams[i].string.strip()
    if col4 == '':
        col4 = 0
    else:
        col4 = int(col4)
    PlMns.append(col4)

# create a list for Penalties
for i in range(4, (len(bothteams)), 22):
    col5 = bothteams[i].string.strip()
    if col5 == '':
        col5 = 0
    else:
        col5 = int(col5)
    PN.append(col5)

# create a list for PIM
for i in range(5, (len(bothteams)), 22):
    col6 = bothteams[i].string.strip()
    if col6 == '':
        col6 = 0
    else:
        col6 = int(col6)
    PIM.append(col6)

# create a list for Total Time on Ice
for i in range(6, (len(bothteams)), 22):
    col7 = bothteams[i].string.strip()
    TOT.append(col7)

# create a list for Shifts
for i in range(7, (len(bothteams)), 22):
    col8 = bothteams[i].string.strip()
    if col8 == '':
        col8 = 0
    else:
        col8 = int(col8)
    Shifts.append(col8)

# create a list for the average Shifts
for i in range(8, (len(bothteams)), 22):
    col9 = bothteams[i].string.strip()
    AvgSh.append(col9)

# create a list for the PP TOI
for i in range(9, (len(bothteams)), 22):
    col10 = bothteams[i].string.strip()
    PP.append(col10)

# create a list for the SH TOI
for i in range(10, (len(bothteams)), 22):
    col11 = bothteams[i].string.strip()
    SH.append(col11)

# create a list for the EV TOI
for i in range(11, (len(bothteams)), 22):
    col12 = bothteams[i].string.strip()
    EV.append(col12)

# create a list for Shots
for i in range(12, (len(bothteams)), 22):
    col13 = bothteams[i].string.strip()
    if col13 == '':
        col13 = 0
    else:
        col13 = int(col13)
    S.append(col13)

# create a list of Attempts Blocked
for i in range(13, (len(bothteams)), 22):
    col14 = bothteams[i].string.strip()
    if col14 == '':
        col14 = 0
    else:
        col14 = int(col14)
    AttBlk.append(col14)

#create a list of Missed Shots
for i in range(14, (len(bothteams)), 22):
    col15 = bothteams[i].string.strip()
    if col15 == '':
        col15 = 0
    else:
        col15 = int(col15)
    MissShot.append(col15)

# create a list for Hits
for i in range(15, (len(bothteams)), 22):
    col16 = bothteams[i].string.strip()
    if col16 == '':
        col16 = 0
    else:
        col16 = int(col16)
    Hits.append(col16)

# create a list for giveaways
for i in range(16, (len(bothteams)), 22):
    col17 = bothteams[i].string.strip()
    if col17 == '':
        col17 = 0
    else:
        col17 = int(col17)
    GV.append(col17)

# create a list for takeaways
for i in range(17, (len(bothteams)), 22):
    col18 = bothteams[i].string.strip()
    if col18 == '':
        col18 = 0
    else:
        col18 = int(col18)
    TK.append(col18)

# create a list for blocked Shots
for i in range(18, (len(bothteams)), 22):
    col19 = bothteams[i].string.strip()
    if col19 == '':
        col19 = 0
    else:
        col19 = int(col19)
    BS.append(col19)

# create a list for FaceOffs Won
for i in range(19, (len(bothteams)), 22):
    col20 = bothteams[i].string.strip()
    if col20 == '':
        col20 = 0
    else:
        col20 = int(col20)
    FW.append(col20)

# create a list for Face Offs Loss
for i in range(20, (len(bothteams)), 22):
    col21 = bothteams[i].string.strip()
    if col21 == '':
        col21 = 0
    else:
        col21 = int(col21)
    FL.append(col21)

#create a list for the FO percentage
for i in range(21, (len(bothteams)), 22):
    col22 = bothteams[i].string.strip()
    if col22 == '':
        col22 = 0
    else:
        col22 = int(col22)
    FOpercentage.append(col22)
FOpercentage.append(0)

# combine all the lists into one
columns = {'Number': Num, 'Pos': Pos, 'Player' : Name, 'Goals' : G, 'Assist': A, 'Points':P, '+/-':PlMns,
        'Penalties':PN, 'PIM':PIM, 'TOI':TOT, 'Shifts':Shifts, 'AvgSh':AvgSh, 'PP':PP, 'SH':SH, 'EV':EV,
        'S':S, 'AttBlk':AttBlk, 'MS':MissShot, 'Hits':Hits, 'GV':GV, 'TK':TK, 'BS':BS, 'FW':FW, 'FL':FL,
        'FO%':FOpercentage}

# create a dataframe to hold all the data
df = pd.DataFrame(columns)
# reindex for cleaner view in excel
df = df.reindex(columns = ['Number', 'Pos', 'Player','Goals', 'Assist', 'Points','+/-', 'Penalties', 'PIM', 'TOI', 'Shifts', 'AvgSh'
                            ,'PP', 'SH', 'EV', 'S', 'AttBlk', 'MS', 'Hits', 'GV', 'TK', 'BS', 'FW', 'FL', 'FO%'])


# export for excel
df.to_excel('gamesummary' + RSoP + GameNumber + '.xlsx')
