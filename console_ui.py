'''
Created on 30 nov. 2016

@author: Camelia
'''
from Exception import IntegerNumberException
from IntegerNumber import IntegerNumber
from lib2to3.fixer_util import Comma
from tests import Test

class ActionCalculator():
    """
    This function handles the whole applicaton
    """
    AllowedOptions = ["1", "2", "3", "4", "5", "x"]
    def __init__(self):
        pass
    
    def displayMenu(self):
        s = ""
        s += "\n Calculator \n"
        s += "\t Available options: \n"
        s += "\t 1 - addition \n"
        s += "\t 2 - subtraction \n"
        s += "\t 3 - multiplication \n"
        s += "\t 4 - division by one digit \n"
        s += "\t 5 - conversion \n"
        s += "\t x - exit \n"
        print(s)
        
    def readIntegerNumber(self):
        """read a number"""
        numericalBase = int(input("Enter base: "))
        repr = input("Enter the number: ")
        return IntegerNumber(numericalBase, repr)
    
    def readOperands(self):
        """function to handle the user interaction by entering two integer numbers"""
        no1 = self.readIntegerNumber()
        no2 = self.readIntegerNumber()
        return no1, no2
        
    def continuity(self):
        input("Press any key to continue :)")
        
    def getSmallIntegerNumber(self):
        number = input("Enter a one-digit number: ")
        while not number in IntegerNumber.NumericalValues.keys():
            number = input("Enter a one-digit number: ")
        number = IntegerNumber.NumericalValues[number]
        return number
    
    def run(self):
        
        while True:
            try:
                self.displayMenu()
                command = input("Enter option: ")
                if command == "1":
                    n, m = self.readOperands()
                    print("\nResult: ", n, " + ", m, " = ", n+m, "\n")
                elif command == "2":
                    n, m = self.readOperands()
                    print("\nResult: ", n, " - ", m, " = ", n-m, "\n")
                elif command == "3":
                    n, m = self.readOperands()
                    print("\nResult: ", n, " * ", m, " = ", n*m, "\n")
                elif command == "4":
                    n = self.readIntegerNumber()
                    m = self.getSmallIntegerNumber()
                    print("\n Result: ")
                    print(n, " / ", m, " = ", n // m, " remainder ", IntegerNumber(n.getNumericalBase(), IntegerNumber.NumericalSymbols[n%m]) )
                elif command == "5":
                    n = self.readIntegerNumber()
                    m = int(input("Enter destination base: "))
                    print("\nResult: ", n, " = ", n.conversionToBase(m))
                elif command == "x":
                    break
                else:
                    print("\nUnknown command...\n")
            except ValueError:
                print("\nValue should be an integer number.\n")
            except IntegerNumberException as ine:
                print("\n\n"+str(ine)+"\n\n")
            except Exception as e:
                print("\n\n"+str(e)+"\n\n")
            self.continuity()
      
c = ActionCalculator()
t = Test()
#t.test()
c.run()              
                    