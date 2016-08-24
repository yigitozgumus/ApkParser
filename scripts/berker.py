import os
import os.path as path

import subprocess

import gradleParser_v2 as gr
from apk_parse.apk import APK
from checkUtil import extractXML, working_directory


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

    def b1(self, configResConfig_list):
        testId = "B1"
        found = False
        resConf_filtered = configResConfig_list.split(",")
        resConf_filtered = [x.strip(" ") for x in resConf_filtered]

        if "resConfigs" in self.gradleDict['android']["defaultConfig"][0]:
            for i in self.gradleDict['android']["defaultConfig"][0]["resConfigs"][0]:
                for conf in resConf_filtered:
                    if i.lower() == conf.lower():
                        found = True
                        break  # found in the config
                if not found:
                    result = "FAILED!"
                    additional = " In your resConfigs, you have: " + i + " but not in config file."
                    self.showResult(testId, result, additional)
                    return
                else:
                    found = False

            for conf in resConf_filtered:
                for i in self.gradleDict['android']["defaultConfig"][0]["resConfigs"][0]:
                    if i.lower() == conf.lower():
                        found = True
                        break  # found in the config
                if not found:
                    result = "FAILED!"
                    additional = " In your config file, you have: " + conf + " but not in manifest."
                    self.showResult(testId, result, additional)
                    return
                else:
                    found = False
        else:
            result = "CONFIRM:"
            additional = " You dont have resConfigs in your project."
            self.showResult(testId, result, additional)
            return

        result = "SUCCEED!"
        additional = " Your resConfigs in config file match with the ones in the manifest."
        self.showResult(testId, result, additional)

    def b4(self):
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

    def b6(self, configTargetSdk):
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

    def b7(self):
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

    def b9(self):
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

    def man2(self):
        testId = "MAN2"

        if "@android:versionName" in self.manifestDict['manifest']:
            version = self.manifestDict['manifest']['@android:versionName']
            result = "CONFIRM:"
            additional = "Dismiss if you updated your version. android:versionName is set to: " + version + "."
        else:
            result = "FAILED!"
            additional = "You need to update android:versionName."

        self.showResult(testId, result, additional)

    def man5(self):
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

    def perm2(self):
        testId = "PERM2"

        result = "CONFIRM:"
        additional = "Check if all the permissions are necessary:"
        counter = 0
        for i in self.apkf.get_permissions():
            additional = additional + "\n==\t- " + self.apkf.get_permissions()[counter]
            counter += 1
        self.showResult(testId, result, additional)

    def sec1(self, configAllowBackup):
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

    def sign1(self):
        testId = "SIGN1"

        if not os.path.exists(self.project_dir + "/release.keystore.jks"):
            result = "FAILED!"
            additional = " release.keystore.jks does not exist in your project path."
            self.showResult(testId, result, additional)
            return;

            # todo checkb2 here
        signing_report = []
        split_string = ":app:signingReport"
        with working_directory(self.project_dir):
            output = subprocess.check_output(["./gradlew", "signingReport"])
            signing_report = output.split("\n")
        # parse result
        signing_report = signing_report[signing_report.index(split_string) + 1:]
        signing_report = [el for el in signing_report if "Error" in el]
        if len(signing_report) == 0:
            result = "SUCCEED."
            additional = "Signing task build is successful, keys are valid"
        else:
            result = "FAILED."
            additional = "Please check assigned keys"
        self.showResult(testId, result, additional)

    def sign3(self):
        testId = "SIGN3"
        keyPath = ''

        try:
            keyPath = self.gradle['android']['signingConfigs'][0]['release'][0]['storeFile'][0][0]
        except:
            result = "FAILED!"
            additional = "There is no given path for release keystore file"
            self.showResult(testId, result, additional)
            return

        if path.exists(keyPath):
            if "/build/" in keyPath:
                result = "FAILED"
                additional = " Your release keystore is in build classpath."
            else:
                result = "SUCCEED!"
                additional = "Your release keystore is not in build classpath."

            self.showResult(testId, result, additional)
        else:
            result = "FAILED!"
            additional = " There is no release keystore in the project!"
            self.showResult(testId, result, additional)


    def prg1(self, proguard_list):
        # prgList = [line.strip() for line in open(self.project_dir+"/app/proguard-rules.pro", "r")]
        testId = "PRG1"
        functs = ["public static boolean isLoggable(java.lang.String, int);",
                  "public static int v(...);",
                  "public static int i(...);",
                  "public static int w(...);",
                  "public static int d(...);",
                  "public static int e(...);"]

        gradlePrgList = self.gradleDict["android"]["buildTypes"][0]["release"][0]["proguardFiles"][0]

        for fileIndex in range(len(gradlePrgList)):

            if not os.path.exists(self.project_dir + "/app/" + gradlePrgList[fileIndex]):
                continue

            prgList = [line.strip() for line in open(self.project_dir + "/app/" + gradlePrgList[fileIndex], "r")]
            prgList = [x.strip(" ") for x in prgList]
            for i in range(len(prgList)):
                if prgList[i].startswith("-assumenosideeffects class android.util.Log {"):
                    i += 1
                    for k in range(len(functs)):
                        if not i + k < len(prgList):
                            break
                        if not prgList[i + k].startswith(functs[k]):
                            break
                        if k == len(functs) - 1:
                            result = "SUCCEED"
                            additional = "You have proper functions to disable logging in " + gradlePrgList[
                                fileIndex] + "."
                            self.showResult(testId,result,additional)
                            return

        result = "FAILED!"
        additional = "You forgot to disable logging in proguard configurations."
        self.showResult(testId,result,additional)

    def prg2(self, configMinifyEn, configShrinkRes):
        testId = "PRG2"
        configMinifyEn = configMinifyEn.lower()
        configShrinkRes = configShrinkRes.lower()

        if "minifyEnabled" in self.gradleDict['android']["buildTypes"][0]["release"][0] and \
                        "shrinkResources" in self.gradleDict['android']["buildTypes"][0]["release"][0]:

            minifyEnabled = self.gradleDict["android"]["buildTypes"][0]["release"][0]["minifyEnabled"][0]
            shrinkResources = self.gradleDict["android"]["buildTypes"][0]["release"][0]["shrinkResources"][0]
            minifyEnabled = minifyEnabled[0].lower()
            shrinkResources = shrinkResources[0].lower()
            if minifyEnabled == configMinifyEn and shrinkResources == configShrinkRes:
                result = "SUCCEED!"
                additional = "minifyEnabled and shrinkResources are set to true."
                self.showResult(testId, result, additional)
                return

        result = "FAILED!"
        additional = "minifyEnabled and shrinkResources must be true."
        self.showResult(testId, result, additional)
