
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from random import random
from math import *

class paletteEff:

    def __init__(self):
        self.name="EffPalette"
    def color_r(self, col):
        if col<0.70:
            return 1
        elif col>95:
            return 0
        else:
            return 1- (col-0.7)/(0.95-0.7)
    def color_g(self, col):
        if col<0.70:
            return 0
        elif col>95:
            return 1
        else:
            return (col-0.7)/(0.95-0.7)        
    def color_b(self, col):    
        return 0
    def color_a(self, col):
        return 0.1

class transformation:

    def __init__(self):
        self.vector=[0,0,0]
        self.rotation=[0,0,0]

    def setPos(self, x, y, z):
        self.vector=[x,y,z]

    def setRot(self,alfa, beta, gamma):
        self.rotation=[alfa,beta,gamma]

    def getAngles(self):
        return self.rotation

    def getPos(self):
        return self.vector

    def goTo(self):
        glTranslatef(self.vector[0], self.vector[1], self.vector[2])
        return

    def goBack(self):
        glTranslatef(-self.vector[0], -self.vector[1], -self.vector[2])
        return
    def rotate(self):
        glRotatef(self.getAngles()[0],1,0,0)
        glRotatef(self.getAngles()[1],0,1,0)
        glRotatef(self.getAngles()[2],0,0,1)
    def unRotate(self):
        glRotatef(-self.getAngles()[2],0,0,1)
        glRotatef(-self.getAngles()[1],0,1,0)
        glRotatef(-self.getAngles()[0],1,0,0)


class shape:
    def __init__(self):
        self.name='GenericShape'
    def draw():
        return

class box(shape):

    def __init__(self, dx, dy, dz):
        self.name="Box"
        self.dx=dx
        self.dy=dy
        self.dz=dz
    def draw(self):
        # now start the quads
        glBegin(GL_QUADS)
        glVertex3f(self.dx, self.dy,-self.dz)
        glVertex3f(self.dx, -self.dy,-self.dz)
        glVertex3f(-self.dx, -self.dy,-self.dz)
        glVertex3f(-self.dx, self.dy,-self.dz)

        glVertex3f(self.dx, self.dy,self.dz)
        glVertex3f(self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, self.dy,self.dz)

        glVertex3f(self.dx, self.dy,-self.dz)
        glVertex3f(self.dx, -self.dy,-self.dz)
        glVertex3f(self.dx, -self.dy,self.dz)
        glVertex3f(self.dx, self.dy,self.dz)

        glVertex3f(-self.dx, self.dy,-self.dz)
        glVertex3f(-self.dx, -self.dy,-self.dz)
        glVertex3f(-self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, self.dy,self.dz)

        glVertex3f(self.dx, self.dy,-self.dz)
        glVertex3f(self.dx, self.dy,self.dz)
        glVertex3f(-self.dx, self.dy,self.dz)
        glVertex3f(-self.dx, self.dy,-self.dz)

        glVertex3f(self.dx, -self.dy,-self.dz)
        glVertex3f(self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, -self.dy,-self.dz)
        glEnd()


    def drawLines(self,black=True):

#        self.dx=self.dx+0.05
#        self.dy=self.dy+0.05
#        self.dz=self.dz+0.05
#        
        glLineWidth(1)
        if(black):
            glColor4f(0,0,0,1)
        else:
            glColor4f(0,0,1,1)
            
        glBegin(GL_LINES);
        glVertex3f(self.dx, self.dy,-self.dz)
        glVertex3f(self.dx, -self.dy,-self.dz)
        glVertex3f(self.dx, -self.dy,-self.dz)
        glVertex3f(-self.dx, -self.dy,-self.dz)
        glVertex3f(-self.dx, -self.dy,-self.dz)
        glVertex3f(-self.dx, self.dy,-self.dz)
        glVertex3f(-self.dx, self.dy,-self.dz)
        glVertex3f(self.dx, self.dy,-self.dz)
        glEnd()
        
        glBegin(GL_LINES);
        glVertex3f(self.dx, self.dy,self.dz)
        glVertex3f(self.dx, -self.dy,self.dz)
        glVertex3f(self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, self.dy,self.dz)
        glVertex3f(-self.dx, self.dy,self.dz)
        glVertex3f(self.dx, self.dy,self.dz)
        glEnd()
        
        glBegin(GL_LINES);
        glVertex3f(self.dx, self.dy,-self.dz)
        glVertex3f(self.dx, self.dy,+self.dz)
        glVertex3f(self.dx, -self.dy,self.dz)
        glVertex3f(self.dx, -self.dy,-self.dz)
        glVertex3f(-self.dx, self.dy,-self.dz)
        glVertex3f(-self.dx, self.dy,+self.dz)
        glVertex3f(-self.dx, -self.dy,self.dz)
        glVertex3f(-self.dx, -self.dy,-self.dz)
        glEnd()
        
