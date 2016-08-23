#!/usr/bin/env python

import yigit
import berker
import checkUtil
import gradleParser_v2
import ConfigParser


class Checklist(object):
    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.checklist_yigit = yigit.ChecklistYigit(self.project_dir, self.apk_dir)
        self.checklist_berker = berker.ChecklistBerker(self.project_dir, self.apk_dir)

    def executeTests(self,config_location):
        config = ConfigParser.ConfigParser()

        config.read(config_location)
        self.checklist_yigit.gen2()
        self.checklist_yigit.b2()
        self.checklist_berker.B4()

        minSdkVersion = config.get('B5', 'minSdkVersion')
        self.checklist_yigit.b5(minSdkVersion)

        targetSdkVersion = config.get('B6', 'targetSdkVersion')
        self.checklist_berker.B6(targetSdkVersion)

        self.checklist_yigit.b7()
        self.checklist_berker.B7()
        self.checklist_yigit.b8()
        self.checklist_berker.B9()

        self.checklist_yigit.man1()
        self.checklist_berker.MAN2()
        self.checklist_yigit.man3()
        self.checklist_yigit.man4()
        self.checklist_berker.MAN5()
        self.checklist_yigit.sign2()
        self.checklist_yigit.sign4()

        self.checklist_berker.PERM2()
        self.checklist_yigit.perm3()

        minifyEnabled = config.get('PRG2', 'minifyEnabled')
        shrinkResources = config.get('PRG2', 'shrinkResources')
        self.checklist_berker.PRG2(minifyEnabled,shrinkResources)

        proguardList = config.get('PRG3', 'proguardList')
        self.checklist_yigit.prg3(proguardList)
        apk_folder_location = config.get('APK1', 'apkFolderLocation')
        self.checklist_yigit.apk1(apk_folder_location)
        self.checklist_yigit.apk2()

        allowBackup = config.get('SEC1','allowBackup')
        self.checklist_berker.SEC1(allowBackup)
        self.checklist_yigit.sec4()

        sdk_location = config.get('GEN4', 'sdkLocation')
        apk_location = config.get('GEN4','apkLocation')
        self.checklist_yigit.gen4(apk_location,sdk_location)




