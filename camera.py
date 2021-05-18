
import requests
import math
import sys
from decimal import Decimal
import urllib3
from requests.auth import HTTPDigestAuth

#global pan1
#global pan2
#global tilt1
#global tilt2

global auth


auth = HTTPDigestAuth('root','pass')


#tilt gar mellan 0 - -90 grader vertikalt

# R = avstand mellan kamerorna (m)
# h = kamerornas hojd från golvet (m)
# pan1 och tilt1 bestäms av användaren
# B = avstandet från kameran till fokuspunkten




# MAC LILLA 00408CB977FF
# Mac STORA ACCC8ED91461
#ip för kamerorna
urlcam1 = 'http://169.254.203.231/axis-cgi/com/ptz.cgi?'
urlcam2 = 'http://169.254.102.3/axis-cgi/com/ptz.cgi?'
#Beräkna

#Denna ska kopplas till calibrate-knappen och ersätta andra calib funken
def newCalibration() :
    q = "query=position"
    r1 = requests.get(urlcam1+q,auth=HTTPDigestAuth('root','pass'))
    r2 = requests.get(urlcam2+q,auth=HTTPDigestAuth('root','pass'))
    t1 = r1.text.splitlines()
    t2 = r2.text.splitlines()
    pan10 = float(t1[0].split('=')[1])
    tilt10 = float(t1[1].split('=')[1])
    pan20 = float(t2[0].split('=')[1])
    tilt20 = float(t2[1].split('=')[1])
    return (pan10,tilt10,pan20,tilt20)

def setPresets(height, spaceBetweenCameras):
    h = height
    R = spaceBetweenCameras
    personHeight = 0

def getVirtualPan(realPan,pan10):
    virPan1=0
    if pan10<0 and realPan<0:
        virPan1=math.fabs(pan10)-math.fabs(realPan)

    if pan10>0 and realPan>0 :
        virPan1=math.fabs(pan10)-math.fabs(realPan)

    if pan10<0 and realPan>0 :
        virPan1=math.fabs(pan10)+math.fabs(realPan)

    if pan10>0 and realPan<0 :
        virPan1=-pan10+realPan

    return virPan1

def tiltCameras(tilt, cameraNumber) :

    if (cameraNumber==1):
        print("Nu är jag i moveCameras")
        r = requests.get(urlcam1+"tilt=-"+str(tilt), auth=HTTPDigestAuth('root','pass'))
        #r = requests.get(urlcam1+"pan="+str(pan), auth=HTTPDigestAuth('root','pass'))
    #    moveothercam(virpan,tilt)
    else:
        r = requests.get(urlcam2+"tilt=-"+str(tilt), auth=HTTPDigestAuth('root','pass'))
        #r = requests.get(urlcam2+"pan="+str(pan), auth=HTTPDigestAuth('root','pass'))

def panCameras(pan, cameraNumber) :

    if (cameraNumber==1):
        #print("Nu är jag i moveCameras")
        #r = requests.get(urlcam1+"tilt=-"+str(tilt), auth=HTTPDigestAuth('root','pass'))
        r = requests.get(urlcam1+"pan="+str(pan), auth=HTTPDigestAuth('root','pass'))
    else:
        #r = requests.get(urlcam2+"tilt=-"+str(tilt), auth=HTTPDigestAuth('root','pass'))
        r = requests.get(urlcam2+"pan="+str(pan), auth=HTTPDigestAuth('root','pass'))

def getPositionCam1():
    r1 =requests.get(urlcam1+"query=position", auth=HTTPDigestAuth('root','pass'))
    text1 = r1.text
    textarray = text1.splitlines()
    pan = float(textarray[0].split('=')[1])
    tilt = math.fabs(float(textarray[1].split('=')[1]))
    return (pan,tilt)

#def calibrate() :
    #r1 =requests.get(urlcam1+"query=position")
    #text1 = r1.text
    #textarray = text1.splitlines()
    #pan10 = -127.51
    #pan20 = -126
    #tilt10 = 0
    #tilt20 = -6.2625
    #r2 =requests.get(urlcam2+"query=position")
    #text2 = r2.text
    #textarray2 = text2.splitlines()
    #print ("kamera 1: ","pan ",pan10," tilt ",tilt10,"kamera 2 ","pan ",pan20," tilt ",tilt20,)

    #r = requests.get(urlcam1+"tilt="+str(tilt10))
    #r = requests.get(urlcam1+"pan="+str(pan10))
    #r = requests.get(urlcam2+"tilt="+str(tilt20))
    #r = requests.get(urlcam2+"pan="+str(pan20))


