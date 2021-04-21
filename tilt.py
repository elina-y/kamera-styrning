#tilt går mellan 0 - -90 grader vertikalt

# R = avstånd mellan kamerorna
# S = kamerornas höjd från golvet
# pan1 och tilt1 bestäms av användaren
# B = avståndet från kameran till fokuspunkten
#VIKTIGT: skriv "import math" i main <3


#Beräkna
getB (S, tilt1):
B = (S - 1.6) / math.sin(tilt1)
return B

# Beräkna pan2
getPan2 (R, pan1, tilt1, B):
Rtak = B*math.cos(tilt1)
Ctak = math.sqrt((R^2) + (Rtak^2) - 2 * R * Rtak * math.cos(pan1))
pan2 = math.asin(Rtak * (math.sin(pan1) / Ctak))
return pan2

# Beräkna tilt2
getTilt2 (R, pan1, tilt1, B, S):
Rvagg = B*math.cos(pan1)
Cvagg = math.sqrt((R^2) + (Rvagg^2) - 2 * R * Rvagg * math.cos(tilt1))
tilt2 = math.asin(Rvagg * (math.sin(tilt1) / Cvagg))
if (tilt2 != 90):
    return tilt2
else():
    C90 = math.sqrt(B^2 - R^2)
    tilt2 = math.asin(S - C90)
