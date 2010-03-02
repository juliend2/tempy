#!/usr/bin/env python2.5
# encoding: utf-8

import os
import re
import cgi
import datetime
import types
from temps import TempsDate,HourBloc,jourdesemaine
import locale

locale.setlocale(locale.LC_NUMERIC, "fr_FR.UTF-8")


path = open('timepath.conf').read().strip()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>TemPy</title>
<link href="/static/styles.css" media="screen" rel="stylesheet" type="text/css" />
</head><body>"""

timeslist= []
dateslist= []

dirList=os.listdir(path) # get the files in the directory
dirList.sort()
qs = cgi.FieldStorage()
try:
	from_date = qs.getvalue('from')
	if type(from_date) is not None:
		dirList = dirList[dirList.index(from_date+'.txt'):]
except :
	pass
print '<p>'+str(len(dirList)) + ' jours calcul&eacute;s</p>'
print '<h1><a href="index.py">Voir Tous</a></h1>'
for fname in dirList:
	match = re.match('(\d\d)\-(\d\d)\-(\d\d)\.txt', fname) # get the txt files
	if match:
		time=TempsDate(match.group(1), match.group(2),match.group(3))
		timeslist.append(time)
		dateslist.append(datetime.date(int(match.group(1))+2000, int(match.group(2)), int(match.group(3))))
		# print time.to_filename()+ '<br/>'
		
now = datetime.date.today()

# print timeslist[0].date.day # the first day

print '<table border="0" width="100%" cellpadding="0" cellspacing="0"><tr>'

projects = {}

for d in range(0, (now-timeslist[0].date).days+1):
	currentdate = timeslist[0].date + datetime.timedelta(days=d)
	if currentdate.weekday() == 0:
		print '</tr><tr>'
	print '<td valign="top" width="14%"><span class="weekday">'+jourdesemaine(currentdate.weekday())+'</span>'
	print '<h1><a href="index.py?from='+currentdate.strftime("%y-%m-%d")+'">'+currentdate.strftime("%d %B %Y") + '</a></h1>'
	currTemps = datetime.date(currentdate.year, currentdate.month, currentdate.day)
	if currTemps in dateslist:
		tdateobj = TempsDate(currentdate.strftime("%y"), currentdate.month, currentdate.day)
		datefile = open(path + tdateobj.to_filename())
		hourblocs = re.split('\n(\t|    |  |)\n', ''.join(datefile.readlines()))
		totalminsbloc = 0
		for bloc in hourblocs:
			try:
				hbloc = HourBloc(bloc)
				print "<h2>"+hbloc.temps_desc+":</h2>"
				hours = hbloc.get_minutes()/60
				mins = hbloc.get_minutes()%60
				projects.get(hbloc.proj_name, hbloc.get_minutes())
				try:
					projects[hbloc.proj_name] += hbloc.get_minutes()
				except KeyError:
					projects[hbloc.proj_name] = hbloc.get_minutes()
				totalminsbloc += hbloc.get_minutes()
				print "<p>"+str(hours)+'h'+ "%02d"%mins +"</p>"
				
			except AttributeError: # when we grab a line that is not a project bloc
				pass
		totalhours =totalminsbloc/60
		totalmins = totalminsbloc%60
		print '<p class="total">Total: <b>'+str(totalhours)+'h'+ "%02d"%totalmins +'</b></p>'
			
		
	print '</td>'
	
print """
			</tr></table><br/>
			<h1>Total d'heures par projets :</h1>
			<dl>"""
for projname,value in projects.items():
	print '<dt>'+projname+' : </dt>'
	hours = value/60
	mins = value%60
	print '<dd>'+str(hours)+'h'+"%02d"%mins+'</dd>'
print '</dl>'
print '</body></html>'