def getB(h,tilt1, myPersonHeight):
    #B är längden till punkten vi vill kolla på, S höjden över golvet

    if tilt1 != 0:
        myB = (h - float(myPersonHeight)) / math.sin(math.radians(tilt1))
    else:
            myB = 4
    print("B",myB)

    return myB

# Beräkna pan2
def getPan2 (pan1, tilt1,R,B):
    Rtak = B*math.cos(math.radians(tilt1))
    Ctak = math.sqrt((math.pow(R,2)) + ((math.pow(Rtak,2)) - 2 * R * Rtak * math.cos(math.radians(pan1))))
    print("Ctak",Ctak)
    pan2 = math.asin(Rtak*(math.sin(math.radians(pan1))/Ctak))
    print("Rtak",Rtak)
    print("pan2", math.degrees(pan2))

    ss1=round(math.sin(math.radians(pan1))/Ctak,3)
    ss2=round(math.sin(pan2)/Rtak,3)
    ss3= round(math.sin(math.pi-math.radians(pan1)-pan2)/R,3)
    print("ss1",ss1,"ss2",ss2,"ss3",ss3)
    print("pan2",math.degrees(pan2))
    if pan1>90 or (ss1 == ss3) :
        return math.degrees(pan2)
    else:
        return 180-math.degrees(pan2)
# Beräkna tilt2

def getTilt2 (pan1, tilt1,R,B, h,personHeight):
    if(pan1>80 and pan1<100 ):
        Rvagg=B*math.sin(math.radians(tilt1))
        Cvagg=math.sqrt(math.pow((h-personHeight),2)+math.pow(R,2))
    elif(pan1>90 and pan1 < 135):
        Rvagg = B*math.cos(math.radians(pan1-90))
        Cvagg = math.sqrt((math.pow(R,2)) + (math.pow(Rvagg,2)) - 2 * R * Rvagg * math.cos(math.radians(180-tilt1)))

    else:
        Rvagg = B*math.cos(math.radians(pan1))
        Cvagg = math.sqrt((math.pow(R,2)) + (math.pow(Rvagg,2)) - 2 * R * Rvagg * math.cos(math.radians(tilt1)))
    print("Rvagg",Rvagg)
    print("Cvagg",Cvagg)

    tilt2 = math.degrees(math.asin(Rvagg * (math.sin(math.radians(tilt1)) / Cvagg)))
    print("tilt2 vid getTilt",tilt2)
    if (math.fabs(tilt2) <65):
        return tilt2
    else:
        print("hej")
        C90 = math.sqrt(B*B - R*R)
        print("C90",C90)
#        print("h-personHeight",h-personHeight)
        morot = (h-personHeight)/C90
        if (morot>1):
            return tilt2
        else:
            tilt2 = math.degrees(math.asin(morot))
            return tilt2


def move() :
    r = requests.get(urlcam2+"tilt=-"+str(tilt2), auth=HTTPDigestAuth('root','pass'))
    r = requests.get(urlcam2+"pan="+str(pan2), auth=HTTPDigestAuth('root','pass'))

#B=0
#h = 1.85
#R = 1.7
#personHeight=1.18
#pan10 = -127.51
#pan20 = -126
#tilt10 = 0
#tilt20 = -6.2625


#while 1!=0 :
#    r1 =requests.get(urlcam1+"query=position", auth=HTTPDigestAuth('root','pass'))
#    text1 = r1.text
#    pan1 = float(textarray[0].split('=')[1])
#    tilt1 = math.fabs(float(textarray[1].split('=')[1]))
#
#    B =  getB(h, tilt1, personHeight)
#
#    virPan1=0
#    if pan10<0 and pan1<0:
#        virPan1=math.fabs(pan10)-math.fabs(pan1)
#
#    if pan10>0 and pan1>0 :
#        virPan1=math.fabs(pan10)-math.fabs(pan1)
#
#    if pan10<0 and pan1>0 :
#        virPan1=math.fabs(pan10)+math.fabs(pan1)
#
#    if pan10>0 and pan1<0 :
#        virPan1=-pan10+pan1
#    print("B",B)
#    print("virpan1",virPan1)
#    virPan2  = getPan2(R,virPan1,tilt1,B)
#   print("tilt2",tilt2)
#    print("pan2",pan2)
#    move()
#    break
