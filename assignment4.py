"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: <Your name>

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

from cProfile import run
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_Fac_num,q):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        car_Fac_num.acquire()
        
        while True:    
            getting = q.get()
            if getting  == MAX_QUEUE_SIZE:
                break
        pass


    def run(self,car_Fac_num,q, car_deal_num):
        for i in range(CARS_TO_PRODUCE):
            # TODO Add you code here
            q.size(10)
            q.put(i)
            car_Fac_num.release()
            car_deal_num.acquire()

        # signal the dealer that there there are not more cars
        pass


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self,q, car_deal_num):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
       
        for i in run:
            CARS_TO_PRODUCE        
        pass

    def run(self,q, car_deal_num, car_Fac_num):
        while True:
            # TODO Add your code here
            for i in range():
                 q.get(i)
                 car_Fac_num + 1
                 car_deal_num.release()



            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    # TODO Create queue251 
    # TODO Create lock(s) ?
    car_Fac_num = threading.Semaphore(0)
    car_deal_num = threading.Semaphore(0)

    q = Queue251()
    
    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    factor = Factory(q,car_Fac_num)
    # TODO create your one dealership
    deal = Dealer(q, car_Fac_num, car_deal_num)
    log.start_timer()

    # TODO Start factory and dealership
    factor.start()
    deal.start()
    # TODO Wait for factory and dealership to complete
    factor.join()
    deal.join()
    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
