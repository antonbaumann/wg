def remove_long_words(old_file, new_file, length):
    file = open(old_file, 'r')
    wordlist = []
    for line in file.readlines():
        if len(line) <= length:
            wordlist.append(line.strip().upper())
    file.close()
    wordlist = sorted(set(wordlist))
    file = open(new_file, 'w')
    for line in wordlist:
        file.write(line+"\n")

if __name__ == '__main__':
    old_file = "wordlist"
    new_file = "wordlist_max_4.txt"
    length = 5
    remove_long_words(old_file, new_file, length)