class volume:

    def __init__(self,name):

        self.name=name
        self.daughters=list()
        self.mother=self
        self.color=0
        self.trans=transformation()
        self.displayTrans=transformation()
        self.palette=paletteEff()
        self.visible=True
        self.id=int()
        self.selected=False
        self.standAlone=False
        
    def setShape(self,shape):
        self.shape=shape

    def setTrans(self, trans):
        self.trans=trans

    def setDisplayTrans(self, trans):
        self.displayTrans=trans

    def setStandAlone(self,sa):
        if self.standAlone != sa:
            # we are actually changing state. need to trigger the actions
            self.standAlone=sa
            if sa:
                self.goToStandAlone()
            else:
                self.backFromStandAlone()

    def addDaughter(self, vol, trans):
        vol.setMother(self)
        vol.setTrans(trans)
        self.daughters.append(vol)

    def setMother(self, a):
        self.mother=a

    def getColor(self):
        return self.color

    def setColor(self,color):
        self.color=color

    def unSelect(self):
        self.selected=False
        # do this recursively for doughters
        if len(self.daughters):
            for vol in self.daughters:
                vol.unSelect()

    def select(self):
        self.selected=True
        print "*****************************************"
        print "Thanks for selecting me!"
        print "My name is", self.name, "son of", self.mother.name
        print "I have ",len(self.daughters), " children"
        print "Type d to hide me and see my children"
        print "Type u to hide me and see my parent"
        print "Right click to concentrate on me only"

    def computeColor(self):
        color=0
        if len(self.daughters):
            for v in self.daughters:
                color+=v.computeColor()
            self.color=color/len(self.daughters)
        return self.color

    def drawColor(self):
        # specify the color from palette
        glColor4f(self.palette.color_r(self.color),
                  self.palette.color_g(self.color),
                  self.palette.color_b(self.color),
                  self.palette.color_a(self.color))

    def showChildren(self):

        if len(self.daughters):
            self.visible=False
            for v in self.daughters:
                v.visible=True

    def setVisible(self):
        self.visible=True
        self.hideChildren()

    def hideChildren(self):

        if len(self.daughters):
            for v in self.daughters:
                v.visible=False
                v.hideChildren()

    def showMother(self):
        if (self.mother.name[0:6]!="sector" and
            self.mother.name[0:5]!="atlas"):
            self.mother.setVisible()

    def applyDrawTransf(self):
        if self.standAlone:
            self.displayTrans.goTo()
            self.displayTrans.rotate()
        else:
            self.trans.goTo()
            self.trans.rotate()

    def unDoDrawTransf(self):
        if self.standAlone:
            self.displayTrans.goBack()
            self.displayTrans.unRotate()
        else:
            self.trans.goBack()
            self.trans.unRotate()

    def goToStandAlone(self):
        #do things here which need to be done when moving to/from from standAlone
        pass

    def backFromStandAlone(self):
        #do things here which need to be done when moving to/from from standAlone
        pass

    def draw(self):
        # go to specified position

        #glPushMatrix()
        self.applyDrawTransf()
        if(self.visible):
            glPushName(self.id) 
            self.drawColor()
            self.shape.draw()
            glPopName()

            if self.selected:
                self.shape.drawLines(False)
    
        # now recursively draw daughters
        if len(self.daughters):
            for v in self.daughters:
                v.draw()
        # be polite and bring cursor back
        # glPopMatrix()
        self.unDoDrawTransf()

