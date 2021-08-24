b = True

while b:
    print('while')
    b= False
else:
    print('else')

A0 = dict(zip(('a','b','c','d','e'),(1,2,3,4,5)))
A1 = range(10)
A2 = sorted([i for i in A1 if i in A0])
A3 = sorted([A0[s] for s in A0])
A4 = [i for i in A1 if i in A3]
A5 = {i:i*i for i in A1}
A6 = [[i,i*i] for i in A1]

print(A0)
print(A1)
print(A2)
print(A3)
print(A4)
print(A5)
print(A6)


class Logger(object):

    def __init__(self, fileName='', toFile=False, toConsole=False):
        self.fileName = fileName
        self.toFile = toFile
        self.toConsole = toConsole
        return

    def printml(self, *args):
        aa = []
        toprint = ''
        for v in args:
            aa.append(str(v))
            toprint = toprint + str(v) + ' '
        if self.toFile and self.toConsole:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
                print(aa[a])
                # print('\n')
            f.close()
        elif self.toFile:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
            f.close()
        elif self.toConsole:
            for a in range(len(aa)):
                print(aa[a])
        else:
            pass
        return


fileName = ''
log = Logger(fileName, toFile=False, toConsole=True)
print2 = log.printml
print2('Logger testing ... 1', 'Logger testing ... 2 ', 'Logger testing ... 666')
