'''
Created on 29 nov. 2016

@author: Camelia
'''
from copy import deepcopy
__author__ = 'camelia' 

from Exception import IntegerNumberException
from math import log


class IntegerNumber():
    '''
    Class to represent an integer number
    Fields:
        self._numberBase : the base of the integer number
        self._numberLength : the number of digits the number has
        self._digits : the list containing the digits of the integer, with the
                    precision that the least significant digits of the number are placed 
                    at the lower index in the array of digits
    '''
    
    AllowedNumericalBases = [2, 3, 4, 5, 6, 7, 8, 9, 10, 16]
    NumericalValues = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, 
                       '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
    NumericalSymbols = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 
                        8:'8', 9:'9', 10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F'}
    
    def __init__(self, numberBase, numberRepr):
        '''
        This is the contructor for the IntegerNumber class
        :parameter numberBase: an integer number - the base of the number's representation
        :parameter numberRepr: a string - the number represented in the base above described
        :raises IntegerNumberException if the base doesn't belong to the list of allowed numerical bases
        '''
        if numberBase not in IntegerNumber.AllowedNumericalBases:
            raise IntegerNumberException("Base not allowed.")
        if numberRepr == "":
            numberRepr = 0
        self._numberBase = numberBase
        self._numberLength = 0
        self._digits = []
        
        for dd in numberRepr:
            if not dd in IntegerNumber.NumericalValues.keys():
                raise IntegerNumberException("Unknown numerical base symbols.")
            if IntegerNumber.NumericalValues[dd] >= numberBase:
                raise IntegerNumberException("Unknown numerical base symbols.")
            self.appendToRepresentation(IntegerNumber.NumericalValues[dd])
        
    def appendToRepresentation(self, numberDigit):
        """
        This function appends a digit in the number at the most significant 
        position of its representation
        :parameter numberDigit which represents the digit appended dureing the 
        operation
        """
        self._digits.append(numberDigit)
        self._numberLength += 1
        
    def getTheValueOfSymbol(self, numberRepresentation):
        """
        This function returns the value of an entered digit in the number
        representation
        :raises ValueError if the digit representation is unknown by the program
        """
        if numberRepresentation in IntegerNumber.NumericalValues.keys():
            return IntegerNumber.NumericalValues[numberRepresentation]
        raise ValueError("Couldn't validate digit...Unrecognised.")
    
    def removeLeadingZeros(self):
        """
        Function to remove the zeros placed in front of all digits in the
        representation of a number; useful operation for example when we subtract
        two numbers and the result has a digit in minus, but after the operation
        a zero remains; let 200 - 190 = 010, the function transforms it to 10
        """
        while len(self) > 0 and self[-1] == 0:
            self._digits.pop()
            self._numberLength -= 1
    
    def __repr__(self):
        """
        Function to convert the number in its own base
        :return a string is returned, representing the number
        """        
        self.removeLeadingZeros()
        numberRepresentation = ""
        for dig in self._digits[::-1]:
            numberRepresentation += IntegerNumber.NumericalSymbols[dig]
        if numberRepresentation  == "":
            numberRepresentation = 0
        return numberRepresentation
    
    
    def __str__(self):
        """
        :return a string representing the number and also the corresponding base
        between brackets
        """
        return repr(self)+" (" + str(self._numberBase) + ") "
    
    def __getitem__(self, index):
        """
        Function(getter for [] operator) to return a certain digit placed in the representation of the
        number at a certain position indicated by the index parameter
        :raises IndexError if the index given as parameter is not within the
        index range of the number considered
        """
        if index >= self._numberLength:
            raise IndexError("Index out of range.")
        return self._digits[index]
    
    def __setitem__(self, keyIndex, numberDigit):
        """
        Function to set [] operator, it sets a certain digit in a number representation
        based on the index given
        :param keyIndex which is an integer number representing the index of
        the digit in the number representation which we want to obtain
        :param numberDigit which is the new value we want to set the digit to
        :raises IndexError if the parameter keyIndex represents an index
        considered to be out of range in the number representation
        """
        if keyIndex > self._numberLength:
            raise IndexError("Key Index out of range.")
        self._digits[keyIndex] = numberDigit
        
    def __len__(self):
        """
        This function returns the number of digits of the number representation
        as an integer number
        """
        return self._numberLength
    
    def getNumericalBase(self):
        """
        Getter for the base of the number
        :return an integer representing the field of base the number has
        """
        return self._numberBase
    
    def __add__(self, nextOperand):
        """"
        This function represents the addition between two integer number objects
        :param nextOperand representing the second operand for the addition process
        while the first one is represented by self
        :return a new integer number representing the sum between self and the
        nextOperand
        :raises ValueError if the second operand is not of the type integerNumber
        or it is represented in other base, different from self
        """
        if not isinstance(nextOperand, IntegerNumber):
            raise ValueError("Addition between different objects, can't perform.")
        if self._numberBase != nextOperand._numberBase:
            raise ValueError("Impossible addition between numbers in different bases.")
        operatingBase = self.getNumericalBase()
        newRepresentation = IntegerNumber(operatingBase, repr(self))
        
        if len(newRepresentation) < len(nextOperand):
            for i in range(0, len(nextOperand) - len(newRepresentation)):
                newRepresentation.appendToRepresentation(0)
        else:
            for i in range(0, len(newRepresentation) - len(nextOperand)):
                nextOperand.appendToRepresentation(0)
                
        carryDigit = 0
        
        for i in range(0, newRepresentation._numberLength):
            value = newRepresentation[i] + nextOperand[i] + carryDigit
            newRepresentation[i] = value % operatingBase
            carryDigit = value // operatingBase
        if carryDigit:
            newRepresentation.appendToRepresentation(carryDigit)
        return newRepresentation
    
    def __sub__(self, nextOperand):
        """
        This function implements the subtraction between self and a new operand
        given as parameter with the name nextOperand, with the precision
        that the parameter nextOperand is the subtrahend and self is the minuent
        :return an IntegerNumber representing the difference between the numbers
        described above
        :raise ValueError if the operand given as parameter is not an instance
        of integer numbers or if the base of this operand is different from the 
        one self has in its representation
        """
        if not isinstance(nextOperand, IntegerNumber):
            raise ValueError("Can't subtract two different objects.")
        if self.getNumericalBase() != nextOperand.getNumericalBase():
            raise ValueError("Can't subtract two numbers with different base representation.")
        newRepresentation = IntegerNumber(self.getNumericalBase(), repr(self))
        carryDigit = 0
        for i in range(len(newRepresentation) - len(nextOperand)):
            nextOperand.appendToRepresentation(0)
        for i in range(0, len(self)):
            newRepresentation[i] = newRepresentation[i] - (nextOperand[i] + carryDigit)
            if newRepresentation[i] < 0:
                carryDigit = 1
            else:
                carryDigit = 0
            if carryDigit:
                newRepresentation[i] += newRepresentation.getNumericalBase()
            
        newRepresentation.removeLeadingZeros()
        return newRepresentation
    
    def __mul__(self, nextOperand):
        """
        This function implements the multiplication between self and the other
        operand represented as input parameter wth the nextOperand name
        :return an IntegerNumber representing the number resulted from the 
        multiplicaton above described
        :raises ValueError if the nextOperand is not of the type IntegerNumber
        or if the base doesn't coincide with the self base
        """
        if not isinstance(nextOperand, IntegerNumber):
            raise ValueError("Can't multiply objects of different types.")
        if self.getNumericalBase() != nextOperand.getNumericalBase():
            raise ValueError("Can't multiply numbers with different base representations.")
        newRepresentation = IntegerNumber(self._numberBase, "0"*(len(self) + len(nextOperand) -1))
        carryDigit = 0
        for i in range(0, len(self)):
            for j in range(0, len(nextOperand)):
                newRepresentation[i+j] += self[i] * nextOperand[j]
        for i in range(0, len(newRepresentation)):
            newRepresentation[i] += carryDigit
            carryDigit = newRepresentation[i] % self.getNumericalBase()
            newRepresentation[i] = newRepresentation[i] % self.getNumericalBase()
            
        while carryDigit > 0:
            newRepresentation.appendToRepresentation(carryDigit%self._numberBase)
            carryDigit = carryDigit // self._numberBase
            
        return newRepresentation    
            
    def __floordiv__(self, nextOperand):
        """
        Function which implements the division of an object of the IntegerNumber
        type and one digit integerNumber object
        nextOperand is the divisor
        :return an IntegerNumber representing the quotient of the division
        :raises valueerror if nextOperand is not a ne-digit number
        """       
        if not isinstance(nextOperand, int):
            raise ValueError("Division is only permitted with a one digit integer as divisor.")
        auxiliary = 0
        newRepresentation = IntegerNumber(self.getNumericalBase(), repr(self))
        for i in reversed(range(0, len(newRepresentation))):
            auxiliary = newRepresentation.getNumericalBase() * auxiliary + newRepresentation[i]
            newRepresentation[i] = auxiliary // nextOperand
            auxiliary = auxiliary % nextOperand
        newRepresentation.removeLeadingZeros()
        return newRepresentation
    
    def __mod__(self, nextOperand):
        """"
        This function implements the division between two numbers of the type IntegerNumber
        from which the second one fgiven as parameter is a one-digit-type number
        :return an IntegerNumber representing the remainder of the diviosion 
        described above
        :raies ValueError if the number given as parameter has more than one digit
        """
        if not isinstance(nextOperand, int):
            raise ValueError("Division is only permitted with an one digit divisor.")
        auxiliary = 0
        for i in reversed(range(0, len(self))):
            auxiliary = (auxiliary * self.getNumericalBase() + self[i]) % nextOperand
        return auxiliary
    
    def IntegerNumberComparison(self, nextOperand):
        """
        Ths function has one parameter representing the number to which self will be compared to
        it returns the value 1 if self is greater than nextOperand, 0 if they are equal to each
        other  and -1 otherwise
        """
        self.removeLeadingZeros()
        nextOperand.removeLeadingZeros()
        if len(self) > len(nextOperand):
            return 1
        elif len(self) < len(nextOperand):
            return -1
        else:
            """
            in this part we check for the digits in the representation from 
            the most significant to the least one
            """
            for i in reversed(range(len(self))):
                if self[i] > nextOperand[i]:
                    return 1
                elif self[i] < nextOperand[i]:
                    return -1
            return 0
    
    def __eq__(self, nextOperand):
        """
        Function to replace the == operator netween self and the IntegerNumber given as
        parameter
        :return the value of True or False
        """
        return self.IntegerNumberComparison(nextOperand) == 0
    
    def __lt__(self, nextOperand):
        """
        Function to replace the < operator netween two IntegerNumber objects
        :return True or False regarding to the comparison result
        """
        return self.IntegerNumberComparison(nextOperand) == -1
    
    def __gt__(self, nextOperand):
        """
        Function to replace the > operator between two IntegerNumber objects
        :return True or false regarding to the specific comparison which leads the 
        operation
        """
        return self.IntegerNumberComparison(nextOperand) == 1
    
    def __ge__(self, nextOperand):
        """
        Function to replace the operation defined by the >= operator between two
        IntegerNumber objects
        :return TRue or False regarding to the operation requirements
        """
        return self.IntegerNumberComparison(nextOperand) >= 0
    
    def substitutionMethodBaseConversion(self, destinationBase):
        """
        This function implements the conversion of self in another given base as parameter
        using the substitution base which is more often reccomended in the case
        when the actual base is less than the base we want to convert the number to
        
        :return an IntegerNUmber representing the number converted to the destinationBase
        described above
        """
        destinationNumber = IntegerNumber(destinationBase, "0")
        basePwr = IntegerNumber(destinationBase, "1")
        for i in range(len(self)):
            destinationNumber = destinationNumber + basePwr * IntegerNumber(destinationBase, IntegerNumber.NumericalSymbols[self[i]])
            basePwr = basePwr * IntegerNumber(destinationBase, IntegerNumber.NumericalSymbols[self._numberBase])
        return destinationNumber
    
    def successiveDivisipnConversionMethod(self, destinationBase):
        """
        This function implements the conversion of self to another base called as parameter
        destinationBase and the succesive division method is used, recommended to be used
        generally when the source base is greater than the destination base from reasons that
        there is only need to divide by one-digit number
        :return an IntegerNumber type object representing self converted to the destinaton base above described
        """
        
        destinationNumber = IntegerNumber(destinationBase, "0")
        basePwr = IntegerNumber(destinationBase, "1")
        interm = IntegerNumber(destinationBase, "10")
        selfie = deepcopy(self)
        while len(selfie) != 0:
            destinationNumber = destinationNumber + basePwr * IntegerNumber(destinationBase, IntegerNumber.NumericalSymbols[selfie % destinationBase])
            selfie = selfie // destinationBase
            basePwr = basePwr * interm
        return destinationNumber
        
    def ConversionIntermediateBase(self, destinationBase):
        number = self.substitutionMethodBaseConversion(10)
        number = number.successiveDivisipnConversionMethod(destinationBase)
        return number
    
    def rapidConversionsMethod(self, destinationBase):
        auxiliary  = ""
        repre = repr(self)
        repre = repre[::-1]
        if self._numberBase < destinationBase:
            manipulator = int(log(destinationBase, self._numberBase))
            i = 0
            while i < self._numberLength:
                current = repre[i:i+manipulator]
                current = current[::-1]
                numberDig = IntegerNumber(self._numberBase, current)
                numberDig = numberDig.substitutionMethodBaseConversion(destinationBase)
                auxiliary += repr(numberDig)
                i += manipulator
        else:
            manipulator = int(log(self._numberBase, destinationBase))
            for i in range(len(self)):
                current = IntegerNumber(self._numberBase, IntegerNumber.NumericalSymbols[self[i]])
                current = current.successiveDivisipnConversionMethod(destinationBase)
                for j in range(0, len(destinationBase)):
                    auxiliary = auxiliary + IntegerNumber.NumericalSymbols[current[i]]
                for j in range(manipulator - len(current)):
                    auxiliary = auxiliary + "0"
        return IntegerNumber(destinationBase, auxiliary[::-1])
    
    def conversionToBase(self, destinationBase):
        """"
        This function takes the decision of implementing the conversion according to 
        the value of the bases in field of requirements, it implements rapid conversions when
        a base is a power of the other, applies substitution method when the source base is
        smaller than the destination base and applies successive divisions method when the destination base is
        smaller than the source base
        :param the destination base representing the integer number (the base in which we want)
        our number to be represented
        :return an IntegerNumber object type representing the actual number already converted to the
        destination base
        """
        if self._numberBase == destinationBase:
            return self
        little = min(self._numberBase, destinationBase)
        """here we performed the comparison between the bases to discover
        which of them is smaller than the other
        """
        big = max(self._numberBase, destinationBase)
        """
        the same implemented process but for the other way around
        """
        if big in [little, little**2, little**3, little**4]:
            return self.rapidConversionsMethod(destinationBase)
        elif self._numberBase <= destinationBase:
            return self.substitutionMethodBaseConversion(destinationBase)
        else:
            return self.successiveDivisipnConversionMethod(destinationBase)