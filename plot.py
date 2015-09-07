import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import math
from os import listdir
import lib_input as li
import datetime

print "Now we are plotting data"

dir='/Users/abramvandergeest/fun+progs/pit_weather/file2plot/'
rangestadate, rangefindate,trainstadate, trainfindate,dir,numyear,runtest,tz=li.input_parameters('input.txt')
dir=dir+'/file2plot/'

now=datetime.datetime.now()

print rangefindate
print trainfindate

files=listdir(dir)
str=dir+'plotdata{:0>4d}-{:0>2d}-01-00.csv'.format(now.year,now.month-1)
month=pd.read_csv(str,index_col='date')
month['meas']=0
month['forest']=0
month['fdiff']=0
month['ada']=0
month['adiff']=0
month['ext']=0
month['ediff']=0
month['comb']=0
month['cdiff']=0
month['sum']=0
month['sdiff']=0
i=0
pp = PdfPages('daily_data_inc.pdf')
#file='plotdata2.csv'
for file in files:
  xlab="time (hr) on {}".format(file[8:18])
  pdf=pd.read_csv(dir+file,index_col='date')
  pdf['sum']=map(lambda f,a:(a+f)/2,pdf['forest'],pdf['ada'])
  pdf['sdiff']=map(lambda m,s:-(m-s),pdf['meas'],pdf['sum'])
  month['meas']=map(lambda m,p:m+p,month['meas'],pdf['meas'])
  month['forest']=map(lambda m,p:m+p,month['forest'],pdf['forest'])
  month['ada']=map(lambda m,p:m+p,month['ada'],pdf['ada'])
  month['ext']=map(lambda m,p:m+p,month['ext'],pdf['ext'])
  month['sum']=map(lambda m,p:m+p,month['sum'],pdf['sum'])
  fm= np.mean(pdf['ext'].values)
  em= np.mean(pdf['forest'].values)
  am= np.mean(pdf['ada'].values)
  pdf['comb']=map(lambda f,e:(f+e)/2-fm+am,pdf['forest'],pdf['ext'])
  pdf['cdiff']=map(lambda c,m:c-m,pdf['comb'],pdf['meas'])
  month['comb']=map(lambda m,p:m+p,month['comb'],pdf['comb'])
  #print fm,em,am
  plt.figure(i) 
  plt.subplot(211) 
  plt.grid(True)
  plt.xlabel(xlab)
  plt.ylabel('T(C)')
  #plt.legend(handles=[red,green,black])
  #plt.plot(pdf['meas'].values,'kD-',pdf['forest'].values,'rs-',pdf['ext'].values,'g^-')
  #plt.plot(pdf['meas'].values,'kD-',label='Measured')
  #plt.plot(pdf['forest'].values,'rs-',label='Random Forest')
  #plt.plot(pdf['ada'].values,'bp-',label='ADA Boost')
  #plt.plot(pdf['ext'].values,'g^-',label='Extra Trees')
  plt.plot(pdf['meas'].values,'kD-',label='Meas.')
  plt.plot(pdf['forest'].values,'rs-',label='Rand.')
  plt.plot(pdf['ada'].values,'bp-',label='ADA')
  plt.plot(pdf['ext'].values,'g^-',label='Extr.')
  plt.plot(pdf['comb'].values,'co-',label='Comb.')
  plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,  ncol=3, mode="expand", borderaxespad=0.)
  plt.subplot(212)
  plt.grid(True)
  plt.xlabel(xlab)
  plt.ylabel('abs(error)')
  #plt.plot(pdf['fdiffabs'].values,'rs-',pdf['adiffabs'].values,'bo-')
  #plt.legend(handles=[red,green,black])
  plt.plot(pdf['fdiff'].values,'rs-',pdf['ediff'].values,'g^-',pdf['adiff'].values,'bp-',pdf['cdiff'].values,'co-')
  pp.savefig(plt.figure(i))
  plt.close(plt.figure(i))
  i=i+1

month['meas']=map(lambda m:m/i,month['meas'])
month['forest']=map(lambda m:m/i,month['forest'])
month['fdiff']=map(lambda m,a:m-a,month['meas'],month['forest'])
month['ada']=map(lambda m:m/i,month['ada'])
month['adiff']=map(lambda m,a:m-a,month['meas'],month['ada'])
month['ext']=map(lambda m:m/i,month['ext'])
month['ediff']=map(lambda m,a:m-a,month['meas'],month['ext'])
month['comb']=map(lambda m:m/i,month['comb'])
month['cdiff']=map(lambda m,a:m-a,month['meas'],month['comb'])
plt.figure(i) 
date=file[8:18].split("-")
xlab="{}-{}".format(date[0],date[1])
plt.subplot(211) 
plt.grid(True)
plt.xlabel(xlab)
plt.ylabel('T(C)')
plt.plot(month['meas'].values,'k-',month['forest'].values,'rs-',month['ext'].values,'g^-',month['ada'].values,'bp-',month['comb'],'co-')
plt.subplot(212)
plt.grid(True)
plt.xlabel(xlab)
plt.ylabel('abs(error)')
plt.plot(month['fdiff'].values,'rs-',month['ediff'].values,'g^-',month['adiff'].values,'bp-',month['cdiff'],'co-')
pp.savefig(plt.figure(i))
plt.close(plt.figure(i))
pp.close()



month['fdiffabs']=map(math.fabs,month['fdiff'])
month['adiffabs']=map(math.fabs,month['adiff'])
month['ediffabs']=map(math.fabs,month['ediff'])
s="ran for avg error ={} ada avg error ={} extra trees avg error={}".format( np.average(month['fdiffabs'].values),np.average(month['adiffabs'].values),np.average(month['ediffabs'].values))
print s
