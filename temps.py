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
import re

def jourdesemaine(day_int):
	if day_int==0:
		return 'Lundi'
	elif day_int==1:
		return 'Mardi'
	elif day_int==2:
		return 'Mercredi'
	elif day_int==3:
		return 'Jeudi'
	elif day_int==4:
		return 'Vendredi'
	elif day_int==5:
		return 'Samedi'
	elif day_int==6:
		return 'Dimanche'
	else:
		return 'Pas un jour de semaine'

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


class HourBloc:
	proj_name = ''
	temps_desc = ''
	proj_string = ''
	def __init__(self, project_string):
		self.proj_string = project_string
		self.temps_desc = self._get_name()
		self.proj_name = self._get_short_name()

	def get_minutes(self):
		minutes = 0
		for t in self._get_hour_lines_list() :
			# print int(t.group(1))
			tfrom = datetime.datetime(2007,01,01,int(t.group(1)), int(t.group(2)))
			tto = datetime.datetime(2007,01,01,int(t.group(3)), int(t.group(4)))
			tdelta = (tto-tfrom)
			minutes += tdelta.seconds / 60
		return minutes

	def _get_name(self):
		match = re.match('([^:]+)', self.proj_string)
		return match.group(0)

	def _get_short_name(self):
		match = re.match('([^\s]+)', self.proj_string)
		return match.group(0)

	def _get_hour_lines_list(self):
		lines  = re.split('\n(\t|    |  )', self.proj_string) # *Keep the order* supports tabs, 2-space soft tabs and 4-space soft tabs. 
		tlist = []
		for line in lines:
			m = re.match('(\d?\d)h(\d\d) - (\d?\d)h(\d\d)', line) # get the hour-minutes
			if m:
				tlist.append(m) # return all the matches objects
		return tlist		



if __name__ == '__main__':
	t = TempsDate(1985,10,23)
	print t.to_filename() # should output: 85-10-23.txt
	
	h = HourBloc("coiteux (ajouter script seo) :\n\t9h25 - 9h45\n  9h55 - 10h00\n    9h55 - 10h00")
	print h._get_hour_lines_list()
 	print h.get_minutes()
	print h.proj_name
	print h.temps_desc
	
	h2 = HourBloc("micrium-salesforce :\n  15h15 - 15h55\n")
	print h2.get_minutes()



