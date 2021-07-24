import json , csv

def makeDB () :
    with open('humanList.json',) as readFile :
        data = json.load(readFile)
        with open('VotersLeft.csv', 'w') as writeFile :
            w = csv.writer(writeFile)
            for k in range(len(data)) :
                w.writerow([data[k].lower()])

def tryvote(adress) :
    members = '[\'' + adress.lower() + '\']'
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
    return ret