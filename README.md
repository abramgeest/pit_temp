Summary:
I decided to learn some basic data science techniques for handling data and for machine
learning.  There for I started with a messy data set (The hourly weather data for Pittsburg
from 1992 onward) cleaned it and use it to perform some basic machine learning to try to
predict the temperature in Pittsburg.

Goal of progam:
1) To predict the temperature in Pittsburg PA for "today"
2) This program was written with the intent to learn basic data science machine
   learning techniques.

Non-standard Required Packages:
scikit-learn
pandas
numpy
matplotlib

How to run:
To run the main program use "python fit_weather.py".  This prints out the predicted
temperatures (the meathods are "for"= Random Forest, "ada"= ADA Boost, "ext"=Extra
Trees, and "measured"=NOAA if that time has already past(does not effect any of the
predictions for the day)), and generates the file used to plot today's temperature
and the files used to print the last months fit for analysis.

After running the main program use "today_plot.py" to plot today's temperature.
After running the main program use "plot.py" to plot the last complete month of data
to get an idea of how good the fits are (they are okay but read the caveats below).

Data:
The list of weather data at "http://www.erh.noaa.gov/pbz/hourlywx/" includes the temperature,
pressure, relative humidity, etc. hourly from mid 1992 to until today.  In the middle of
February 2000 the format changed such that the date is listed with every hourly entry.
For my analysis I use the data from March 2000 onwards.


Required directories:
"raw_data" - files from NOAA with all lines but data removed
"file2print"- files used in "plot.py" to plot the last full month's data (for test)

Inputs:
The file "input.txt" contains the inputs for this program.  Either " " or "=" can be
used to separate flag and value.
  Flags:
    numyears = number of years of the three month period including today to use in
      training
    test = determines if data for the last full month of data is printed for analysis
      true if =1, false if =0
    dir = the directory to use for this project
    tz =  timezone relative to Pittsburg

Caveats:
Ths was done as a quick study of machine learning.  I learned a lot, but this implementation
is not optimized.  I am working on a newer version that is set up much better, but this is
what I had time to post.


Future:
I am currently writing an new version with sqlite3 handeling the data (to speed things up) 
that is more efficient with the data cleaning.

is not optimized.  I am working on a newer version that is set up much better, but this is
what I had time to post.
