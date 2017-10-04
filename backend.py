from collections import Counter


def word_count (list1):
    counter = dict()
    for i in list1:
        counter[i] = counter.get(i,0) +1 
        
    for i,j in counter.items():
        print (i,j)


## take input string s and convert to a list

s = "This ,is a TEst."

input_string = s.lower()
word_list = input_string.split()
print word_list
