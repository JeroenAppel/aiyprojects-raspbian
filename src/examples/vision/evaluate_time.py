import time

def getMilliseconds():
    millis = int(round(time.time() * 1000))
    return millis

def itemLost(lastseen, current):
    if lastseen is None:
        return False
    else:
        if (lastseen + 5000) < current:
            return True
        else:
            return False
        
lostItem = False
time_banana_lastseen = None
current_time = None
seen = False

while lostItem == False:
    current_time = getMilliseconds()
    lostItem = itemLost(time_banana_lastseen, current_time)
    if seen == False:
        time_banana_lastseen = current_time
        seen = True
    print (lostItem)
    print (time_banana_lastseen)
    print (current_time)

time.sleep(10)

current_time = getMilliseconds()
lostItem = itemLost(time_banana_lastseen, current_time)
if lostItem == True:
    time_banana_lastseen = current_time
    lostItem = itemLost(time_banana_lastseen, current_time)
    if lostItem == False:
        print('Happy!')