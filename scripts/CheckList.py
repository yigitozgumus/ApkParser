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

        # self.checklist_yigit.B2()
        # self.checklist_berker.B4()
        #
        # minSdkVersion = config.get('B5', 'minSdkVersion')
        # self.checklist_yigit.B5(minSdkVersion)
        #
        # targetSdkVersion = config.get('B6', 'targetSdkVersion')
        # self.checklist_berker.B6(targetSdkVersion)
        #
        # self.checklist_yigit.B7()
        # self.checklist_berker.B7()
        # self.checklist_yigit.B8()
        # self.checklist_berker.B9()
        #
        # self.checklist_yigit.MAN1()
        # self.checklist_berker.MAN2()
        # self.checklist_yigit.MAN3()
        # self.checklist_berker.MAN5()
        #
        # self.checklist_yigit.SIGN4()
        #
        # self.checklist_berker.PERM2()
        # self.checklist_yigit.PERM3()
        #
        # minifyEnabled = config.get('PRG2', 'minifyEnabled')
        # shrinkResources = config.get('PRG2', 'shrinkResources')
        # self.checklist_berker.PRG2(minifyEnabled,shrinkResources)
        #
        # proguardList = config.get('PRG3', 'proguardList')
        # self.checklist_yigit.PRG3(proguardList)
        #
        # self.checklist_yigit.APK2()
        #
        # allowBackup = config.get('SEC1','allowBackup')
        # self.checklist_berker.SEC1(allowBackup)
        # self.checklist_yigit.SEC4()
        # self.checklist_yigit.SIGN2()
        sdk_location = config.get('GEN4', 'sdkLocation')
        apk_location = config.get('GEN4','apkLocation')
        self.checklist_yigit.GEN4(apk_location,sdk_location)
