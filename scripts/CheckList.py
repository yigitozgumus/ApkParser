#!/usr/bin/env python

import yigit
import berker

class Checklist(object):

    def __init__(self,project_dir,apk_dir):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.checklist_yigit = yigit.ChecklistYigit(self.project_dir,self.apk_dir)
        self.checklist_berker = berker.ChecklistBerker(self.project_dir,self.apk_dir)

    def executeTests(self):

        # self.checklist_yigit.B2()
        # self.checklist_berker.B4()
        # self.checklist_yigit.B5()
        # self.checklist_berker.B6()
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
        # self.checklist_berker.PRG2()
        self.checklist_yigit.PRG3(['proguard-android.txt','proguard-rules.pro'])

        self.checklist_yigit.APK2()

        self.checklist_berker.SEC1()
        self.checklist_yigit.SEC4()


