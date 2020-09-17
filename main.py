# Project 2 - Snow Leopards vs Billy Goats
# Name: Chi Gou Lo
# Snow Leopards are played by the computer
# Billy Goats are played by human
# Reference:
# Goat image - http://www.freepik.com/free-photos-vectors/goat
# Leopard image - http://www.thinkstockphotos.co.uk/image/stock-illustration-black-cat-head-icon/466404305


from graphics import *
from math import *
from random import *
from time import *

wSize = 600

def main():
    # setting up the game board
    win = GraphWin('Problem Solving and Programming - Project 2',wSize,wSize)
    win.setBackground(color_rgb(58,83,155))
    win.setCoords(0,0,wSize,wSize)
    ptList = drawBoard(win)
    ptsonboardGUI(ptList, win)
    GoatsOccup = []
    LeopardsOccup = []
    unOccup = list(range(0,24))
    GoatPieces = []
    LeopardPieces = []
    notifyg, notifys, notifysw, notifygw, notifylt = notifyGUI(win)
    count = 4
    # let the human player place Billy Goats        
    for turn in range(1,4):
        while len(GoatPieces)!= turn*4:
            notifygp = Text(Point(wSize/2,wSize-40), "Place "+str(count)+" More Goat/s")#extra notification
            notifygp.setStyle('bold')
            notifygp.setTextColor('white')
            notifygp.setSize(10)
            notifygp.draw(win)
            pt = win.getMouse()
            d,nn=findNN(pt, ptList)
            if nn not in GoatsOccup:
                if nn not in LeopardsOccup:
                    myImage = Image(Point(ptList[nn].getX(),ptList[nn].getY()), 'goat.png')
                    myImage.draw(win)
                    GoatPieces.append(myImage)
                    GoatsOccup.append(nn)
                    unOccup.remove(nn)
                    notifygp.undraw()
                    count = count -1
        notifyg.undraw()
        notifys.draw(win)
        notifylt.draw(win)
        count = 4
        sleep(1)
    # let the computer place Snow Leopards
        while len(LeopardPieces) != turn:
            place = randrange(1,24)
            if place not in GoatsOccup:
                if place not in LeopardsOccup:
                    myImage = Image(Point(ptList[place].getX(),ptList[place].getY()), 'leopard.png')
                    myImage.draw(win)
                    LeopardPieces.append(myImage)
                    LeopardsOccup.append(place)
                    unOccup.remove(place)
                    sleep(0.5)
        notifylt.undraw()
        notifys.undraw()
        notifyg.draw(win)
    end = False
    # Gamestart
    while end == False:
    # let the human player move a Goat
        moveGoat(win,ptList,Occup,Pieces,unOccup)
        notifyg.undraw()
        notifys.draw(win)
    # let the computer move a Leopard
        AImoveLeopard(win,ptList,LeopardsOccup,LeopardPieces,unOccup, GoatPieces, GoatsOccup)
        check = GoatsOccup.count(1000)
        notifys.undraw()
        notifyg.draw(win)
    # decide who won the game
        end = blocked(LeopardsOccup, unOccup)
        if check == len(GoatsOccup): #leopard wins if all goats are eaten
            notifyg.undraw()
            notifysw.draw(win)# leopard wins notification
            sys.exit()
    # if no one wins, game continues
    notifyg.undraw()
    notifygw.draw(win) # goat wins notification

def drawBoard(win): # DO NOT change this function. It is provided to help you. It draws the board and returns a list of Points (24 points)
    bk = wSize/8 # block size
    ptList = []
    for i in range(1,4):
        ptList = ptList + [Point(bk*i,bk*i), Point(bk*i,4*bk), Point(bk*i,bk*(8-i)),Point(4*bk,bk*(8-i)),
                       Point(bk*(8-i),bk*(8-i)),Point(bk*(8-i), 4*bk), Point(bk*(8-i),bk*i),Point(4*bk,bk*i)]
        pp = Polygon(ptList[-8:])
        pp.setWidth(5)
        pp.setOutline(color_rgb(243,156,18))
        pp.draw(win)
    for i in range(8):
        ll = Line(ptList[i],ptList[i+16])
        ll.setWidth(5)
        ll.setFill(color_rgb(243,156,18))
        ll.draw(win)
    return ptList


