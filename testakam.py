import requests
import time
#import urllib3
#from requests.auth import HTTPBasicAuth
#from urllib.parse import urlencode

#http = urllib3.PoolManager()
#auth = urllib3.make_headers(HTTPBasicAuth('root','pass'))
#payload = {'inUserName': 'root','inUserPass':'pass'}
url = 'http://169.254.135.93/axis-cgi/com/ptz.cgi?query=position'

 #r = requests.get(url, auth=('root', 'pass'))
#r = requests.post(url,payload)
r = requests.get('http://169.254.135.93/axis-cgi/com/ptz.cgi?pan=-89')

time.sleep(2)



req = requests.get(url)


#r = requests.post('http://169.254.203.231/axis-cgi/com/ptz.cgi?tilt=50')
text = req.text
textarray = text.splitlines()
pan = float(textarray[0].split('=')[1])
tilt = float(textarray[1].split('=')[1])
test = 5+pan

if "tilt" in text:
    print ("tilt")

print (test)

#URL ="http://169.254.30.179/axis-cgi/com/ptz.cgi?query=position"
#username = 'root'
#password = 'pass'
#values = { 'username': username,'password': password }
#data = urllib.urlencode(values)
#req = urllib3.request(URL, data)
#response = urllib2.urlopen(req)
#result = response.read()
#r = requests.get(url,HTTPBasicAuth('root','pass'))
