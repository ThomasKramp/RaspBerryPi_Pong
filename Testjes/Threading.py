from threading import Thread

import time

#Een functie die we willen gaan threaden
def func(naam, tijdsduur,herhaling):
    print("ik ben: " + naam)
    while(herhaling > 0):
        time.sleep(tijdsduur)
        print(naam + "          " + str(time.time()))
        herhaling -= 1
    
    print(naam + " is klaar")

#Het aanmaken van de threadings
opdr1 = Thread (target=func, args=("func1", 1, 6))
opdr2 = Thread (target=func, args=("func2", 0.5, 12))

opdr1.start()
opdr2.start()


