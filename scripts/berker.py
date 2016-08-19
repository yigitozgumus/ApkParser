from apk_parse.apk import APK
import string
from checkUtil import extractXML
import gradleParser as gr


class ChecklistBerker(object):
    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir

        self.apk_dir = apk_dir
        self.apkf = APK(apk_dir)

        self.manifestDict = extractXML(project_dir, apk_dir)
        self.gradleDict = gr.GradleParser(self.project_dir + "/app").parse()

    def B4(self):
        print "\n========== B4 Test ==========\n"

        appId = self.apkf.get_package()
        startingName = "com.monitise.mea."
        if appId.startswith(startingName):
            print "SUCCEED! Your project name starts with \"com.monitise.mea\"."
        else:
            print "FAILED! Your project name does not start with \"com.monitise.mea\" It starts with " + appId

    def B6(self,configTargetSdk):
        print "\n========== B6 Test ==========\n"
        configTargetSdk
        targetSDK = self.apkf.get_target_sdk_version()
        if configTargetSdk == targetSDK:
            print "SUCCESS! Your targetSdkVersion is: " + targetSDK + "."
        else:
            print "FAILED! Your targetSdkVersion should be " + configTargetSdk + " but it is " + targetSDK + "."

    def B7(self):
        print "\n========== B7 Test ==========\n"

        for dep in self.gradleDict["dependencies"]["compile"]:
            if "com.google.android.gms:play-services:" in dep:
                print "FAILED! Google Play Services API should be included as separate dependencies."
                return

        print "SUCCEED! Google Play Services API is not included with just one line. (or not included at all)"

    def B9(self):
        print "\n========== B9 Test ==========\n"

        if self.manifestDict.has_key("debuggable"):
            deb = self.manifestDict['manifest']['application']['@android:debuggable']
            if deb:
                print "FAILED! debuggable should not be set to true."
                return

        print "SUCCEED! debuggable is not set to true."

    def MAN2(self):
        print "\n========== MAN2 Test ==========\n"

        if "@android:versionName" in self.manifestDict['manifest']:
            version = self.manifestDict['manifest']['@android:versionName']
            print "CONFIRM: Dismiss if you updated your version. android:versionName is set to: " + version + "."
        else:
            print "FAILED! You need to update android:versionName."

    def MAN5(self):
        print "\n========== MAN5 Test ==========\n"

        if "@android:installLocation" in self.manifestDict['manifest']:
            location = self.manifestDict['manifest']['@android:installLocation']
            if location == "externalOnly":
                print "FAILED! You cannot set android:installLocation to externalOnly."
                return

        print "SUCCEED! android:installLocation is not set to externalOnly."

    def PERM2(self):
        print "\n========== PERM2 Test ==========\n"

        print "CONFIRM: Check if all the permissions are necessary:"
        counter = 0
        for i in self.apkf.get_permissions():
            print "\t- " + self.apkf.get_permissions()[counter]
            counter += 1

    def SEC1(self,configAllowBackup):
        print "\n========== SEC1 Test ==========\n"

        if "@android:allowBackup" in self.manifestDict['manifest']['application']:
            backup = self.manifestDict['manifest']['application']['@android:allowBackup']
            if backup == configAllowBackup:
                print "SUCCEED! android:allowBackup is set to " + backup
            else:
                print "FAILED! android:allowBackup is set to " + backup + ". But it must be " + configAllowBackup+ "."
            return
        elif configAllowBackup:
            print "FAILED! You need to specift android:allowBackup as true."
        else:
            print "SUCCEED! Your android:allowBackup is set to false by default."

    def PRG2(self,configMinifyEn,configShrinkRes):
        print "\n========== PRG2 Test ==========\n"

        if "minifyEnabled" in self.gradleDict['android']["buildTypes"]["release"] and \
                        "shrinkResources" in self.gradleDict['android']["buildTypes"]["release"]:

            minifyEnabled = self.gradleDict["android"]["buildTypes"]["release"]["minifyEnabled"][0]
            shrinkResources = self.gradleDict["android"]["buildTypes"]["release"]["shrinkResources"][0]

            if minifyEnabled == configMinifyEn and shrinkResources == configShrinkRes:
                print "SUCCEED! minifyEnabled and shrinkResources are set to true."
                return

        print "FAILED! minifyEnabled and shrinkResources must be true."