def blocked(Occup, unOccup): # returns True if all pieces in Occup are blocked otherwise False
    blocked = len(Occup)
    for i in Occup: # choose a piece from the list to check
        for ii in unOccup: 
            if i%8==0:
                if ii == i+1:
                    blocked = blocked - 1 #to count how many is blocked
                if ii == i+7:
                    blocked = blocked - 1
                if ii == i+8:
                    blocked = blocked - 1
                if ii == i-8:
                    blocked = blocked - 1
            elif i%8 == 7:
                if ii == i-1:
                    blocked = blocked - 1
                if ii == i-7:
                    blocked = blocked - 1
                if ii == i+8:
                    blocked = blocked - 1
                if ii == i-8:
                    blocked = blocked - 1
            else:
                if ii == i+1:
                    blocked = blocked - 1
                if ii == i-1:
                    blocked = blocked - 1
                if ii == i+8:
                    blocked = blocked - 1
                if ii == i-8:
                    blocked = blocked - 1
                
    if blocked == len(Occup): # check the amount of pieces are blocked
        return True # all pieces blocked
    else:
        return False # at least one is not blocked
    
def moveGoat(win,ptList,Occup,Pieces,unOccup): # allows user to move a Goat to a valid location and updates the relevant lists
    nn1 = 0
    nn2 = 0
    notifyselect = Text(Point(wSize/2,20), 'Please Select a Piece') # extra notification
    notifyselect.setStyle('bold')
    notifyselect.setSize(10)
    notifyselect.setTextColor('white')
    notifymove = Text(Point(wSize/2,20), 'Please Select a Location to Move/Deselect')
    notifymove.setStyle('bold')
    notifymove.setSize(10)
    notifymove.setTextColor('white')
    notifyinvalid = Text(Point(wSize/2,20), 'Invalid Move')
    notifyinvalid.setStyle('bold')
    notifyinvalid.setSize(10)
    notifyinvalid.setTextColor('white')
    while nn1==nn2:
        notifyselect.draw(win)
        pt = win.getMouse() # allow the human to select and unselect (by clicking twice) a piece.
        d1,nn1=findNN(pt, ptList)
        if nn1 in Occup:
            notifyselect.undraw()
            notifymove.draw(win)
            txt = Text(Point(ptList[nn1].getX(),ptList[nn1].getY()+37.5), "SELECTED")
            txt.setStyle("bold")
            txt.setSize(10)
            txt.setTextColor('white')
            txt.draw(win) # mark on the selected goat
            pos = Occup.index(nn1)
            pt = win.getMouse()
            d2,nn2=findNN(pt, ptList)
            if nn2 in unOccup: # valid move
                txt.undraw() # undraw mark
                notifymove.undraw()
                for i in range(100):
                    Pieces[pos].move(1/100*(ptList[nn2].getX()-ptList[nn1].getX()),1/100*(ptList[nn2].getY()-ptList[nn1].getY()))
                    sleep(0.01)
                Occup[pos]= nn2
                unOccup.remove(nn2)
                unOccup.append(nn1)
                return
            elif nn2 ==nn1: # deselection
                txt.undraw() # undraw mark
                notifymove.undraw()
            else: # invalid move
                txt.undraw() # undraw mark
                notifymove.undraw()
                notifyinvalid.draw(win)
                sleep(1)
                notifyinvalid.undraw()
                nn2=nn1
        if nn1 not in Occup: # invalid selection
            nn2=nn1
     
