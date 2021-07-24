import json , csv


def try_vote(adress) :
    members = adress.lower()
    ret = False
    lines =  list()
    with open('humanList.json', 'r') as readFile:
        reader = json.load(readFile)
        for row in reader:
            if str(row) != str(members) :
                lines.append(row)
    if ret :
        with open('VotersLeft.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
    return ret