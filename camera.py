<<<<<<< HEAD
import requests
<<<<<<< HEAD
#import urllib3
#from requests.auth import HTTPBasicAuth
#from urllib.parse import urlencode

#http = urllib3.PoolManager()
#auth = urllib3.make_headers(HTTPBasicAuth('root','pass'))
#payload = {'inUserName': 'root','inUserPass':'pass'}
url = 'http://169.254.203.231/axis-cgi/com/ptz.cgi?query=position'

 #r = requests.get(url, auth=('root', 'pass'))
#r = requests.post(url,payload)
r = requests.get('http://169.254.203.231/axis-cgi/com/ptz.cgi?tilt=27')
req = requests.get(url)


#r = requests.post('http://169.254.203.231/axis-cgi/com/ptz.cgi?tilt=50')
print(req.text)
text = req.text
textarray = text.splitlines()
pan = float(textarray[0].split('=')[1])
tilt = float(textarray[1].split('=')[1])
test = 5+pan

if "tilt" in text:
    print ("tilt")

print (test)

#URL ="http://169.254.30.179/axis-cgi/com/ptz.cgi?query=position"
username = 'root'
password = 'pass'
#values = { 'username': username,'password': password }
#data = urllib.urlencode(values)
#req = urllib3.request(URL, data)
#response = urllib2.urlopen(req)
#result = response.read()
#r = requests.get(url,HTTPBasicAuth('root','pass'))
=======
import math
from decimal import Decimal
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

=======
>>>>>>> d5cf306478ae0923b76242712f44240ef861ffc2

<<<<<<< HEAD
=======

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
    Ctak = math.sqrt(((math.pow(R,2)) + ((math.pow(Rtak,2)) - 2 * R * Rtak * math.cos(pan1))))
    pan2 = math.degrees(math.asin(Rtak*(math.sin(pan1)/Ctak)))
    return str(pan2)

# Beräkna tilt2
def getTilt2 (R, pan1, tilt1, B, S):
    Rvagg = B*math.cos(pan1)
    Cvagg = math.sqrt((math.pow(R,2)) + (math.pow(Rvagg,2)) - 2 * R * Rvagg * math.cos(tilt1))
    tilt2 = math.degrees(math.asin(Rvagg * (math.sin(tilt1) / Cvagg)))
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
#Innan
def calibrate() :
    r1 =requests.get(urlcam1+"query=position")
    text1 = r1.text
    textarray = text.splitlines()
    pan10 = float(textarray[0].split('=')[1])
    tilt10 = float(textarray[1].split('=')[1])

    r2 =requests.get(urlcam2+"query=position")
    text1 = r2.text
    textarray = text.splitlines()
    pan20 = float(textarray[0].split('=')[1])
    tilt20 = float(textarray[1].split('=')[1])

S = 1.3
R = 0.12

calibrate()
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
>>>>>>> abc6c5edde5c1537e1a2eeb984a49965c672a64d
>>>>>>> 22172f015a561998fa0930e4c62947221a7346a2
