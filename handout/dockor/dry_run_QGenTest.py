# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 14:55:43 2019

@author: zhang
"""


# NLTK practice
'''
import nltk
nltk.download('punkt')

sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
tokens


from nltk.parse import CoreNLPParser

# Lexical Parser
parser = CoreNLPParser(url='http://localhost:9000')

list(parser.parse('What is the airspeed of an unladen swallow ?'.split()))
'''

# Question Generation/Answering - Neural Dependency
from nltk.parse.corenlp import CoreNLPDependencyParser

str1 = 'Obama is the President .'

dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
parses = dep_parser.parse(str1.split())

#[[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parses]

for parse in parses:
    for governor, dep, dependent in parse.triples():
        print(governor, dep, dependent)
        
        if (dep == 'nsubj') & (dependent[1] == 'NNP'):
            person = dependent[0]
            
list1 = str1.split()

num = list1.index(person)
list1[num] = 'Who'
str1_out = ' '.join(list1)




# Question Generation - NER
from nltk.parse import CoreNLPParser
ner_tagger = CoreNLPParser(url='http://localhost:9000', tagtype='ner')

str2 = 'Rami Eid is studying at Stony Brook University in NY'
str3 = 'Beijing is the capital of China'
str4 = 'Shanghai is to the south of Beijing.'

str5 = 'Jack is on the mountain'

#list(ner_tagger.tag((str1.split())))

list2 = list(ner_tagger.tag((str1.split())))


# For words tagged as PER, we can use "Who" to replace the original words
for (x,y) in list2:
    if y == 'PERSON':
        num2 = list2.index((x,y))

list3 = str1.split()
list3[num2] = 'Who'
str3_out = ' '.join(list3)

# For words tagged as LOC, we can use "Which + that tag(city, country, etc.)" to replace the original words




    
            
            