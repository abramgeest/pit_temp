#!/usr/bin/python
#Filename get_lib.py
import os
import urllib
import math
import datetime
from dateutil.relativedelta import relativedelta

def data_cr(tz):
  "given a time zone (distance to EST) see if data is up to date"
  today=datetime.datetime.now()
  good=[' EST ',' EDT ']
  tyr=today.year
  tmo=today.month
  tda=today.day
  thr=today.hour
  print tyr,tmo,tda,thr
  file="raw_data/hr_pit_{:0>4d}.{:0>2d}".format(tyr,tmo)
  tf=open(file,'r')
  lines=tf.readlines()
  tf.close()
  for line in lines:
    if any(g in line for g in good):
      ol=line
  ol=cl(ol).strip().split()
  dyr=int(ol[3])
  dmo=int(ol[1])
  dda=int(ol[2])
  dhr=int(ol[0])
  print ol
  datatime=datetime.datetime(dyr,dmo,dda,dhr)
  dt=-2+tz
  dt=datetime.timedelta(hours=dt)
  print datatime
  if today+dt>datatime:
    return 1
  return 0

def text2csv(ld,year,month,day):
  "takes a line string and converts it into a csv data file in C,month as integer"
  #ld=line2.strip().split()      
  if len(ld)<10: 
    la=[None,None,None,None,None,None,None,None,None,None]
    la[0]=ld[0] ;    la[1]=month;    la[2]=day ;    la[3]=year
    la[4]='NA'  ;    la[5]='NaN';    la[6]='NaN' ;    la[7]='NaN'
    la[8]='MISG';    la[9]='NaN'
    ld=la
  hr=ld[0];  mo=ld[1];  da=ld[2];  yr=ld[3];  we=ld[4];  tf=ld[5];  df=ld[6];  rh=ld[7]; wd=ld[8];  pr=ld[9][:5] 
  #Checking if there are any missing values and making sure they 
  #   are passed through to be delt with later
  #I also convert F to tenths of C and inch Mercury to tenths of hecopascals
  if math.isnan(float(tf)):
    tc=float('NaN')
  else:
    tc=int(10*(float(tf)-32)*5/9)
  if math.isnan(float(df)):
    dc=float('NaN')
  else:
    dc=int(10*(float(df)-32)*5/9)
  pr=float(pr)
  if math.isnan(pr):
    pmm=float('NaN')
  else:
    pmm=int(3386*pr)/10  #in mercury to tenths of hectopascals
  rh=float(rh)
  #print line in csv format
  date="{}-{}-{}-{}".format(yr,mo,da,hr)
  out="{},{},{},{},{},{},{}\n".format(date,tc,dc,rh,pmm,wd,we)
  return out
  
def num2month(str):
  "converts number to month"
  mo=int(str)
  if   mo==1 :out="JAN"
  elif mo==2 :out="FEB"
  elif mo==3 :out="MAR"
  elif mo==4 :out="APR"
  elif mo==5 :out="MAY"
  elif mo==6 :out="JUN"
  elif mo==7 :out="JUL"
  elif mo==8 :out="AUG"
  elif mo==9 :out="SEP"
  elif mo==10:out="OCT"
  elif mo==11:out="NOV"
  elif mo==12:out="DEC"
  return out


def cl(line):
  "cleans up the line into more usaeable data"
  m=1
  out=line
  out=out.replace('EDT','')
  out=out.replace('EST','')
  for mo in {"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"}:
    if   mo=="JAN": m=1
    elif mo=="FEB": m=2
    elif mo=="MAR": m=3
    elif mo=="APR": m=4
    elif mo=="MAY": m=5
    elif mo=="JUN": m=6
    elif mo=="JUL": m=7
    elif mo=="AUG": m=8
    elif mo=="SEP": m=9
    elif mo=="OCT": m=10
    elif mo=="NOV": m=11
    elif mo=="DEC": m=12
    month=" {:0>2d}".format(m)
    out=out.replace(mo,month)
  for i in range(1,12):
    am="{: >2d}AM".format(i)
    mil=" {:0>2d}".format(i)
    out=out.replace(am,mil)
  out=out.replace('12AM',' 00')
  for i in range(1,12):
    pm="{: >2d}PM".format(i)
    mil=" {:0>2d}".format(i+12)
    out=out.replace(pm,mil)
  out=out.split('WCI',1)[0]
  out=out.split('   .',1)[0]
  out=out.replace('12PM',' 12')
  out=out.replace('FRZ DRZL','FRZDRZL ')
  out=out.replace('DRZL/FOG','DRZLFOG ')
  out=out.replace('LGT RAIN','LGTRAIN ')
  out=out.replace('LT RAIN ','LGTRAIN ')
  out=out.replace('HVY RAIN','HVYRAIN ')
  out=out.replace('FRZ RAIN','FRZRAIN ')
  out=out.replace('LGT SNOW','LGTSNOW ')
  out=out.replace('HVY SNOW','HVYSNOW ')
  out=out.replace('MIX PCPN','MIXPCPN ')
  out=out.replace('MM.MMM','NaN   ')
  out=out.replace('MM ','NaN   ')
  out=out.replace('N/A','NaN')
  out=out.replace('NOT AVBL','  NA    NaN NaN NaN MISG        NaN ')
  return out

