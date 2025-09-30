"""
TurtleAnimateLibrary is a library for generation and viewing of turtle based visualisations and animations
"""

# Imports
import turtle

# Turtle Shape Functions
# Level 1
def DrawPartialCircle(tur, r, percent):
    '''
    Draw a partial circle with radius r and percent of the circle to be drawn
    '''
    tur.circle(r, percent)

# Level 2
def DrawLeftDownSemiCircle(tur, r):
    '''
    Draw a left down semi circle with radius r
    '''
    tur.setheading(-90)
    DrawPartialCircle(tur, -r, 180)

def DrawRightUpSemiCircle(tur, r):
    '''
    Draw a right up semi circle with radius r
    '''
    tur.setheading(90)
    DrawPartialCircle(tur, -r, 180)

def DrawLeftUpSemiCircle(tur, r):
    '''
    Draw a left up semi circle with radius r
    '''
    tur.setheading(90)
    DrawPartialCircle(tur, r, 180)

def DrawRightDownSemiCircle(tur, r):
    '''
    Draw a right down semi circle with radius r
    '''
    tur.setheading(-90)
    DrawPartialCircle(tur, r, 180)

# List Visualisations
def List_TurtleValuePlot(values, titles=[""]):
    '''
    Visualise a list of values as a turtle plot
    '''
    if len(values) == 0:
        return

    tur = turtle.Turtle()
    wn = turtle.Screen()
    wn.title(titles[0])

    tur.setpos(0, values[0])
    for i in range(len(values[1:])):
        tur.goto(i+1, values[i])
    turtle.done()
    # tur.clear()

def List_TurtleValueAlternatingCurves(values, titles=[""], scale=1):
    '''
    Visualise a list of values as turtle curves alternating between up and down
    '''
    if len(values) == 0:
        return

    tur = turtle.Turtle()
    wn = turtle.Screen()
    wn.title(titles[0])
    
    tur.penup()
    tur.setpos(values[0], 0)
    tur.setheading(90)
    tur.pendown()

    altUpDir = True
    for i in range(1, len(values)):
        if values[i] >= values[i-1]:
            if altUpDir:
                DrawRightUpSemiCircle(tur, scale*(values[i]-values[i-1])/2)
            else:
                DrawRightDownSemiCircle(tur, scale*(values[i]-values[i-1])/2)
        else:
            if altUpDir:
                DrawLeftUpSemiCircle(tur, scale*(values[i-1]-values[i])/2)
            else:
                DrawLeftDownSemiCircle(tur, scale*(values[i-1]-values[i])/2)
        altUpDir = not altUpDir
    
    turtle.done()
    # tur.clear()

def List_TurtleValueFixedCurves(values, titles=[""], scale=1, leftDown=True, rightUp=True):
    '''
    Visualise a list of values as turtle curves with fixed directions
    '''
    if len(values) == 0:
        return

    tur = turtle.Turtle()
    wn = turtle.Screen()
    wn.title(titles[0])

    tur.penup()
    tur.setpos(values[0], 0)
    tur.setheading(90)
    tur.pendown()

    for i in range(1, len(values)):
        if values[i] >= values[i-1]:
            if rightUp:
                DrawRightUpSemiCircle(tur, scale*(values[i]-values[i-1])/2)
            else:
                DrawRightDownSemiCircle(tur, scale*(values[i]-values[i-1])/2)
        else:
            if leftDown:
                DrawLeftDownSemiCircle(tur, scale*(values[i-1]-values[i])/2)
            else:
                DrawLeftUpSemiCircle(tur, scale*(values[i-1]-values[i])/2)
    
    turtle.done()
    # tur.clear()