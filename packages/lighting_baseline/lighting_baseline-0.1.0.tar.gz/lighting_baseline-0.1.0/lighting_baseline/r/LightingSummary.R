#!/usr/bin/env Rscript
#
#---------------------------------------------------------------------------------------
#Lighting Fault Detection and Energy Quantification ©2014,
#The Regents of the University of California, through Lawrence Berkeley National
#Laboratory (subject to receipt of any required approvals from the U.S.
#Department of Energy).  All rights reserved.
#
#If you have questions about your rights to use or distribute this software,
#please contact Berkeley Lab's Technology Transfer Department at TTD@lbl.gov
#referring to "Lighting Fault Detection and Energy Quantification (LBNL Ref 2014-173)".
#
#NOTICE:  This software was produced by The Regents of the University of
#California under Contract No. DE-AC02-05CH11231 with the Department of Energy.
#For 5 years from November 25, 2014, the Government is granted for itself and
#others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide
#license in this data to reproduce, prepare derivative works, and perform
#publicly and display publicly, by or on behalf of the Government. There is
#provision for the possible extension of the term of this license. Subsequent to
#that period or any extension granted, the Government is granted for itself and
#others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide
#license in this data to reproduce, prepare derivative works, distribute copies
#to the public, perform publicly and display publicly, and to permit others to
#do so. The specific term of the license can be identified by inquiry made to
#Lawrence Berkeley National Laboratory or DOE. Neither the United States nor the
#United States Department of Energy, nor any of their employees, makes any
#warranty, express or implied, or assumes any legal liability or responsibility
#for the accuracy, completeness, or usefulness of any data, apparatus, product,
#or process disclosed, or represents that its use would not infringe privately
#owned rights.
#---------------------------------------------------------------------------------------
# 
########
# Lighting Summary App
#
# Input:
#	required: 
#		time series of lighting load
# 	optional: 
#		file containing a list of holiday dates
#		
#
# Outputs:
# 	1. Mean load for each non-holiday half-hour during the week
#	2. weekend, weekday, and holiday average load shape and median load shape
#	3. Mean load on (weekday, weekend, holiday) x (day [default 6am-6pm], night) 
#	4. Number of high, medium, and low hours per week
#
# Details
#	Time intervals are assumed constant
# 	Missing data are ignored
#

library("optparse")
option_list = list(
	make_option(c("-l","--loadFile"),
		help="Name of load data file (Required)"),
	make_option(c("-H","--HolidayFile"),
		help="Name of file containing holiday dates (Optional)"),			
	make_option(c("-s","--summaryStatisticsFile"),
		default="summaryStatisticsFile.csv",
		help="Name of output file for summary statistics [default %default]"),
	make_option(c("-w","--workDays"),
		default="12345",
		help="Which days are workdays? 0 = Sunday, etc. [default %default]"),
	make_option(c("-W","--workdayStart"),
		default="6:30",
		help="When is start of 12-hour 'workday'? [default %default]"),				
	make_option(c("-v","--verbosity"),
		default=1,
		help="determine what progress and error reports to print (non-neg integer) [default %default]")	
	)
	
opt = parse_args(OptionParser(option_list=option_list))	


getTime = function(timeInfo,verbose=1) {
	# given a vector of timestamps using one of the following timestamp types, return
	# a vector of POSIXlt times:
	# 1. Year-month-day Hours:Minutes:Seconds
	# 2. Seconds since 1970-01-01 00:00:00
	# 3. Milliseconds since 1970-01-01 00:00:00
	# 
	if (verbose > 1) { print("starting getTime()")}
	if (verbose > 3) { print(timeInfo[1]) }
	if(grepl(":",timeInfo[1])[1]) {
		time = strptime(timeInfo,format="%Y-%m-%d %H:%M:%S")
	} else {
		if (!is.numeric(timeInfo[1])) {
			stop("Time is not in a recognized format")
		}
		if (timeInfo[1] > 3e9) {
			# If time is in seconds, then this would represent sometime after 2066 
			# so assume time is in milliseconds	
			timeNum = timeInfo/1000
		} else {
			timeNum = timeInfo
		}		
		time = as.POSIXlt(timeNum,origin="1970-01-01")
	}
	return(time)	
}


