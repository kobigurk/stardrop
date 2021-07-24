import json , csv
from collections import namedtuple
from os import close

def makeDB () :
    imp = open('humanList.json',)
    data = json.load(imp)
    w = csv.writer(open('VotersLeft.csv', 'w'))
    for k in range(len(data)) :
        w.writerow([data[k]])
    imp.close()

def tryvote(adress) :
    members = '[\'' + adress + '\']'
    ret = False
    lines =  list()
    with open('VotersLeft.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if str(row) != str(members) :
                lines.append(row)
            else :
                ret = True
    if ret :
        with open('VotersLeft.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
            writeFile.close()
    readFile.close()
    return ret
