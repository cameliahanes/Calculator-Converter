'''
Created on 29 nov. 2016

@author: Camelia
'''
from copy import deepcopy
from unittest import TestCase
from IntegerNumber import IntegerNumber
from random import randint
import random


__author__ = 'camelia'



class Test(TestCase):
    '''
    class used for testing the application 
    '''

    allowedNumericalBases = [2, 3, 4, 5, 6, 7, 8, 9, 10, 16]
    
    def defineRandomIntegerNumber(self, numericalBase):
        l = randint(1, 10)
        representation = ""
        for i in range(l):
            representation += IntegerNumber.NumericalSymbols[randint(0, numericalBase-1)]
        number = IntegerNumber(numericalBase, representation)
        number.removeLeadingZeros()
        return number
    
    def toBase10Converter(self, representation, numericalBase):
        number = 0
        for i in range(len(representation)):
            number = number * numericalBase + IntegerNumber.NumericalValues[representation[i]]
        return number
    
    def testAdditionBetweenIntegers(self):
        numericalBase = random.choice(Test.allowedNumericalBases)
        number1 = self.defineRandomIntegerNumber(numericalBase)
        number2 = self.defineRandomIntegerNumber(numericalBase)
        numberResulted = number1 + number2
        assert(self.toBase10Converter(repr(number1), numericalBase) + self.toBase10Converter(repr(number2), numericalBase) == self.toBase10Converter(numberResulted, numericalBase))
     
    def randomTestConversion(self):
        x = self.defineRandomIntegerNumber(10)
        y = deepcopy(x)
        for i in range(randint(1, 10)):
            newBase = random.choice(Test.AllowedBases)
            x = x.conversionToBase(newBase)
        x = x.conversionToBase(10)
        assert(x == y)   
    
    def testConversions(self):
        assert(IntegerNumber(4, "33221100").conversionToBase(9) == IntegerNumber(9, "106810"))
        assert(IntegerNumber(4, "123032122").conversionToBase(16) == IntegerNumber(16, "1B39A"))
        assert(IntegerNumber(4, "33221100") + IntegerNumber(4, "123032122") == IntegerNumber(4, "222313222"))
        assert(IntegerNumber(7, "1230056").conversionToBase(4) == IntegerNumber(4, "212230223"))
        assert(IntegerNumber(7, "445566").conversionToBase(4) == IntegerNumber(4, "103033320"))
        assert(IntegerNumber(16, "ABCDE1").conversionToBase(4) == IntegerNumber(4, "222330313201"))
        assert(IntegerNumber(16, "7").conversionToBase(8) ==  IntegerNumber(8, "7"))
        assert(IntegerNumber(6, "54321").conversionToBase(5) == IntegerNumber(5, "214330"))
        assert(IntegerNumber(6, "3").conversionToBase(2) == IntegerNumber(2, "11"))

        assert(IntegerNumber(7, "1230056") - IntegerNumber(7, "445566") == IntegerNumber(7, "451160"))
        assert(IntegerNumber(16, "ABCDE1") * IntegerNumber(16, "7") == IntegerNumber(16, "4B2A127"))
        assert(IntegerNumber(6, "54321") // 3 == IntegerNumber(6, "15304"))
        assert(IntegerNumber(6, "54321") // 4 == IntegerNumber(6, "12350"))
        assert(IntegerNumber(10, "120") % 7 == 1)
        assert(IntegerNumber(10, "17") * IntegerNumber(10, "7") + IntegerNumber(10, "1") == IntegerNumber(10, "120"))

    
    def test(self):
        for i in range(randint(1, 100)):
            self.testAdditionBetweenIntegers()
        for i in range(10):
            self.randomTestConversion()
        self.testConversions()