def AImoveLeopard(win,ptList,LeopardsOccup,LeopardPieces,unOccup, GoatPieces, GoatsOccup):
    # intelligent move for the Leopards. checks if any of the Leopards can eat a Goat. If so, it makes the corresponding move to eat the Goat
    for i in GoatsOccup:
        if i == 9 or i == 11 or i == 13 or i == 15:
            for ii in LeopardsOccup:
                if ii == i-8 or ii == i+8:
                    for iii in unOccup:
                        if iii == i-8 or iii == i+8:
                            pos = LeopardsOccup.index(ii)
                            for move in range(100):
                                LeopardPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            LeopardsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            pos = GoatsOccup.index(i)
                            GoatPieces[pos].undraw()
                            GoatsOccup[pos] = 1000
                            unOccup.append(i)
                            return
        if i%8 == 1 or i%8==3 or i%8==5:
            for ii in LeopardsOccup:
                if ii == i+1 or ii == i-1:
                    for iii in unOccup:
                        if iii == i-1 or iii == i+1:
                            pos = LeopardsOccup.index(ii)
                            for move in range(100):
                                LeopardPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            LeopardsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            pos = GoatsOccup.index(i)
                            GoatPieces[pos].undraw()
                            GoatsOccup[pos] = 1000
                            unOccup.append(i)
                            return
        if i == 8 or i == 10 or i == 12 or i == 14:
            for ii in LeopardsOccup:
                if ii == i-8 or ii == i+8:
                    for iii in unOccup:
                        if iii == i-8 or iii == i+8:
                            pos = LeopardsOccup.index(ii)
                            for move in range(100):
                                LeopardPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            LeopardsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            pos = GoatsOccup.index(i)
                            GoatPieces[pos].undraw()
                            GoatsOccup[pos] = 1000
                            unOccup.append(i)
                            return
        if i%8 == 7:
            for ii in LeopardsOccup:
                if ii == i-7 or ii == i-1:
                    for iii in unOccup:
                        if iii == i-7 or iii == i-1:
                            pos = LeopardsOccup.index(ii)
                            for move in range(100):
                                LeopardPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            LeopardsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            pos = GoatsOccup.index(i)
                            GoatPieces[pos].undraw()
                            GoatsOccup[pos] = 1000
                            unOccup.append(i)
                            return
    end = blocked(LeopardsOccup, unOccup) # check if all pieces are blocked. If not, continues
    while end==False: # performs a random Leopard move to a valid location.
        i = choice(LeopardsOccup)
        if i%8 == 7:
            for ii in unOccup:
                        if ii == i-7 or ii == i-1 or ii == i+8 or ii == i-8:
                            pos = LeopardsOccup.index(i)
                            for move in range(100):
                                LeopardPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                sleep(0.01)
                            LeopardsOccup[pos] = ii
                            unOccup.remove(ii)
                            unOccup.append(i)
                            return
        if i%8 == 0:
            for ii in unOccup:
                        if ii == i+1 or ii == i+7 or ii == i+8 or ii == i-8:
                            pos = LeopardsOccup.index(i)
                            for move in range(100):
                                LeopardPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                sleep(0.01)
                            LeopardsOccup[pos] = ii
                            unOccup.remove(ii)
                            unOccup.append(i)
                            return
        if i%8 == 1 or i%8 == 2 or i%8 == 3 or i%8 == 4 or i%8 == 5 or i%8 == 6:
            for ii in unOccup:
                        if ii == i+1 or ii == i-1 or ii == i+8 or ii == i-8:
                            pos = LeopardsOccup.index(i)
                            for move in range(100):
                                LeopardPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                sleep(0.01)
                            LeopardsOccup[pos] = ii
                            unOccup.remove(ii)
                            unOccup.append(i)
                            return

def findNN(pt, ptList):
    # returns the index number and distance of the nearest point from pt.
    # allows the user to click near the location and not pricesly on top of the locaion to place/select/move a piece
    d=1000
    for i in range(24):
        if sqrt((ptList[i].getX() - pt.getX())**2 +(ptList[i].getY() - pt.getY())**2) <= d:
            d=sqrt((ptList[i].getX() - pt.getX())**2 +(ptList[i].getY() - pt.getY())**2)
            nn=i
    return d, nn

#additional functions:
def notifyGUI(win): #Set up all the notification texts and extra
    notifyg = Text(Point(wSize/2,wSize-20), 'Goats Turn')
    notifyg.setStyle('bold')
    notifyg.setTextColor('white')
    notifyg.draw(win)
    notifys = Text(Point(wSize/2,wSize-20), 'Snow Leopard Turn')
    notifys.setStyle('bold')
    notifys.setTextColor('black')
    notifysw = Text(Point(wSize/2,wSize-20), 'Snow Leopard Win')
    notifysw.setStyle('bold')
    notifysw.setTextColor('black')
    notifygw = Text(Point(wSize/2,wSize-20), 'Goats Win')
    notifygw.setStyle('bold')
    notifygw.setTextColor('white')
    notifylt = Text(Point(wSize/2,wSize-40), 'Please Wait...')
    notifylt.setStyle('bold')
    notifylt.setSize(10)
    notifylt.setTextColor('black')
    return notifyg, notifys, notifysw, notifygw, notifylt

