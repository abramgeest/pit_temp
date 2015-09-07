import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import math
from os import listdir
import lib_input as li
import datetime
print "Now we are plotting data"
dir='/Users/abramvandergeest/fun+progs/pit_weather/'
dir='/Users/abramvandergeest/fun+progs/pit_git/'
rangestadate, rangefindate,trainstadate, trainfindate,dir,numyear,runtest,tz=li.input_parameters('input.txt')

file="today.csv"
pp = PdfPages('today.pdf')
now=datetime.datetime.now()
dstr="2015-07-30"
dstr="{:4d}-{:0>2d}-{:0>2d}".format(now.year,now.month,now.day)

pdf=pd.read_csv(dir+'/'+file,index_col='date')
meas=[71,71,72,69,70,71,69,68,68,72,76,78,81,83,85]
meas=map(lambda tf:10*(float(tf)-32)*5/9,meas)
meas=map(lambda tf:float(tf)/10,meas)
meas=pdf['exp'].values
#meas2=pdf['exp'].values.remove("    ")
#meas=print meas
print meas[3]

xlab="time (hr) today, {}".format(dstr)
plt.figure(0) 
plt.grid(True)
plt.xlabel(xlab)
plt.ylabel('T(C)')
#plt.plot(pdf['forest'].values,'rs-',pdf['ada'].values,'bo-',pdf['extra'].values,'g^-',meas,'kD-')
plt.plot(meas,'kD-',label='Measeured')
plt.plot(pdf['forest'].values,'rs-',label='Random Forest')
plt.plot(pdf['extra'].values,'g^-',label='Extra Trees')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,  ncol=3, mode="expand", borderaxespad=0.)
pp.savefig(plt.figure(0))
pp.close()

