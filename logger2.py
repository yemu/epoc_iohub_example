from epoc_iohub import EmotivDevice
from time import clock, sleep
import sys
from multiprocessing import Process

# Enumerations for EEG channels (14 channels)
CH_F3, CH_FC5, CH_AF3, CH_F7, CH_T7,  CH_P7, CH_O1,\
CH_O2, CH_P8,  CH_T8,  CH_F8, CH_AF4, CH_FC6,CH_F4 = range(14)

emotiv = EmotivDevice()

emotiv.startAcuisition()
from psychopy.core import getTime
import numpy as np

SAMPLE_SIZE=1000

def printGroupStats(sample_array,sample_count,sample_type_label):
    if  sample_count > 0:
        sample_array=sample_array[:sample_count]

    if  sample_count > 0 or  sample_count == -1:
        print sample_type_label,' ( in msec ):'
        print '\tCount:',len(sample_array)
        print '\tMin:',sample_array.min()
        print '\tMax:',sample_array.max()
        print '\tmean:',sample_array.mean()
        print '\tmedian:',np.median(sample_array)
        print '\tstd:',sample_array.std()
        print
    else:
        print 'Warning: {0} collected no sample data'.format(sample_type_label)

def checkTiming(get_func):

    signal_durs = np.zeros(SAMPLE_SIZE)
    sig_i,none_i= 0,0
    tot_time=getTime()*1000
    start_time=0
    count = 0
    while start_time- tot_time<=10000:
        start_time=getTime()*1000.0
        signal = get_func()
        if not signal==None:
            count+=1
            print signal
        sig_time=getTime()*1000.0
        sig_dur=sig_time-start_time

        if sig_i<SAMPLE_SIZE:
            signal_durs[sig_i]=sig_dur
            sig_i+=1
        elif sig_i==SAMPLE_SIZE and sig_i!=-1:
            sig_i=-1
    print count
    printGroupStats(signal_durs,sig_i,"Read Stats - %s" % get_func.__name__)

checkTiming(emotiv.getSignal)
#checkTiming(emotiv.getBatteryLevel)
#checkTiming(emotiv.getGyroFromQueue)
#checkTiming(emotiv.getGyroY)
