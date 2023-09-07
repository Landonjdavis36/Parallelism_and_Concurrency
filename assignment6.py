"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Landon Davis
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime
from unicodedata import name

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, parent_connection, marble_count, creator_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.marble_count = marble_count
        self.parent_connection = parent_connection
        self.creator_delay = creator_delay
        
        print("this is marble creator __init__")
        
    def run(self):
        print("this is marble creator run")
        for i in range(self.marble_count):
            colors_size = len(self.colors)
            random_index = random.randint(0, colors_size-1)
            marble = self.colors[random_index]
            self.parent_connection.send(marble)
            time.sleep(self.creator_delay)
        self.parent_connection.send("END")
        self.parent_connection.close()

        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles       '''
        


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, when there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, child_connection, parent_connection, bag_count, bagger_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.child_connection = child_connection
        self.parent_connection = parent_connection
        self.count = 0
        self.bag_count = bag_count
        self.bagger_delay = bagger_delay

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while 1:
            bag = Bag()

            for i in range(0,self.bag_count):           # create a bag of bag_count = 7
                marble = self.child_connection.recv()
                bag.add(marble)

            #    
            print(bag.items)
            self.parent_connection.send(bag)            
            time.sleep(self.bagger_delay)
            self.count += 1
            print(f"sending bag n{self.count}")
            

            if marble == "END":
                self.parent_connection.send("END")
                self.parent_connection.close()  
                break   
            # print("Received the message: {}".format(marble))
            

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, child_connection, parent_connection, assembler_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.child_connection = child_connection
        self.parent_connection = parent_connection
        self.assembler_delay = assembler_delay

    def run(self):
        
        while 1:            

            bag = self.child_connection.recv()
            #print(f"receiving bag {bag.items}")

            random_index = random.randint(0, len(self.marble_names)-1)
            large_marble = self.marble_names[random_index]
            gift = Gift(large_marble, bag) 

            # self.parent_connection.send(gift)            
            time.sleep(self.assembler_delay)          
            

            if bag == "END":
                self.parent_connection.send("END")
                self.parent_connection.close()  
                break   
        
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, child_connection, filename, wrapper_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.child_connection = child_connection
        self.filename = filename
        self.wrapper_delay = wrapper_delay

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        while 1:
            gift = self.child_connection.recv()
            f = open(self.filename, "w")
            if gift == "END":
                f.close()
                break  

            f.write(f"Created - {datetime.now().time()}: Large marble: {gift.large_marble}, marbles: {gift.marbles}")
            

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_parent, creator_child = mp.Pipe()        # to be used for the communication between the Marble creator and the Bagger
    bagger_parent, bagger_child = mp.Pipe()          # to be used for the communication between the Bagger and the Assembler
    assembler_parent, assembler_child= mp.Pipe()   # to be used for the communication between the Assembler and the Wrapper

    # TODO create variable to be used to count the number of gifts

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    creator_process = Marble_Creator(creator_parent, settings[MARBLE_COUNT], settings[CREATOR_DELAY])
    bagger_process = Bagger(creator_child, bagger_parent, settings[BAG_COUNT], settings[BAGGER_DELAY])
    assembler_process = Assembler(bagger_child, assembler_parent, settings[ASSEMBLER_DELAY])
    wrapper_process = Wrapper(assembler_child, BOXES_FILENAME, settings[WRAPPER_DELAY])

    log.write('Starting the processes')
    creator_process.start()
    bagger_process.start()
    assembler_process.start()
    wrapper_process.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    creator_process.join()
    bagger_process.join()
    assembler_process.join()
    wrapper_process.join()

    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.



if __name__ == '__main__':
    main()

list = []

for i in range(0,7):
    list.append(i)