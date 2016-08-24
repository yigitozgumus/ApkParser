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
        # config = ConfigParser.ConfigParser()
        #
        # config.read(config_location)

        test_results = self.checklist_yigit.execute_test_batch(config_location)
        for i in test_results:
            print i

        # self.checklist_berker.b4()
        # targetSdkVersion = config.get('B6', 'targetSdkVersion')
        # self.checklist_berker.b6(targetSdkVersion)
        # self.checklist_berker.b7()
        # self.checklist_berker.b9()
        # self.checklist_berker.man2()
        # self.checklist_berker.man5()
        # self.checklist_berker.perm2()
        # minifyEnabled = config.get('PRG2', 'minifyEnabled')
        # shrinkResources = config.get('PRG2', 'shrinkResources')
        # self.checklist_berker.prg2(minifyEnabled,shrinkResources)
        #
        # allowBackup = config.get('SEC1','allowBackup')
        # self.checklist_berker.sec1(allowBackup)





