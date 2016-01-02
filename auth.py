__author__ = 'Andre'

word = 'cek'

with open('user.txt','r') as searchfile:
    for line in searchfile:
        user = line.split('\t')[0]
        passwd = line.split('\t')[1]
        if word in line:
            print 'yes'
            print user
            print passwd
            break
