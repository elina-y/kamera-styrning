import requests
urlcam1 = 'http://root.pass@169.254.203.231/axis-cgi/com/ptz.cgi?'
r = requests.get(urlcam1+"tilt="+"50")
r = requests.get(urlcam1+"pan="+"50")
print(r.text)