class panel(volume):
    def __init__(self,type):
        volume.__init__(self,"panel")
        self.name="panel"
        #types are ML, MS, OL, OS
        dx=0
        dy=0.01
        dz=14

        if(type=="ML"):
            dx=0.5*2/2.
            dz=12
        elif(type=="OL"):
            dx=0.5*3/2.
        elif(type=="MS"):
            dx=0.5*1.5/2.
            dz=12
        elif(type=="OS"):
            dx=0.5*2/2.

        dz=dz*0.5/28.

        self.setShape(box(dx,dy,dz))
        self.setColor(0.7+0.3*random())
        self.id=1
        self.visible=False

class station(volume):

    def __init__(self,type):
        volume.__init__(self,"station")
        self.visible=True
        #types are ML, MS, OL, OS
        dx=0
        dy=0.1
        dz=14

        if(type=="ML"):
            dx=2
            dz=12
        elif(type=="OL"):
            dx=3
        elif(type=="MS"):
            dx=1.5
            dz=12
        elif(type=="OS"):
            dx=2

        dz=dz*0.9/14.

        self.setShape(box(dx,dy,dz))
        self.visible=False
        self.name="station"

        # put 8 panels into one station

        panel1=panel(type)
        panel1.name=panel1.name+str(1)
        transf1=transformation()
        transf1.setPos(-dx/2.,dy/2.,-dz/2.)
        self.addDaughter(panel1,transf1)
        
        panel2=panel(type)
        panel2.name=panel2.name+str(2)
        transf2=transformation()
        transf2.setPos(dx/2.,dy/2.,-dz/2.)
        self.addDaughter(panel2,transf2)
        
        panel3=panel(type)
        panel3.name=panel3.name+str(3)
        transf3=transformation()
        transf3.setPos(-dx/2.,dy/2.,dz/2.)
        self.addDaughter(panel3,transf3)
        
        panel4=panel(type)
        panel4.name=panel4.name+str(4)
        transf4=transformation()
        transf4.setPos(dx/2.,dy/2.,dz/2.)
        self.addDaughter(panel4,transf4)
        
        panel5=panel(type)
        panel5.name=panel5.name+str(5)
        transf5=transformation()
        transf5.setPos(-dx/2.,-dy/2.,-dz/2.)
        self.addDaughter(panel5,transf5)

        panel6=panel(type)
        panel6.name=panel6.name+str(6)
        transf6=transformation()
        transf6.setPos(dx/2.,-dy/2.,-dz/2.)
        self.addDaughter(panel6,transf6)

        panel7=panel(type)
        panel7.name=panel7.name+str(7)
        transf7=transformation()
        transf7.setPos(-dx/2.,-dy/2.,dz/2.)
        self.addDaughter(panel7,transf7)

        panel8=panel(type)
        panel8.name=panel8.name+str(8)
        transf8=transformation()
        transf8.setPos(dx/2.,-dy/2.,dz/2.)
        self.addDaughter(panel8,transf8)


class layer(volume):

    def __init__(self,type):
        volume.__init__(self,"layer")
        self.visible=True
        #types are ML, MS, OL, OS
        dx=0
        dy=0.1
        dz=14
        
        if(type=="ML"):
            dx=2
            dz=12
        elif(type=="OL"):
            dx=3
        elif(type=="MS"):
            dx=1.5
            dz=12
        elif(type=="OS"):
            dx=2

        theLayerShape=box(dx,dy,dz)
        self.setShape(theLayerShape)

        #build stations
        for i in range(0,14):
            theChamber=station(type)
            theChamber.setColor(1*i/14.)
            theChamber.id=i+1
            theChamber.visible=False
            theChamber.name="station"+str(i+1)
            
            transf=transformation()
            transf.setPos(0,0,-dz+(i+0.5)*dz/7.)
            
            self.addDaughter(theChamber,transf)	

