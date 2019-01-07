import json
import sys
sys.path.append("../..")
import os


dir1 = os.path.abspath('../..')
dir2 = dir1 + '\cam4\scripts\cookies\\'
with open(dir2+"aol@hotmail.txt", 'r') as fp:
    cookies = json.load(fp)

# print(cookies)
with open(dir2+'test'+".com.txt", 'w') as fp:
    json.dump(cookies, fp) 

dir1 = os.path.abspath('')
dir2 = dir1 + '\cookies_email\\aol\\'
with open(dir2+"1.com.txt", 'w') as fp:
    json.dump(cookies, fp) 