import time
import requests
import os
import threading

import downloadAndParse as dp


THREAD_COUNT = 20

try:
    os.mkdir("set-images")
except:
    # dir already exits don't create it again
    pass


# To get the list of sets we will use the scryfall API, a call to just the sets page willa return 
# the list of all sets that we can thin iterate through


# Each set will run on its own thread to prevent this process from taking literal days


setCodes = []
cardAmount = []


scryfallData = requests.get("https://api.scryfall.com/sets").json()["data"]


for mtgSet in scryfallData:
    setCodes.append(mtgSet["code"])
    cardAmount.append(mtgSet["card_count"])







threads = []

for setCode in setCodes:
    
    # print(setCodes.index(setCode))
    maxSetNum = cardAmount[setCodes.index(setCode)]
    # print(maxSetNum)
    try:
        os.mkdir(f"set-images/{setCode}")
    except:
        # dir already exits don't create it again
        pass
    t = threading.Thread(target=dp.downloadSetImages, args=(setCode, maxSetNum))
    t.daemon = True
    threads.append(t)
    
    
# Start each thread
for t in threads:
    if threading.active_count() < THREAD_COUNT:
        t.start()
        print(f"Starting Thread {threading.active_count()}")

try:
    while True:
        time.sleep(0.1) # Main thread keeps running
except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Exiting.")
    # Daemon threads will automatically terminate