class sector(volume):
    def __init__(self,type):
        volume.__init__(self,"sector")
        self.visible=False
        self.offset=8
        #type is O or S
        dx=6
        dy=40
        dz=14
        if(type=="S"):
            dx=4
        
        theSectorShape=box(dx,dy,dz)
        self.setShape(theSectorShape)

        if(type=="L"):
            #build 3 large layers
            theLayer1=layer("ML")
            theLayer1.name="layer1"
            theLayer2=layer("ML")
            theLayer2.name="layer2"
            theLayer3=layer("OL")
            theLayer3.name="layer3"
            transf1=transformation()
            transf2=transformation()
            transf3=transformation()
            transf1.setPos(0,3+3,0)
            transf2.setPos(0,3+3.5,0)
            transf3.setPos(0,3+5.6,0)

            self.addDaughter(theLayer1,transf1)
            self.addDaughter(theLayer2,transf2)
            self.addDaughter(theLayer3,transf3)

        if(type=="S"):
            #build 3 large layers
            theLayer1=layer("MS")
            theLayer1.name="layer1"
            theLayer2=layer("MS")
            theLayer2.name="layer2"
            theLayer3=layer("OS")
            theLayer3.name="layer3"
            theLayer1.id=100
            theLayer2.id=200
            theLayer3.id=300
            transf1=transformation()
            transf2=transformation()
            transf3=transformation()
            transf1.setPos(0,3+4.0,0)
            transf2.setPos(0,3+4.5,0)
            transf3.setPos(0,3+6.5,0)

            self.addDaughter(theLayer1,transf1)
            self.addDaughter(theLayer2,transf2)
            self.addDaughter(theLayer3,transf3)

    def goToStandAlone(self):
        # need special tuning of layers position if drawing in standAlone
        for l in self.daughters:
            l.trans.vector[1]=l.trans.vector[1]-self.offset

    def backFromStandAlone(self):
        # need special tuning of layers position if drawing in standAlone
        for l in self.daughters:
            l.trans.vector[1]=l.trans.vector[1]+self.offset

    def setVisible(self):
        pass

    def hideChildren(self):
        pass


class atlas(volume):

    def __init__(self):

        self.volDict=dict()
        volume.__init__(self,"atlas")
        self.visibile=False
        dx=4000
        dy=4000
        dz=4000
        theShape=box(dx,dy,dz)
        self.setShape(theShape)
        self.id=1

        for i in range(8):
            theSector1=sector("L")
            theSector1.name="sector"+str(2*i+1)
            theSector2=sector("S")
            theSector2.name="sector"+str((2*i+1)+1)
            theSector1.id=(2*i+1)*1000000
            theSector2.id=((2*i+1)+1)*1000000
            angle1=i*90/2.
            angle2=i*90/2+90/4.
            transf1=transformation()
            transf1.setPos(0,0,0)
            transf1.setRot(0,0,angle1)
            self.addDaughter(theSector1,transf1)
            transf2=transformation()
            transf2.setPos(0,0,0)
            transf2.setRot(0,0,angle2)
            self.addDaughter(theSector2,transf2)
            # now all daughters were added: can calculate IDs

        for sectorL in self.daughters:
            nsect=int(sectorL.name[6:])
            sectorL.id=nsect
            self.volDict[sectorL.id]=sectorL
            for layerL in sectorL.daughters:
                nlay=int(layerL.name[5:])
                layerL.id=nlay+sectorL.id*100
                # to be sure: better to hide childrens
                layerL.hideChildren()
                self.volDict[layerL.id]=layerL
                for chamber in layerL.daughters:
                    nch=int(chamber.name[7:])
                    chamber.id=nch+layerL.id*100
                    self.volDict[chamber.id]=chamber
                    for panels in chamber.daughters:
                        np=int(panels.name[5:])
                        panels.id=np+chamber.id*10
                        self.volDict[panels.id]=panels
        self.computeColor()
                    
    def setVisible(self):
        pass

    def hideChildren(self):
        pass
