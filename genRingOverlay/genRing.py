import sys
import numpy
import csv

from drawNetwork import *

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs < 2):
	print "Usage : python genRing.py serverCoords.csv\n    serverCoords.csv: the file of all coordinates\n"
	sys.exit()

coordsFileName = cmdArgs[1]

#print cmdArgs[0], cmdArgs[1], cmdArgs[2]
#print "Node File Name: ", nodeFileName
#print "Route File Name: ", routeFileName

try:
	with open(coordsFileName, 'rb') as coordsFile:
		nodes = coordsFile.read().split('\n')
		# print nodes
except IOError:
	print "Could not open file ", nodeFileName, ", please check the existence of file!"
	sys.exit()

#x = input("Press Enter to continue ...")

serverCoords = {}
servers = []
for server in nodes:
	items = server.split(",")
	if len(items) > 2:
		name = items[0]
		coords = (float(items[1]), float(items[2]))
		serverCoords.update({name:coords})
		servers.append(name)
	# else:
		# print "wrong dimension ", items

# print serverCoords

leftServers = servers
startServer = leftServers[0]
leftServers.remove(startServer)
curServer = startServer
overlayLinks = []

while leftServers:
	d = 100.0
	chosenServer = leftServers[0]
	curCoords = numpy.array(serverCoords.get(curServer))
	for candidate in leftServers:
		candidateCoords = numpy.array(serverCoords.get(candidate))
		dist = numpy.linalg.norm(curCoords - candidateCoords)
		if dist < d:
			d = dist
			chosenServer = candidate
	overlayLinks.append((curServer, chosenServer))
	print curServer, ", ", chosenServer
	curServer = chosenServer
	leftServers.remove(chosenServer)

overlayLinks.append((curServer, startServer))
# print overlayLinks
print curServer, ", ", startServer
	
draw_graph(overlayLinks, None, 'spring')
