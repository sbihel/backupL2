from tkinter import *
import os

def findColor(rate):
    if rate == 100:
        return "#C3C3C3"
    elif rate >=90:
        return "#CAB8B8"
    elif rate >=80:
        return "#D4ADAD"
    elif rate >=70:
        return "#DB9F9F"
    elif rate >=60:
        return "#E19191"
    elif rate >=50:
        return "#E98080"
    elif rate >= 40:
        return "#EC6565"
    elif rate >= 30:
        return "#F35050"
    elif rate >=20:
        return "#F73A3A"
    elif rate >=10:
        return "#F91D1D"
    else:
        return "#DB1111"
    


def displayShipTK(ship, weapon, drone, room):

    tk = Tk()

    if 'xmlShips' in os.getcwd():
        os.chdir('..')
    
    can = Canvas(tk, bg='black', width=600, height=500)
    can.pack()

    typeShip = ship.getType()
    nameShip = ship.getName()
        
    tk.title("Ship " +nameShip + ' ' + typeShip + ' ' + str(ship.getID()))

    # print(os.getcwd())

    wall = PhotoImage(file="pictures/fond2.gif")
    fire = PhotoImage(file="pictures/fire.gif")
    can.create_image((0, 0), image=wall)

    
    sprite = PhotoImage(file="pictures/shipsSprites/" + nameShip + ".gif")
    xsprite, ysprite = 0, 0
    
    if nameShip == 'kestrel' and typeShip == 'typeB':
        ysprite += 15
    elif nameShip == 'engiCruiser' :
        xsprite -= 75
    
    can.create_image((260 + xsprite, 140 + ysprite), image=sprite)

    m = 50  # margin
    c = 3  # coefficient
    
    nbf = 120

    # Display rooms and systems in them
    for r in ship.getRooms():
        c1, c2 = r.getCoords()
        oxyrate = r.getOxygen()
        coloroxy = findColor(oxyrate)
        can.create_rectangle(c1[0]*c + m, c1[1]*c + m, c2[0]*c + m, c2[1]*c + m, fill=coloroxy, outline="black")
        system = r.getSystem()
        cm1, cm2 = c1[0], c1[1]

        if r.getNB() == room:
            r.getCoords()
            #can.create_oval(c1[0]*c + m, c1[1]*c + m, c2[0]*c + m, c2[1]*c + m, fill='red')
            locals()['img20' + str(r.getNB())] = PhotoImage(file="pictures/cible.gif").subsample(3, 3)
            can.create_image((cm1*c + m + 15, cm2*c + m + 15), image=locals()['img20'+str(r.getNB())])

        if r.getFire():
            print("Fire")
            locals()['img' + str(nbf)] = PhotoImage(file="pictures/fire.gif")
            can.create_image((cm1*c + m + 15, cm2*c + m + 15), image=locals()['img'+str(nbf)])
            nbf += 1

        if system != False :

            locals()['img' + str(r.getNB())] = PhotoImage(file="pictures/systems/"+str(system)+".gif").subsample(5, 5)
            
            if c2[0] - c1[0] != 10:
                cm1 += 5
            if c2[1] - c1[1] != 10:
                cm2 += 5
            can.create_image((cm1*c + m + 15, cm2*c + m + 15), image=locals()['img'+str(r.getNB())])
            
        

    # Basic coords for the statistics for the ship
    c1, c2 = 50, 250
    nb = 20  # Increment for the for

    # Display the stats
    for s in ship.getSystems():
        locals()['img' + str(nb)] = PhotoImage(file="pictures/systems/"+s.getName()+".gif").subsample(5, 5)
        can.create_image((c1, c2 + (nb-20)*20), image=locals()['img'+str(nb)])
        nb += 1
        
        maxPower = s.getCurrentMaxPower()
        ionPower = s.getPowerIonised()
        inItPower = s.getPowerInIt()
        for i in range(maxPower):
            if i >= (maxPower - ionPower):
                can.create_rectangle(c1 + 10 + i*15, c2 + ((nb-20)*20)-25, c1+20+i*15, c2 + ((nb-20)*20)-15,
                                         fill="blue", outline="black")
            else:
                can.create_rectangle(c1 + 10 + i*15, c2 + ((nb-20)*20)-25, c1+20+i*15, c2 + ((nb-20)*20)-15,
                                         fill="white", outline="black")
        for i in range( inItPower - ionPower):
            can.create_rectangle(c1 + 10 + i*15, c2 + ((nb-20)*20)-25, c1+20+i*15, c2 + ((nb-20)*20)-15,
                                     fill="green", outline="black")

        if s.getName() == 'weaponControl':  # Save sur weapon system in sysweap
            sysweap = s
        if s.getName() == 'droneControl':  # Save sur weapon system in sysweap
            sysdrone = s

    # Display weapons
    lw = sysweap.getWeapons()
    for weap in range(len(lw)):
        # One place for every weapons
        w = lw[weap]
        if weap == 0:
            wx, wy = 300, 300
            wx, wy = 300, 300
        elif weap == 1:
            wx, wy = 300, 400
        elif weap == 2:
            wx, wy = 400, 300
        else:
            wx, wy = 400, 400
        if w == weapon:
                can.create_oval(wx-30, wy-30, wx+30, wy+30, fill='green')
                can.create_oval(wx-20, wy-20, wx+20, wy+20, fill='black')

        # print(lw[weap].getName())
        locals()['img' + str(nb)] = PhotoImage(file="pictures/weapons/"+lw[weap].getName()+".gif")
        can.create_image(wx, wy, image=locals()['img'+str(nb)])
        nb += 1

    # Display drones
    if ship.hasSystem('droneControl'):
        ld = sysdrone.getDrones()
        for dr in range(len(ld)):
            # One place for every weapons
            if dr == 0:
                wx, wy = 500, 300
            elif dr == 1:
                wx, wy = 500, 400
            elif dr == 2:
                wx, wy = 600, 300
            else:
                wx, wy = 600, 400
            if dr == drone:
                can.create_oval(wx-30, wy-30, wx+30, wy+30, fill='green')

            # print(ld[drone].getName())
            locals()['img' + str(nb)] = PhotoImage(file="pictures/drones/"+ld[dr].getName()+".gif")
            can.create_image(wx, wy, image=locals()['img'+str(nb)])
            nb += 1
    else:
        can.create_text((550, 350), text='No drones', fill='green', width=40)

    # Display the doors
    doors = ship.getDoors()
    for d in doors:
        coords = d.getPosition()
        if str(coords[0])[-1] == '5':
            x1, y1, x2, y2 = coords[0]-2, coords[1], coords[0]+2, coords[1]
        else:
            x1, y1, x2, y2 = coords[0], coords[1]-2, coords[0], coords[1]+2
        can.create_line(x1*c+m, y1*c+m, x2*c+m, y2*c+m, fill="red", width=3)

    # Display crew
    for crew in ship.getCrew():
        race = crew.getRace()
        x, y = crew.getPosition()

        locals()['img' + str(nb)] = PhotoImage(file="pictures/crew/"+race+".gif").subsample(3, 3)
        can.create_image(x*c+m, y*c+m, image=locals()['img'+str(nb)])
        nb += 1

    HP = ship.getHP()
    can.create_rectangle(10, 10, 20+30*15, 30, fill='red')
    can.create_rectangle(10, 10, 20+HP*15, 30, fill='green')

    can.update()
    nbID = '0'

    nameFile = ship.getName()+'-' + ship.getType() + '-' + str(ship.getID()) + '-00000'

    os.chdir('ps')
    files = os.listdir()

    while nameFile+'.ps' in files:
        oldNBID = str(nbID)[:]
        nbID = int(nbID)+1
        nameFile = nameFile[:-5] + "%05d" % (nbID,)

    
    can.postscript(file=nameFile+'.ps', colormode='color')
    os.chdir('..')

    tk.quit()
    tk.destroy()
    # tk.mainloop()


def quitter(self):
    self.quit()
    self.destroy()


