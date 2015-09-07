print "importing modules"
import os
import math
import pandas as pd
import numpy as np
from sklearn.ensemble  import RandomForestRegressor
from sklearn.ensemble  import ExtraTreesClassifier
from sklearn.tree      import DecisionTreeRegressor
from sklearn.ensemble  import AdaBoostRegressor
from sklearn.externals import joblib
import datetime
import lib_fit as lf 
import lib_getbig as lgb
from dateutil.relativedelta import relativedelta
import lib_input as li


print "Defining inputs"
rangestadate, rangefindate,trainstadate, trainfindate,dir,numyear,runtest,tz=li.input_parameters('input.txt')

dir1=dir+"/raw_data"
if not os.path.exists(dir1):
  os.makedirs(dir1)

dir1=dir+"/file2plot"
if not os.path.exists(dir1):
  os.makedirs(dir1)

#print dir
print "getting info for training"
print "DOWNLOADING FILES (TRAIN)"
lgb.download_files(rangestadate,rangefindate,dir)
print "PROCESSING FILES INTO data_0.csv (TRAIN)"
lgb.preprocessing(rangestadate,rangefindate,dir)
lgb.processing('data_0.csv')

print "reading and cleaning training data"
mypath='/Users/abramvandergeest/fun+progs/pit_weather/'
mypath=dir
csvfile='data_0.csv'
file=mypath+'/'+csvfile
train=pd.read_csv(file,index_col='date')
train=lf.clean_col(train)

print 'We need to take the training data and put it in a format of ["features","trained result"]'
a=[]
for i in range(0,numyear):
  dy=relativedelta(years=i)
  datei=trainstadate+dy
  date =trainfindate+dy
  dt = datetime.timedelta(hours=1)
  while(datei<date):
    row=lf.features_gen(train,datei.year,datei.month,datei.day,datei.hour)
    l=len(row)
    a.append(row)
    datei=datei+ dt

a=np.vstack(a)

print l

print 'Now we are machine learning'

print "forest learning"
M=1
forest = RandomForestRegressor(n_estimators = 150)
forest = forest.fit(a[:,:l-M],a[:,l-M])
print "extra tree learning"
extra = ExtraTreesClassifier(n_estimators = 150)
extra=extra.fit(a[:,:l-M],a[:,l-M])
print "ada learning"
rng = np.random.RandomState(1)
ada=AdaBoostRegressor(DecisionTreeRegressor(max_depth=4), n_estimators=250, random_state=rng)
ada.fit(a[:,:len(a[0])-M],a[:,len(a[0])-M])

print "predicting with test data"

print "reading and cleaning test data"
test=train[train.index!='2000-01-01-00']

#Writing a file for each day of a month with the predicted versus measeured data
#setting up dataframes to hold the predicted data for each prediction meathod
testada=test[test.index!='2000-01-01-00']#copies dataframe without directly referencing the same data
testfor=test[test.index!='2000-01-01-00']
testext=test[test.index!='2000-01-01-00']

#setting up the start day/time
now=datetime.datetime.now()
month=now.month-1
startday=datetime.datetime(now.year,now.month-1,01,0)
print "start day:",startday
numdays=31
if month==2:numday=28
elif month==4 or month==6 or month==9 or month == 1:
  numday=30
dt = datetime.timedelta(hours=1)
#loop over each day in the month
if runtest==1: 
  for i in range(0,numdays):
   #setting up day and file for the day's data
   d=startday+relativedelta(days=i)
   di=d
   file=dir+"/file2plot/plotdata{}.csv".format(lf.date2str(di))
   fplot=open(file,'w')
   header="date,meas,forest,fdiff,ada,adiff,ext,ediff\n"
   fplot.write(header)
   #loop over each hr in the day
   for i in range(0,24):
     di=di+dt

     #getting experimental data
     meas=test.loc[lf.date2str(di),'tc']

     #getting random forest prediction and setting storing it for further use
     newdffor=pd.DataFrame({'tc':[-1000],'dc':[-1000],'rh':[-1000],'pdp':[-1000],'wd':['NA'],'we':['NA']},index=['2000-01-01-00'])
     brft=lf.features_gen(testfor,di.year,di.month,di.day,di.hour)
     out   =forest.predict(brft[:len(brft)-1])[0]
     newdffor.index=[lf.date2str(di)]
     newdffor.loc[lf.date2str(di),'tc']=out
     newdffor.loc[lf.date2str(di),'we']='FORPRED'
     testfor=testfor[testfor.index!=lf.date2str(di)]
     testfor=pd.concat([testfor,newdffor])
     frtdiff=out/10-meas/10

     #getting ada prediction and setting storing it for further use
     newdfada=pd.DataFrame({'tc':[-1000],'dc':[-1000],'rh':[-1000],'pdp':[-1000],'wd':['NA'],'we':['NA']},index=['2000-01-01-00'])
     bada=lf.features_gen(testada,di.year,di.month,di.day,di.hour)
     outada=ada.predict([bada[:len(bada)-1]])[0]
     newdfada.index=[lf.date2str(di)]
     newdfada.loc[lf.date2str(di),'tc']=outada
     newdfada.loc[lf.date2str(di),'we']='ADAPRED'
     testada=testada[testada.index!=lf.date2str(di)]
     testada=pd.concat([testada,newdfada])
     adadiff=outada/10-meas/10

     #getting random forest prediction and setting storing it for further use
     newdfext=pd.DataFrame({'tc':[-1000],'dc':[-1000],'rh':[-1000],'pdp':[-1000],'wd':['NA'],'we':['NA']},index=['2000-01-01-00'])
     bext=lf.features_gen(testext,di.year,di.month,di.day,di.hour)
     outext=extra.predict(bext[:len(brft)-1])[0]
     newdfext.index=[lf.date2str(di)]
     newdfext.loc[lf.date2str(di),'tc']=out
     newdfext.loc[lf.date2str(di),'we']='FORPRED'
     testext=testext[testext.index!=lf.date2str(di)]
     testext=pd.concat([testext,newdfext])
     extdiff=outext/10-meas/10

     #writing to file
     s2="{:0>4d}-{:0>2d}-{:0>2d}:{:0>2d},{:4.1f},{:4.1f},{:4.1f},{:4.1f},{:4.1f},{:4.1f},{:4.1f}\n".format(di.year,di.month,di.day,di.hour,meas/10,out/10,frtdiff,outada/10,adadiff,outext/10,extdiff)
     fplot.write(s2)
  
  fplot.close()

