# Import the libraries needed
import pygame
import math

pygame.init()

# Dimension of the paper with the empty map
paperwidth = 1434 // 3
paperheight = 1674 // 3
screen = pygame.display.set_mode([paperwidth, paperheight])

map = pygame.image.load("Map.png")
map = pygame.transform.scale(map, (paperwidth, paperheight))
startingX = 441
startingY = 277
origin = (startingX, startingY) #Starting point (SUN location)

# Convert the length of radial velocity line into image pixels
edgeX = 187
edgeY = 25
rvLength = pygame.Vector2(startingX - edgeX, startingY - edgeY).magnitude()
maxVelocity = 12_000

# Convert the angle of right ascension into angles in pi
minRA = 12
maxRA = 16
oneUnitRA = (math.pi / 2) / (maxRA - minRA)
angleOffset = (math.pi -  (math.pi / 2)) / 2

# Converts RA M and RA S into RA H
def totalRH(rh, rm, rs):
    return rh + rm / 60 + rs / 3600


# Converts angle and velocity into pixels, where top left of the window is (0, 0)
def getPointCoordinate(rh, rm, rs, v):
    ratioRV = v / maxVelocity
    rhTotal = totalRH(rh, rm, rs) # convert rh rm and rs all into one fractional rh
    initialAngle = (rhTotal - minRA) * oneUnitRA
    rotatedAngle = initialAngle + math.pi / 2 + angleOffset
    rotatedAngle = math.pi * 2 - rotatedAngle

    x = math.cos(rotatedAngle)
    y = math.sin(rotatedAngle)
    return origin + pygame.Vector2(x, y) * ratioRV * rvLength

#Draws the points on the screen
def printPoint(points):
    for point in points:
        pygame.draw.circle(map, pygame.Color("BLUE"), point, 2)

#Draw for all galaxy numbers in the data
def drawData(data):
    points = []
    for row in data:
        points.append(getPointCoordinate(row[0], row[1], row[2], row[3]))
    printPoint(points)

#Read the csv table data 
def readData():
    f = open(r"C:\Users\Samantha\Downloads\Lab_4_astr\table.csv")
    lines = f.readlines()
    f.close()
    #Start from row 4 to avoid the NA values in the table
    lines = lines[4:]
    lines = [line.replace("\n", "").split(',') for line in lines]  
    lines = [row[3:6] + [row[12]] for row in lines] 
    lines = [[float(i) for i in row] for row in lines]
    print(lines)
    return lines
rows = readData()

# Run program window
running = True
while running:
    # Run until close button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # White screen background color
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    screen.blit(map, (0, 0))

    drawData(rows)
    #print(pygame.mouse.get_pos()) To get original position on screen pixels

    # Flip the display
    pygame.display.flip()
pygame.quit()