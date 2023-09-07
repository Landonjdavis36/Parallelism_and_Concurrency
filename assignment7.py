"""
Course: CSE 251, week 14
File: common.py
Author: <Landon Davis>

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')


You will lose 10% if you don't detail your part 1 
and part 2 code below

Describe how to speed up part 1
I created the tree and the individuals would be pulled and added to the tree. To make it fasterI used threads when dealing with the husband, wife, child. Which found and added them to the tree quicker.

Describe how to speed up part 2


I created the tree and the individuals would be pulled and added to the tree. To make it faster I used a qeue and threads when dealing with the husband, wife, child. Which found and added them to the tree quicker.

10% Bonus to speed up part 3

I created the tree and the individuals would be pulled and added to the tree. To make it faster I used a qeue and threads when dealing with the husband, wife, child. Which found and added them to the tree quicker.


"""
from asyncio import threads
import queue
import re
from urllib.request import Request

from sqlalchemy import true
from common import *

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # TODO - implement Depth first retrieval
    if family_id == None:
        return
#Creates the Family tree using a thread.
    if tree.does_family_exist(family_id) == False:
        req_family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
        req_family.start()
        req_family.join()

        if len(req_family.response) > 0:
            family = Family(0, req_family.response)

            tree.add_family(family)

    else:
            family = tree.get_family(family_id)
#Creates the husband and uses a thread.
    if tree.does_person_exist(family.husband) == False:
        req_husband = Request_thread(f'{TOP_API_URL}/person/{family.husband}')
#Starts and ends the thread.        
        req_husband.start()
        req_husband.join()

        if len(req_husband.response) > 0:
            husband = Person(req_husband.response)
#Adds Husband to tree.            
            tree.add_person(husband)
            family = tree.get_family(family_id)
#Creates the wife and uses a thread.
    if tree.does_person_exist(family.wife) == False:
        req_wife = Request_thread(f'{TOP_API_URL}/person/{family.wife}')
#Starts and ends the thread.         
        req_wife.start()
        req_wife.join()

        if len(req_wife.response) > 0:
            wife = Person(req_wife.response)
#Adds wife to tree.            
            tree.add_person(wife)
#Creates the child and uses a thread.
    for child in family.children:
        if tree.does_person_exist(child) == False:
            req_child = Request_thread(f'{TOP_API_URL}/person/{child}')
#Starts and ends the thread.            
            req_child.start()
            req_child.join()

            if len(req_child.response) > 0:
                child_obj = Person(req_child.response)
#Adds child to tree.               
                tree.add_person(child_obj)
#Creates the threads for the husband and wife. It points to the depth function and the tree as an argument.
    husband_thread = threading.Thread(target=depth_fs_pedigree, args=(husband.parents, tree))
    wife_thread = threading.Thread(target=depth_fs_pedigree, args=(wife.parents, tree))
#Starts and ends the threads.
    husband_thread.start()
    wife_thread.start()
    husband_thread.join()
    wife_thread.join()
    
# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    # TODO - implement breadth first retrieval

#Creates the Queue.
    q = queue.Queue()
    q.put(start_id)
#Creates a threads.
    threads = [threading.Thread(target=breadth_thread, args=(tree, q)) for i in range(20)]
#Starts and ends the threads.
    for t in threads:
        t.start()
    for t in threads:
        t.join()
#Creates a function and uses the same code to create a tree and the family memebers but this time puts it in a queue.
def breadth_thread(tree, q):

    while true:
        family_id = q.get()


        if family_id == None:
            return
#Creates the family tree.
        if tree.does_family_exist(family_id) == False:
            req_family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
#Start and ends the thread.               
            req_family.start()
            req_family.join()

            if len(req_family.response) > 0:
                family = Family(0, req_family.response)

                tree.add_family(family)

        else:
            family = tree.get_family(family_id)
#Creates the husband and uses a thread.
        if tree.does_person_exist(family.husband) == False:
            req_husband = Request_thread(f'{TOP_API_URL}/person/{family.husband}')
#Start and ends the thread.               
            req_husband.start()
            req_husband.join()

            if len(req_husband.response) > 0:
                husband = Person(req_husband.response)
#Adds husband to tree.               
                tree.add_person(husband)
#Puts the husband in the queue.                
                q.put(husband.parents)
#Creates the wife and uses a thread.
        if tree.does_person_exist(family.wife) == False:
            req_wife = Request_thread(f'{TOP_API_URL}/person/{family.wife}')
#Start and ends the thread.            
            req_wife.start()
            req_wife.join()

            if len(req_wife.response) > 0:
                wife = Person(req_wife.response)
#Adds wife to tree.                
                tree.add_person(wife)
#Puts the wife in the queue.               
                q.put(wife.parents)
#Creates the child and uses a thread.
        for child in family.children:
            if tree.does_person_exist(child) == False:
                req_child = Request_thread(f'{TOP_API_URL}/person/{child}')
 #Start and ends the thread.                  
                req_child.start()
                req_child.join()

                if len(req_child.response) > 0:
                    child_obj = Person(req_child.response)
#Adds child to tree.                    
                    tree.add_person(child_obj)




# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
#Creates the Queue.
    q = queue.Queue()
#Puts in the queue.
    q.put(start_id)
#Creates the threads.
    threads = [threading.Thread(target=breadth_thread, args=(tree, q)) for i in range(5)]
#Starts and ends the threads.
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    

   
