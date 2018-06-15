# Load Shodan API
import shodan
import random
SHODAN_API_KEY = "KyoKnUyEq3QbaaicBRPHkhu0T0pYzyEx"
sapi = shodan.Shodan(SHODAN_API_KEY)

# Open the databases for analysis.
maxdb = open("City/cityv4.csv","r")
zipdb = open ("zipcodes/zipdb.csv","r")



# Let's try to make sure our city and state are strings.
city = "columbus"
state = "oh"

# Get a neat random number so our filenames are more or less unique
filerandomizer = random.randint(1,1000)
# Open a KML file to write to.
kmlout = open("kml/" + city + state + str(filerandomizer) + ".kml","w")
kmlout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n<Folder>\n<Document>")
kmlout.write("<Style id=\"downArrowIcon\">\n    <IconStyle>\n        <Icon>\n          <href>http://maps.google.com/mapfiles/kml/pal4/icon28.png</href>\n        </Icon>\n      </IconStyle>\n    </Style>")
print("\nFilename is " + city + state + str(filerandomizer) + ".kml\n")


print("Searching for IP addresses in " + city + "...\n")
usrzipcode = []
# We need to read each line from the zipcode database
for line in zipdb:
    current = zipdb.readline()
    # Now,  break each line of the csv file on the commas. This makes a list.
    currentlist = current.split(",")
    # Cities are held in the fourth list item and states in the fifth.
    # If the city list element matches the user's city input,
    # and at the same time, matches the user's state input,
    currentcity = currentlist[3].lower()
    currentcity = currentcity.replace('"','')
    currentstate = currentlist[4].lower()
    currentstate = currentstate.replace('"','')
    if currentcity == city:
        if currentstate == state:
            # We will add the zipcode to the list to process later.
            usrzipcode.append(currentlist[1].replace('"',''))
    else:
        pass


# Start a counter to list the number of lines read through the maxmind db.
count = 0
# Start a counter to list the number of lines read in the current city and zipcode.
ipcount = 0
# This will be our counter for the number of IPs that Shodan can see,
yescount = 0
# And this will be our counter for the number of IPs it cannot.
nocount = 0

# Let's read every line in the maxmind db.
for line in maxdb:
    current = maxdb.readline()
    # Break each line in the csv files on the commas.
    currentlist = current.split(",")
    # The maxmind zipcodes are held in the seventh. If the maxmind db entry matches the user's found zipcode from earlier,
    for i in range(len(usrzipcode)):
        if currentlist[6] == usrzipcode[i]:
            # If we get a match to our desired zipcode, let's count it as an ip we're interested in.
            ipcount += 1
            # Next, I'm going to map it with kml. Later, we'll cram everything into shodan as well.
            kmlout.write("<Placemark>\n")

            # Let's take the current IP we're looking at. It comes with a port number, but sapi.host() just wants an IP.
            current_ip_with_port = str(currentlist[0])
            # So unfuck that,
            ip_with_port_split_list = current_ip_with_port.split("/")
            # And take just the IP.
            current_ip = ip_with_port_split_list[0]
            # Before I throw it to Shodan, I'm going to finish the mapping tags in our kml file.
            kmlout.write("\n<name>" + str(current_ip) + "</name>\n")
            kmlout.write("\n<description>" + "Coordinates: " + str(currentlist[8]) + "," + str(currentlist[7] + "<br/>" + "Accuracy: " + str(currentlist[9]) + "</description>\n"))
            kmlout.write("<Point>\n<coordinates>" + str(currentlist[8]) + "," + str(currentlist[7]) + "</coordinates>\n</Point>")
            kmlout.write("</Placemark>")
            # And throw it at Shodan. We should wrap this up in a try/except, because if Shodan has no results
            # for a particular IP address, I don't want it to stop the program. Instead let's have it just
            # tell us that and we'll move on.
            try:
                current_result_shodan_host = sapi.host(current_ip)
                yescount += 1
                print("Shodan result found.")
                # Let's access the neat little dictionaries that Shodan spits out and take the useful information.
                # We're going to need to mark the location of our IP, so let's write a placemark starter to file.
                kmlout.write("<Placemark>\n    <styleUrl>#downArrowIcon</styleUrl>\n")
                for key,data in current_result_shodan_host.items():
                    if key == 'city':
                        current_city = data
                    elif key == 'region_code':
                        current_region = data
                    elif key == 'isp':
                        current_isp = data
                    elif key == 'ip_str':
                        current_ip = data
                    elif key == 'ports':
                        current_ports_available = data
                    elif key == 'latitude':
                        current_latitude = data
                    elif key == 'longitude':
                        current_longitude = data
                    elif key == 'module':
                        current_module = data
                    elif key == 'product':
                        current_product = data
                    elif key == 'os' and str(data).lower() != 'none':
                        current_os = data
                    else:
                        pass
                try:
                    # Let's label this point on the map with the IP address we're interested in.
                    kmlout.write("  <name>" + str(current_ip) + "</name>\n")
                except:
                    pass

                # We're going to start the description tag and end it later on. It's going to have whatever information
                # we do. This is what shows up in the balloon text.
                kmlout.write("  <description>")

                try:
                    kmlout.write("  City: " + str(current_city) + "<br/>")
                except:
                    pass
                try:
                    kmlout.write("  Region: " + str(current_region) + "<br/>")
                except:
                    pass            
                #try:
                #    try:
                #        str(current_isp).replace("&","&amp;")
                #    except:
                #        pass
                #    kmlout.write("  ISP: " + str(current_isp) + "<br/>")
                #except:
                #    pass
                try:
                    kmlout.write("  Open Ports: " + str(current_ports_available) + "<br/>")
                except:
                    pass
                try:
                    kmlout.write("  Product: " + str(current_product) + "<br/>")
                except:
                    pass
                try:
                    kmlout.write("  Module: " + str(current_module) + "<br/>")
                except:
                    pass
                try: kmlout.write(" OS: " + str(current_os) + "<br/>")
                except:
                    pass
                kmlout.write("  </description>\n")
                kmlout.write("  <Point>\n")
                kmlout.write("      <coordinates>" + str(current_longitude) + "," + str(current_latitude) + "</coordinates>\n")
                kmlout.write("  </Point>\n")
                kmlout.write("</Placemark>\n")
            except  shodan.APIError:
                nocount += 1
        # Otherwise,
        else:
            # We don't care about that entry in the maxmind database.
            pass
print("Of " + str(ipcount) + " IP addresses found in the zipcode(s) " + str(usrzipcode) + ", Shodan successfully queried " + str(yescount) + " addresses for information, and failed to query " + str(nocount) + " addresses.")
maxdb.close()
zipdb.close()
kmlout.write("</Document>\n</Folder>\n</kml>")
kmlout.close()