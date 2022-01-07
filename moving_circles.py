import tkinter as tk
from enum import Enum
import math
    
class MovingCircles:
    class State(Enum):
        WAITING_FOR_FIRST = 1 #1st circle
        WAITING_FOR_SECOND = 2 #2nd circle
        WAITING_FOR_DRAG = 3  #Dragging action by user

    def __init__(self):
        # Creates the window
        self.state = self.State.WAITING_FOR_FIRST
        self.r = 20 #radius
        self.window = tk.Tk() 
        self.window.title("Moving Circles")

        self.canvas = tk.Canvas(self.window, width = 400, height = 400, bg = 'white') 
        self.canvas.grid(row = 1, column = 1)
        
        #Button frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.grid(row =2, column = 1)

        #Actual Buttons
        self.clear_button = tk.Button(self.button_frame,
                text = "Clear", command = self.clear)
        self.clear_button.grid(row = 1, column = 1)
        self.quit_button = tk.Button(self.button_frame,
                text = "Quit", command = self.quit)
        self.quit_button.grid(row = 1, column = 2)

        # Set up mouse click handlers for user
        self.canvas.bind("<ButtonRelease-1>", self.mouse_click_handler)
        self.window.mainloop()
    

    def mouse_click_handler(self, event):
        """ Creates two circles based on where the user clicks using his mouse. 
            Displays distance between the two circles as well as a line and its label """

        if self.state == self.State.WAITING_FOR_FIRST: #waiting for the first mouse  click to create 1st circle
            self.center_x_circle_one = event.x
            self.center_y_circle_one = event.y

            self.circle1 = self.canvas.create_oval(self.center_x_circle_one -
            self.r, self.center_y_circle_one - self.r,
            self.center_x_circle_one + self.r,
            self.center_y_circle_one + self.r,
            fill = "red", tags = "b1")

            self.state = self.State.WAITING_FOR_SECOND

        elif self.state == self.State.WAITING_FOR_SECOND: #waiting for the second mosue click to create 2nd circle
            self.center_x_circle_two = event.x
            self.center_y_circle_two = event.y

            self.circle2 = self.canvas.create_oval(self.center_x_circle_two -
            self.r, self.center_y_circle_two - self.r,
            self.center_x_circle_two + self.r,
            self.center_y_circle_two + self.r,
            fill = "red", tags = "b2")
            self.canvas.create_line(self.center_x_circle_one,
            self.center_y_circle_one,
            self.center_x_circle_two,
            self.center_y_circle_two,
            fill = "red", tags = "line")

            #calculates the distance between the two circles and displays it through a line
            self.distance = math.sqrt((self.center_x_circle_two-self.center_x_circle_one)**2 +
            (self.center_y_circle_two-self.center_y_circle_one)**2)

            self.center_x = (self.center_x_circle_two +
            self.center_x_circle_one) / 2
            self.center_y = (self.center_y_circle_two +
            self.center_y_circle_one) / 2
            self.canvas.create_text(self.center_x, self.center_y, text = f"{self.distance:.2f}", tags = "text")
            self.state = self.State.WAITING_FOR_DRAG

            #Binds mouse handler to C1 and C2 obects 
            self.canvas.tag_bind(self.circle1, "<B1-Motion>",
            self.mouse_handler1)
            self.canvas.tag_bind(self.circle2, "<B1-Motion>",
            self.mouse_handler2)

    def mouse_handler1(self,event):
        """
        This handles the new placement of circle 1 as well as the drag action.
        It changes the distance inbetween and updates it. 
        """
        #Handles/tracks the mouse movement in canvas
        self.delta_x = event.x - self.center_x_circle_one
        self.delta_y = event.y - self.center_y_circle_one
        self.canvas.move(self.circle1, self.delta_x, self.delta_y)


        #Line and text are deleted before new ones are added in
        self.canvas.delete("line") 
        self.canvas.delete("text")

        #Redraws/recreates the updated position and lines 
        self.canvas.create_line(event.x, event.y,
        self.center_x_circle_two,
        self.center_y_circle_two,
        fill = "red", tags = "line")

        #calculates new distance
        self.distance = math.sqrt((event.x-self.center_x_circle_two)**2 + 
        (event.y-self.center_y_circle_two)**2)

        self.center_x = (self.center_x_circle_two + event.x) / 2
        self.center_y = (self.center_y_circle_two + event.y) / 2
        
        self.canvas.create_text(self.center_x, self.center_y, 
        text = f"{self.distance:.2f}", tags = "text")
        self.canvas.update_idletasks()

        #updates the position of the circle to the mouse location (user chosen)
        self.center_x_circle_one = event.x
        self.center_y_circle_one = event.y

    def mouse_handler2(self,event):
        """ 
        This handles the new placement of circle 2 as well as the drag action.
        It changes the distance inbetween and updates it.
        """
        #Handles/tracks the mouse movement in canvas
        self.delta_x = event.x - self.center_x_circle_two
        self.delta_y = event.y - self.center_y_circle_two
        self.canvas.move(self.circle2, self.delta_x, self.delta_y)
        #Line and text are deleted before new ones are added in
        self.canvas.delete("line")
        self.canvas.delete("text")
        #Redraws/recreates the updated position and lines 
        self.canvas.create_line(self.center_x_circle_one,
        self.center_y_circle_one,
        event.x, event.y,
        fill = "red", tags = "line")
        
        #calculates new distance
        self.distance = math.sqrt((event.x-self.center_x_circle_one)**2 +
        (event.y-self.center_y_circle_one)**2)
        self.center_x = (self.center_x_circle_one + event.x) / 2
        self.center_y = (self.center_y_circle_one + event.y) / 2

        self.canvas.create_text(self.center_x, self.center_y, text = f"{self.distance:.2f}", tags = "text")
        self.canvas.update_idletasks()
        #updates the position of the circle to the mouse location (user chosen)
        self.center_x_circle_two = event.x
        self.center_y_circle_two = event.y

    def quit(self):
        """ Simply terminates the window/program """
        self.window.destroy()
    
    def clear(self):
        """
        Clears the simulation everytime that a new point is chosen by the users mouse
        so that is can start over
        """
        self.canvas.delete("b1")
        self.canvas.delete('b2')
        self.canvas.delete('line')
        self.canvas.delete('text') 
        self.state = self.State.WAITING_FOR_FIRST 

if __name__ == "__main__":
    MovingCircles()