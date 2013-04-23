"""THIS IS WORK IN PROGRESS.
Showcase of a spiderweb (drawing with pyglet)"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math

import pyglet
    
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pyglet_util import draw_space

window = pyglet.window.Window()
space = pymunk.Space()

space.gravity = 0,-900
space.damping = .999
print space.damping
c = Vec2d(window.width /2., window.height / 2.)
print "center", c

bs = []
dist = .3

cb = pymunk.Body(1,1)
cb.position = c
s = pymunk.Circle(cb, 1) # to have something to grab
space.add(cb, s)


#generate each crossing in the net
for x in range(0,101):
    b = pymunk.Body(1, 1)
    v = Vec2d.unit()
    v.angle_degrees = x*18
    print "angle", round(v.angle_degrees), 
    scale = window.height / 2. / 6. * .5
    
    dist += 1/18. 
    dist = dist ** 1.005
    
    offset = 0
    offset = [0.0, -0.80, -1.0, -0.80][((x*18) % 360)/18 % 4]
    offset = .8 + offset
    
    offset *= dist**2.8 / 100.
    
    print "offset", offset
    
    v.length = scale * (dist + offset) 
    
    b.position = c + v
    s = pymunk.Circle(b, 1)
    space.add(b,s)
    bs.append(b)
    
def add_joint(a,b):
    rl = a.position.get_distance(b.position) * 0.9
    stiffness = 5000.
    damping = 100
    j = pymunk.DampedSpring(a, b, (0,0), (0,0), rl, stiffness, damping)
    j.max_bias = 1000
    #j.max_force = 50000
    space.add(j)
    
for b in bs[:20]:
    add_joint(cb,b)
    
for i in range(len(bs)-1):
    add_joint(bs[i], bs[i+1])

    i2 = i+20
    if len(bs) > i2:
        add_joint(bs[i], bs[i2])   
    
#the attach points
static_bs = []
for b in bs[-17::4]:
    static_body = pymunk.Body()
    static_body.position = b.position
    static_bs.append(static_body)
    
    j = pymunk.PivotJoint(static_body, b, static_body.position)
    space.add(j)

def update(dt):
    # Note that we dont use dt as input into step. That is because the 
    # simulation will behave much better if the step size doesnt change 
    # between frames.
    r = 10
    for x in range(r):
        space.step(1./30./r)
    

pyglet.clock.schedule_interval(update, 1/30.)

selected = None
selected_joint = None
mouse_body = pymunk.Body()

@window.event
def on_mouse_press(x, y, button, modifiers):
    print "press", x,y
    mouse_body.position = x,y
    hit = space.nearest_point_query_nearest((x,y),10)
    if hit != None:
        global selected
        body = hit['shape'].body
        print "GOT ONE!", body
        rest_length = mouse_body.position.get_distance(body.position)
        print rest_length
        stiffness = 1000
        damping = 10
        selected = pymunk.DampedSpring(mouse_body, body, (0,0), (0,0), rest_length, stiffness, damping)
        space.add(selected)
        
@window.event
def on_mouse_release(x, y, button, modifiers):
    print "release", x,y
    global selected
    if selected != None:
        space.remove(selected)
        selected = None
    

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    mouse_body.position = x,y
    print x,y
    
@window.event
def on_draw():
    window.clear()
    pyglet.gl.glColor3f(1,1,1)
    a = []
    for b in bs:
        a += [b.position.x, b.position.y]
    pyglet.gl.glPointSize(4)
    pyglet.graphics.draw(len(a)/2, pyglet.gl.GL_POINTS, ('v2f',a))
    #pyglet.graphics.draw(len(a)/2, pyglet.gl.GL_LINE_STRIP, ('v2f',a))
    
    a = []
    for j in space.constraints:
        a += [j.a.position.x, j.a.position.y, j.b.position.x, j.b.position.y]
        pass
    
    pyglet.graphics.draw(len(a)/2, pyglet.gl.GL_LINES, ('v2f',a))
 
    
    for x in range(20):
        l = []
        for b in bs[x::20]:
            l += [b.position.x, b.position.y]
        #pyglet.graphics.draw(len(l)/2, pyglet.gl.GL_LINE_STRIP, ('v2f',l))
    a = []
    for x in range(5):
        v = Vec2d.unit()
        v.angle_degrees = x * 360 / 5
        v.length = 500
        v += c
        a += [c.x, c.y, v.x, v.y]
    
    #pyglet.graphics.draw(len(a), pyglet.gl.GL_LINES, ('v2f',a))
    
    pyglet.gl.glColor3f(1,0,1)
    pyglet.gl.glPointSize(6)
    a = []
    for b in static_bs:
        a += [b.position.x, b.position.y]
        pyglet.graphics.draw(len(a)/2, pyglet.gl.GL_POINTS, ('v2f',a))
    
        
pyglet.app.run()