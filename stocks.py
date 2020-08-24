from yahoo_fin import stock_info as si
from time import sleep
from threading import Thread, Lock
import os
import pickle

class Alert:
    ticker = "NA"
    price = float(0)
    way = 1

    def __init__(self, stock, p, w):
        self.ticker = stock
        self.price = p
        self.way = w

    # Stopping the alert after is has hit the target
    def stopAlert(self, alert, Alertlist):
        Alertlist.remove(alert)
        outfile = open(filename, "wb")
        pickle.dump(alertList, outfile)
        outfile.close()

    # The notifier function
    def notify(self, title, subtitle, message):
        t = '-title {!r}'.format(title)
        s = '-subtitle {!r}'.format(subtitle)
        m = '-message {!r}'.format(message)
        os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

    # Function that constantly checks the price
    def checkPrice(self, alertlist):
        while (True and stop):
            for alert in alertlist:
                if (alert.way == str(1)):
                    if (float("%.2f" %((si.get_live_price(alert.ticker))))) > float(alert.price):
                        Alert.notify(Alert, title  = alert.ticker.upper() + "'s price broke " + str(alert.price),
                        subtitle = alert.ticker.upper() + " is at " + str(("%.2f" %((si.get_live_price(alert.ticker))))),
                        message  = "{} price is above {}".format(alert.ticker.upper(), alert.price))
                        Alert.stopAlert(Alert, alert, alertlist)
                elif(alert.way == str(2)):
                    if((float("%.2f" %((si.get_live_price(alert.ticker))))) < float(alert.price)):
                        Alert.notify(Alert, title = alert.ticker.upper() + "'s price hit target",
                        subtitle = alert.ticker.upper() + " is at " + str(("%.2f" %((si.get_live_price(alert.ticker))))),
                        message  = "{} price is below {}".format(alert.ticker.upper(), alert.price))
                        Alert.stopAlert(Alert, alert ,alertlist)

    # Function that creates an alert and adds it to the list of alerts
    def createAlert(self, alertList):
        stock = input("\n    What is the ticker symbol of the stock?\n     :: ")
        price = -1.0
        while(price < 0.0):
            try:
                price = float(input("    What is the price you want to hit?\n     :: "))
                if(price < 0):
                    print("\n    Invalid price!\n")
            except ValueError:
                print("\n    Invalid input!\n")
        way = -1
        while(way != str(1) and way != str(2)):
            way = input("    Do you want it to go above or below?\n     1.Above 2.Below\n     :: ")
            if(way != str(1) and way != str(2)):
                print("\n    Invalid Answer!\n")
        
        try:    
            ("%.2f" %((si.get_live_price(stock))))
            alert = Alert(stock, price, way)
            alertList.append(alert)
            outfile = open(filename, "wb")
            pickle.dump(alertList, outfile)
            outfile.close()
            print("\n    Alert created successfully!")
        except AssertionError:
            print()
            print("      " + "-"*21)
            print("     | Stock doesn't exist |")
            print("      " + "-"*21)

    # Function to print and alert
    def printAlert(self, alert):
        print("Ticker: {} to hit price: {}".format(alert.ticker.upper(), alert.price))


# Create and open files to store and load info
filename = "alerts"

try:
    infile = open(filename, "xb")
except FileExistsError:
    infile = open(filename, "rb")

# Read files
try:
    infile = open(filename, "rb")
    alertList = pickle.load(infile)
    infile.close()
except EOFError:
    alertList = list()

# Variable to stop the thread and close the program
stop = True

# Thread to keep checking the prices
t = Thread(target=Alert.checkPrice, args=(Alert, alertList,))
t.start()

# Continually waiting for input    
choice = str(-1)
while choice != str(0):
    try:
        choice = input("\n     :: Menu ::\n    1. Create new alert.\n"
                    "    2. Check the price of a stock.\n"
                    "    3. Print all the current alerts\n"
                    "    4. Remove an alert\n"
                    "    0. Exit program\n     :: ")

        if(choice == str(1)):
            Alert.createAlert(Alert, alertList)
            
        if(choice == "2"):
            ticker = input("\n    Which stock:\n     ::")
            try:
                price = ("%.2f" %((si.get_live_price(ticker))))
                print(" "*5 + ticker.upper() + " price: " + str(price) + " USD")
            except AssertionError:
                print()
                print("      " + "-"*21)
                print("     | Stock doesn't exist |")
                print("      " + "-"*21 + "\n")
        
        if(choice == str(3)):
            print()
            print("  ----- List of current alerts -----")
            for alert in alertList:
                print("    ", end = " ")
                Alert.printAlert(Alert, alert)
        
        if(choice == str(4)):
            print()
            print("  ----- List of current alerts -----")
            i = 1
            for alert in alertList:
                print("    " + str(i) + ".", end = " ")
                Alert.printAlert(Alert, alert)
                i+=1
            remove = input("\n    Which alert do you wish to remove?\n    Select 0 to leave.\n     :: ")
            while int(remove) != 0:
                if (remove == -999):
                    print("\n  ----- List of current alerts -----")
                    i = 1
                    for alert in alertList:
                        print("    " + str(i) + ".", end = " ")
                        Alert.printAlert(Alert, alert)
                        i+=1
                    remove = input("\n    Which alert do you wish to remove?\n    Select 0 to leave.\n     :: ")
                if (int(remove) > i-1 or int(remove) < 0):
                    print("\n    Invalid alert!\n")
                    remove = input("    Which alert do you wish to remove?\n    Select 0 to leave.\n     :: ")
                elif(int(remove) == 0):
                    break
                else:
                    del alertList[int(remove)-1]
                    outfile = open(filename, "wb")
                    pickle.dump(alertList, outfile)
                    outfile.close()
                    remove = -999

        if(choice == str(0)):
            print("    Closing program")
            outfile = open(filename, "wb")
            pickle.dump(alertList, outfile)
            outfile.close()
            stop = False
            break
    except KeyboardInterrupt:
        print("\n    Ctrl+C again to force quit program")
        break