def ptsonboardGUI(ptList, win): #draw dots on the point to show player the place to click 
    for i in ptList:
        circ = Circle(i, 8)
        circ.setFill(color_rgb(243,156,18))
        circ.setOutline(color_rgb(243,156,18))
        circ.draw(win)

def AImoveGoat(win,ptList,LeopardsOccup,LeopardPieces,unOccup, GoatPieces, GoatsOccup):
    for i in LeopardsOccup:
        if i == 0 or i == 2 or i == 4 or i == 6 or i == 16 or i == 18 or i == 20 or i == 22:
            for ii in GoatsOccup:
                if ii == i-8 or ii == i+8:
                    for iii in unOccup:
                        if iii == i-16 or iii == i+16:
                            pos = GoatsOccup.index(ii)
                            for move in range(100):
                                GoatPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            GoatsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            return
        if i == 1 or i == 3 or i == 5 or i == 7 or i == 17 or i == 19 or i == 21 or i == 23:
            for ii in GoatsOccup:
                if ii == i-8 or ii == i+8:
                    for iii in unOccup:
                        if iii == i-16 or iii == i+16:
                            if ii == 15:
                                for iiii in unOccup:
                                    if iiii == ii-1 or iiii == ii-7:
                                        pos = GoatsOccup.index(ii)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[iiii].getX()-ptList[ii].getX()),1/100*(ptList[iiii].getY()-ptList[ii].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = iiii
                                        unOccup.append(ii)
                                        unOccup.remove(iiii)
                                        return
                            if ii == 13 or ii == 11 or ii == 9:
                                for iiii in unOccup:
                                    if iiii == ii+1 or iiii == ii-1:
                                        pos = GoatsOccup.index(ii)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[iiii].getX()-ptList[ii].getX()),1/100*(ptList[iiii].getY()-ptList[ii].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = iiii
                                        unOccup.append(ii)
                                        unOccup.remove(iiii)
                                        return
##                            elif ii == 13 or ii == 11 or ii == 9 or ii == 15: 
##                                pos = GoatsOccup.index(ii)
##                                for move in range(100):
##                                    GoatPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
##                                    sleep(0.01)
##                                GoatsOccup[pos] = iii
##                                unOccup.append(ii)
##                                unOccup.remove(iii)
##                                return
        if i%8 == 0:
            for ii in GoatsOccup:
                if ii == i+1 or ii == i+7:
                    for iii in unOccup:
                        if iii == i+2 or iii == i+6:
                            pos = GoatsOccup.index(ii)
                            for move in range(100):
                                GoatPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            GoatsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            return
        if i%8 == 2 or i%8 == 4:
            for ii in GoatsOccup:
                if ii == i+1 or ii == i-1:
                    for iii in unOccup:
                        if iii == i+2 or iii == i-2:
                            pos = GoatsOccup.index(ii)
                            for move in range(100):
                                GoatPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            GoatsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            return
        if i%8==6:
            for ii in GoatsOccup:
                if ii == i+1 or ii == i-1:
                    for iii in unOccup:
                        if iii == i-6 or iii == i-2:
                            pos = GoatsOccup.index(ii)
                            for move in range(100):
                                GoatPieces[pos].move(1/100*(ptList[iii].getX()-ptList[ii].getX()),1/100*(ptList[iii].getY()-ptList[ii].getY()))
                                sleep(0.01)
                            GoatsOccup[pos] = iii
                            unOccup.append(ii)
                            unOccup.remove(iii)
                            return
    while True:
        i = choice(GoatsOccup)
        if i%8 == 1 or i%8 == 3 or i%8 == 5:
            for ii in unOccup:
                if ii == i+1 or ii == i-1:
                    pos = GoatsOccup.index(i)
                    for move in range(100):
                        GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                        sleep(0.01)
                    GoatsOccup[pos] = ii
                    unOccup.append(i)
                    unOccup.remove(ii)
                    return
        if i%8 == 7:
            for ii in unOccup:
                if ii == i-1 or ii == i-7:
                    pos = GoatsOccup.index(i)
                    for move in range(100):
                        GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                        sleep(0.01)
                    GoatsOccup[pos] = ii
                    unOccup.append(i)
                    unOccup.remove(ii)
                    return
        if i%8 == 0:
            for ii in unOccup:
                if ii == i+8 or ii == i-8:
                    pos = GoatsOccup.index(i)
                    for move in range(100):
                        GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                        sleep(0.01)
                    GoatsOccup[pos] = ii
                    unOccup.append(i)
                    unOccup.remove(ii)
                    return
            for ii in unOccup:
                if ii == i+1 or ii == i+7:
                    for iii in LeopardsOccup:
                        if i == 8:
                            if ii == 9:
                                if iii != ii+1 or iii != ii+8 or iii != ii-8:
                                    pos = GoatsOccup.index(i)
                                    for move in range(100):
                                        GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                        sleep(0.01)
                                    GoatsOccup[pos] = ii
                                    unOccup.append(i)
                                    unOccup.remove(ii)
                                    return
                            if ii == 15:
                                if iii != ii-1 and iii != ii+8 and iii != ii-8:
                                    pos = GoatsOccup.index(i)
                                    for move in range(100):
                                        GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                        sleep(0.01)
                                    GoatsOccup[pos] = ii
                                    unOccup.append(i)
                                    unOccup.remove(ii)
                                    return
                        else:
                            if iii != i+2 or iii != i+6:
                                pos = GoatsOccup.index(i)
                                for move in range(100):
                                    GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                    sleep(0.01)
                                GoatsOccup[pos] = ii
                                unOccup.append(i)
                                unOccup.remove(ii)
                                return
        if i%8 == 2 or i%8 == 4 or i%8 == 6:
            for ii in unOccup:
                if ii == i+1 or ii == i-1:
                    for iii in LeopardsOccup:
                        if i%8 == 6:
                            if i<8 or i>15:
                                if ii == i+1:
                                    if iii != i-6:
                                        pos = GoatsOccup.index(i)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = ii
                                        unOccup.append(i)
                                        unOccup.remove(ii)
                                        return
                                if ii == i-1:
                                    if iii !=i-2:
                                        pos = GoatsOccup.index(i)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = ii
                                        unOccup.append(i)
                                        unOccup.remove(ii)
                                        return
                            else:
                                if ii == i+1:
                                    if iii != i-6 or iii!=i+9 or iii!=i-7:
                                        pos = GoatsOccup.index(i)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = ii
                                        unOccup.append(i)
                                        unOccup.remove(ii)
                                        return
                                if ii == i-1:
                                    if iii != i-2 or iii!=i-9 or iii!=i+7:
                                        pos = GoatsOccup.index(i)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = ii
                                        unOccup.append(i)
                                        unOccup.remove(ii)
                                        return
                        else:
                            if i<8 or i>15:
                                if ii == i+1:
                                        if iii != i+2:
                                            pos = GoatsOccup.index(i)
                                            for move in range(100):
                                                GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                                sleep(0.01)
                                            GoatsOccup[pos] = ii
                                            unOccup.append(i)
                                            unOccup.remove(ii)
                                            return
                                if ii == i-1:
                                    if iii != i-2:
                                        pos = GoatsOccup.index(i)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = ii
                                        unOccup.append(i)
                                        unOccup.remove(ii)
                                        return
                            else:
                                if ii == i+1:
                                        if iii != i+2 or iii != i+9 or iii!= i-7:
                                            pos = GoatsOccup.index(i)
                                            for move in range(100):
                                                GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                                sleep(0.01)
                                            GoatsOccup[pos] = ii
                                            unOccup.append(i)
                                            unOccup.remove(ii)
                                            return
                                if ii == i-1:
                                    if iii != i-2 or iii!=i-9 or iii!=i+7:
                                        pos = GoatsOccup.index(i)
                                        for move in range(100):
                                            GoatPieces[pos].move(1/100*(ptList[ii].getX()-ptList[i].getX()),1/100*(ptList[ii].getY()-ptList[i].getY()))
                                            sleep(0.01)
                                        GoatsOccup[pos] = ii
                                        unOccup.append(i)
                                        unOccup.remove(ii)
                                        return
                                        
main()
