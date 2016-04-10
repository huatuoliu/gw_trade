#import pytesseract
#coding:utf-8
import os, sys
import re
#import Image
def get_vcode(vcode_file, decode_file):
    cmd = r'"D:\Program Files\Tesseract-OCR\tesseract.exe "' + " " +  vcode_file + " " + decode_file
    print cmd
    os.system(cmd)
    f = open(decode_file+".txt", 'r')
    tmp_line = f.readline().strip()
    return tmp_line
'''''
if len(sys.argv) < 2:
    print 'Usage: ./test.py file_name'
    sys.exit()
file_name=sys.argv[1]
print get_vcode(r"d:\1.jpg", r"d:\vcode")
'''''
x=-6/13
print x


n = 2
m = 3
matrix = [None]*2
#for i in range(len(matrix)):
#    matrix[i] = [0]*3

#matrix[0][1] = 123
matrix[0].append(1233)
print(matrix)

exit()
test_str = u"alert aaa12312.2。" \
           u"alert aaa12312"
#reg = re.compile(ur'.*alert.*(\d{4,})')
reg = re.compile(u'alert.*?(\d+\.\d*)')
match = reg.search(test_str)
if match:
    #reg = re.compile(ur'\d{4,}')
    print match.group(1)