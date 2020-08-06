from cmu_112_graphics import *
from PIL import Image
import copy
import random
import os
import math
#antiquewhite, lightskyblue2,rosybrown

def drawButton(canvas,cx,cy,w,h,onClick,text,color)->None:
    """draw a Button with the given coordinate and size"""
    canvas.create_rectangle(cx-w/2, cy-h/2, cx+w/2, cy+h/2,
    fill=color,onClick=onClick,width=0)
    canvas.create_text(cx, cy, text=text, font="Helvetica 40 bold",fill="white")
def drawButton2(canvas,cx,cy,w,h,onClick,text,color)->None:
    """draw a Button with the given coordinate and size"""
    canvas.create_oval(cx-w/2, cy-h/2, cx+w/2, cy+h/2,
    fill=color,onClick=onClick,width=0)
    canvas.create_text(cx, cy, text=text, font="Helvetica 40 bold",fill="white")

class Board():
    def __init__(self,board,mode):
        """each food has x,y coordinate"""
        self.piecesMainBoard=[]
        self.pieces=[]#SideBar
        self.board=board
        self.mode=mode
        self.totalpage=self.mode.cols
        self.numPage=0
        self.piecesize=mode.piecesize

    def add(self,piece):
        self.pieces.append(piece)

    def shuffle(self):
        i=0
        random.shuffle(self.pieces)
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                self.pieces[i].y=100+row*self.piecesize
                self.pieces[i].x=50
                i+=1

    def flipForward(self):
        """flip one Page forward"""
        if self.numPage<self.totalpage - 1:
            self.numPage+=1
            return True
        if self.numPage==self.totalpage:
            return False

    def flipBackward(self):
        """flip one Page backward"""
        if self.numPage==0:
            return False
        else:
            self.numPage-=1
            return True

    def showSideBar(self,canvas):
        """renders the image of our piece"""
        currenty=100
        for piece in self.pieces:
            piece.y=-50
        start=self.numPage*self.totalpage
        for i in range(start,start+self.totalpage):
            self.pieces[i].y=currenty
            currenty+=self.piecesize
            self.pieces[i].render(canvas)
        for piece in self.pieces:
            if piece.isselected==True:
                piece.dropShadow(canvas)
                piece.render(canvas)
        if self.numPage!=self.totalpage-1:
            drawButton2(canvas, 150, 950, 60, 60,self.flipForward,"⬇","skyblue2")
        if self.numPage!=0:
            drawButton2(canvas, 150, 50, 60, 60,self.flipBackward,"⬆","skyblue2")


    def showMainBoard(self,canvas):
        for piece in self.piecesMainBoard:
            piece.render(canvas)
            ############display in side bar according to page num

            #draw Sidebar horizontal lines
        for i in range(len(self.board)+1):
            x2=50
            y2=100+self.piecesize*i
            x3=250
            y3=100+self.piecesize*i
            canvas.create_line(x2,y2,x3,y3,width=5,fill="antiquewhite")

        #create vertical and horizontal bold outline

        # for i in range(len(self.board)+1):
        #     x0=300+self.piecesize*i
        #     y0=100
        #     x1=300+self.piecesize*i
        #     y1=900
        #     canvas.create_line(x0,y0,x1,y1,width=5,fill="antiquewhite")
        # for a in range(len(self.board)+1):
        #     for i in range(len(self.board)+1):
        #         x2=300
        #         y2=100+self.piecesize*i
        #         x3=1100
        #         y3=100+self.piecesize*i
        #         canvas.create_line(x2,y2,x3,y3,width=5,fill="antiquewhite")
        for piece in self.piecesMainBoard:
            if piece.isselected==True:
                piece.dropShadow(canvas)
                piece.render(canvas)
            #print(piece.__repr__())


