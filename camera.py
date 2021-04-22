import requests
import math
from decimal import Decimal
global pan1
global pan2
global tilt1
global tilt2
global R
global S
global B


#tilt gar mellan 0 - -90 grader vertikalt

# R = avstand mellan kamerorna (m)
# S = kamerornas hojd från golvet (m)
# pan1 och tilt1 bestäms av användaren
# B = avstandet från kameran till fokuspunkten
#VIKTIGT: skriv "import math" i main <3

#todo:
#1. fixa hämta ip automatiskt.
#2.

# MAC LILLA 00408CB977FF
# Mac STORA ACCC8ED91461

urlcam1 = 'http://169.254.203.231/axis-cgi/com/ptz.cgi?'
urlcam2 = 'http://169.254.135.93/axis-cgi/com/ptz.cgi?'

#print(req.text)
#req = requests.get(urlcam1+"query=position")
#text = req.text
#textarray = text.splitlines()
#pan1 = float(textarray[0].split('=')[1])
#tilt1 = float(textarray[1].split('=')[1])
#Beräkna
def getB(S, tilt1):
    B = (S - 1.6) / math.sin(tilt1)
    return B

# Beräkna pan2
def getPan2 (R, pan1, tilt1, B):
    Rtak = B*math.cos(tilt1)
    Ctak = math.sqrt((R*R) + (Rtak*Rtak) - 2 * R * Rtak * math.cos(pan1))
    pan2 = math.asin(Rtak * (math.sin(pan1) / Ctak))
    return str(pan2)

# Beräkna tilt2
def getTilt2 (R, pan1, tilt1, B, S):
    Rvagg = B*math.cos(pan1)
    Cvagg = math.sqrt((R*R) + (Rvagg*Rvagg) - 2 * R * Rvagg * math.cos(tilt1))
    tilt2 = math.asin(Rvagg * (math.sin(tilt1) / Cvagg))
    if (tilt2 != 90):
        return str(tilt2)
    else:
        C90 = math.sqrt(B*B - R*R)
        tilt2 = math.asin(S - C90)
        return str(tilt2)

def move() :
    r = requests.get(urlcam1+"tilt="+str(tilt1))
    r = requests.get(urlcam1+"pan="+str(pan1))
    r = requests.get(urlcam2+"tilt=-"+tilt2)
    r = requests.get(urlcam2+"pan=-"+pan2)

S = 1.3
R = 0.12
while 1!=0 :
    print("Bestäm pan")
    pan1 = input()
    #pan1 = "32"
    print ("Bestäm tilt")
    tilt1= input()
    #tilt1 = "64"
    print("du har valt "+pan1+" och "+ tilt1)
    pan1 = Decimal(pan1)
    tilt1 = Decimal(tilt1)
    B = getB(S,tilt1)
    pan2  = getPan2(R,pan1,tilt1,B)
    tilt2 = getTilt2(R,pan1,tilt1,B,S)
    move()
    continue
