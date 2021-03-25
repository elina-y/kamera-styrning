import requests
URL = "https://apkollen.se/api/v1?"

# location given here
category = "sprit"
price = "40,50"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'category':category , 'price': price}
#PARAMS = {'price': price}
#PARAMS = {'category':category}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
#r=requests.get(url=URL)

data = r.json()

# extracting latitude, longitude and formatted address
# of the first matching location
#latitude = data['results'][0]['geometry']['location']['lat']
#longitude = data['results'][0]['geometry']['location']['lng']
#formatted_address = data['results'][0]['formatted_address']

# printing the output
#print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
    #%(latitude, longitude,formatted_address))

print(data)
