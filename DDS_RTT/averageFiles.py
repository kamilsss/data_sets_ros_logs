#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import csv
from operator import add

A = os.listdir('.');

lenA = len(A);

i = 0;
navFiles = [];
vidFiles = [];
ddsNavFiles = [];
ddsVidFiles = [];
while i < lenA:
  if(A[i].startswith("log_file_image")):
    vidFiles.append(A[i]);
  elif(A[i].startswith("log_file_nav")):
    navFiles.append(A[i]);
  elif(A[i].startswith("log_file_dds_image")):
    ddsVidFiles.append(A[i]);
  elif(A[i].startswith("log_file_dds_nav")):
    ddsNavFiles.append(A[i]);
  i+=1;


print "Processing ",
print len(navFiles),
print " Navdata files and ",
print len(vidFiles),
print " Video Files"

if(len(navFiles) != len(vidFiles)):
  print "mismatching no. of vidFiles and navFiles.. please check current working directory.."
  exit();

i = 0;

totalNavAvg = [0 for x in range(500)]
totalVidAvg = [0 for x in range(500)]

navRange = range(0,100000,200);
vidRange = range(0,15000,30);

ddsTotalNavAvg = [0 for x in range(500)]
ddsTotalVidAvg = [0 for x in range(500)]

ddsNavRange = range(0,100000,200);
ddsVidRange = range(0,15000,30);

while i < len(navFiles):
  navLines = [line.rstrip('\n') for line in open(navFiles[i])];
  vidLines = [line.rstrip('\n') for line in open(vidFiles[i])];
  ddsNavLines = [line.rstrip('\n') for line in open(ddsNavFiles[i])];
  ddsVidLines = [line.rstrip('\n') for line in open(ddsVidFiles[i])];

  navDelays = np.zeros((500,1));
  vidDelays = np.zeros((500,1));
  ddsNavDelays = np.zeros((500,1));
  ddsVidDelays = np.zeros((500,1));

  lineCount = 0;
  while lineCount < 500:
    navDelays[lineCount] = float(navLines[lineCount]);
    vidDelays[lineCount] = float(vidLines[lineCount]);
    totalNavAvg[lineCount] += (float)(navLines[lineCount]);
    totalVidAvg[lineCount] += (float)(vidLines[lineCount]);
    ddsNavDelays[lineCount] = float(ddsNavLines[lineCount]);
    ddsVidDelays[lineCount] = float(ddsVidLines[lineCount]);
    ddsTotalNavAvg[lineCount] += (float)(ddsNavLines[lineCount]);
    ddsTotalVidAvg[lineCount] += (float)(ddsVidLines[lineCount]);

    lineCount+=1;
  i+=1;
  navDelays = np.vstack(navDelays);
  vidDelays = np.vstack(vidDelays);
  ddsNavDelays = np.vstack(ddsNavDelays);
  ddsVidDelays = np.vstack(ddsVidDelays);

totalNavAvg = [ x/len(navFiles) for x in totalNavAvg];
totalVidAvg = [ x/len(vidFiles) for x in totalVidAvg];
ddsTotalNavAvg = [ x/len(navFiles) for x in ddsTotalNavAvg];
ddsTotalVidAvg = [ x/len(vidFiles) for x in ddsTotalVidAvg];

#displaying the error bar graph for images and navdata combined
plt.ylabel('Averagea delay of last 30 Image frames (sec)')
plt.xlabel('Number of Image frames received (10mins duration)')
axes = plt.gca()
axes.set_ylim([0.02,0.15])
plt.plot(vidRange,totalVidAvg,label='MQTT Image')
plt.plot(ddsVidRange,ddsTotalVidAvg,label='DDS Image')
plt.legend()
plt.show()

plt.ylabel('Averagea delay of last 200 Navdata frames(sec)')
plt.xlabel('Number of Navdata frames received (10mins duration)')
axes = plt.gca()
axes.set_ylim([0.02,0.10])
plt.plot(navRange,totalNavAvg,label='MQTT Navdata')
plt.plot(ddsNavRange,ddsTotalNavAvg, label='DDS Navdata')
plt.legend()
plt.show()

#print len([name for name in    os.listdir('.') if os.path.isfile(name)])
