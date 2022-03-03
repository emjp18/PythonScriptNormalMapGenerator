import sys
from typing import Literal
import PIL
import math
import PySide6.QtCore
from PIL import Image
from PySide6 import QtCore, QtWidgets, QtGui
def findL(rgb):
    #(0.299*R + 0.587*G + 0.114*B)
    #(0.2126*R + 0.7152*G + 0.0722*B)
    #sqrt( 0.299*R^2 + 0.587*G^2 + 0.114*B^2 )
    r = math.pow(rgb[0], 2)*0.299
    g = math.pow(rgb[1], 2)*0.587
    b = math.pow(rgb[2], 2)*0.114
    lum = math.sqrt(r+g+b)
    return lum

def floatToInteger(rgb):
        rgb[0] = max(0.0, min(1.0,rgb[0]))
        rgb[1] = max(0.0, min(1.0,rgb[1]))
        rgb[2] = max(0.5, min(1.0,rgb[2]))
        if rgb[0] == 1:
                rgb[0] = 255
        else:
                rgb[0] = math.floor(rgb[0]*256)
        if rgb[1] == 1:
                rgb[1] = 255
        else:
                rgb[1] = math.floor(rgb[1]*256)
        if rgb[2] == 1:
                rgb[2] = 255
        else:
                rgb[2] = math.floor(rgb[2]*256)
        return rgb

def findL1(rgb):
	high = -1
	low = 256
	for v in rgb:
		if v > high:
			high = v
		if v < low:
			low = v
	return ((high+low)/2)
def findL2(rgb):
    lum = rgb[0]+rgb[1]+rgb[2]
    lum/=3
    return lum
def normalize(rgb):
     if rgb[0]==rgb[1]==rgb[2]==0:
         return rgb
     else:
         m = math.sqrt((rgb[0]*rgb[0])+(rgb[1]*rgb[1])+(rgb[2]*rgb[2]))
         rgb[0] = rgb[0]*(1/m)
         rgb[1] = rgb[1]*(1/m)
         rgb[2] = rgb[2]*(1/m)
         return rgb

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.selectFile = QtWidgets.QPushButton("Select File to Convert")
        self.run = QtWidgets.QPushButton("CreateNormalTexture")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.run)
        self.layout.addWidget(self.selectFile)
        self.run.clicked.connect(self.convert)
        self.selectFile.clicked.connect(self.openFileDialog)
        self.path = ''
    def openFileDialog(self):
        self.fileDialogue = QtWidgets.QFileDialog()
        self.fileDialogue.setFileMode(QtWidgets.QFileDialog.AnyFile)
        self.fileDialogue.setNameFilter("Images (*.png *.jpg)")
        self.path = self.fileDialogue.getOpenFileName()
        
    def convert(self):
        #print(self.path[0])
        if self.path[0]=='':
            return
        im = Image.open(self.path[0])
        px = im.load()
        for w in range(im.width):
            for h in range(im.height):
                if w>0:
                    rgbLeft = px[w-1,h]
                else:
                    rgbLeft = px[w,h]
                if w < im.width-1:
                    rgbRight = px[w+1,h]
                else:
                    rgbRight = px[w,h]
                if h>0:
                    rgbUp = px[w,h-1]
                else:
                    rgbUp = px[w,h]
                if h < im.height-1:
                    rgbDown = px[w,h+1]
                else:
                    rgbDown = px[w,h]
                    
                if w>0 and h>0:
                    rgbTopLeft = px[w-1,h-1]
                elif w>0 and h == 0:
                    rgbTopLeft = px[w-1,h]
                elif w == 0 and h>0:
                    rgbTopLeft = px[w,h-1]
                else:
                    rgbTopLeft = px[w,h]
                if w > 0 and h < im.height-1:
                    rgbBottomLeft = px[w-1,h+1]
                elif w>0 and h == im.height-1:
                    rgbBottomLeft = px[w-1,h]
                elif w == 0 and h < im.height-1:
                    rgbBottomLeft = px[w,h+1]
                else:
                    rgbBottomLeft = px[w,h]
                if h > 0 and w < im.width-1:
                    rgbUpRight = px[w+1,h-1]
                elif h == 0 and w < im.width-1:
                    rgbUpRight = px[w+1,h]
                elif h > 0 and w == im.width-1:
                    rgbUpRight = px[w,h-1]
                else:
                    rgbUpRight = px[w,h]
                if h < im.height-1 and w < im.width-1:
                    rgbDownRight = px[w+1,h+1]
                elif h == im.height-1 and w < im.width-1:
                    rgbDownRight = px[w+1,h]
                elif h < im.height-1 and w == im.width-1:
                    rgbDownRight = px[w,h+1]
                else:
                    rgbDownRight = px[w,h]  
                rgbUpRightLum = findL(rgbUpRight)
                rgbRightLum = findL(rgbRight)
                rgbDownRightLum = findL(rgbDownRight)
                rgbTopLeftLum = findL(rgbTopLeft)
                rgbLeftLum = findL(rgbLeft)
                rgbBottomLeftLum = findL(rgbBottomLeft)
                rgbDownLum = findL(rgbDown)
                rgbUpLum = findL(rgbUp)
                r = (rgbUpRightLum + 2.0 * rgbRightLum + rgbDownRightLum) - (rgbTopLeftLum + 2.0 * rgbLeftLum + rgbBottomLeftLum)
                g = (rgbBottomLeftLum + 2.0 * rgbDownLum + rgbDownRightLum) - (rgbTopLeftLum + 2.0 * rgbUpLum + rgbUpRightLum)
                b = 1
                nRGB = [r, g, b]
                #nRGB = normalize(nRGB)
                rgb = floatToInteger(nRGB)
                rgbT = (rgb[0], rgb[1], rgb[2], 255)
                px[w,h] = rgbT
                
        im.save('converted.png')
             
app = QtWidgets.QApplication([])
widget = MyWidget()
widget.resize(800, 600)
widget.show()
sys.exit(app.exec())   
    