# Open the databases for analysis.
maxdb = open("City/cityv4.csv","r")
zipdb = open ("zipcodes/zipdb.csv","r")

# Let's try to make sure our city and state are strings.
city = "las vegas"
state = "nv"



print("Searching for IP addresses in " + city + "...\n")
usrzipcode = []
# We need to read each line from the zipcode database
for line in zipdb:
    current = zipdb.readline()
    # Now,  break each line of the csv file on the commas. This makes a list.
    currentarray = current.split(",")
    # Cities are held in the fourth list item and states in the fifth.
    # If the city list element matches the user's city input,
    # and at the same time, matches the user's state input,
    currentcity = currentarray[3].lower()
    currentcity = currentcity.replace('"','')
    currentstate = currentarray[4].lower()
    currentstate = currentstate.replace('"','')
    if currentcity == city:
        if currentstate == state:
            # We will add the zipcode to the list to process later.
            usrzipcode.append(currentarray[1].replace('"',''))
    else:
        pass


# Start a counter to list the number of lines read through the maxmind db.
count = 0
# Start a counter to list the number of lines read in the current city and zipcode.
truecount = 0
# Let's read every line in the maxmind db.
for line in maxdb:
    current = maxdb.readline()
    # Break each line in the csv files on the commas.
    currentarray = current.split(",")
    # The maxmind zipcodes are held in the seventh. If the maxmind db entry matches the user's found zipcode from earlier,
    for i in range(len(usrzipcode)):
        if currentarray[6] == usrzipcode[i]:
            # We will print the correct values from the maxmind database.
            print("IP/Port: " + currentarray[0].replace("/",":") + "\nLatitude: " + currentarray[7] + "\nLongitude: " + currentarray[8] + "\nAccuracy (km): " + currentarray[9])
            # We read a line that matched our user's preference, so count.
            truecount = truecount + 1
        # Otherwise,
        else:
            # We don't care about that entry in the maxmind database.
            pass
    # Regardless, we read a line, so count.
    count = count + 1
print(str(count) + " lines read, " + str(truecount) + " " + city + " IP addresses found.")
maxdb.close()
zipdb.close()