print "Pridicting the next 24hrs"
ft=open('today.csv','w')
header="date,forest,ada,extra,exp\n"
ft.write(header)
now=datetime.datetime.now()
d=datetime.datetime(now.year,now.month,now.day,0)
#setting up dataframes to hold the predicted data for each prediction meathod
#copies dataframe without directly referencing the same data
testada=test[test.index!='2000-01-01-00']
testfor=test[test.index!='2000-01-01-00']
testext=test[test.index!='2000-01-01-00']
#looping over 24s using the previously predicted temp in the features
for i in range(0,24):
  #setting up the date`
  dt = datetime.timedelta(hours=i)
  di=d+dt
  date=datetime.datetime(di.year,di.month,di.day,di.hour)
  strdate="{:4d}-{:0>2d}-{:0>2d}-{:0>2d}".format(date.year,date.month,date.day,date.hour)
  try:
    exp=test.loc[strdate,'tc']
  except:
    exp=9999

  #getting random forest prediction and setting storing it for further use
  newdffor=pd.DataFrame({'tc':[-1000],'dc':[-1000],'rh':[-1000],'pdp':[-1000],'wd':['NA'],'we':['NA']},index=['2000-01-01-00'])
  brft=lf.features_gen(testfor,di.year,di.month,di.day,di.hour)
  out   =forest.predict(brft[:len(brft)-1])[0]
  newdffor.index=[lf.date2str(di)]
  newdffor.loc[lf.date2str(di),'tc']=out
  newdffor.loc[lf.date2str(di),'we']='FORPRED'
  newdffor.head(0)
  testfor=testfor[testfor.index!=lf.date2str(di)]
  testfor=pd.concat([testfor,newdffor])

  #getting ada prediction and setting storing it for further use
  newdfada=pd.DataFrame({'tc':[-1000],'dc':[-1000],'rh':[-1000],'pdp':[-1000],'wd':['NA'],'we':['NA']},index=['2000-01-01-00'])
  bada=lf.features_gen(testada,di.year,di.month,di.day,di.hour)
  outada=ada.predict([bada[:len(bada)-1]])[0]
  newdfada.index=[lf.date2str(di)]
  newdfada.loc[lf.date2str(di),'tc']=outada
  newdfada.loc[lf.date2str(di),'we']='ADAPRED'
  testada=testada[testada.index!=lf.date2str(di)]
  testada=pd.concat([testada,newdfada])

  #getting random forest prediction and setting storing it for further use
  newdfext=pd.DataFrame({'tc':[-1000],'dc':[-1000],'rh':[-1000],'pdp':[-1000],'wd':['NA'],'we':['NA']},index=['2000-01-01-00'])
  bext=lf.features_gen(testext,di.year,di.month,di.day,di.hour)
  outext=extra.predict(bext[:len(brft)-1])[0]
  newdfext.index=[lf.date2str(di)]
  newdfext.loc[lf.date2str(di),'tc']=out
  newdfext.loc[lf.date2str(di),'we']='FORPRED'
  testext=testext[testext.index!=lf.date2str(di)]
  testext=pd.concat([testext,newdfext])
  if exp != 9999: 
    e="{:4.1f}".format(exp/10) 
  else: 
    e="NaN"

  #exporting
  #s2="{:0>4d}-{:0>2d}-{:0>2d}:{:0>2d},{:4.1f},{:4.1f},{:4.1f}\n".format(di.year,di.month,di.day,di.hour,out/10,outada/10,outext/10)
  s2="{:0>4d}-{:0>2d}-{:0>2d}:{:0>2d},for={:4.1f},ada={:4.1f},ext={:4.1f},measured={:4s}".format(di.year,di.month,di.day,di.hour,out/10,outada/10,outext/10,e)
  print s2
  s="{:0>4d}-{:0>2d}-{:0>2d}:{:0>2d},{:4.1f},{:4.1f},{:4.1f},{:4s}\n".format(di.year,di.month,di.day,di.hour,out/10,outada/10,outext/10,e)
  ft.write(s)
ft.close()