class Piece():
    def __init__(self,image,dirs,pos,app):
        (self.x,self.y)=pos
        (self.row,self.col)=dirs
        self.app=app
        self.piecesize=self.app.piecesize
        self.image=image
        self.isselected=False
        self.neighbors=[]
        self.diff=(0,0)
        (self.finalc,self.finalr)=pos

        (self.rx,self.ry)=(self.x,self.y)


    def clicked(self):
        print("clicked")

    def getneighbours(self):
        self.neightbours=[]
        offsets=((-1,0),(1,0),(0,-1),(0,1))

    def drag(self,x,y):
        """drag to move a selected piece"""
        (diffx, diffy)=self.diff
        self.x=x+diffx
        self.y=y+diffy
    def display(self,canvas):
        x0,y0=self.x,self.y

    def render(self,canvas):
        #print("x,y",self.x,self.y)
        x0,y0=self.x,self.y
        x1=x0+self.piecesize
        y1=y0+self.piecesize
        canvas.create_rectangle(x0,y0,x1,y1,fill="white",
        outline="antiquewhite",onClick=self.clicked)
        canvas.create_image((x0+x1)//2,(y0+y1)//2,image=self.image)
        # canvas.create_rectangle(x0,y0,x1,y1,fill="cyan",
        # outline="antiquewhite",onClick=self.clicked)

    def dropShadow(self,canvas):
        margin=20
        a0,b0=self.x+margin,self.y+margin
        a1=a0+self.piecesize
        b1=b0+self.piecesize
        canvas.create_rectangle(a0,b0,a1,b1,fill="black",
        width=0)


class StartMode(Mode):
    def appStarted(self):
        pass
    def modeActivated(self):
        print("In Start Mode...")
    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill="antiquewhite",width=0)
        drawButton(canvas, 100, self.height-60, 120, 60,
        self.onClick,"Back","skyblue2")