readLightingInputFiles = function(inLoadFile,verbose=1,intervalMinutes=15) {
	if (verbose > 1) { print("starting readInputFiles()") }
	if (verbose > 3) { 
		print(inLoadFile)
	}
	loadDat = read.table(inLoadFile,as.is=T,sep=",",header=F)
	loadTime = getTime(loadDat[,1],verbose=verbose)
	loadTimeNum = as.numeric(loadTime)	
	dataLoad = loadDat[,2]
		
	# Aggregate load data to a reasonable interval length. intervalMinutes controls
	# the timescale at which the baseline is being fit (typically will be something
	# like 15 minutes or an hour). We start by aggregating to a timescale finer than
	# intervalMinutes but not by a lot. 
	# If for example intervalMinutes=15, we aggregate to 5-minute chunks. 
	# If the original data are at, say, 20s, then this way we avoid carrying 
	# around tens or hundreds of times more data than needed.
	aggregateMinutes = intervalMinutes/3
	t0 = min(loadTime,na.rm=T)
	tLoadMinutesSinceStart = difftime(loadTime,t0,units="mins") 
	
	# If the time period between measurements is less than intervalMinutes/3, then
	# we want to accumulate multiple measurements into our time intervals: two or more
	# measurements get the same value of intervalLoadSinceStart. But if the
	# time period between measurements is already longer than intervalMinutes/3, then just
	# use the measurements as they are; each measurement gets its own intervalLoadSinceStart. 
	intervalLoadSinceStart = 1+floor(tLoadMinutesSinceStart/aggregateMinutes)
	dataLoadAggregated = aggregate(dataLoad,by=list(intervalLoadSinceStart),mean,
		na.action=na.omit)[,2]
	
	# the timestamp for the interval is the time at the _end_ of the interval
	loadTimeNum = as.numeric(loadTime)		
	timeLoadAggregatedNum = aggregate(loadTimeNum,by=list(intervalLoadSinceStart),max,
		na.rm=T)[,2]

	# We have to be explicit about the time format we want, otherwise
	#  there's a problem at midnight, e.g.: 2013-08-01 00:00:00 turns into just
	# 2013-08-01, and that causes problems later. 		
	timeLoadAggregated = strftime(
		as.POSIXlt(timeLoadAggregatedNum,origin="1970-01-01"),
		format="%Y-%m-%d %H:%M:%S")	
	
	dataTime = timeLoadAggregated  

	if (verbose > 3) { print("done reading input files; defining variables")}	
	loadVec = dataLoadAggregated
	
	
	Out = NULL
	Out$dataTime = dataTime
	Out$loadVec = loadVec
	if (verbose > 1) { print("leaving readInputFiles") }
	return(Out)
}	

