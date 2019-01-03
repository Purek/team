import os
import time


def writelog(runinfo):
    file=open(os.getcwd()+"\log.txt",'a+')
    file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" : \n"+runinfo+"\n")
    file.close()


if __name__=='__main__':
    writelog('...')
    print('...')