class LevelMode(Mode):
    def appStarted(self):
        self.rowcol=6
        self.levels=[]
        self.generateLevel()
    def modeActivated(self):
        print("In Level Mode...")
        print("level==",self.levels)

    def generateLevel(self):
        self.levels=[]
        for f in os.listdir('.'):
            if f.endswith(".png") or f.endswith(".jpg"):
                image=self.loadImage(f)
                w,h=image.size
                scale=min(w,h)
                imagesize=800
                image=self.scaleImage(image,imagesize/scale)
                image=image.crop((0,0,800,800))
                imageW,imageH=image.size
                smol=self.scaleImage(image,300/imageW)
                images,imageh=smol.size
                self.levels.append((smol,images,imageh))
        return self.levels
    def onClick(self):
        self.app.setActiveMode("start")
    def onClick0(self):
        """When the Back button is clicked, set active mode
        to start mode"""
        self.app.setActiveMode("play")
        self.rowcol=4
    def onClick1(self):
        """When the Back button is clicked, set active mode
        to start mode"""
        self.app.setActiveMode("play")
        self.rowcol=6
    def onClick2(self):
        """When the Back button is clicked, set active mode
        to start mode"""
        self.app.setActiveMode("play")
        self.rowcol=8
    # def drawDir(self):
    #     for level in self.generateLevel:
    #



    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill="antiquewhite",width=0)
        for i in range(len(self.levels)):
            w=self.levels[i][1]
            h=self.levels[i][2]
            margin=300
            marginy=300
            if i<2:
                canvas.create_rectangle(i*300+margin-w/2,marginy-h/2,i*300+margin+w/2,marginy+h/2,fill="white",onClick=self.onClick0)
                canvas.create_image(i*300+margin,marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(i*300+margin,marginy-h/2+20,text=f"level{i}",font="Helvetica 40 bold",fill="white")

            if 2<=i<=3:
                canvas.create_rectangle(i*300+margin-w/2,marginy-h/2,i*300+margin+w/2,marginy+h/2,fill="white",onClick=self.onClick1)
                canvas.create_image(i*300+margin,marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(i*300+margin,marginy-h/2+20,text=f"level{i}",font="Helvetica 40 bold",fill="white")
            if i>3:
                n=i%4
                canvas.create_rectangle(n*300+margin-w/2,300+marginy-h/2,n*300+margin+w/2,300+marginy+h/2,fill="white",onClick=self.onClick2)
                canvas.create_image(n*300+margin,300+marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(n*300+margin,marginy+h/2+50,text=f"level{i}",font="Helvetica 40 bold",fill="white")
            if i>4:
                n=i%4
                canvas.create_rectangle(n*300+margin-w/2,300+marginy-h/2,n*300+margin+w/2,300+marginy+h/2,fill="white",onClick=self.onClick1)
                canvas.create_image(n*300+margin,300+marginy,image=ImageTk.PhotoImage(self.levels[i][0]))
                canvas.create_text(n*300+margin,marginy+h/2+50,text=app.getUserInput("Name your level:"))
        drawButton(canvas, 1300, self.height-130, 150, 60,
        self.onClick,"Back","skyblue2")




from PIL import Image
class PlayMode(Mode):
    def appStarted(self):
        """take in a start board, initializes data"""
        self.rows=6
        self.cols=6
        self.squaresize=800
        self.piecesize=int(self.squaresize/self.cols)
        self.square=([[0]*self.cols for row in range(self.rows)])
        self.hint=False

        self.doubleclick=None
        self.temp=None
        self.imagesize=self.squaresize
        self.image=self.loadImage('level2.png')
        w,h=self.image.size
        scale=min(w,h)
        self.image=self.scaleImage(self.image,self.imagesize/scale)
        self.image=self.image.crop((0,0,self.squaresize,self.squaresize))
        self.imageW,self.imageH=self.image.size
        self.smol=self.scaleImage(self.image,2500/scale)
        self.temploc=None

        self.pieces=self.createPiece()
        self.pieces.shuffle()
        # self.sides=SideBar(self.side,self)

        self.pieceschain = [[]]

    def modeActivated(self):
        print("In Play Mode...")

    def check(self):
        for piece in self.pieces.pieces:
            if piece.x>=300:
                self.pieces.pieces.remove(piece)
                self.pieces.piecesMainBoard.append(piece)
                break

        for piece in self.pieces.piecesMainBoard:
            if piece.x<300:
                self.pieces.piecesMainBoard.remove(piece)
                self.pieces.pieces.append(piece)
                break
    def createPiece(self):
        pieces=Board(self.square,self)
        for row in range(self.rows):
            for col in range(self.cols):
                x0=col*self.piecesize
                y0=row*self.piecesize
                x1=x0+self.piecesize
                y1=y0+self.piecesize
                iImage=ImageTk.PhotoImage(self.image.crop((x0,y0,x1,y1)))
                piece=Piece(iImage,(row,col),(x0+300,y0+100),self)
                pieces.add(piece)
        return pieces
    def mouseDragged(self, event):
        for piece in self.pieces.piecesMainBoard:
            if piece.isselected:
                piece.drag(event.x,event.y)
                for chain in self.pieceschain:
                    if piece in chain:
                        for neighbor in chain:
                            if neighbor is not piece:
                                neighbor.drag(event.x, event.y)
            self.check()

        for piece in self.pieces.pieces:
            if piece.isselected:
                piece.drag(event.x,event.y)
            self.check()

    def mousePressed(self, event):
        for piece in self.pieces.piecesMainBoard:
            if piece.isselected==True:
                return False
        for piece in self.pieces.pieces:
            if piece.isselected==True:
                return False
        x,y=event.x,event.y
        for piece in self.pieces.piecesMainBoard:
            if piece.y<=y<=piece.y+self.piecesize and piece.x<=x<=piece.x+self.piecesize:
                self.temploc=(piece.x,piece.y)
                print('mousePressedTemp:', self.temploc)
                piece.isselected=True
                piece.diff=(piece.x-x,piece.y-y)
                for chain in self.pieceschain:
                    if piece in chain:
                        for neighbor in chain:
                            if neighbor is not piece:
                                neighbor.diff=(neighbor.x-x,neighbor.y-y)
                # for neighbor in piece.neighbors:
                #     neighbor.isSelected=True
                #     neighbor.diff=(neighbor.x-x,neighbor.y-y)
                break
        for piece in self.pieces.pieces:
            if piece.y<=y<=piece.y+self.piecesize and piece.x<=x<=piece.x+self.piecesize:
                self.temploc=(piece.x,piece.y)
                print('mousePressedTemp:', self.temploc)
                piece.isselected=True
                piece.diff=(piece.x-x,piece.y-y)


    def canBeNeib(self,piece,otherpiece):
        if otherpiece is piece:
            return False
        print("Looking for neighb")
        oneThird = piece.piecesize//3
        maxDist = piece.piecesize + oneThird
        minDist = piece.piecesize - oneThird
        if piece.col==otherpiece.col:
            if piece.row == otherpiece.row + 1:
                if minDist<=piece.y-otherpiece.y<=maxDist and abs(piece.x-otherpiece.x)<=oneThird:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x
                    piece.y=otherpiece.y+piece.piecesize
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
            elif piece.row == otherpiece.row - 1:
                if minDist<=otherpiece.y-piece.y<=maxDist and abs(piece.x-otherpiece.x)<=oneThird:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x
                    piece.y=otherpiece.y-piece.piecesize
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
        if piece.row==otherpiece.row:
            if piece.col == otherpiece.col + 1:
                if abs(piece.y-otherpiece.y)<=oneThird and minDist<=piece.x-otherpiece.x<=maxDist:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x+piece.piecesize
                    piece.y=otherpiece.y
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
            elif piece.col == otherpiece.col - 1:
                if abs(piece.y-otherpiece.y)<=oneThird and minDist<=otherpiece.x-piece.x<=maxDist:
                    oldx, oldy = piece.x, piece.y
                    piece.x=otherpiece.x-piece.piecesize
                    piece.y=otherpiece.y
                    self.alignNeibWithMerge(piece,oldx,oldy)
                    return True
        return False

    def alignNeibWithMerge(self,piece,oldx,oldy):
        for chain in self.pieceschain:
            if piece in chain:
                for neighbor in chain:
                    if neighbor is not piece:
                        neighbor.x = neighbor.x + (piece.x - oldx)
                        neighbor.y = neighbor.y + (piece.y - oldy)

    def mouseReleased(self,event):
        print("Board==",self.pieces.piecesMainBoard)
        """release mouse to release the piece"""

        x,y=event.x,event.y
        if x<300:
            ##### Do nothing for now
            print("Not allowed to put pieces back to sidebar")
            return

        for piece in (self.pieces.piecesMainBoard + self.pieces.pieces):
            if piece.isselected:
                piece.isselected=False

                (diffx,diffy)=piece.diff
                print("piece:", piece.x, " ", piece.y)
                print("event x, y:", x, " ", y)
                print("diff x, y:", diffx, " ", diffy)
                #diffx, diffy = x - piece.rx, y - piece.ry
                (piece.rx,piece.ry)=(x,y)

                thisChain = []
                for chain in self.pieceschain:
                    if piece in chain:
                        thisChain = chain

                ####### See if we can nail any pieces together
                for otherpiece in self.pieces.piecesMainBoard:
                    for chainpiece in thisChain+[piece]:
                        if otherpiece not in thisChain and self.canBeNeib(chainpiece,otherpiece):
                            print("Found Neighb: ", otherpiece.x, " , ", otherpiece.y)

                            ###### Merge with neighbor chain
                            otherChain = []
                            for chain in self.pieceschain:
                                if otherpiece in chain:
                                    otherChain = chain
                            print("thisChain is: ", thisChain)
                            print("otherChain is: ", otherChain)

                            if thisChain == [] and otherChain ==[]:
                                self.pieceschain.append([piece, otherpiece])
                            elif thisChain == []:
                                otherChain.append(piece)
                            elif otherChain == []:
                                thisChain.append(otherpiece)
                            else:
                                thisChain.extend(otherChain)
                                self.pieceschain.remove(otherChain)
                break


        self.check()

        # print("Board=",self.pieces.piecesMainBoard)
        # print("Side=",self.pieces.pieces)
        print("Chains=",len(self.pieceschain))
        # self.temploc=None


    def onClick(self):
        """When the Back button is clicked, set active mode
        to level mode"""
        self.app.setActiveMode("level")

    def redrawAll(self, canvas):
        canvas.create_rectangle(0,0,1500,1000,fill="antiquewhite",width=0)
        canvas.create_rectangle(50,100,250,900,fill="snow3",width=0)
        canvas.create_rectangle(300,100,1100,900,fill="snow3",width=0)
        canvas.create_image(1300,150,image=ImageTk.PhotoImage(self.smol))

        self.pieces.showSideBar(canvas)
        self.pieces.showMainBoard(canvas)
        drawButton(canvas, 1300, self.height-130, 150, 60,
        self.onClick,"Back","skyblue2")




class SquarePal(ModalApp):
    def appStarted(self):
        """Add all three modes to the Agar Game,
        set inital mode to play mode"""
        self.addMode(PlayMode(name="play"))
        self.addMode(StartMode(name="start"))
        self.addMode(LevelMode(name="level"))
        self.rowcol=6

        self.setActiveMode("play")


    def getState(self):
        pass
SquarePal(width=1500,height=1000)
