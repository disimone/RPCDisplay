#!/usr/bin/python

if __name__ == '__build__':
        raise Exception

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import RPCDisplay

from random import random

import sys

ESCAPE = '\033'

window = 0

atlas=RPCDisplay.atlas()
atlas.visible=False

# set current volume to be deisplayed
currentVolume=atlas

mouseMode="r"
posx=0
posy=0
posz=-50
rotx=0
roty=0
lastx=0
lasty=0

selected=0

# set up a light 
lightOnePosition = (0, 100, 100.0, 0.0)
lightOneColor = (0.99, 0.99, 0.99, 1.0) 

lightTwoPosition = (0.0, -100, -100.0, 0.0)
lightTwoColor = (0.99, 0.99, 0.99, 1.0) 


def InitGL(Width, Height):                              # We call this right after our OpenGL window is created.

    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                                   # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                             # Enables Depth Testing
    glEnable(GL_LINE_SMOOTH)
    glShadeModel(GL_SMOOTH)                             # Enables Smooth Color Shading

    
#    # initialize lighting
#   glLightfv (GL_LIGHT0, GL_POSITION, lightOnePosition)
#   glLightfv (GL_LIGHT0, GL_DIFFUSE, lightOneColor)
#   glEnable (GL_LIGHT0)
#   glLightfv (GL_LIGHT1, GL_POSITION, lightTwoPosition)
#   glLightfv (GL_LIGHT1, GL_DIFFUSE, lightTwoColor)
#   glEnable (GL_LIGHT1)
#   glEnable (GL_LIGHTING)
#   glColorMaterial (GL_FRONT_AND_BACK, GL_DIFFUSE)
#   glEnable (GL_COLOR_MATERIAL)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                                    # Reset The Projection Matrix
                                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def ReSizeGLScene(Width, Height):
    if Height == 0:
            Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawOnClick():


# 	global atlas,posx,posy,posz,rotx,roty,currentVolume
#        glInitNames();
#	glPushName(0);
#
#	glMatrixMode(GL_PROJECTION);
#	
#        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);     # Clear The Screen And The Depth Buffer
#        glLoadIdentity();
#
#	transf=RPCDisplay.transformation()
#        glLoadIdentity();
#
#	transf.setRot(roty,rotx,0)
#	transf.setPos(posx,posy,posz)
#
#	currentVolume.setStandAlone(True)
#	currentVolume.setDisplayTrans(transf)
#	currentVolume.draw()
#

	global posx,posy,posz,rotx,roty,lastx,lasty,currentVolume

        viewport=glGetIntegerv(GL_VIEWPORT);
        glInitNames();
	glPushName(0);
	glMatrixMode(GL_PROJECTION);
	glPushMatrix()
	glLoadIdentity();

	gluPickMatrix(lastx, viewport[3]-lasty, 1., 1., viewport);

	gluPerspective(45.0, (viewport[2]-viewport[0])/(viewport[3]-viewport[1]), 0.1, 100.0);
	
	glMatrixMode(GL_MODELVIEW);

	transf=RPCDisplay.transformation()
        glLoadIdentity();
	currentVolume.setStandAlone(True)
	transf.setRot(roty,-rotx,0)
	transf.setPos(posx,posy,posz)

	currentVolume.setStandAlone(True)
	currentVolume.setDisplayTrans(transf)
	currentVolume.draw()
	
	glMatrixMode(GL_PROJECTION);
	
	glPopMatrix();

def DrawATLAS():

 	global atlas,posx,posy,posz,rotx,roty,currentVolume
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);     # Clear The Screen And The Depth Buffer
        glLoadIdentity();

	transf=RPCDisplay.transformation()
        glLoadIdentity();

	transf.setRot(roty,-rotx,0)
	transf.setPos(posx,posy,posz)

	currentVolume.setStandAlone(True)
	currentVolume.setDisplayTrans(transf)
	currentVolume.draw()

	glutSwapBuffers()

def switchVolume(vol):
	global rotx,roty,posx,posy,posz,lastx,lasty,currentVolume
	# reset display transf
	rotx=0
	roty=0
	posx=0
	posy=0
	posz=-20

	# tune posz depending on target volume
	if vol.name=="atlas":
		posz=-50
	elif vol.name[0:5]=="layer" or vol.name[0:6]=="sector":
		posz=-30
	elif vol.name[0:7]=="station":
		posz=-10
	elif vol.name[0:5]=="panel":
		posz=-5

	# display volume
	currentVolume.setStandAlone(False)
	# special action for layers: we always want to see the full sector
	if(vol.name[0:5]=="layer"):
		vol.mother.setStandAlone(True)
		currentVolume=vol.mother
	else:
		vol.setStandAlone(True)
		currentVolume=vol
		
	currentVolume.setVisible()

