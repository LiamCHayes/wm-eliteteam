### A program that allows easy input into CSV file for WM team progress tracking

## Setup
from modules import teamtracker
tracker = teamtracker()

## Run the code
while True:
    #get input
    newdata = tracker.getinput()

    #stop program if input is Quit, add benchmark if input is Benchmark, or add climb or lift
    if newdata.capitalize() == 'Quit':
        break
    elif newdata.capitalize() == 'Group':
        tracker.groups()
    elif newdata.capitalize().split()[0] == 'Lookup':
        tracker.get_data()
    else:
        tracker.input_data()
    


    