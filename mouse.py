import time    
import sys
from Quartz.CoreGraphics import * # imports all of the top-level symbols in the module

def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)
def mousemove(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx,posy);
def mouseclickdn(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
def mouseclickup(posx,posy):
    mouseEvent(kCGEventLeftMouseUp, posx,posy);
def mousedrag(posx,posy):
    mouseEvent(kCGEventLeftMouseDragged, posx,posy);

positions = []

def leftClickFunc(proxy, type, event, c):
    global positions
    point = CGEventGetLocation(event)
    print 'Left click', point.x, point.y, CGEventGetType(event)
    
    positions.append(point)
    if len(positions) == 2:
        outline_selection()
        positions = []
        
        
def outline_selection():
    
    x1 = int(positions[0].x)
    y1 = int(positions[0].y)
    
    x2 = int(positions[1].x)
    y2 = int(positions[1].y)
    
    step_count = 10
    if x2 > x1:
        steps = (x2-x1)/step_count + 1
    else:
        steps = (x2-x1)/step_count - 1
    
    print steps, x1,y1," ",x2,y2, range(x1, x2, steps)

    mouseclickup(x2,y2)
    time.sleep(0.05)
    mousemove(x1,y1)
    for x_d in xrange(x1, x2, steps):
        mousedrag(x_d,y1)
        time.sleep(0.05)
    
#    mousemove(posx,posy)
    
def rightClickFunc(proxy, type, event, c):
    point = CGEventGetLocation(event)
    print 'Right click', point.x, point.y, CGEventGetType(event)
    rl = CFRunLoopGetCurrent()
    CFRunLoopStop(rl);
    
tap = CGEventTapCreate(kCGHIDEventTap, kCGHeadInsertEventTap,
    kCGEventTapOptionListenOnly, (1 << kCGEventLeftMouseDown),
    leftClickFunc, None)
    
tap2 = CGEventTapCreate(kCGHIDEventTap, kCGHeadInsertEventTap,
    kCGEventTapOptionListenOnly, (1 << kCGEventRightMouseDown),
    rightClickFunc, None)

runLoopSource = CFMachPortCreateRunLoopSource(None, tap, 0);
runLoopSource2 = CFMachPortCreateRunLoopSource(None, tap2, 0);

CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, kCFRunLoopDefaultMode);
CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource2, kCFRunLoopDefaultMode);

CGEventTapEnable(tap, True);

print 'Startup'
CFRunLoopRun();
print 'After loop'