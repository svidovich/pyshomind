import kmlgen
city = "columbus"
state = "oh"
zipfname = 'zipdb'
maxfname = 'cityv4'

# Initialize the output file
filename = kmlgen.kmlinit(city, state)

# Get the databases
zipdb,maxdb = kmlgen.dbcollect(zipfname, maxfname)

# Draw the output file
kmlgen.kmlPlace(zipdb, maxdb, filename, city, state)

# Close the database files
kmlgen.dbkill(zipdb,maxdb)

# Close the output file
kmlgen.kmlkill(filename)