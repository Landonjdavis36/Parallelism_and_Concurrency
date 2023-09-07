"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: Landon Davis

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
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

        # Display the car that has was just created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, cars_q, slots_at_dealership, cars_available_in_factory, barrier, n_factory, cars_created, n_dealerships):
        threading.Thread.__init__(self)
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        self.cars_q = cars_q
        self.slots_at_dealership = slots_at_dealership
        self.cars_available_in_factory = cars_available_in_factory
        self.barrier = barrier
        self.n_factory = n_factory 
        self.cars_created = cars_created
        self.n_dealerships = n_dealerships
    


    def run(self):
        # TODO produce the cars, then send them to the dealerships

        # TODO wait until all of the factories are finished producing cars

        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        
        for i in range(self.cars_to_produce+1):
            
            # Check to see if there are slots in at the dealership
            self.slots_at_dealership.acquire()
            new_car = Car()
            self.cars_q.put(new_car)
            print("Creating a car")
            

            # signal the dealer that there is a car on the queue
            self.cars_available_in_factory.release() 


        # signal the dealer that there there are not more cars
        for _ in range(self.n_dealerships):
            self.cars_q.put("No more cars")        
              
        self.barrier.wait()
        self.cars_available_in_factory.release()

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, cars_q, slots_at_dealership, cars_available_in_factory, queue_stats, lock, sold_cars, n_dealer, barrier):
        threading.Thread.__init__(self)
        self.cars_q = cars_q
        self.slots_at_dealership = slots_at_dealership
        self.cars_available_in_factory = cars_available_in_factory
        self.queue_stats = queue_stats
        self.lock = lock
        self.sold_cars = sold_cars
        self.n_dealer = n_dealer
        self.barrier = barrier

    def run(self):
        while True:
            # TODO handle a car
            
            with self.lock:
                # Check to see if anything is in the factory
                self.cars_available_in_factory.acquire()

                # Update queue_stats for our plot
                # self.queue_stats[self.cars_q.get_max_size()] += 1

                car = self.cars_q.get()   # Sell a car
                self.sold_cars += 1
                if car == "No more cars":
                    break    
                
                # One extra slot is available in our dealership
                self.slots_at_dealership.release()            

                # Sleep a little - don't change.  This is the last line of the loop
                time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))

            self.barrier.wait()

def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """
    sold_cars = 0
    cars_created = 0

    # TODO Create semaphore(s)
    slots_at_dealership = threading.Semaphore(MAX_QUEUE_SIZE)
    cars_available_in_factory = threading.Semaphore(0)

    # TODO Create queue
    cars_q = Queue251()   

    # TODO Create lock(s)
    lock = threading.Lock()

    # TODO Create barrier(s)
    factory_barrier = threading.Barrier(factory_count)
    dealer_barrier = threading.Barrier(dealer_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factories = Queue251()
    for n_factory in range(factory_count):
        factory = Factory(cars_q, slots_at_dealership, cars_available_in_factory, factory_barrier, n_factory+1, cars_created, dealer_count)
        factories.put(factory)

    # TODO create your dealerships
    dealerships = Queue251()
    for n_dealer in range(dealer_count):
        dealer = Dealer(cars_q, slots_at_dealership, cars_available_in_factory, dealer_stats, lock, sold_cars, n_dealer+1, dealer_barrier)
        dealerships.put(dealer)

    log.start_timer()

    # TODO Start all dealerships
    for dealer_thread in dealerships.items:
        dealer_thread.start()

    time.sleep(1)   # make sure all dealers have time to start

    # TODO Start all factories
    for factory_thread in factories.items:
        factory_thread.start()

    # TODO Wait for factories and dealerships to complete
    # Probably use barriers here
    for dealer_thread in dealerships.items:
        dealer_thread.join()

    for factory_thread in factories.items:
        factory_thread.join()


    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    factory_stats = [] # CHANGE THIS LATER!!!
    return (run_time, cars_q.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factor Stats   : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


