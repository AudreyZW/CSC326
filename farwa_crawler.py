#function which returns a tuple of the key and its value
#word is a list that is passed to this function by the parser
#basically this should make a dictionary of the word's id as the key and have
#a set of ids as the value

def get_inverted_index(word, pairs_):
    for i in word:
        for d in pairs:
            if i == d:
                index_ = pairs[d]
                key_ = d
    return (key_,index_)

#reading the urls from the text file and storing in list

if __name__ == "__main__":
    # creating a list to hold the urls
    list1 = []
    filename = "urls.txt"
    with open(filename) as f:
        list1 = ((f.read().splitlines()))

#put each url in a dictionary with its id being the key, making sure duplicates are accounted for

    pairs = {}
    v = 1
    for i in list1:
        if i not in pairs:
            pairs[i] = v
            v = v + 1

    for k in pairs:
        print (pairs[k], k)

    t = get_inverted_index(["test1"], pairs)

