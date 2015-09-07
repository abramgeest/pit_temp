import os
import math
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import datetime
from dateutil.relativedelta import relativedelta

def date2str(date):
  "converts a datetime.datetime object to a str of the format of the pandas index"
  str="{:4d}-{:0>2d}-{:0>2d}-{:0>2d}".format(date.year,date.month,date.day,date.hour)
  return str

def str2date(s):
  "converts a string of the pandas index formate to a datetime.datetime object"
  sl=[int(i) for i in s.split('-')]
  d=datetime.datetime(sl[0],sl[1],sl[2],sl[3])
  return d
  
def gendt(i):
  "creates a timedelta object with i=hours"
  return datetime.timedelta(hours=i)

def strdate_add(s,i):
  "given a string date and the number of hours to add gives new string"
  #return date2str(str2date(ilist[i])+gendt(-1+count))
  return date2str(str2date(s)+gendt(i))

def  clean_col(Atrain):
  #This data cleaning doesn't consider things like press=0, or wierd T jumps
  for col in ['tc']:
    ilist=Atrain[Atrain[col].isnull()].index.tolist()
    i=0
    while i<=len(ilist)-1:
      count=2
      while math.isnan(Atrain.loc[strdate_add(ilist[i],-1+count),col]):
        count=count+1
      diff=(Atrain.loc[strdate_add(ilist[i],-1+count),col]-Atrain.loc[strdate_add(ilist[i],-1),col])/count
      Atrain.loc[ilist[i],col]=Atrain.loc[strdate_add(ilist[i],-1),col]+diff
      i=i+1
    ilist=Atrain[Atrain[col].isnull()].index.tolist()
    for i in range(0,len(ilist)):
      print col,i,ilist[i]
  return Atrain

def features_gen(train,yr,mo,da,hr):
   "makes a row from the data for a given time"
   d=datetime.datetime(yr,mo,da,hr)
   N=24
   #dateinfo holds the date, ts has the temp/press for the last N hours,
   #  odates is tc for 24 hrs, 1 week, 1month, 3month,6month,9mo, 1 yr, 2yr, 3yr
   #  and tres is the temp of that time to be trained against
   strdate="{:4d}-{:0>2d}-{:0>2d}-{:0>2d}".format(d.year,d.month,d.day,d.hour)
   dateinfo=np.array([yr,mo,da,hr])
   if strdate in train.index:
     tres=np.array([train.loc[strdate,'tc']])
   else:
     tres=np.array([-100])
   ts=np.arange(1,N+1)
   for i in range(1,len(ts)+1):
     dt=datetime.timedelta(hours=-i)
     di=d+dt
     strdate="{:4d}-{:0>2d}-{:0>2d}-{:0>2d}".format(di.year,di.month,di.day,di.hour)
     ts[N-i]=train.loc[strdate,'tc']
   odates=np.arange(11)
   tstr=date2str(d+relativedelta(days=-1))
   odates[0]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(days=-7))
   odates[1]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(months=-1))
   odates[2]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(months=-3))
   odates[3]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(months=-6))
   odates[4]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(months=-9))
   odates[5]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(years=-1))
   odates[6]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(years=-2))
   odates[7]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(years=-3))
   odates[8]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(years=-4))
   odates[9]=train.loc[tstr,'tc']
   tstr=date2str(d+relativedelta(years=-5))
   odates[10]=train.loc[tstr,'tc']
   tsavg=np.average(ts)
   row=np.concatenate((dateinfo,ts,odates,tres),axis=0)
   return row
