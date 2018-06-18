# This file has a bunch of classes in it. Maybe I know what I'm doing.

import datetime, csv

# This function takes the city and state of interest as strings and initializes a kml file based on them.
# The filename will use the current time in hhmmss format. It returns the filename to use as a string.
# You MUST begin your program with this.
def kmlinit(city, state):
    print("Initializing output file...")
    city = city.lower()
    state = state.lower()
    # Get the current time
    time = datetime.datetime.now().time()
    # Change it into a string
    time = str(time)
    # Split it up...
    tlist = time.split(':')
    # Get rid of the milliseconds...
    seclist = tlist[2].split('.')
    # Format the filename.
    filename = "kml/" + city + state + tlist[0] + tlist[1] + seclist[0] + ".kml"
    print("The filename is " + str(filename) + ".")
    # Open a kml file to write to using the generated filename.
    kmlout = open(filename,"w")
    # Build the kml header.
    kmlout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n<Folder>\n<Document>")
    # Close the file.
    kmlout.close()
    # Return the filename.
    return filename

# This function closes the kml output file that you've been writing to after finishing it out a little bit.
# It takes the filename of interest as an argument. You MUST conclude your program with this.
def kmlkill(filename):
    print("Finishing output file " + filename + ".")
    kmlout = open(filename,'a')
    kmlout.write("</Document>\n</Folder>\n</kml>")
    kmlout.close()

# This function takes the names of the databses you have as strings, and then opens
# them to be read. It returns the databases themselves.
def dbcollect(zipfname, maxfname):
    print("Opening databases.")
    zipdb = open("zipcodes/" + zipfname + ".csv","r")
    maxdb = open("city/" + maxfname + ".csv","r")
    return zipdb,maxdb

# This function closes the database files.
def dbkill(zip, max):
    print("Closing databases.")
    zip.close()
    max.close()

# This function takes as arguments the kml filename as a string, the zipcode database, the maxmind database, and the city
# and state as a string. It accesses the databases using csv, cross-referencing them. It then generates kml to make a placemark.
def kmlPlace(zipdb, maxdb, filename, city, state):
    city = city.lower()
    state = state.lower()
    kmlout = open(filename,"a")
    zips = []
    count = 0
    for line in zipdb:
        count += 1
        zipline = zipdb.readline()
        zipsplit = zipline.split(',')
        zipcity = zipsplit[3].lower().replace('\"','')
        zipstate = zipsplit[4].lower().replace('\"','')
        if zipcity == city and zipstate == state:
            zips.append(zipsplit[1])
        else:
            pass
    cutzips = []
    for i in zips:
        if i not in cutzips:
            cutzips.append(i)
    for line in maxdb:
        maxline = maxdb.readline()
        maxsplit = maxline.split(',')
        for entry in cutzips:
            zipfixed = entry.lower().replace('\"','')
            if zipfixed == maxsplit[6]:
                latitude = maxsplit[7]
                longitude = maxsplit[8]
                address_rough = maxsplit[0]
                address_list = address_rough.split('/')
                address = address_list[0]
                port = address_list[1]
                accuracy = maxsplit[9]
                kmlout.write("\n<Placemark>")
                kmlout.write("\n<name>" + str(address) + "</name>\n")
                kmlout.write("\n<description>" + "Coordinates: " + str(longitude) + "," + str(latitude) + "<br/>" + "Accuracy: " + str(accuracy) + "Port: " + str(port) + " </description>\n")
                kmlout.write("<Point>\n<coordinates>" + str(longitude) + "," + str(latitude) + "</coordinates>\n</Point>")
                kmlout.write("</Placemark>")
            else:
                pass