AggregateLoad = function(timestamp,load,outIntervalMinutes=15,
	thresholdPct = 50, verbose=1 ) {
	if (verbose > 1) { print("starting AggregateLoad()") }
	# Given load data collected at specified times, calculate the
	# average load at different time intervals.
	# If some data are missing from an output interval, adjust for them if the percent 
	#   missing is under a specified threshold; otherwise return NA for the interval
	
	time = getTime(timestamp,verbose=verbose)
	# If load is reported as NA, discard that data point
	iWhichOK = which(!is.na(load))
	time = time[iWhichOK]
	load = load[iWhichOK]
	
	timeNum = as.numeric(time)
	nT = length(timeNum)
	timeDiff = timeNum[2:nT] - timeNum[1:(nT-1)]
	loadMeasurementIntervalSec = median(timeDiff,na.rm=T) # time interval in seconds
				
	# calculate the cumulative energy as of the end of each measured interval; convert
	# to kWh instead of kWs:
	cumEnergy = cumsum(loadMeasurementIntervalSec * load)/3600 
	cumEnergy = c(0,cumEnergy)
	
	# find start of first load time interval
	time0 = time[1] - loadMeasurementIntervalSec	
	timeEnergyNum = c(as.numeric(time0),timeNum)
	
	# Find the first output interval for which the load is completely known
	# Choose possible interval end times by starting the possibilities on an hour.
	# (We expect outIntervalMinutes to divide into 60, although we don't require it)
	# The first "pretty" output time that is after the start of the first load
	# interval will not necessarily work, since the load interval may be too
	# short. For instance, if the first load interval is 20s long and runs 
	# from 8:59:45 to 9:00:05, 9:00 will not work for the first output interval if we
	# want intervals to be 15 minutes long. Step through output interval start times
	# until we find one that works.
	endTime = time[1] - (time[1]$min*60 + time[1]$sec)
	startTime = endTime - outIntervalMinutes*60 
	goodInterval = F
	while (!goodInterval) {
		if (startTime >= time0) {
			timeOutNum = seq(from=as.numeric(endTime),to=timeNum[nT],
				by=outIntervalMinutes*60)
			goodInterval = T	
		} else {
			startTime = endTime
			endTime = endTime + outIntervalMinutes*60
		}			
	}		
	  	
	outIntervalSec = outIntervalMinutes*60
	cumEnergyAtOutIntervalEnd = approx(timeEnergyNum,cumEnergy,timeOutNum)$y
	cumEnergyAtOutIntervalStart = approx(timeEnergyNum,cumEnergy,timeOutNum-outIntervalSec)$y
	energyOut = cumEnergyAtOutIntervalEnd - cumEnergyAtOutIntervalStart
	powerOut = energyOut/(outIntervalMinutes/60)  # Energy is in kWh, so use time in hours

	# #
	# Determine what fraction of seconds in each interval have meter data
	cumSecWithKnownLoad = c(0,cumsum(rep(loadMeasurementIntervalSec,nT)))
	cumSecKnownAtIntervalEnd = approx(timeEnergyNum,cumSecWithKnownLoad,timeOutNum)$y
	cumSecKnownAtIntervalStart = approx(timeEnergyNum,cumSecWithKnownLoad,timeOutNum-outIntervalSec)$y	
	secKnownInInterval = cumSecKnownAtIntervalEnd - cumSecKnownAtIntervalStart
	fracMissingInInterval = 1-secKnownInInterval/(outIntervalMinutes*60)

	okCorrectMissing = fracMissingInInterval < 
		(thresholdPct)/100
	powerOut[okCorrectMissing] = 
		powerOut[okCorrectMissing]/(1-fracMissingInInterval[okCorrectMissing])
	powerOut[!okCorrectMissing] = NA

	nP = length(powerOut)
	if (is.na(powerOut[nP])) {
		# Not enough data to complete the final interval so discard it
		powerOut = powerOut[-nP]
		timeOutNum = timeOutNum[-nP]
		fracMissingInInterval = fracMissingInInterval[-nP] 
	}
	
	timeOut = as.POSIXlt(timeOutNum,origin="1970-01-01")
	
	Out = NULL
	Out$time = timeOut
	Out$timeNum = timeOutNum
	Out$load = powerOut
	Out$intervalMinutes = outIntervalMinutes
	Out$loadMeasurementIntervalMinutes = loadMeasurementIntervalSec/60
	Out$pctMissing = round(100*fracMissingInInterval,3)
	
	if(verbose > 1) {print("leaving AggregateLoad()") }
	return(Out)
}


