import pygame, Player, random, TextObject, MenuButton
from pygame.locals import *
import resourceManager, TextObject
from time import sleep
pygame.init()

class BoardSpot(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.mouseOver = False
        self.token = ""
        self.position = pos
        self.rect = pygame.Rect((0,0),(100,100))
        self.rect.midtop = self.position

    def is_mouse_over(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] < self.rect.x:
            return False
        if mousePos[0] > self.rect.x + self.rect.w:
            return False
        if mousePos[1] < self.rect.y:
            return False
        if mousePos[1] > self.rect.y + self.rect.h:
            return False
        return True

    def set_token(self,board,multiplayer=False):
        if self.token == "":
            self.token = board.currentPlayer.token
            if multiplayer == False:
                board.getnextplayer()
        else:
            error = "That spot already has a token on it!"
            board.errorObject.update_message(error)

    def update(self):
        if self.is_mouse_over() == True:
            self.mouseOver = True
        else:
            self.mouseOver = False

    def draw(self,screen,x,o):
        if self.mouseOver == True:
            pygame.draw.rect(screen,(115,205,205),self.rect)
        else:
            pass
        if self.token != "":
            if self.token == "X":
                screen.blit(x,self.rect)
            else:
                screen.blit(o,self.rect)

class Board(object):
    def __init__(self,player1,player2,windowWidth,windowHeight,multiplayer=False,username=""):
        self.player1 = player1
        self.player2 = player2

        self.image_X,self.image_X_Rect = resourceManager.load_image("X.png",-1)
        self.image_O,self.image_O_Rect = resourceManager.load_image("O.png",-1)

        self.currentPlayer = None
        self.gameOver = False

        self.play_again = MenuButton.MenuButton("Play Again?",(windowWidth/2+110,windowHeight-60),60)

        # do not touch these 2, they will be used in multiplayer games
        self.multiplayer = multiplayer
        self.username = username
        self.started = False
        self.go = False

        # load and position the tic-tac-toe board
        self.board_image,self.board_rect = resourceManager.load_image("board.png",-1)
        self.board_rect.midtop = (windowWidth/2,0)

        # create error text object and current player text object
        self.currentPlayerTextObject = TextObject.TextObject((windowWidth/2,windowHeight-110),50,(255,255,0),"")
        self.errorObject = TextObject.TextObject((windowWidth/2,windowHeight-50),50,(255,0,0),"")

        # Here is how the board spots are indexed in the list
        #    |   |
        #  0 | 3 | 6
        #--------------
        #  1 | 4 | 7
        #--------------
        #  2 | 5 | 8
        #    |   |
        #
        # now let's actually spawn the board spots
        self.spots = []
        for i in range(3):
            for j in range(3):
                pos = (self.board_rect.x + 58 + (130 * i),self.board_rect.y + 7 + (130 * j))
                self.spots.append(BoardSpot(pos))


        self.row1 = [self.spots[0],self.spots[3],self.spots[6]]
        self.row2 = [self.spots[1],self.spots[4],self.spots[7]]
        self.row3 = [self.spots[2],self.spots[5],self.spots[8]]

        self.col1 = [self.spots[0],self.spots[1],self.spots[2]]
        self.col2 = [self.spots[3],self.spots[4],self.spots[5]]
        self.col3 = [self.spots[6],self.spots[7],self.spots[8]]

        self.diag1 = [self.spots[0],self.spots[4],self.spots[8]]
        self.diag2 = [self.spots[6],self.spots[4],self.spots[2]]

        self.conditions = [self.row1,self.row2,self.row3,self.col1,self.col2,self.col3,self.diag1,self.diag2]

    def getnextplayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        elif self.currentPlayer == self.player2:
            self.currentPlayer = self.player1
        if self.currentPlayer.name == self.username:
            self.go = True
        self.currentPlayerTextObject.update_message("It is " + self.currentPlayer.name + "'s turn!")
        self.errorObject.update_message("")
        
    def setplayers(self,p1,p2,setcurrent=True,currentIndex=0):
        # set the game players and randomly choose one of them to go first
        self.player1 = p1
        self.player2 = p2
        if setcurrent == True:
            self.setcurrentplayer(currentIndex)
    def setcurrentplayer(self,index):
        if index == 0:
            self.currentPlayer = self.player1
        else:
            self.currentPlayer = self.player2
        self.currentPlayerTextObject.update_message("It is " + self.currentPlayer.name + "'s turn!")
        if self.currentPlayer.name == self.username:
            self.go = True
    def start_game(self):
        self.started = True
        self.currentPlayerTextObject.update_message("Both players are here!")
        sleep(1)
        self.currentPlayerTextObject.update_message("It is " + self.currentPlayer.name + "'s turn!")
    def domove_multiplayer(self,events,client):
        if self.started == True:
            for i in self.spots:
                if i.mouseOver == True:
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                if self.currentPlayer != None and self.currentPlayer.name == self.username:
                                    i.set_token(self,True)
                                    boardinfo = ""
                                    for i in self.spots:
                                        if i.token == "":
                                            boardinfo += "N"
                                        else:
                                            boardinfo += i.token.upper()
                                    self.go = False
                                    client.send_message("_SENDBOARDINFO_" + boardinfo)
            self.checkforwin()
        elif self.started == False:
            self.currentPlayerTextObject.update_message("Waiting for other player to join...")

    def domove(self,events):
        if self.currentPlayer.type == "Human":
            for i in self.spots:
                if i.mouseOver == True:
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                if self.multiplayer == False:
                                    i.set_token(self)
                                else:
                                    if self.currentPlayer.name == self.username:
                                        i.set_token(self)        
        elif self.currentPlayer.type == "AI":
            self.doaimove()
        self.checkforwin()
        
    def doaimove(self):
        sleep(0.5)

        otherPlayer = None
        if self.currentPlayer == self.player1:
            otherPlayer = self.player2
        else:
            otherPlayer = self.player1

        if self.spots[4].token == "":
            self.spots[4].set_token(self)
        else:
            #loop through each row/col/diag and check to see if the ai can win. 
            #If not, then check to see if the ai can block the player's move. 
            #If neither, try picking a corner. If not, then randomly pick a spot
            gone = False
            for i in self.conditions:
                for j in i:
                    if self.GetAmountOfMatchingTextInLine(i, self.currentPlayer.token) == 2:
                        if j.token == "" and gone == False:
                            j.set_token(self) 
                            gone = True
                            break
            for i in self.conditions:
                for j in i:
                    if self.GetAmountOfMatchingTextInLine(i, otherPlayer.token) == 2:
                        if j.token == "" and gone == False:
                            j.set_token(self)
                            gone = True
                            break
            while self.GetAmountOfFilledSpots() < len(self.spots) and gone == False:
                randInt = random.randint(0, len(self.spots)-1)
                if self.IsAtLeast1CornerToFill() == True:
                    if gone == False and self.spots[randInt].token == "":
                        if self.spots[randInt] == self.spots[0] or self.spots[randInt] == self.spots[6] or self.spots[randInt] == self.spots[2] or self.spots[randInt] == self.spots[8]:
                            self.spots[randInt].set_token(self)
                            gone = True
                            break
                else:
                    if gone == False and self.spots[randInt].token == "":
                        self.spots[randInt].set_token(self)
                        gone = True
                        break
        sleep(0.5)

    def IsAtLeast1CornerToFill(self):
        for s in self.spots:
            if s.token == "":
                if s == self.spots[0] or s == self.spots[6] or s == self.spots[2] or s == self.spots[8]:
                    return True
        return False

    def GetAmountOfMatchingTextInLine(self,line,token):
        amount = 0
        for i in line:
            if i.token == token:
                amount+=1
        return amount
    def GetAmountOfFilledSpots(self):
        amount = 0
        for i in self.spots:
            if i.token != "":
                amount+=1
        return amount

    def resetboard(self,index=0):
        for i in self.spots:
            i.token = ""
        self.setplayers(self.player1,self.player2,True,index)
        self.gameOver = False

    def checkforwin(self):
        winner = ""
        for i in self.conditions:
            count = 0
            win = True
            winningToken = "None"
            for j in i:
                if count == 0:
                    winningToken  = j.token
                else:
                    if j.token != winningToken: 
                        win = False
                        break
                count += 1
            if win == True:
                if winningToken != "None":
                    if self.player1.token == winningToken:
                        winner = "Player 1"
                    elif self.player2.token == winningToken:
                        winner = "Player 2"
        count1 = 0
        for i in self.spots:
            if i.token != "":
                count1 += 1
        if count1 >= 9:
            winner = "None"
        if winner == "Player 1":
            self.currentPlayerTextObject.update_message(self.player1.name + " wins!")
            self.gameOver = True
            self.errorObject.update_message("")
        elif winner == "Player 2":
            self.currentPlayerTextObject.update_message(self.player2.name + " wins!")
            self.gameOver = True
            self.errorObject.update_message("")
        elif winner == "None":
            self.currentPlayerTextObject.update_message("The game ended in a tie!")
            self.gameOver = True
            self.errorObject.update_message("")

    def update(self,events,client):
        self.currentPlayerTextObject.update()
        self.errorObject.update()
        for i in self.spots:
            i.update()
            
        if self.gameOver == False:
            if self.multiplayer == False:
                self.domove(events)
            else:
                self.domove_multiplayer(events,client)
        else:
            self.play_again.update()
            if self.play_again.is_clicked(events) == True:
                if self.multiplayer == True:
                    client.send_message("_RESTARTBOARD_")
                else:
                    self.resetboard()
    def draw(self, screen):
        if self.gameOver == True:
            self.play_again.draw(screen)
        screen.blit(self.board_image,self.board_rect)
        self.currentPlayerTextObject.draw(screen)
        self.errorObject.draw(screen)
        for i in self.spots:
            i.draw(screen,self.image_X,self.image_O)
