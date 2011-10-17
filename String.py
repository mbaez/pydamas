#!/usr/bin/python

__author__="mxbg"
__date__ ="$15/01/2010 11:57:19 PM$"
class String:
	def __init__(self, text=""):
		self.text=text
		self.list=[]
		self.add(text)
	def add(self,str):
		self.list.append(str)
		self.text=""
		
		map(self.concatenar,self.list)
	def pop(self):
		try:
			self.list.pop()
		except:
			return False
		self.text=""
		map(self.concatenar,self.list)    
		return True
	def concatenar(self,str):
		self.text=self.text+str
