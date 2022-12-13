from grids import Grid
import time, os, random
grid = Grid(' ')
#define grid
grid.CreateGrid(50, 30, '#')


class OLD_METHODE: #uses multithreading instead, more possibilities more easily but uses more system resources
    def show():
        while True:
            grid.ShowGrid()
            time.sleep(0.5)
            os.system('cls')


    def snow(X,fillChar = '*', XMOD = 0, YMOD=0):
        curX = X
        curY = grid.GRID_MAX_Y
        OLDPOS = (curX, curY)
        for x in range(curY+1):
            #grid.set(curX+(x*XMOD), curY-x)
            if x != 0:
                try:
                    grid.set(OLDPOS[0], OLDPOS[1]-1, "#") #cleaner
                except: break
            try:
                grid.set(curX, curY-1, fillChar) #-1 for last cleanup
            except: pass
            OLDPOS = (curX, curY)
            curY-=1
            curY+=YMOD
            curX+=XMOD
            time.sleep(0.5)

class LIGHTNING:
    def makeSchemePre(self, pos, Type):
        return ((pos), Type)
    
    def __init__(self, startPos, MinLen=3, MaxLen=4) -> None:
        self.genScheme = []
        self.curpos = 0
        self.retrieve = False
        self.didFlash = False
        self.flashed = 0
        lightLen = random.randint(MinLen, MaxLen)
        lastPos = startPos
        for x in range(lightLen):
            activity = random.randint(1, 5)
            lastPos = (lastPos[0], lastPos[1]-1)
            #add to right
            if activity == 1:
                lastPos = (lastPos[0]+1, lastPos[1])
                self.genScheme.append(self.makeSchemePre(lastPos, '\\'))
            elif activity == 2:
                lastPos = (lastPos[0]-1, lastPos[1])
                self.genScheme.append(self.makeSchemePre(lastPos, '/'))
            else:
                self.genScheme.append(self.makeSchemePre(lastPos, '|'))
                


def rain(XMOD=0, YMOD=-1, PARTICLE_CHAR="*", BACKGROUNDCHAR='#', waitTimer=0.5, PARTS=1, chance_lightning=100, lightning_maxlen=5, lightning_minlen=3, maxLightFlashes = 0):
    global grid
    #Not multithreaded so uses less resource 
    Curr_Particles = []
    lightnings = []
    while True:
        os.system('cls') #clears screen
        grid.ShowGrid()

        #Gens num, if correct it makes a lightning object
        ranNum = random.randint(0, chance_lightning)
        if ranNum == round(chance_lightning/2) and chance_lightning != 0:
            lightnings.append(LIGHTNING(((random.randint(0, grid.GRID_MAX_X)), grid.GRID_MAX_Y), MaxLen=lightning_maxlen, MinLen=lightning_minlen))
        
        #generates new particle
        for x in range(PARTS):
            Curr_Particles.append(((random.randint(0, grid.GRID_MAX_X)), grid.GRID_MAX_Y))
        pos = []
        #Removes old particles that already 'landed'
        for x in range(len(Curr_Particles)-1):
            if Curr_Particles[x][1] <= 0:
                pos.append(x)
        for x in pos:
            Curr_Particles.pop(x)
        
        #Creates new grid
        grid.CreateGrid(grid.GRID_MAX_X, grid.GRID_MAX_Y, BACKGROUNDCHAR)

        #gravity
        for x in range(len(Curr_Particles)-1):
            Curr_Particles[x] = (Curr_Particles[x][0]+XMOD,Curr_Particles[x][1]+YMOD)
        pos = 0
        for part in Curr_Particles:
            try:
                grid.set(part[0], part[1], PARTICLE_CHAR)
            except(IndexError):
                Curr_Particles.pop(pos)
            pos+=1

        #Creates lightning
        poS = 0
        for light in lightnings:
            if light.curpos >= len(light.genScheme) and light.flashed < maxLightFlashes and not light.didFlash:
                light.flashed +=1
                light.didFlash = True
            elif not light.retrieve:
                for x in range(light.curpos):
                    temp = light.genScheme[x]
                    pos = temp[0]
                    try:
                        grid.set(pos[0], pos[1], temp[1])
                    except(IndexError):
                        pass
            elif light.retrieve:
                for x in range(light.curpos):
                    temp = light.genScheme[x]
                    pos = temp[0]
                    try:
                        grid.set(pos[0], pos[1], temp[1])
                    except(IndexError):
                        pass
                light.curpos-=1
            light.didFlash = False
            if not light.retrieve:
                light.curpos+=1
            if light.curpos >= len(light.genScheme):
                light.retrieve = True
            if light.retrieve and light.curpos == 0:
                lightnings.pop(poS)
            #if light.curpos >= len(light.genScheme) and light.retrieve:
            #    lightnings.pop(poS)
            poS+=1
        time.sleep(waitTimer)
        





rain(XMOD=-1, PARTICLE_CHAR='.', waitTimer=0.08, PARTS=1, BACKGROUNDCHAR=' ', chance_lightning=10, lightning_maxlen=12, lightning_minlen=5, YMOD=-1, maxLightFlashes=3)

#Just an example ^^^
