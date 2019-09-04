import time
import enum

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

# Temp variables which will now be used to test the program
lostItem = False

# For the demo, the label starts with banana
label = 'banana'

# Actual variables which will be used in the program
class wait_status(enum.Enum): 
    waitForRemove = 1
    waitForAdd = 2

current_time = None

supported_fruits = ('banana', 'apple', 'orange')

fruit_seen = {
    'banana':0,
    'apple':0,
    'orange':0
    }

fruit_status = {
    'banana':wait_status.waitForAdd,
    'apple':wait_status.waitForAdd,
    'orange':wait_status.waitForAdd
    }

while lostItem == False:
    current_time = getMilliseconds()
    
    if label in supported_fruits:
        fruit_seen[label] = current_time
        if fruit_status[label] == wait_status.waitForAdd:
            print('Send message to FruitNinja: ' + label + ' added')
            fruit_status[label] = wait_status.waitForRemove
            
            # For this test, we will flip the label to None after the first seen action
            label = None

    for fruit in fruit_status:
        # We will now check all the fruits which are not detected.
        if (label in supported_fruits) == False:
            if fruit_status[fruit] == wait_status.waitForRemove:
                lostItem = itemLost(fruit_seen[fruit], current_time)
                if lostItem == True:
                    print('Send message to FruitNinja: ' + fruit + ' removed')
                    fruit_status[fruit] = wait_status.waitForAdd
                    
# Everything below this point is for testing purposes only.

    print (lostItem)
    print (fruit_seen['banana'])
    print (current_time)

time.sleep(10)

current_time = getMilliseconds()
lostItem = itemLost(fruit_seen['banana'], current_time)
if lostItem == True:
    fruit_seen['banana'] = current_time
    lostItem = itemLost(fruit_seen['banana'], current_time)
    if lostItem == False:
        print('Happy!')