def keyPressed(*args):

    global mouseMode,rotx,roty,posx,posz,posy,selected,currentVolume

    if args[0] == "r" or args[0] == "z" or args[0] == "m":
	    mouseMode=args[0]
	    print "You are in ",mouseMode," mouseMode. Type c if you get lost.." 
    if args[0] == "c":
	    print "centering scene"
	    rotx=0
	    roty=0
	    posx=0
	    posy=0
	    posz=-50
	    glutPostRedisplay ()
    if(selected):
	    if args[0] == "d":
		    print "processing key d for selected ",selected
		    atlas.volDict[selected].showChildren()
		    # move selection to first daughter
		    if len( atlas.volDict[selected].daughters):
			    selected=atlas.volDict[selected].daughters[0].id
			    atlas.volDict[selected].select()
	    if args[0] == "u":
		    print "processing key u for selected ",selected
		    if(atlas.volDict[selected].standAlone):
			    switchVolume(atlas.volDict[selected].mother)
		    else:
			    atlas.volDict[selected].showMother()
			    # move selection to mother
		    selected=atlas.volDict[selected].mother.id
		    atlas.volDict[selected].select()
		    atlas.volDict[selected].hideChildren()

    if args[0]=="U":
	    print "moving UP the geom tree, from ",currentVolume.name," to ",currentVolume.mother.name
	    switchVolume(currentVolume.mother)
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
            sys.exit()


def MouseClick(button,state,x,y):
	import operator
	global lastx,lasty,selected
	
	lastx=x
	lasty=y
	if button == GLUT_LEFT_BUTTON and state ==  GLUT_UP  :
		result = glSelectWithCallback(x, y, DrawOnClick)
		if result and len(result)>1:
			# protect against unnamed objects
			result1=[x for x in result if len(x[2])==2]
			if len(result1):
				result1=sorted(result1,key=operator.itemgetter(1))
				if selected:  #change selection
					atlas.volDict[selected].unSelect()
				selected=result1[0][2][1]
				atlas.volDict[selected].select()
				# don't change selection if unnamed vol was selected
			
		else:
			if selected:
				# unselect selection, if any
				atlas.volDict[selected].unSelect()
			selected=0
			
	elif button == GLUT_RIGHT_BUTTON and state ==  GLUT_UP:
		print "right button pressed"
		result = glSelectWithCallback(x, y, DrawOnClick)
		if result and len(result)>1:
			# protect against unnamed objects
			result1=[x for x in result if len(x[2])==2]
			if len(result1):
				result1=sorted(result1,key=operator.itemgetter(1))
				if selected:  #change selection
					atlas.volDict[selected].unSelect()
				selected=result1[0][2][1]
				atlas.volDict[selected].select()
				switchVolume(atlas.volDict[selected])
		else:
			if selected:
				# unselect selection, if any
				atlas.volDict[selected].unSelect()
			selected=0
	viewport=glGetIntegerv(GL_VIEWPORT);
	ReSizeGLScene(viewport[2], viewport[3])
	
# get notified of mouse motions
def MouseMotion (x, y):
	global rotx, roty,posx,posy,posz,mouseMode,lastx,lasty
#	specialKey = glutGetModifiers();
#	print specialKey
	if mouseMode=="r":
		if lastx>x: rotx+=1
		else: rotx-=1
		if lasty<y: roty+=1
		else: roty-=1
	elif mouseMode=="m":
		if lastx<x: posx+=0.3
		else: posx-=0.3
		if lasty>y: posy+=0.3
		else: posy-=0.3
	elif mouseMode=="z":
		if lasty>y: posz+=0.3
		else: posz-=0.3
#	if specialKey==GLUT_ACTIVE_ALT:
#		if lastx<x: posx+=0.3
#		else: posx-=0.3
#		if lasty>y: posy+=0.3
#		else: posy-=0.3
#	elif specialKey==GLUT_ACTIVE_CTRL:
#		if lasty>y: posz+=0.3
#		else: posz-=0.3
#	else:
#		rotx = x
#		roty = y
	lastx=x
	lasty=y
	glutPostRedisplay ()


def main():

        global window
        glutInit(sys.argv)

        # Select type of Display mode:
        #  Double buffer
        #  RGBA color
        # Alpha components supported
        # Depth buffer
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        # get a 640 x 480 window
        glutInitWindowSize(640, 480)
        # the window starts at the upper left corner of the screen 
        glutInitWindowPosition(0, 0)
        # Okay, like the C version we retain the window id to use when closing, but for those of you new
        # to Python (like myself), remember this assignment would make the variable local and not global
        # if it weren't for the global declaration at the start of main.
        window = glutCreateWindow("AAD: Andrea's ATLAS Display")
        # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
        # set the function pointer and invoke a function to actually register the callback, otherwise it
        # would be very much like the C version of the code.

	glutDisplayFunc(DrawATLAS)
        glutMotionFunc(MouseMotion)
	glutMouseFunc(MouseClick)

        # Uncomment this line to get full screen.
        # glutFullScreen()
        # When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawATLAS)
        # Register the function called when our window is resized.
        glutReshapeFunc(ReSizeGLScene)
        
        # Register the function called when the keyboard is pressed
        glutKeyboardFunc(keyPressed)
        # Initialize our window. 

        InitGL(640, 480)
        # Start Event Processing Engine 
        glutMainLoop()
	
# Print message to console, and kick off the main to get it rolling.^M
print "Hit ESC key to quit."
main()
