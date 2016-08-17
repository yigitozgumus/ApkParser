from apk_parse.apk import APK
import string
from checkUtil import extractXML
import gradleParser as gr


class ChecklistBerker(object):
    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.apkf = APK("/Users/senolb/Desktop/pokemon.apk")
        self.manifestDict = extractXML(project_dir, project_dir + "/app/build/outputs/apk/apk-debug.apk")
        gradleRaw = gr.GradleParser(project_dir + "/app")
        self.gradleDict = gradleRaw.parse()

    def B4(self):
        appId = self.apkf.get_package()
        startingName = "com.monitise.mea."
        if appId.startswith(startingName):
            print "B4 succeed! Your project name starts with \"com.monitise.mea\"."
        else:
            print "B4 failed! Your project name does not start with \"com.monitise.mea\" It starts with " + appId

    def B6(self):
        targetSDK = self.apkf.get_target_sdk_version()
        print "B6 Test: Your targetSdkVersion is: " + targetSDK + \
              ". Please check if this is the most recent api version that app is tested against."

    def B7(self):
        for i in self.gradleDict["dependencies"]:
            if "com.google.android.gms:play-services:" in i:
                print "B7 failed! Google Play Services API should be included as separate dependencies."
                return
        print "B7 succeed! Google Play Services API is not included with just one line. (or not included at all)"

    def B9(self):
        if self.manifestDict.has_key("debuggable"):
            deb = self.manifestDict['manifest']['application']['@android:debuggable']
            if deb:
                print "B9 failed! debuggable should not be set to true."
                return
        print "B9 succeed! debuggable is not set to true."

    def MAN2(self):
        if "@android:versionName" in self.manifestDict['manifest']:
            version = self.manifestDict['manifest']['@android:versionName']
            print "MAN2 Test: Dismiss if you updated your version. android:versionName is set to: " + version
        print "MAN2 failed! You need to update android:versionName."

    def MAN5(self):
        if "@android:installLocation" in self.manifestDict['manifest']:
            location = self.manifestDict['manifest']['@android:installLocation']
            if location == "externalOnly":
                print "MAN5 failed! You cannot set android:installLocation to externalOnly."
                return
        print "MAN5 succeed! android:installLocation is not set to externalOnly."

    def PERM2(self):
        print "PERM2 Test: Check if all the permissions are necessary:"
        counter = 0
        for i in self.apkf.get_permissions():
            print "\t- " + self.apkf.get_permissions()[counter]
            counter += 1

    def SEC1(self):
        if "@android:allowBackup" in self.manifestDict['manifest']['application']:
            backup = self.manifestDict['manifest']['application']['@android:allowBackup']
            if backup:
                print "SEC1 failed! android:allowBackup is set to true."
                return

        print "SEC1 succeed! android:allowBackup is set to false.n"

    def PRG2(self):
        if self.gradleDict.has_key("minifyEnabled") & self.gradleDict.has_key("shrinkResources"):
            minifyEnabled = self.gradleDict["android"]["buildTypes"]["release"]["minifyEnabled"][0]
            shrinkResources = self.gradleDict["android"]["buildTypes"]["release"]["shrinkResources"][0]

            if minifyEnabled & shrinkResources:
                print "PRG2 succeed! minifyEnabled and shrinkResources are set to true."
                return
        print "PRG2 failed! minifyEnabled and shrinkResources must be true."
