
import requests
import math
import sys
from decimal import Decimal
import urllib3
from requests.auth import HTTPDigestAuth

global pan1
global pan2
global tilt1
global tilt2
global R
global S
global B
global tilt20
global pan20
global tilt10
global pan10
global auth

#Testa med httpdigest. Har skapat en global vid namn auth för detta!

#tilt gar mellan 0 - -90 grader vertikalt

# R = avstand mellan kamerorna (m)
# S = kamerornas hojd från golvet (m)
# pan1 och tilt1 bestäms av användaren
# B = avstandet från kameran till fokuspunkten
#VIKTIGT: skriv "import math" i main <3



# MAC LILLA 00408CB977FF
# Mac STORA ACCC8ED91461
#ip för kamerorna
urlcam1 = 'http://169.254.203.231/axis-cgi/com/ptz.cgi?'
urlcam2 = 'http://169.254.135.93/axis-cgi/com/ptz.cgi?'
r=requests.get(url,auth=HTTPDigestAuth(’root’,’pass’))
auth = HTTPDigestAuth(’root’,’pass’)
#print(req.text)
#req = requests.get(urlcam1+"query=position")
#text = req.text
#textarray = text.splitlines()
#pan1 = float(textarray[0].split('=')[1])
#tilt1 = float(textarray[1].split('=')[1])
#Beräkna
def calibrate() :
    r1 =requests.get(urlcam1+"query=position",auth)
    text1 = r1.text
    textarray = text1.splitlines()
    #pan10 = float(textarray[0].split('=')[1])
    #tilt10 = float(textarray[1].split('=')[1])
    pan10 = -127.51
    pan20 = -126
    tilt10 = 0
    tilt20 = -6.2625
    r2 =requests.get(urlcam2+"query=position",auth)
    text2 = r2.text
    textarray2 = text2.splitlines()
    #pan20 = float(textarray2[0].split('=')[1])
    #tilt20 = float(textarray2[1].split('=')[1])
    print ("kamera 1: ","pan ",pan10," tilt ",tilt10,"kamera 2 ","pan ",pan20," tilt ",tilt20,)

    r = requests.get(urlcam1+"tilt="+str(tilt10))
    r = requests.get(urlcam1+"pan="+str(pan10))
    r = requests.get(urlcam2+"tilt="+str(tilt20))
    r = requests.get(urlcam2+"pan="+str(pan20))


def getB(S, tilt1):
    #B är längden till punkten vi vill kolla på, S höjden över golvet
    if tilt1 != 0:
        B = (S - 1.6) / math.sin(math.radians(tilt1))
    else:
            B = (S - 1.6)
    return B

# Beräkna pan2
def getPan2 (R, pan1, tilt1, B):
    Rtak = B*math.cos(math.radians(tilt1))
    Ctak = math.sqrt(((math.pow(R,2)) + ((math.pow(Rtak,2)) - 2 * R * Rtak * math.cos(math.radians(pan1)))))
    pan2 = math.degrees(math.asin(Rtak*(math.sin(math.radians(pan1))/Ctak)))
    return str(pan2)

# Beräkna tilt2
def getTilt2 (R, pan1, tilt1, B, S):
    Rvagg = B*math.cos(math.radians(pan1))
    Cvagg = math.sqrt((math.pow(R,2)) + (math.pow(Rvagg,2)) - 2 * R * Rvagg * math.cos(math.radians(tilt1)))
    tilt2 = math.degrees(math.asin(Rvagg * (math.sin(math.radians(tilt1)) / Cvagg)))-tilt20
    if (tilt2 != 90):
        return str(tilt2-tilt20)
    else:
        C90 = math.sqrt(B*B - R*R)
        tilt2 = math.degrees(math.asin(S - C90))
        return str(tilt2-tilt20)

def move() :
    r = requests.get(urlcam1+"tilt="+str(tilt1))
    r = requests.get(urlcam1+"pan="+str(pan1))
    r = requests.get(urlcam2+"tilt=-"+tilt2)
    r = requests.get(urlcam2+"pan=-"+pan2)
#Innan
#K1: pan 127.51, tilt 0. K2: pan -126, tilt -6.2625


S = 1.8
R = 1.2
pan10 = -127.51
pan20 = -126
tilt10 = 0
tilt20 = -6.2625

calibrate()

while 1!=0 :

    print("Bestäm pan")
    pan1 = input() #input ges i riktiga koordinater
    #pan1 = "120"

    print ("Bestäm tilt") #input exit om du vill stänga
    tilt1= input() #input ges i riktiga koordinater

    #tilt1 = "0"
    #if input() == "Calibrate":
    #    calibrate()

    print("du har valt "+pan1+" och "+ tilt1)
    pan1 = Decimal(pan1)
    tilt1 = Decimal(tilt1)
    #B = getB(S,tilt1)
    B=2

    virPan1=0
    if(pan10<0 && pan1<0){
        virPan1=math.abs(pan10)-math.abs(pan1)
    }
    if(pan10>0 && pan1>0){
        virPan1=math.abs(pan10)-math.abs(pan1)
    }
    if(pan10<0 && pan1>0){
        virPan1=math.abs(pan10)+math.abs(pan1)
    }
    if(pan10>0 && pan1<0){
        virPan1=-pan10+pan1
    }

    virPan2  = getPan2(R,virPan1,tilt1,B)

    #tilt2 = getTilt2(R,pan1,tilt1,B,S)
    #print(pan2, tilt2)
    print(virPan2)
    #move()
    continue
