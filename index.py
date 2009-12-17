#!/usr/bin/env python
# encoding: utf-8

import os
import re
import datetime
from temps import TempsDate

path = '/Users/juliend2/Desktop/Dropbox/perso/ressources/TEMPS/'

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
print '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'
print '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
print '<title>TemPy</title>'
print '</head><body>'

timeslist= []
dateslist= []

dirList=os.listdir(path) # get the files in the directory
for fname in dirList:
	match = re.match('(\d\d)\-(\d\d)\-(\d\d)\.txt', fname) # get the txt files
	if match:
		time=TempsDate(match.group(1), match.group(2),match.group(3))
		timeslist.append(time)
		dateslist.append(datetime.date(int(match.group(1))+2000, int(match.group(2)), int(match.group(3))))
		# print time.to_filename()+ '<br/>'
		
now = datetime.date.today()

# print timeslist[0].date.day # the first day

print '<table border="1"><tr>'

for d in range(0, (now-timeslist[0].date).days):
	currentdate = timeslist[0].date + datetime.timedelta(days=d)
	if currentdate.weekday() == 0:
		print '</tr><tr>'
	print '<td>'
	print str(currentdate)
	currTemps = datetime.date(currentdate.year, currentdate.month, currentdate.day)
	if currTemps in dateslist:
		tdateobj = TempsDate(currentdate.strftime("%y"), currentdate.month, currentdate.day)
		datefile = open(path + tdateobj.to_filename())
		# lines = ''.join(datefile.readlines())
		hourblocs = re.split('\n\t?\n', ''.join(datefile.readlines()))
		
		
	print '</td>'
	
print '</tr></table>'

print '</body></html>'
