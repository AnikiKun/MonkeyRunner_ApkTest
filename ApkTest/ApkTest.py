#!/usr/bin/env monkeyrunner
# -*- coding: utf-8 -*-

import time
import sys
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

#设置应用包名和入口Activity名
pakageName = 'com.hujiang.cctalk'
componentName = 'com.hujiang.cctalk/.MainActivity'

#APP启动时等待时间(秒)
startTime = 5

#获取年月日时分秒
now = time.strftime("%Y-%m-%d-%H-%M-%S")

#python中获取当前运行的文件的名字
name=sys.argv[0].split("\\")
filename=name[len(name)-1]

#MonkeyRunner下获取运行的文件所在的路径
rootpath  = os.path.split(os.path.realpath(sys.argv[0]))[0]

#指定位置
dir = rootpath + "/apk/"
screenPath = rootpath + "/screenShot/"
logpath = rootpath + "/log/"

#获取待测APK个数
countPak = len(os.listdir(dir))

#新建一个Log文件
if not os.path.isdir(logpath):
    os.mkdir(logpath)
log = open( logpath + filename[0:-3] + "-log" +now + ".txt" , 'w')

#开始连接设备
print("Connecting...")
device = MonkeyRunner.waitForConnection()
log.write("连接设备...\n")

#卸载应用
print('Removing...')
device.removePackage(pakageName)
print ('Remove Successful!')
MonkeyRunner.sleep(2)
log.write("初始化应用环境...\n")
countOK = 0
countNO = 0

for i in os.listdir(dir):
    print('Installing...<%s>'%i)
    log.write("==========安装应用==========\n")
    path = dir + '//' + i
    #安装应用
    device.installPackage(path)
    print('Install Successful!')

    #打开应用
    device.startActivity(component=componentName)
    MonkeyRunner.sleep(startTime)
    log.write("启动App...\n")

    #截图
    result=device.takeSnapshot()
    print("Take ScreenShot...")

    #保存截图
    result.writeToFile(screenPath + i + '.png','png')
    
    #进行图片比较
    resultTrue=MonkeyRunner.loadImageFromFile(screenPath + r'basePic.png')
    print "Pic Comparing..."
    log.write("对比图片中...\n")
    if(result.sameAs(resultTrue,0.9)):
        print("%s is OK!"%i)
        log.write("比较通过！--%s--包可用！\n"%i)
        #卸载应用
        print('Removing...')
        log.write("初始化应用环境，移除中...\n")
        device.removePackage(pakageName)
        print ('Remove Successful!')
        log.write("==========移除完毕==========\n")
        countOK += 1
        MonkeyRunner.sleep(2)
    else:
        print("False!Please check %s!"%i)
        log.write("比较失败！请检查安装包--%s--是否可用！\n"%i)
        break

log.write("共测试 %s 个包，%d 个通过。"%(countPak,countOK))