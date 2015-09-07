import os
import urllib
import math
import datetime
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from lib_get import text2csv, num2month,cl,data_cr


def download_files(start,finish,dir):
  good=[' EST ',' EDT ']
  mydir=dir
  preurl='http://www.erh.noaa.gov/pbz/hourlywx/'
  datei=start
  now=datetime.datetime.now()
  while(datei<finish):
    #print datei
    yr=datei.year
    mo=datei.month
    file= "hr_pit_{:0>2d}.{:0>2d}".format(yr-2000,mo)
    fileo="raw_data/hr_pit_{:0>4d}.{:0>2d}".format(yr,mo)
    url=preurl+file
    #print url
    out=mydir+fileo
    #print out
    if not os.path.isfile(fileo) or (yr==now.year and mo==now.month):
      urllib.urlretrieve (url, out)
      old=open(out)
      lines=old.readlines()
      old.close()

      #Getting rid of duplicate lines (common in Nov-Dec 2008)
      data=[]
      for line in lines:
        if any(g in line for g in good):
          data.append(line)
      out2=out+"test"
      out2=out
      f=open(out2,'w')
      linea=data[0]
      f.write(linea)
      for i in range(1,len(data)):
        lineb=data[i]
        if not (linea[:9] == lineb[:9]):
          f.write(lineb)
        linea=lineb

    datei=datei+ relativedelta(months=1)

def preprocessing(start,finish,dir):
  datesep=['PITTSBURGH PA AIRPORT']
  good=[' EST ',' EDT ']
  newcsv=open('data_0.csv', 'w')
  headercsv='date,tc,dc,rh,pdp,wd,we\n'
  date=finish
  datei=start
  print date
  newcsv.write(headercsv)
  while(datei<date):
    yr=datei.year
    mo=datei.month
    oldfile=dir+'raw_data/hr_pit_{:4d}.{:0>2d}'.format(yr,mo)
    old=open(oldfile)
    lines=old.readlines()
    old.close()
    month=num2month(mo)
    oldda='01'
    for line in lines:
      if any(g in line for g in good):
        line2=cl(line)+'\n'
        if len(line2.split())>=10:
          ld=line2.strip().split()
          da=ld[2]
          ldata=text2csv(ld,yr,mo,oldda)
          oldda=da
          newcsv.write(ldata)
    datei=datei+ relativedelta(months=1)
  newcsv.close()

def processing(datacsv):
  data=pd.read_csv(datacsv,index_col='date')
  sl=[int(i) for i in data.index[0].split('-')]
  sd=datetime.datetime(sl[0],sl[1],sl[2],sl[3])
  sl=[int(i) for i in data.index[data.shape[0]-1].split('-')]
  fd=datetime.datetime(sl[0],sl[1],sl[2],sl[3])
  print "starting date is",sd
  print "finishing date is",fd

  w=open(datacsv,'w')
  headercsv='date,tc,dc,rh,pdp,wd,we\n'
  w.write(headercsv)
  dt=datetime.timedelta(hours=+1)
  d=sd
  while(d<fd):
    d=d+dt
    s="{:4d}-{:0>2d}-{:0>2d}-{:0>2d}".format(d.year,d.month,d.day,d.hour)
    if not (s in data.index):
      s=s+",nan,nan,nan,nan,MISG,NA"
    else:
      temp=data.loc[s,['tc','dc','rh','pdp','wd','we']].values
      if len(temp)!=6:
        temp=temp[0]
      s=s+",{},{},{},{},{},{}".format(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5])
    s=s+'\n'
    w.write(s)
  w.close()
