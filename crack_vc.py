#import pytesseract
import os, sys
#import Image

class crack_vc:
	def __init__(self):
		self.vcode = ""
		self.ocr_path = r'"D:\Program Files\Tesseract-OCR\tesseract.exe "'
	def get_vcode(self, vcode_file, decode_file):
		df_path = decode_file+".txt"
		if os.path.isfile(df_path):
			os.remove(df_path)
		cmd =self.ocr_path  + " " +  vcode_file + " " + decode_file
		print cmd
		os.system(cmd)
		f = open(decode_file+".txt", 'r')
		tmp_line = f.readline().strip()
		return tmp_line

#print crack_vc().get_vcode(r'd:\1.jpg', r'd:\vcode')
