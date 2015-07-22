from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
import csv
import easygui
import sys


def getAddressFrom(street1,street2,city,state,zip):
	return "{0} {1},{2},{3},{4}".format(street1,street2,city,state,zip)


input_path = easygui.fileopenbox(msg='Please open input csv file', title='Open File', default='~/Desktop/', filetypes=['*.csv','*.CSV'], multiple=False)

if(not input_path or input_path=='.'):
	sys.exit()

addresses = []
with open(input_path, 'rb') as csvfile:
	address_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	#skip first line
	address_reader.next()
	for row in address_reader:
		addresses.append(row)


print addresses

geolocator = GoogleV3()
homeAddress = "1200 N. Phillip's Ave,OKC,OK,73104"

homeLocation = geolocator.geocode(homeAddress);

output_lines = []
#add headers
output_lines.append(['ID','address','kilometers','meters','miles','feet','nautical miles'])
for address in addresses:
	remoteAddress1 = address[1]
	remoteAddress2 = address[2]
	remoteCity = address[3]
	remoteState = address[4]
	remoteZip = address[5]

	remoteLocation = geolocator.geocode(getAddressFrom(remoteAddress1,remoteAddress2,remoteCity,remoteState,remoteZip));

	d = vincenty((homeLocation.latitude,homeLocation.longitude), (remoteLocation.latitude,remoteLocation.longitude))
	line = [address[0],', '.join(address),d.km,d.m,d.mi,d.ft,d.nm]
	output_lines.append(line)

#write output

output_path = easygui.filesavebox(msg='Where would you like to save the output', title='Save output', default='~/Desktop/output.csv', filetypes=['*.csv'])
print output_path
if(not output_path or output_path=='.'):
	sys.exit()

with open(output_path, 'wb') as csvfile:
    distance_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for row in output_lines:
    	distance_writer.writerow(row)


sys.exit()


