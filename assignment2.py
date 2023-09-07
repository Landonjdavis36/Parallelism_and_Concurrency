"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from concurrent.futures import thread
from datetime import datetime, timedelta
from urllib import response
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'
url = TOP_API_URL
# Global Variables
call_count = 0

def updating():
  global call_count
  call_count += 1

# TODO Add your threaded class definition here
class try_threadss(threading.thread):
  def __init__(self,url):
      super().__init__()
      self.url = url

  def run(self):
    response = requests.get(self.url)
    if response.status_code == 200:
      self.data = response.json()
      updating()
      
    def thread_list(thread, target):
        return [try_threadss(i) for i in (thread.data['url'][5][target])]
    def data(thread_list):
      new_list = []
      for i in range(len(thread_list)):
          thread_list[i].start()
          thread_list[i].join()
          new_list.append(thread_list[i].data['url'])
      return sorted(new_list)

      
      
      #def EP6():
          #people = threading.thread(http://127.0.0.1:8790/people/6)
          #films = thread.threading('http://127.0.0.1:8790/films/6')
          #species = thread.threading('http://127.0.0.1:8790/species/6')
          #vehicles = thread.threading('http://127.0.0.1:8790/vehicles/6')
          #starships = thread.threading('http://127.0.0.1:8790/starships/6')

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    thread1 = try_threadss(url)
    thread1.start()
    thread1.join()
    thread1.url = thread1.data['http://127.0.0.1:8790/films/6']
    thread2 = try_threadss(thread1.url)
    thread2.start()
    thread2.join()
    
    print("People : ", len(thread2.data['http://127.0.0.1:8790/People/6']))
    print(', '.join('People'))
    print()


    print("Planets : ", len(thread2.data['http://127.0.0.1:8790/Planets/6']))
    print(', '.join('Planets'))
    print()
    
    print("Starships : ", len(thread2.data['http://127.0.0.1:8790/starships/']))
    print(', '.join('Starships'))
    print()

    print("Vehicles : ", len(thread2.data['http://127.0.0.1:8790/vehicles/6']))

    print(', '.join('Vehicles'))
    print()
    print("Species : ", len(thread2.data['http://127.0.0.1:8790/species/6']))
    print(', '.join('Species'))
    print()


    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
