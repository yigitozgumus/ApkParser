from apk_parse.apk import APK
import string
from checkUtil import extractXML


class ChecklistBerker(object):

    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.apkf = APK("/Users/senolb/Desktop/pokemon.apk")
        self.manifestDict = extractXML(project_dir, apk_dir)
        print self.manifestDict


    def B4(self):
        appId = self.apkf.get_package()
        startingName = "com.monitise.mea."
        if appId.startswith(startingName):
            print "B4 succeed! Your project name starts with \"com.monitise.mea\"."
        else:
            print "B4 failed! Your project name does not start with \"com.monitise.mea\" It starts with " + appId

    def B6(self):
        targetSDK = self.apkf.get_target_sdk_version()
        print "B6 Test: Your targetSdkVersion is: " + targetSDK +\
              ". Please check if this is the most recent api version that app is tested against."


    def MAN5(self):
        if "@android:installLocation" in self.manifestDict['manifest']:
            location = self.manifestDict['manifest']['@android:installLocation']
            if location == "externalOnly":
                print "MAN5 failed! You cannot set android:installLocation to externalOnly."
                return
        print "MAN5 succeed! Your android:installLocation is not set to externalOnly."

    def MAN2(self):
        if "@android:versionName" in self.manifestDict['manifest']:
            version = self.manifestDict['manifest']['@android:versionName']
            print "MAN2 Test: Dismiss if you updated your version. android:versionName is set to: " + version
        print "MAN2 failed! You need to update android:versionName."

    def SEC1(self):
        if "@android:allowBackup" in self.manifestDict['manifest']['application']:
            backup = self.manifestDict['manifest']['application']['@android:allowBackup']
            if backup:
                print "SEC1 failed! android:allowBackup is set to true"
                return

        print "SEC1 succeed! android:allowBackup is set to false"