calcSummaryStats = function(timeVec,loadVec,workdays="12345",workhoursStart="06:30",
	holidayDates=NULL, summaryStatisticsFile=summaryStatisticsFile,
		intervalMinutes=30,verbose=1) {
	if (verbose > 1) { print("starting calcSummaryStats()") }
		if(is.null(intervalMinutes)) {
		intervalMinutes= as.numeric(median(difftime(timeVec[2:6],timeVec[1:5],units="mins")))
	}

	if(is.null(intervalMinutes)) {
		intervalMinutes= as.numeric(median(difftime(timeVec[2:6],timeVec[1:5],units="mins")))
	}
	
	workHoursMins = as.numeric(unlist(strsplit(workhoursStart,":")))
	workStartMins = 60*workHoursMins[1]+workHoursMins[2]
	workPeriodDef=c(-1,workStartMins,workStartMins+12*60,24*60+1)
	 
	workdays = as.numeric(unlist(strsplit(workdays,split="")))
	
	dayOfWeekStartMinutes = (0:8)*(24*60)
	workdayStartMinutes = dayOfWeekStartMinutes[workdays] # 
		
	minuteOfWeek = 24*60*timeVec$wday+60*timeVec$hour + timeVec$min
	
	if (!is.null(holidayDates)) {
		okHoliday = as.character(round.POSIXt(timeVec,units="days")) %in% holidayDates
	} else {
		okHoliday = rep(F,length(timeVec))
	}
	
	# minor complication: The data from 00:00 are from the previous day. For instance, if 
	# data are aggregated to 1/2 hour, the first data point we want is from 00:30, not
	# 00:00. For a given day, we only want data that come in strictly _after_ the
	# start of the day. 
	dayOfWeek = as.numeric(cut(minuteOfWeek,breaks=dayOfWeekStartMinutes))-1  
	periodOfDay = as.numeric(cut(60*timeVec$hour + timeVec$min,breaks=workPeriodDef))
	
	okWorkday = dayOfWeek %in% workdays
	okWorkHours = periodOfDay==2
		
	workdayDayMean = mean(loadVec[okWorkday & okWorkHours & !okHoliday],na.rm=T)
	workdayNightMean =  mean(loadVec[okWorkday & !okWorkHours & !okHoliday],na.rm=T)
	nonworkdayDayMean = mean(loadVec[!okWorkday & okWorkHours & !okHoliday],na.rm=T)
	nonworkdayNightMean = mean(loadVec[!okWorkday & !okWorkHours & !okHoliday],na.rm=T)
	holidayDayMean = mean(loadVec[okWorkHours & okHoliday],na.rm=T)
	holidayNightMean = mean(loadVec[!okWorkHours & okHoliday],na.rm=T)
	
	# Depending on the length of the time series and whether it contains holidays,
	# the mean non-holiday weekly load can differ from the mean of the load time series.
	# Here we calculate the mean load for a week that contains no holidays. 
	nonHolidayWeekMean = (length(workdays)*mean(c(workdayDayMean,workdayNightMean)) +
		(7-length(workdays))*(mean(c(nonworkdayDayMean,nonworkdayNightMean))))/7

	Out = NULL
	Out$workdayDayMean = round(workdayDayMean,2)
	Out$workdayNightMean = round(workdayNightMean,2)
	Out$nonworkdayDayMean = round(nonworkdayDayMean,2)
	Out$nonworkdayNightMean = round(nonworkdayNightMean,2)
	Out$holidayDayMean = round(holidayDayMean,2)
	Out$holidayNightMean = round(holidayNightMean,2)
	Out$nonHolidayWeekMean = round(nonHolidayWeekMean,2)
	
	if(verbose > 4) { print(Out) }
	
#
	write(t(cbind(names(Out),round(unlist(Out),3))),
	summaryStatisticsFile,ncol=2,sep=",")
	
	
#	write.table(t(unlist(Out)),file=summaryStatisticsFile,sep=",",
#		row.names=T,col.names=F,quote=F)
	
	if (verbose > 1) { print("leaving calcSummaryStats()") }
	return(Out)
}



main = function(loadFile = inLoadFile,holidayFile=NULL,
	summaryStatisticsFile=summaryStatisticsFile,
	workdays="12345",workhoursStart="6:30",verbose = verbose) {
	if (verbose > 0) { print("starting main()") }
	if (verbose > 4) {
		print(paste("loadfile =",loadFile))
		print(paste("holidayFile =",holidayFile))
		print(paste("summaryStatisticsFile =",summaryStatisticsFile))
		print(paste("workdays =",workdays))
		print(paste("workhoursStart",workhoursStart))
	}	

	aa = readLightingInputFiles(loadFile,verbose=verbose)
	if (!is.null(holidayFile)) {
		bb = read.table(holidayFile,sep=",",header=F,as.is=T)
		hdates = strptime(bb[,1],format="%Y-%m-%d")
	} else {
		hdates = NULL
	}	
	
	
	agg = AggregateLoad(aa$dataTime,aa$loadVec,verbose=verbose)
	
	ss = calcSummaryStats(agg$time,agg$load,workdays=workdays,
		workhoursStart=workhoursStart,holidayDates = hdates,
		summaryStatisticsFile=summaryStatisticsFile,
		verbose=verbose)	

	if (verbose > 0) { print("leaving main()") }
	
}	


###
###
###

if (is.null(opt$loadFile)) {
	stop("Error: no input Load File is defined.")
} else {
	inLoadFile=opt$loadFile
}
if (is.null(opt$HolidayFile)) {
	holidayFile = NULL
} else {
	holidayFile = opt$HolidayFile
}
summaryStatisticsFile = opt$summaryStatisticsFile
workdays = opt$workDays
workhoursStart = opt$workdayStart

verbosity = opt$verbosity

if (verbosity > 5) {
	print(opt)
}	

main(loadFile = inLoadFile, 
	holidayFile=holidayFile,summaryStatisticsFile=summaryStatisticsFile,
	workdays=workdays,workhoursStart=workhoursStart,
	verbose = verbosity)

	