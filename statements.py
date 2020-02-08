# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
    	self._WordList = [] #define a private list to store the words and tag

    def add(self,stem,cat):
    	self._WordList.append((stem, cat))  #add word and tag to the list

    def getAll(self,cat):
    	_OutSet = [] # The list to return
    	for index in range(len(self._WordList)):
    		if(self._WordList[index][1] == cat):
    			_OutSet.append(self._WordList[index][0])
    	return list(set(_OutSet)) #delete the 

class FactBase:
    """stores unary and binary relational facts"""
    def __init__(self):
    	self._Unary = []
    	self._Binary = []

    def addUnary(self,pred,e1):
    	self._Unary.append((pred,e1))

    def addBinary(self,pred,e1,e2):
    	self._Binary.append((pred,e1,e2))

    def queryUnary(self,pred,e1):
    	for index in range(len(self._Unary)):
    		if(self._Unary[index][0] == pred):
    			if(self._Unary[index][1] == e1):
    				return True
    	return False

    def queryBinary(self,pred,e1,e2):
    	for index in range(len(self._Binary)):
    		if(self._Binary[index][0] == pred):
    			if(self._Binary[index][1] == e1 and self._Binary[index][2] == e2):
    				return True
    	return False


import re
from nltk.corpus import brown 

BrownVBZ = []
BrownVB = []
for each in brown.tagged_words():
    if (list(each)[1] == 'VBZ'):
        BrownVBZ.append(list(each)[0])
    elif (list(each)[1] == 'VB'):
        BrownVB.append(list(each)[0])

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    _output = ""
    vowel = ['a','e','i','o','u']
    if(s in BrownVBZ or s in BrownVB):
        if(s == "has"):
            _output = "have"   #if s == has, rederive it to have
        elif not(re.match("([A-Z]|[a-z])+[^e]s$",s) == None):
            _output = s[0:-1]
        elif not(re.match("([A-Z]|[a-z])+ies$",s) == None):
            if(len(s) > 4):
                _output = s[0:-3] + 'y'
            elif(len(s) == 4 and not s[0] in vowel):
                _output = s[0:-1]
        elif not(re.match("([A-Z]|[a-z])+([ox]|ch|sh|ss|zz)es$",s) == None):
            _output = s[0:-2]
        elif not(re.match("([A-Z]|[a-z])+([^s]ses$|[^z]zes$)",s) == None):
            _output = s[0:-1]
        elif not(re.match("([A-Z]|[a-z])+([^iosxzh]es$|[^cs]hes$)",s) == None):
            _output = s[0:-1]
        else:
            return s
        if not(_output in BrownVB):
            _output = ""
    else: 
        _output = "" 

    return _output

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.