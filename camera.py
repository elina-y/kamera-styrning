import requests
import math

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
    Ctak = math.sqrt((R^2) + (Rtak^2) - 2 * R * Rtak * math.cos(pan1))
    pan2 = math.asin(Rtak * (math.sin(pan1) / Ctak))
    return string(pan2)

# Beräkna tilt2
def getTilt2 (R, pan1, tilt1, B, S):
    Rvagg = B*math.cos(pan1)
    Cvagg = math.sqrt((R^2) + (Rvagg^2) - 2 * R * Rvagg * math.cos(tilt1))
    tilt2 = math.asin(Rvagg * (math.sin(tilt1) / Cvagg))
    if (tilt2 != 90):
        return string(tilt2)
    else:
        C90 = math.sqrt(B^2 - R^2)
        tilt2 = math.asin(S - C90)
        return string(tilt2)

while(true):
    pan1 = input()
    tilt1= input()
    B = getB(S,tilt2)
    pan2  = getPan2(R,pan1,tilt1,B)
    tilt2 = getTilt2(R,pan1,tilt1,B,S)
    
