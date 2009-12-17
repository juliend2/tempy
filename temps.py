#!/usr/bin/env python
# encoding: utf-8
"""
temps.py

Created by Julien Desrosiers on 2009-12-16.
Copyright (c) 2009 Julien Desrosiers. All rights reserved.
"""

import sys
import os
import datetime

class TempsDate:
	day=0
	month=0
	year=0	
	def __init__(self,year,month,day):
		self.day = int(day)
		self.month = int(month)
		self.year = int(year) + 2000 # yeah i know, pre-2000 dates wont work. too bad
		self.date = datetime.date(self.year, self.month, self.day)
	def to_filename(self):
		return self.date.strftime("%y-%m-%d.txt")

if __name__ == '__main__':
	t = TempsDate(23,10,1985)
	print t.to_filename() # should output: 85-10-23.txt

