import os
import time


def sendTable(listShip, tableResults, nbFights):

    table, maxi = addSum(tableResults)
    table2 = modifyTable(listShip, table)
    if 'TournamentResults' not in os.getcwd():
        os.chdir('../TournamentResults')

    day = time.strftime("%x")
    h = time.strftime("%H:%M")

    nbID = '0'
    nameFile = nbID + '_' + day[:2] + '-' + day[3:5] + '_' + h[:2] + '-' + h[3:5] + '.html'

    files = os.listdir()

    while nameFile in files:
        nbID = str(int(nbID)+1)
        nameFile = str(nbID) + '_' + nameFile[len(nbID)+1:]
    
    file = open(nameFile, "w")
    file.write(head(nameFile))
    file.write(body(table2, nbFights, maxi))
    file.write(bottom())
    file.write(paragraph(len(listShip), nbFights))

    file.close()
    os.chdir('..')


def addSum(table):
    tab = []
    listsum = []
    for l in table:
        nb = sum(l)
        tab += [l + [nb]]
        listsum += [nb]
    listsum.sort()
    listsum = listsum[-3:]
    print(listsum)
    return tab, listsum


def modifyTable(listShip, tableResults):

    table = [['X'] + ['<a href="../xmlShips/' + listShip[i] + '" target="_blank" >' + str(i+1) +
                      '</a>' for i in range(len(listShip))] + [' Victories Sum']]
    print(listShip, tableResults)
    for i in range(len(listShip)):
        table += [[]]
        table[i+1] = [str(i+1)+'_'+listShip[i]] + [nb for nb in tableResults[i]]
    return table


def head(date):
    return '<html lang="fr-FR"><head><meta charset="utf-8"> \n <link rel="stylesheet"  type="text/css" ' \
           ' media="screen" href="style.css" /> \n <title>Results' + date[:-4] + '</title> \n </head> \n <body>' \
           ' <h1>Tournament results </h1> '


def body(table, nbFights, maxi):

    bodyCode = '<table> \n'

    nbligne = 0
    for l in table:
        nbcase = 0

        bodyCode += '<tr> \n'

        if nbligne != 0:
            for c in l:
                if nbcase != 0:
                    if nbligne == nbcase:
                        bodyCode += '<td> X </td>'

                    elif nbcase == len(table):
                        if len(maxi)>=3:
                            if int(c) == maxi[2]:
                                bodyCode += '<td bgcolor="#CFC556">' + str(c) + '</td>'
                            elif int(c) == maxi[1]:
                                bodyCode += '<td bgcolor="#B5B5B5">' + str(c) + '</td>'
                            elif int(c) == maxi[0]:
                                bodyCode += '<td bgcolor="#AB8A41">' + str(c) + '</td>'
                            else:
                                bodyCode += '<td>' + str(c) + '</td>'
                        else:
                            bodyCode += '<td>' + str(c) + '</td>'
                    else:
                        if int(c) > 2*nbFights//3:
                            bodyCode += '<td bgcolor="#32A43B">' + str(c) + '</td>'
                        elif int(c) > nbFights//2:
                            bodyCode += '<td bgcolor="#B3D173">' + str(c) + '</td>'
                        else:
                            bodyCode += '<td bgcolor="#D1B873">' + str(c) + '</td>'
                else:
                    bodyCode += '<td>' + str(c) + '</td>'
                nbcase += 1
        else:
            for c in l:
                bodyCode += '<td>'
                bodyCode += str(c)
                bodyCode += '</td>'

        # print(l, c, nbcase, nbligne, )
        nbligne += 1

        bodyCode += '</tr> \n'

    bodyCode += '</table> \n'
    return bodyCode


def bottom():
    return '</body></html>'


def paragraph(n, nbF):
    return '<p>Tournament with '+str(n)+' ships with '+str(nbF)+' fights.</p>'


