import sys
import csv

totalArgs = len(sys.argv)
cmdArgs = sys.argv

if (totalArgs != 3):
	print "Usage : python genMatrix.py nodes.csv routes.csv\n    nodes.csv: the file of all hosts and switches\n    routes.csv: the file saving all routes"
	sys.exit()

nodeFileName = cmdArgs[1]
routeFileName = cmdArgs[2]

#print cmdArgs[0], cmdArgs[1], cmdArgs[2]
#print "Node File Name: ", nodeFileName
#print "Route File Name: ", routeFileName

try:
	with open(nodeFileName, 'rb') as nodesFile:
		nodes = nodesFile.read().split('\n')
		# print nodes
except IOError:
	print "Could not open file ", nodeFileName, ", please check the existence of file!"
	sys.exit()

#x = input("Press Enter to continue ...")

pLinks = []
try:
	with open(routeFileName, 'rb') as routesFile:
		routes = routesFile.read().split('\n')
		for route in routes:
			items = route.split(",")
			for i, item in enumerate(items):
				if i == 0:
					preItem = nodes.index(item.rstrip())
					pLink = str(preItem)
				else:
					if item.rstrip() in nodes:
						itemIdx = nodes.index(item.rstrip())
						pLink = pLink + "," + str(itemIdx)
						if pLink not in pLinks:
							pLinks.append(pLink)
						preItem = itemIdx
						pLink = str(preItem)

except IOError:
	print "Could not open file ", routeFileName, ", please check the existence of file!"
	sys.exit()		

for pLink in pLinks:
	print pLink

