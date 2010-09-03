#!usr/bin/python
import urllib
import math
import sys
from PIL import Image

topleftx = 0
toplefty = 0
bottomrightx = 0
bottomrighty = 0
minwidth  = 0
minheight = 0
zoom = 0

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return(xtile, ytile)

def parseargs():
    state= ""
    global topleftx
    global toplefty
    global bottomrightx
    global bottomrighty
    global minwidth
    global minheight
    for arg in sys.argv:
        print arg
        if arg=="-min":
            state = "MINSIZE0"
        elif state=="MINSIZE0":
            minwidth = int(arg)
            state="MINSIZE1"
        elif state=="MINSIZE1":
            minheight= int(arg)
            state=""
        elif arg == "-rect":
            state="RECT0"
        elif state == "RECT0":
            topleftx=float(arg)
            state= "RECT1"
        elif state == "RECT1":
            toplefty=float(arg)
            state = "RECT2"
        elif state == "RECT2":
            bottomrightx = float(arg)
            state = "RECT3"
        elif state == "RECT3":
            bottomrighty = float(arg)
            state = ""

def calczoom():
    global zoom
    global topleft
    global bottomright
    global width
    global height
    for zoom in range(18):
        topleft = deg2num(topleftx, toplefty, zoom)
        bottomright = deg2num(bottomrightx, bottomrighty, zoom)
        width = abs(topleft[0]-bottomright[0])*256
        height = abs(topleft[1]-bottomright[1])*256
        if width>=minwidth and height>=minheight:
            break

def pulltile(zoom, x, y):
    global image
    global xcount
    global ycount
    url = "http://tile.openstreetmap.org/"+repr(zoom)+"/"+repr(x)+"/"+repr(y)+".png"
    #print "Pulling Tile "+ url
    tile = Image.open(urllib.urlretrieve(url)[0])
    #print "Putting it at "+repr(xcount*256)+ ", "+repr(ycount*256)
    image.paste(tile,(xcount*256,ycount*256))


parseargs()
calczoom()
#print "Zoom: ",zoom
xcount = 0
ycount = 0
width = abs((bottomright[0]-topleft[0])*256)
height = abs((topleft[1]-bottomright[1])*256)
print "Resulting Map will be "+repr(width)+"x"+repr(height)+"px"
image = Image.new("RGB", (width,height), "white")

print topleft[0], bottomright[0]
print  topleft[1],bottomright[1]
steps = (bottomright[0]-topleft[0])*(bottomright[1]-topleft[1])
ysteps = (bottomright[1]-topleft[1])
for x in range(topleft[0], bottomright[0]):
    for y in range(topleft[1],bottomright[1]):
        pulltile(zoom,x,y)
        ycount+=1
        print int((ysteps*xcount+ycount)/float(steps)*100),"% complete"
    ycount = 0
    xcount+=1
image.save("karte.png", "PNG")
    