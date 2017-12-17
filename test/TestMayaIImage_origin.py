#!D:/Program Files/Autodesk/Maya2016/bin/mayapy.exe
# TestMayaIImage.py

import maya.standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds

import maya.OpenMaya as om 
import maya.cmds as cmds

# print cmds.file( f=True, new=True )

filename = "C:/Users/siras/Desktop/test_playblast/up.jpg"

# image = om.MImage()
# image.readFromFile(filename)
# pixels = image.pixels()
# image.release()

# print pixels

class MayaImage :
	"""
	The main class, needs to be constructed with a filename
	
	REF : https://jonmacey.blogspot.com/2011/04/using-maya-mscriptutil-class-in-python.html
	"""

	def __init__(self,filename) :
		""" constructor pass in the name of the file to load (absolute file name with path) """

		# create an MImage object
		self.image=om.MImage()

		# read from file MImage should handle errors for us so no need to check
		self.image.readFromFile(filename)

		# as the MImage class is a wrapper to the C++ module we need to access data
		# as pointers, to do this use the MScritUtil helpers
		self.scriptUtilWidth  = om.MScriptUtil()
		self.scriptUtilHeight = om.MScriptUtil()

		# first we create a pointer to an unsigned in for width and height
		widthPtr  = self.scriptUtilWidth.asUintPtr()
		heightPtr = self.scriptUtilHeight.asUintPtr()

		# now we set the values to 0 for each
		self.scriptUtilWidth.setUint( widthPtr, 0 )
		self.scriptUtilHeight.setUint( heightPtr, 0 )

		# now we call the MImage getSize method which needs the params passed as pointers
		# as it uses a pass by reference
		self.image.getSize( widthPtr, heightPtr )

		# once we get these values we need to convert them to int so use the helpers
		self.m_width  = self.scriptUtilWidth.getUint(widthPtr)
		self.m_height = self.scriptUtilHeight.getUint(heightPtr)

		# now we grab the pixel data and store
		self.charPixelPtr = self.image.pixels()

		# query to see if it's an RGB or RGBA image, this will be True or False
		self.m_hasAlpha = self.image.isRGBA()

		# if we are doing RGB we step into the image array in 3's
		# data is always packed as RGBA even if no alpha present
		self.imgStep = 4

		# finally create an empty script util and a pointer to the function
		# getUcharArrayItem function for speed
		scriptUtil = om.MScriptUtil()
		self.getUcharArrayItem =scriptUtil.getUcharArrayItem
  
	def width(self) :
		""" return the width of the image """
		return self.m_width
	 
	def height(self) :
		""" return the height of the image """
		return self.m_height
	 
	def hasAlpha(self) :
		""" return True is the image has an Alpha channel """
		return self.m_hasAlpha

	def getPixel(self,x,y) :
		""" get the pixel data at x,y and return a 3/4 tuple depending upon type """
		# check the bounds to make sure we are in the correct area
		if x<0 or x>self.m_width :
			print "error x out of bounds\n"
			return
		if y<0 or y>self.m_height :
			print "error y our of bounds\n"
			return
		# now calculate the index into the 1D array of data
		index=(y*self.m_width*4)+x*4
		# grab the pixels
		red 	= self.getUcharArrayItem(self.charPixelPtr,index)
		green 	= self.getUcharArrayItem(self.charPixelPtr,index+1)
		blue 	= self.getUcharArrayItem(self.charPixelPtr,index+2)
		alpha 	= self.getUcharArrayItem(self.charPixelPtr,index+3)
		return (red,green,blue,alpha)

if __name__ == '__main__':
	
	img=MayaImage(filename)
	print img.width()
	print img.height()
	xoffset = -img.width()/2
	yoffset = -img.height()/2
	 
	for y in range (0,img.height()) :
		for x in range(0,img.width()) :
			r,g,b,a=img.getPixel(x,y)

			print (y,x)
		# if r > 10 :
			# cmds.polyCube(h=float(r/10))
			# cmds.move(xoffset+x,float(r/10)/2,yoffset+y)