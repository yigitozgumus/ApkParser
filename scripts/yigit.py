#!/usr/bin/env python

from checkUtil import working_directory
from checkUtil import extractXML
from apk_parse import apk
import subprocess
import gradleParser
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

    def __init__(self,project_dir,apk_dir):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.manifest = extractXML(project_dir,apk_dir)
        self.apkf_inspect = apk.APK(apk_dir)
        self.gradle = gradleParser.GradleParser(self.project_dir+"/app").parse()

    def B2(self):
        """
        This test executes gradle signing Report
        :param project_dir: Project location
        :return: to be documented
        """
        print "\n========== B2 Test ==========\n"
        #TODO release key check will be added
        with working_directory(self.project_dir):
            output =  subprocess.check_output(["./gradlew","signingReport"])
            if "BUILD SUCCESSFUL" in output:
                print "Signing task build is successful, keys are valid"
            else:
                print "Please check assigned keys"

    def createAPK(self):
        """

        :return:
        """
        with working_directory(self.project_dir):
            subprocess.check_output(["./gradlew","assembleRelease"])
        self.is_apk_created = True
        # print "Apk file is created"

    def B5(self):
        """

        :return:
        """
        print "\n========== B5 Test ==========\n"
        if(not self.is_apk_created):
            self.createAPK()
        min_sdk = self.apkf_inspect.get_min_sdk_version()
        if(min_sdk == 16):
            print " Minimum sdk version is 16. Test successful."
        else:
            print "Test failed. Your project's minimum sdk is not 16, it is " +min_sdk+". "

    def B7(self):
        """

        :return:
        """
        print "\n========== B7 Test ==========\n"
        #TODO ask the checklist item
        if(not self.is_apk_created):
            self.createAPK()
        compile_sdk = self.gradle["android"]["compileSdkVersion"][0]
        print "Project compileSdkVersion is " + compile_sdk + \
                ". Check for behavioral changes accordingly"

    def B8(self):
        """

        :return:
        """
        print "\n========== B8 Test ==========\n"

        dependencies = self.gradle["dependencies"]["compile"]

        is_valid = True
        for dependency in dependencies:
            if not(re.search("\d+.\+", dependency)== None):
                is_valid = False
                print "Please check the latest version of " + dependency[1:-1]
        if is_valid:
            print "Every dependency injected has a specific version"
        else:
            print "Test failed."



    def MAN1(self):
        """

        :return:
        """
        print "\n========== MAN1 Test ==========\n"
        #TODO How to read previous version code ?
        versionCode = self.gradle['android']['defaultConfig']['versionCode'][0]
        print "Current version code is " + versionCode

    def MAN3(self):
        """

        :return:
        """
        print "\n========== MAN3 Test ==========\n"
        version_name = self.gradle["android"]["defaultConfig"]["versionName"][0]
        versions = version_name.split(".")
        if(not(len(versions) == 4)):
            print "Version name does not follow <major>.<minor>.<patch>.<buildNumber> convention."
        else:
            print "Version name is valid"

    def SIGN4(self):
        """

        :return:
        """
        print "\n========== SIGN4 Test ==========\n"
        #TODO improve test logic.
        config_values = self.gradle["android"]["signingConfigs"]["config"]
        num_configs = len(config_values.keys())
        isValid = True
        if(num_configs < 4):
            print "all values for the signingConfig are not defined.\n Defined are below:\n"
            for key in config_values.keys():
                print "the key name is" + key + "and its value is" + config_values[key][0][1:-1]
            return
        for check in config_values.keys():
            if( len(config_values[check]) == 0):
                print "Check " + check + " value"
                isValid =False
        if(isValid):
            print "All signingConfig values are valid"

    def PERM3(self):
        """

        :return:
        """
        print "\n========== PERM3 Test ==========\n"

        if (not self.is_apk_created):
            self.createAPK()
        feature_list = self.manifest['manifest']
        if 'uses-feature' in feature_list:
            if (not(len(feature_list) == 0)):
                print " to be implemented"
            else:
                print "There is no uses-feature tag in this AndroidManifest.xml"

    def PRG3(self):
        """

        :return:
        """
        print "\n========== PRG3 Test ==========\n"
        proguard_files = self.gradle["android"]["buildTypes"]["release"]["proguardFiles"]
        proguard_size = len(proguard_files)
        if(proguard_size < 2):
            print "Please check whether proguard-rules.pro or proguard-android.txt is added."
            return
        elif(proguard_size >= 2):
            print "Added proguard files listed below:\n"
            for i in range(len(proguard_files)):
                if(i==0):
                    result = re.search("\'[\s\S]+\'",proguard_files[i])
                    print str(i+1) + "-) " +   result.group(0)
                else:
                    print str(i+1) + "-) " + proguard_files[i]



    def APK2(self):
        """

        :return:
        """
        print "\n========== APK2 Test ==========\n"
        if (not self.is_apk_created):
            self.createAPK()
        apk_size = os.path.getsize(self.apk_dir)
        apk_rest = apk_size % (1024 * 1024)
        apk_size = apk_size / (1024 * 1024)

        if (apk_size < 15):
            print "Test succeed. Apk size is within limits.(" + str(apk_size)+","+str(apk_rest) + "mb)."
        else:
            print "Apk size exceeds limits (>15mb)."

    def SEC4(self):
        """

        :return:
        """
        print "\n========== SEC4 Test ==========\n"
        if (not self.is_apk_created):
            self.createAPK()
        activities = self.manifest['manifest']['application']['activity']
        services = self.manifest['manifest']['application']['service']
        receivers = self.manifest['manifest']['application']['receiver']
        isValid = True
        for check in activities:
            if 'intent-filter' in check:
                if '@android:exported' in check:
                    if check['@android:exported'] == 'false' in check:
                        pass
                    else:
                        isValid = False
                        print check['@android:name']+ "\t--> android:exported value should be set to false"
                else:
                    isValid = False
                    print check['@android:name']+ "\t--> Please add android:exported=\"false\" attribute"

        for check in services:
            if 'intent-filter' in check:
                if '@android:exported' in check:
                    if check['@android:exported'] == 'false' in check:
                        pass
                    else:
                        isValid = False
                        print check['@android:name']+ "\t--> android:exported value should be set to false"
                else:
                    isValid = False
                    print check['@android:name']+ "\t--> Please add android:exported=\"false\" attribute"
        for check in receivers:
            if 'intent-filter' in check:
                if '@android:exported' in check:
                    if check['@android:exported'] == 'false' in check:
                        pass
                    else:
                        isValid = False
                        print check['@android:name']+ "\t--> android:exported value should be set to false"
                else:
                    isValid = False
                    print check['@android:name']+ "\t--> Please add android:exported=\"false\" attribute"

        if(isValid):
            print "Test is successful."
        else:
            print "Test failed."
