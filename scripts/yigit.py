#!/usr/bin/env python

from checkUtil import working_directory
from checkUtil import extractXML
from apk_parse import apk
import subprocess
import re
import os

class ChecklistYigit(object):
    """
    This class checks certain checklist items regarding the Android project

    Attributes:
        project_dir : Project directory of the Android app
    """
    is_apk_created = False
    apk_location = "/app/build/outputs/apk/app-release.apk"

    def __init__(self,project_dir):
        self.project_dir = project_dir
        self.apkf_inspect = apk.APK(project_dir+self.apk_location)

    def B2(self,project_dir):
        """
        This test executes gradle signing Report
        :param project_dir: Project location
        :return: to be documented
        """
        with working_directory(project_dir):
            subprocess.call(["./gradlew","signingReport"])

    def createAPK(self,project_dir):
        with working_directory(project_dir):
            subprocess.call(["./gradlew","assembleRelease"])
        self.is_apk_created = True
        print "Apk file is created"

    def B5(self,project_dir):

        if(not self.is_apk_created):
            self.createAPK(project_dir)

        min_sdk = self.apk_inspect.get_min_sdk_version()
        if(min_sdk == 16):
            print " Minimum sdk version is 16. Test successful."
        else:
            print "Please check minimum sdk version of the project."

    def B7(self,project_dir):
        #TODO ask the checklist item
        if(not self.is_apk_created):
            self.createAPK(project_dir)
        compileSdk = self.apk_inspect.get_element("uses-sdk","compileSdkVersion")
        print compileSdk

    def B8(self,project_dir):
        #TODO more comprehensive ?
        with working_directory(project_dir):
            output =  subprocess.check_output(["./gradlew","androidDependencies"])
            pattern = re.compile(".\+")
            result = pattern.search(output)
            if(result == None):
                print "Each dependency injected has a specific version "
            else:
                print "Check dependencies"


    def MAN1(self,project_dir):
        #TODO How to read previous version code ?
        with working_directory(project_dir+"/build"):
            file = open("build.gradle","r")
            pattern = re._compile("versionCode")
            for line in file:
                match = pattern.search(line)
                if(not (match == None)):
                    temp,ver = line.split(" ")
                    print ver
    def MAN3(self,project_dir):
        with working_directory(project_dir+"/build"):
            file = open("build.gradle","r")
            pattern = re._compile("versionName")
            for line in file:
                match = pattern.search(line)
                if(not(match == None)):
                    temp,ver = line.split(" ")
                    versions = ver.split(".")
                    if(not(len(versions) == 4)):
                        print "Version name does not follow <major>.<minor>.<patch>.<buildNumber> convention."
                    else:
                        print "Version name is valid"

    def SIGN4(self,project_dir):
        #TODO improve test logic.
        with working_directory(project_dir+"/build"):
            password_check = {"storePassword": 0,"keyAlias":0,"keyPassword":0}
            file = open("build.gradle","r")
            for line in file:
                if "storePassword" in line: password_check["storePassword"] = 1
                elif "keyAlias" in line: password_check["keyAlias"] = 1
                elif "keyPassword" in line: password_check["keyPassword"] = 1
            if 0 in password_check.values():
                print " Check signing Release password values"
            else:
                print " Signing Release Passsword values are validated"

    def PERM3(self,project_dir):
        #TODO gradle parser would be better choice
        if (not self.is_apk_created):
            self.createAPK(project_dir)
        manifest = extractXML(project_dir,project_dir+self.apk_location)
        feature_list = manifest['manifest']['@uses-feature']
        if (not(len(feature_list) == 0)):
            print " to be implemented"

    def APK2(self,project_dir):
        if (not self.is_apk_created):
            self.createAPK(project_dir)
        apk_size = os.path.getsize(project_dir+self.apk_location)
        apk_size = apk_size / (1024 * 1024)
        if (apk_size < 15):
            print "Apk size is within limits."
        else:
            print "Apk size exceeds limits (>15mb)."

    def SEC4(self,project_dir):
        if (not self.is_apk_created):
            self.createAPK(project_dir)
        manifest = extractXML(project_dir, project_dir + self.apk_location)
