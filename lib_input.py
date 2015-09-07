import os
import datetime

def input_parameters(file):
  "sets up the dates and info for starting the precition"
  numyear=3
  test=0

  today=datetime.datetime.now()

  month=today.month
  year=today.year

  rangestadate=datetime.datetime(2006,01,01,0)
  rangefindate=datetime.datetime(2015,07,16,18)

  trainstadate=datetime.datetime(year-numyear-1,month-1,1,0)
  #make sure the last day works for the month
  day=31
  if month+1==2:day=28
  elif month+1==4 or month+1==6 or month+1==9 or month+1 == 1:
    day=30
  trainfindate=datetime.datetime(year-numyear-1,month+1,day,23)
  print trainstadate,trainfindate

  rangestadate=datetime.datetime(trainstadate.year-5,01,01,0)
  rangefindate=today

  dir= os.getcwd()+"/"
  filename=dir+file
  f=open(filename,'r')
  line=f.readline()
  while(line):
    info=line.split('#')[0]
    flags=info.replace("="," ").split()
    if   flags[0]=="numyears": numyear=int(flags[1])
    elif flags[0]=="test": test=int(flags[1])
    elif flags[0]=="dir": dir=flags[1]
    elif flags[0]=="tz": tz=int(flags[1])
    
    #print flags
    line=f.readline()
  f.close()

  out = (rangestadate, rangefindate,trainstadate, trainfindate,dir,numyear,test,tz)
  return out

