import pygame as pg
import random
import time
pg.init()
# Game window
width = 1200
height = 800

screen = pg.display.set_mode((width, height))
pg.display.set_caption("shoot2")
bg = pg.image.load("41500.png")

# Character and objects
def character(x, direction):
    if direction > 0:
        avatar = pg.image.load("character.png")
    elif direction < 0:
        avatar = pg.image.load("character_left.png")
    screen.blit(avatar, [x, 550])

def ammo(x):

    ammo_img = pg.image.load("ammo.png")
    screen.blit(ammo_img, [x, 560])

def enemy(x):
    if x[0]>0:
        enemy=pg.image.load("reverse_enemy.png")
    else: 
        enemy=pg.image.load("enemy.png")
    screen.blit(enemy,[x[1],550])

# Helper functions
def move(speed, pose):
    global player_change_x, position
   

    player_change_x = speed
    position = pose

def boost_speed(speed):
    global player_change_x
    if pg.key.get_pressed()[pg.K_d]:
        player_change_x = speed
    elif pg.key.get_pressed()[pg.K_a]:
        player_change_x = -speed

def stop():
    global player_change_x
    player_change_x = 0

def fire():
    global ammo_list

    ammo_list = [ammo for ammo in ammo_list if abs(ammo[0])<screen.get_width()]
    
    if position > 0:
        ammo_list.append([position_x + 60,position])
    else:
         ammo_list.append([position_x - 30,position])

def spawn():
    if random.choice([-1,1]) > 0:
        enemy_list.append([1,screen.get_width()])
    else :
        enemy_list.append([-1,-100])

# Game variables
run = True
clock=pg.time.Clock()
position_x = screen.get_width() / 2
player_change_x = 0
velocity = 4
boost = 7
position = 1
ammo_speed = 15
ammo_list = []
enemy_hitpoint=2
enemy_speed=4
enemy_list=[]
spawn_time=1000
last_spawn_time=pg.time.get_ticks()
score=0

key_pressed = {
    pg.K_d: lambda: move(velocity, 1),
    pg.K_a: lambda: move(-velocity, -1),
    pg.K_LSHIFT: lambda: boost_speed(boost),
    "left click": fire
}

key_released = {
    pg.K_d: lambda: stop() if player_change_x > 0 else None,
    pg.K_a: lambda: stop() if player_change_x < 0 else None,
    pg.K_LSHIFT: lambda: boost_speed(velocity)
}

# Main loop
while run:
    screen.blit(bg, [0, 0])

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN and event.key in key_pressed:
            key_pressed[event.key]()
        elif event.type == pg.KEYUP and event.key in key_released:
            key_released[event.key]()
        elif event.type == pg.MOUSEBUTTONDOWN :
            if pg.mouse.get_pressed()[0]:
                key_pressed["left click"]()
            
    
            
    if position_x+60 > screen.get_width() or position_x < 0:
        if position_x <0 :
            position_x = 0
        else:
            position_x = screen.get_width() -60
    else:
        position_x += player_change_x
    
    character(position_x, position)
    
    # Update and render ammo
    for i in range(len(ammo_list)):
        if ammo_list[i][1] > 0:
            ammo_list[i][0] += ammo_speed
        elif ammo_list[i][1] < 0:
            ammo_list[i][0] -= ammo_speed
    
    for ammo_x in ammo_list:
        ammo(ammo_x[0])
        
    for i in range(len(enemy_list)):
        if enemy_list[i][0] > 0:
            enemy_list[i][1] -= enemy_speed
        elif enemy_list[i][0] < 0:
            enemy_list[i][1] += enemy_speed
      

    for i in enemy_list:
        enemy(i)
        if abs(position_x-i[1]) < 20:
            run=False
       
    current_spawn_time=pg.time.get_ticks()

    if current_spawn_time - last_spawn_time > spawn_time:
        spawn()
        last_spawn_time=current_spawn_time


    for i in ammo_list:
        for j in enemy_list:
            if abs(i[0]-j[1])<10:
                enemy_list.remove(j)
                ammo_list.remove(i)
                spawn_time-=2
                enemy_speed+=0.025
                score+=1
              
    pg.display.update()
    clock.tick(60)

pg.quit()
print(score)
 