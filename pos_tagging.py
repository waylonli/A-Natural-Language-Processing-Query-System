# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    word = ""
    tag = ""
    single = set()
    plural = set()
    with open("sentences.txt", "r") as f:
        for line in f:
            for each in line.split():
                word, tag = each.split('|')
                if(tag == 'NN'):
                    single.add(word)
                elif(tag == 'NNS'):
                    plural.add(word)
    return list(single.intersection(plural))


unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    _output = ""
    vowel = ['a','e','i','o','u']
    if(s in unchanging_plurals_list):
        _output = s
    elif not(re.match("([A-Z]|[a-z])+men$",s) == None):
        _output = s[0:-2] + 'an'
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

    return _output

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    tags = []
    tempV = verb_stem(wd)
    tempN = noun_stem(wd)
    for each in function_words_tags:
        (word,tag) = each
        if(wd == word):
            tags.append(tag)
    if(wd in lx.getAll('P')):
        tags.append('P')
    if(wd in lx.getAll('A')):
        tags.append('A')
    if(tempN in lx.getAll('N')):
        if(wd in unchanging_plurals_list):
            tags.append('Ns')
            tags.append('Np')
        elif not(tempN == wd):
            tags.append('Np')
        else:
            tags.append('Ns')
    if(tempV in lx.getAll('I')):
        if not(tempV == wd):
            tags.append('Is')
        else:
            tags.append('Ip')
    if(tempV in lx.getAll('T')):
        if not(tempV == wd):
            tags.append('Ts')
        else:
            tags.append('Tp')
    return tags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
