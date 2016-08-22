from apk_parse.apk import APK
import string
from checkUtil import extractXML
import gradleParser_v2 as gr
import CheckList


class ChecklistBerker(object):
    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir

        self.apk_dir = apk_dir
        self.apkf = APK(apk_dir)

        self.manifestDict = extractXML(project_dir, apk_dir)
        self.gradleDict = gr.GradleParserNew(self.project_dir + "/app").parse(False)

    def showResult(self, testId, result, additional):
        print "\n\n============ " + testId + " Test ==========================================="
        print "=="
        print "==\t" + result + additional
        print "=="
        print "==================================================================\n"

    def B4(self):
        testId = "B4"
        appId = self.apkf.get_package()
        startingName = "com.monitise.mea."
        if appId.startswith(startingName):
            result = "SUCCEED!"
            additional = "Your project name starts with \"com.monitise.mea\"."
        else:
            result = "FAILED!"
            additional = "Your project name does not start with \"com.monitise.mea\" It starts with " + appId
        self.showResult(testId, result, additional)

    def B6(self, configTargetSdk):
        testId = "B6"
        configTargetSdk
        targetSDK = self.apkf.get_target_sdk_version()
        if configTargetSdk == targetSDK:
            result = "SUCCESS!"
            additional = "Your targetSdkVersion is: " + targetSDK + "."
        else:
            result = "FAILED!"
            additional = "Your targetSdkVersion should be " + configTargetSdk + " but it is " + targetSDK + "."

        self.showResult(testId, result, additional)

    def B7(self):
        testId = "B7 Test"
        for dep in self.gradleDict["dependencies"]["compile"]:
            if "com.google.android.gms:play-services:" in dep:
                result = "FAILED!"
                additional = "Google Play Services API should be included as separate dependencies."
                self.showResult(testId, result, additional)
                return
        result = "SUCCEED!"
        additional = "Google Play Services API is not included with just one line. (or not included at all)"
        self.showResult(testId, result, additional)

    def B9(self):
        testId = "B9"
        if '@android:debuggable' in self.manifestDict['manifest']['application']:
            deb = self.manifestDict['manifest']['application']['@android:debuggable']
            deb = deb.lower()
            if deb == "true":
                result = "FAILED!"
                additional = "debuggable should not be set to true."
                self.showResult(testId, result, additional)
                return
        result = "SUCCEED!"
        additional = "debuggable is not set to true."
        self.showResult(testId, result, additional)

    def MAN2(self):
        testId = "MAN2"

        if "@android:versionName" in self.manifestDict['manifest']:
            version = self.manifestDict['manifest']['@android:versionName']
            result = "CONFIRM:"
            additional = "Dismiss if you updated your version. android:versionName is set to: " + version + "."
        else:
            result = "FAILED!"
            additional = "You need to update android:versionName."

        self.showResult(testId, result, additional)

    def MAN5(self):
        testId = "MAN5"

        if "@android:installLocation" in self.manifestDict['manifest']:
            location = self.manifestDict['manifest']['@android:installLocation']
            if location == "externalOnly":
                result = "FAILED!"
                additional = "You cannot set android:installLocation to externalOnly."
                self.showResult(testId, result, additional)
                return
        result = "SUCCEED!"
        additional = " android:installLocation is not set to externalOnly."
        self.showResult(testId, result, additional)

    def PERM2(self):
        testId = "PERM2"

        result = "CONFIRM:"
        additional = "Check if all the permissions are necessary:"
        counter = 0
        for i in self.apkf.get_permissions():
            additional = additional + "\n==\t- " + self.apkf.get_permissions()[counter]
            counter += 1
        self.showResult(testId, result, additional)

    def SEC1(self, configAllowBackup):
        testId = "SEC1"
        configAllowBackup = configAllowBackup.lower()

        if "@android:allowBackup" in self.manifestDict['manifest']['application']:
            backup = self.manifestDict['manifest']['application']['@android:allowBackup']
            backup = backup.lower()
            configAllowBackup = configAllowBackup.lower()
            if backup == configAllowBackup:
                result = "SUCCEED!"
                additional = "android:allowBackup is set to " + backup
            else:
                result = "FAILED!"
                additional = "android:allowBackup is set to " + backup + ". But it must be " + configAllowBackup + "."
        elif configAllowBackup == "true":
            result = "FAILED!"
            additional = "You need to specify android:allowBackup as true."
        else:
            result = "SUCCEED!"
            additional = "Your android:allowBackup is set to false by default."
        self.showResult(testId, result, additional)

    def PRG2(self, configMinifyEn, configShrinkRes):
        testId = "PRG2"
        configMinifyEn = configMinifyEn.lower()
        configShrinkRes = configShrinkRes.lower()

        if "minifyEnabled" in self.gradleDict['android']["buildTypes"][0]["release"][0] and \
                        "shrinkResources" in self.gradleDict['android']["buildTypes"][0]["release"][0]:

            minifyEnabled = self.gradleDict["android"]["buildTypes"][0]["release"][0]["minifyEnabled"][0]
            shrinkResources = self.gradleDict["android"]["buildTypes"][0]["release"][0]["shrinkResources"][0]
            minifyEnabled = minifyEnabled.lower()
            shrinkResources = shrinkResources.lower()
            if minifyEnabled == configMinifyEn and shrinkResources == configShrinkRes:
                result = "SUCCEED!"
                additional = "minifyEnabled and shrinkResources are set to true."
                self.showResult(testId, result, additional)
                return

        result = "FAILED!"
        additional = "minifyEnabled and shrinkResources must be true."
        self.showResult(testId, result, additional)
