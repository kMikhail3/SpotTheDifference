from datetime import datetime
from pathlib import Path
import os
import shutil
import cv2
from matplotlib import pyplot as plt
import numpy as n
from PIL import Image, ImageChops

filesPath = r"[insert directory for unsorted images]"
files = Path(filesPath)
dayPath = Path(r"[insert directory for day path]")
nightPath = Path(r"[insert directory for night path]")

j = 0

for img in files.iterdir(): 
    
    #Take the time component from the file name, and index out the first four digits.
    nameStem = img.stem
    fileType, date, time = nameStem.split('_')
    #[0][1] represent hours and [2][3] represent minutes
    twentyFourHour = int(time[0] + time[1] + time[2] + time[3])
    ext = filesPath + "\\"+ "\\"+ nameStem+".jpg"
    
    #readImg = cv2.imread(nameStem)
    
    readImg = cv2.imread(ext)
    median = cv2.medianBlur(readImg, (5))
    #cv2.imshow("avg", median) <- to see individual results
    #cv2.waitKey(0)

    cv2.imwrite(ext, median)
    

    #Up to and including 19:30 is day. Beyond that is night => sorts into appropriate folders 
    if (twentyFourHour <= 1930) :
        shutil.move(img, dayPath)
        print ("Moved to day: ", nameStem)
    else:
        shutil.move(img, nightPath)
        print("Moved to night: ", nameStem)

print("---Day---")
for img in dayPath.iterdir():

    j += 1 
    if (j==4):
        print("Image Four:", img.stem)
        img4day = Image.open(img)
    if (j==5):
        print("Image Five:", img.stem)
        img5day = Image.open(img)
diffDay = ImageChops.difference(img4day,img5day)
print(diffDay)
print(diffDay.getbbox())

if diffDay.getbbox():
    diffDay.show()

j=0
print("---Night---")

for img in nightPath.iterdir():
    j += 1 
    if (j==4):
        print("Image Four:", img.stem)
        img4night = Image.open(img)
    if (j==5):
        print("Image Five:", img.stem)
        img5night = Image.open(img)
diffNight = ImageChops.difference(img4night,img5night)
print(diffNight)
print(diffNight.getbbox())

if diffNight.getbbox():
    diffNight.show()
