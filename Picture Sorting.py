# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 21:02:42 2022

@author: alexa
"""

import os
import exifread
import cv2



print("Hello, and welcome to a simple tool for organizing your photos and videos. \nYour pictures will be sorted according to the year and month they were taken, and will seperate the ones that are blurry.")
input("------------ PRESS ANY KEY TO CONTINUE ------------")
print("Enjoy!")
source = input("Enter the path of where your pictures are located: ")
destination = input("Enter the destination of where you want your organized pictures and videos to be stored: ")

count = 1
def getFolderSize(path):
    size = 0
    def getSubFolderSize(path, size):
        directoryContent = os.listdir(path)
        size += len(directoryContent)
        for i in directoryContent:
            if isFolder(path+ "\\" +i):
                size -= 1
                size = getSubFolderSize(path+"\\"+i, size)
            
        return size
    size = getSubFolderSize(path, size)
    return size 


    
def getFolderContent(path, dest):
    totalSize = getFolderSize(path)
    
    def getSubFolderContent(path, dest, count, totalSize):
        videoDest = dest+"\\"+"videos"
        a = os.listdir(path) 
        for i in a:
            
            if isFolder(path+"\\"+ i):
                count = getSubFolderContent(path+"\\"+i, dest, count, totalSize)
                continue

            elif isImage(i) == True:
                moveImage(path, dest, i)
                print("File %d out of %d processed" %(count, totalSize))
                count += 1
            elif isVideo(videoDest+i):
                moveVideo(path, dest, i, videoDest)
                print("File %d out of %d processed" %(count, totalSize))
                count += 1
            else:
                print("File %d out of %d cannot be processed" %(count, totalSize))
                count += 1
        return count
    getSubFolderContent(path, dest, count, totalSize)
    return ("%d pictures successfully processed" %(totalSize))
    


def moveVideo(path, dest, i, videoDest):
        try:
            #print("Moving: "+i+" to video folder")
            os.rename(path+"\\"+i, videoDest+"\\"+i)
            
        except FileExistsError:
            #print(i + " Could not be copied")
            file = open(dest+"file errors.txt", "w+")
            file.write(i)
        except FileNotFoundError:
            createDir(videoDest)
            #print("Moving: "+i+" to video folder")
            os.rename(path+"\\"+i, videoDest+"\\"+i)


def moveImage(path, dest, i):
    image = cv2.imread(path+"\\"+i)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    try: 
        temp_dest = getDestination(getDate(path+"\\"+i), dest)
    except KeyError:
        temp_dest = dest+"\\"+"Unorganizable"
        if not os.path.exists(temp_dest):
            os.mkdir(temp_dest)
    finally:
        #print(cv2.Laplacian(gray, cv2.CV_64F).var())
        if cv2.Laplacian(gray, cv2.CV_64F).var() > 95:
            #print("Moving: "+i+" to " + temp_dest)
            try:
                os.rename(path+"\\"+i, temp_dest+"\\"+i)
            except FileExistsError:
                file = open(dest+"file errors.txt", "w+")
                file.write(i)
                return
        else:
            try:
                os.rename(path+"\\"+i, temp_dest+"\\"+"Blurry"+"\\"+i)
                #print("Moving: "+i+" to the blurry folder")
            except FileNotFoundError:
                createDir(temp_dest+"\\"+"Blurry")
                os.rename(path+"\\"+i, temp_dest+"\\"+"Blurry"+"\\"+i)
                #print("Moving: "+i+" to the blurry folder")
            except FileExistsError:
                file = open(dest+"file errors.txt", "w+")
                file.write(i)
                return            

def isFolder(path):
    if os.path.isdir(path):
        return True
    return False              
                
def isImage(filename):
    imageExtensions = ["png", "jpg", "jpeg", "tif", "gif"]
    ext = filename.index(".")
    extension = filename[ext+1:]
    if extension.lower() in imageExtensions:
        return True
    return False

def isVideo(filename):
    videoExtensions = ["mp4", "mov", "mkv", "3gp"]
    ext = filename.index(".")
    extension = filename[ext+1:]
    if extension.lower() in videoExtensions:
        return True
    return False
    
                
def getDestination(date, dest):
    
    year = date[0:4]
    month = date[5:7]
    dest_path = dest+"\\"+year+"\\"+month

    if not os.path.exists(dest+"\\"+year):
        os.mkdir(dest+"\\"+year)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    if not os.path.exists(dest_path+"\\"+"Blurry"):
        os.mkdir(dest_path+"\\"+"Blurry")
    
    return dest_path
    
        

def createDir(path):
    os.mkdir(path)
    
    
def getDate(file):
    with open(file, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        dateTaken = tags["EXIF DateTimeOriginal"]
        return str(dateTaken)



print(getFolderContent(source, destination))

#getFolderContent(source, destination)