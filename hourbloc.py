#!/usr/bin/env python
# encoding: utf-8
"""
hourbloc.py

Created by Julien Desrosiers on 2009-12-16.
Copyright (c) 2009 Julien Desrosiers. All rights reserved.
"""

import sys
import os
import datetime
import re

class HourBloc:
	proj_short_name = ''
	proj_desc = ''
	proj_string = ''
	def __init__(self, project_string):
		self.proj_string = project_string
		self.proj_desc = self._get_name()
		self.proj_short_name = self._get_short_name()
		
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
		lines  = re.split('\n\t', self.proj_string)
		tlist = []
		for line in lines:
			m = re.match('(\d?\d)h(\d\d) - (\d?\d)h(\d\d)', line) # get the hour-minutes
			if m:
				tlist.append(m) # return all the matches objects
		return tlist		

	
if __name__ == '__main__':
	h = HourBloc("coiteux (ajouter script seo) :\n\t9h25 - 9h45\n\t9h55 - 10h00")
	print h._get_hour_lines_list()
 	print h.get_minutes()
	print h.get_name()
	print h.get_short_name()
