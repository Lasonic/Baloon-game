# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 22:48:52 2020

@author: Pawel Mieszczanek
"""
from tkinter import *
from tkinter.ttk import *
import random
import time

class Player(object):
    
    def __init__(self):
        self.root = Tk()
        self.current_cannon_coords = [475,225]                                  # Centre of the cannon as [x,y] 
        self.current_target_coords = [30,235]                                   # Centre of the target as [x,y]
        self.current_bullet_coords = [0,0]                                      # Initiate bullet coords
        self.bullet_fired = False                                               # Bullet fired flag
        self.current_time = time.perf_counter()                                     # Current time
        self.missed_shots = [0]                                                 # 
        self.run_game = True                                                    # Run game flag
    
    
    
        self.window_init()                                                      # Create a window
        self.cannon_draw()                                                      # Create a cannon
        self.target_draw()                                                      # Create a target
        self.root.bind("<Up>",self.move_up)                                       # Assing Up arrow, down arrow and space key
        self.root.bind("<Down>",self.move_down)
        self.root.bind("<space>",self.shoot)
    
    def window_init(self):
        self.root.geometry("500x500")                                           # Main window size 
        self.frame = Frame(self.root)                                           # Create a frame
        self.frame.pack()                                                        
        self.C = Canvas(self.frame,bg = "yellow", height = 500, width = 500)    # Create a canvas    
        self.C.pack()        
        
    def cannon_draw(self):                                                      
        self.cannon = self.C.create_rectangle(self.current_cannon_coords[0]-25,self.current_cannon_coords[1]-25,self.current_cannon_coords[0]+25,self.current_cannon_coords[1]+25,fill="black",tags="cannon" )                   # Create a cannon
        self.C.pack()  
    
    def target_draw(self):
        self.target = self.C.create_oval(self.current_target_coords[0]-20,self.current_target_coords[1]-20,self.current_target_coords[0]+20,self.current_target_coords[1]+20,fill="red",tags="target")
        self.C.pack()
        
    def move_down(self,event):
    # Move down 10 pixels
        self.C.delete(self.cannon)
        self.current_cannon_coords[1] += 10
        self.cannon_draw()
        self.C.update()

    def move_up(self,event):
        # Move up 10 pixels
        self.C.delete(self.cannon)
        self.current_cannon_coords[1] -= 10
        self.cannon_draw()
        self.C.update()
    
    def update_target(self):
        self.C.delete(self.target)
        self.target_draw()
        self.C.update()
     
    def shoot(self,event):
        # Shoot a 5x5 pix bullet if no other bullets are fired
        if not self.bullet_fired:
            self.current_bullet_coords[0] = self.current_cannon_coords[0]-30
            self.current_bullet_coords[1] = self.current_cannon_coords[1]
            self.bullet = self.C.create_rectangle(self.current_bullet_coords[0]-5,self.current_bullet_coords[1]-5,self.current_bullet_coords[0]+5,self.current_bullet_coords[1]+5,fill="grey",tags="bullet" )
            self.bullet_fired = True
        
    def update_bullet(self):
        # Bullet moves 10 pixels at a time
        self.C.delete(self.bullet)
        self.current_bullet_coords[0] -= 10
        self.bullet = self.C.create_rectangle(self.current_bullet_coords[0]-5,self.current_bullet_coords[1]-5,self.current_bullet_coords[0]+5,self.current_bullet_coords[1]+5,fill="grey",tags="bullet" )
        self.C.update()
        
        
    def scoring(self):
        # If bullet is withing the current coords of the target, stop the game and display the score.
        # Otherwise, continue counting missed shots
        if self.bullet_fired:
            if (self.current_bullet_coords[0] - self.current_target_coords[0]) < 20 and ((self.current_bullet_coords[1] - self.current_target_coords[1]) < 20 and (self.current_bullet_coords[1] - self.current_target_coords[1]) > -20) :
                print('Target shot, you win!')
                self.C.delete(self.bullet)
                self.display_score()
                self.bullet_fired = False
                self.run_game = False
                
            elif self.current_bullet_coords[0] < 15:
                print('Target missed!')
                self.C.delete(self.bullet)
                self.bullet_fired = False
                self.missed_shots[0] += 1;                                 
    
    def display_score(self):
        self.str_to_disp = "You missed " + str(self.missed_shots[0]) + " shots"
        self.C.create_text(250,250,fill="darkblue",font="Times 20 bold",text="You missed " + str(self.missed_shots[0]) +" shots!")
        self.C.update() 

    def target_move(self):
        # Target moves up and down at random 10 ouxels at a time
        self.movement = random.randint(0,1)
        if self.movement == True and self.current_target_coords[1] < 450:
            self.current_target_coords[1] += 10
            self.update_target()
        elif self.movement == False and self.current_target_coords[1] > 50: 
            self.current_target_coords[1] -= 10
            self.update_target() 

def main():
    
     p1 = Player()
     tic_target = time.perf_counter()
     tic_bullet = tic_target
     while True:
         # Target moves every 0.1 seconds, 10 pixels at a time
         if time.perf_counter() - tic_target > 0.1 and p1.run_game == True:        
             p1.target_move()
             tic_target = time.perf_counter()
         # Bullet moves every 0.05 seconds, 10 pixels at a time    
         if p1.bullet_fired == True and time.perf_counter() - tic_bullet > 0.05 and p1.run_game == True:
             p1.update_bullet()
             tic_bullet = time.perf_counter()
         if p1.run_game == True:
             p1.scoring()
             p1.root.update()
         if p1.run_game == False:
             print("\nThe programm will close in 5 seconds...")
             p1.exit_message = "The program will close in 5 seconds... "
             p1.C.create_text(250,400,fill="darkblue",font="Times 12",text=p1.exit_message)
             p1.C.update()
             time.sleep(5)
             p1.root.destroy()
             break
             
if __name__ == '__main__':
     main()


#time.perf_counter

 