#!/usr/bin/python

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.Tk import *

def select(event):
   result = glSelectWithCallback
   (event.x, event.y, renderPick)
   print str(result)
   if result and result[0][2]:
      if result[0][2][-1] == 0: print 'CUBE!'
      elif result[0][2][-1] == 1: print 'SPHERE!'
      else: print 'NOTHING!'

def renderPick():
   glPushName(0)
   drawCube()
   glPopName()
   glPushName(1)
   drawSphere()
   glPopName()

def drawCube():
   glPushMatrix()
   glTranslatef(-2.0, 0.0, 0.0)
   glMaterialfv(GL_FRONT, GL_AMBIENT,
   [0.1745, 0.0, 0.1, 0.0])
   glMaterialfv(GL_FRONT, GL_DIFFUSE,
   [0.6, 0.0, 0.1, 0.0])
   glMaterialfv(GL_FRONT, GL_SPECULAR,
   [0.7, 0.6, 0.8, 0.0])
   glutSolidCube(1)
   glPopMatrix()

def drawSphere():
   glPushMatrix()
   glTranslatef(2.0, 0.0, 0.0)
   glMaterialfv(GL_FRONT, GL_AMBIENT,
   [0.1745, 0.0, 0.1, 0.0])
   glMaterialfv(GL_FRONT, GL_DIFFUSE,
   [0.1, 0.0, 0.6, 0.0])
   glMaterialfv(GL_FRONT, GL_SPECULAR,
   [0.7, 0.6, 0.8, 0.0])
   glutSolidSphere(1, 35, 35)
   glPopMatrix()

def display(togl):
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glMaterialf(GL_FRONT, GL_SHININESS, 80)
   drawCube()
   drawSphere()
   glFlush()

togl = Opengl(width = 300, height = 200, double = 1)
togl.bind("<Control-Button-1>", select)
togl.redraw  = display
togl.pack(side = 'top', expand = 1, fill = 'both')
togl.basic_lighting()
togl.set_background(0, 0, 0)
togl.mainloop()
