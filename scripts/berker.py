import os
import os.path as path
import ConfigParser
import gradleParser_v2 as gr
from apk_parse.apk import APK
from checkUtil import extractXML, working_directory


class ChecklistBerker(object):
    is_apk_created = False
    apk_location = "/app/build/outputs/apk/app-external-release.apk"
    test_results = []

    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir

        self.apk_dir = apk_dir
        self.apkf = APK(apk_dir)

        self.manifestDict = extractXML(project_dir, apk_dir)
        self.gradleDict = gr.GradleParserNew(self.project_dir + "/app").parse(False)

    def execute_test_batch(self, config_location):
        config = ConfigParser.ConfigParser()
        config.read(config_location)

        resCongList = config.get('B1', 'resConfigs')
        self.test_results.append(self.b1(resCongList))
        self.test_results.append(self.b4())
        targetSdkVersion = config.get('B6', 'targetSdkVersion')
        self.test_results.append(self.b6(targetSdkVersion))
        self.test_results.append(self.b7())
        self.test_results.append(self.b9())

        self.test_results.append(self.man2())
        self.test_results.append(self.man5())
        self.test_results.append(self.sign1())
        self.test_results.append(self.sign3())
        self.test_results.append(self.perm2())

        self.test_results.append(self.prg1())
        minifyEnabled = config.get('PRG2', 'minifyEnabled')
        shrinkResources = config.get('PRG2', 'shrinkResources')
        self.test_results.append(self.prg2(shrinkResources, minifyEnabled))
        allowBackup = config.get('SEC1', 'allowBackup')
        self.test_results.append(self.sec1(allowBackup))
        return self.test_results

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
                    result = "FAILED."
                    additional = " In your resConfigs, you have: " + i + " but not in config file."
                    return (testId, self.b1_descp(), (result, additional))
                else:
                    found = False

            for conf in resConf_filtered:
                for i in self.gradleDict['android']["defaultConfig"][0]["resConfigs"][0]:
                    if i.lower() == conf.lower():
                        found = True
                        break  # found in the config
                if not found:
                    result = "FAILED."
                    additional = " In your config file, you have: " + conf + " but not in manifest."
                    return (testId, self.b1_descp(), (result, additional))
                else:
                    found = False
        else:
            result = "CONFIRM:"
            additional = " You dont have resConfigs in your project."
            return (testId, self.b1_descp(), (result, additional))

        result = "SUCCEED."
        additional = " Your resConfigs in config file match with the ones in the manifest."
        return (testId, self.b1_descp(), (result, additional))

    def b1_descp(self):
        return "Make sure to minimize res configs by only including necessary resources (localization etc.)"

    def b4(self):
        testId = "B4"
        appId = self.apkf.get_package()
        startingName = "com.monitise.mea."
        if appId.startswith(startingName):
            result = "SUCCEED."
            additional = "Your project name starts with \"com.monitise.mea\"."
        else:
            result = "FAILED."
            additional = "Your project name does not start with \"com.monitise.mea\" It starts with " + appId
        return (testId, self.b4_descp(), (result, additional))

    def b4_descp(self):
        return "Make sure that applicationId respects com.monitise.mea.<product> convention unless other indicated."

    def b6(self, configTargetSdk):
        testId = "B6"
        configTargetSdk
        targetSDK = self.apkf.get_target_sdk_version()
        if configTargetSdk == targetSDK:
            result = "SUCCEED."
            additional = "Your targetSdkVersion is: " + targetSDK + "."
        else:
            result = "FAILED."
            additional = "Your targetSdkVersion should be " + configTargetSdk + " but it is " + targetSDK + "."

        return (testId, self.b6_descp(), (result, additional))

    def b6_descp(self):
        return "Make sure that targetSdkVersion is set to most recent api version that app is tested against."

    def b7(self):
        testId = "B7 Test"
        for dep in self.gradleDict["dependencies"]["compile"]:
            if "com.google.android.gms:play-services:" in dep:
                result = "FAILED."
                additional = "Google Play Services API should be included as separate dependencies."
                return (testId, self.b7_descp(), (result, additional))
        result = "SUCCEED."
        additional = "Google Play Services API is not included with just one line. (or not included at all)"
        return (testId, self.b7_descp(), (result, additional))

    def b7_descp(self):
        return "Make sure that any Google Play Services API is included as separate dependencies."

    def b9(self):
        testId = "B9"
        if '@android:debuggable' in self.manifestDict['manifest']['application']:
            deb = self.manifestDict['manifest']['application']['@android:debuggable']
            deb = deb.lower()
            if deb == "true":
                result = "FAILED."
                additional = "debuggable should not be set to true."
                return (testId, self.b9_descp(), (result, additional))
        result = "SUCCEED."
        additional = "debuggable is not set to true."
        return (testId, self.b9_descp(), (result, additional))

    def b9_descp(self):
        return "Make sure that release build type in gradle build file doesn't have debuggable set to true."

    def man2(self):
        testId = "MAN2"

        if "@android:versionName" in self.manifestDict['manifest']:
            version = self.manifestDict['manifest']['@android:versionName']
            result = "CONFIRM:"
            additional = "Dismiss if you updated your version. android:versionName is set to: " + version + "."
        else:
            result = "FAILED."
            additional = "You need to update android:versionName."

        return (testId, self.man2_descp(), (result, additional))

    def man2_descp(self):
        return "Make sure that android:versionName attribute is updated."

    def man5(self):
        testId = "MAN5"

        if "@android:installLocation" in self.manifestDict['manifest']:
            location = self.manifestDict['manifest']['@android:installLocation']
            if location == "externalOnly":
                result = "FAILED."
                additional = "You cannot set android:installLocation to externalOnly."
                return (testId, self.man5_descp(), (result, additional))
        result = "SUCCEED."
        additional = " android:installLocation is not set to externalOnly."
        return (testId, self.man5_descp(), (result, additional))

    def man5_descp(self):
        return "Make sure that android:installLocation attributes is not set to externalOnly."

    def perm2(self):
        testId = "PERM2"

        result = "CONFIRM:"
        additional = "Check if all the permissions are necessary:"
        counter = 0
        for i in self.apkf.get_permissions():
            additional = additional + "\n\t- " + self.apkf.get_permissions()[counter]
            counter += 1
        return (testId, self.perm2_descp(), (result, additional))

    def perm2_descp(self):
        return "Make sure that app is NOT requesting any unnecessary permissions."

    def sec1(self, configAllowBackup):
        testId = "SEC1"
        configAllowBackup = configAllowBackup.lower()

        if "@android:allowBackup" in self.manifestDict['manifest']['application']:
            backup = self.manifestDict['manifest']['application']['@android:allowBackup']
            backup = backup.lower()
            configAllowBackup = configAllowBackup.lower()
            if backup == configAllowBackup:
                result = "SUCCEED."
                additional = "android:allowBackup is set to " + backup
            else:
                result = "FAILED."
                additional = "android:allowBackup is set to " + backup + ". But it must be " + configAllowBackup + "."
        elif configAllowBackup == "true":
            result = "FAILED."
            additional = "You need to specify android:allowBackup as true."
        else:
            result = "SUCCEED."
            additional = "Your android:allowBackup is set to false by default."
        return (testId, self.sec1_descp(), (result, additional))

    def sec1_descp(self):
        return "Make sure to set android:allowBackup to false unless otherwise indicated."

    def sign1(self):
        testId = "SIGN1"

        if not os.path.exists(self.project_dir + "/release.keystore.jks"):
            result = "FAILED."
            additional = " release.keystore.jks does not exist in your project path."
            return (testId, self.sign1_descp(), (result, additional))

    def sign1_descp(self):
        return "Make sure that a release keystore is created and used to sign any release configuration " \
               "(prod-release, internal-release, external-release etc.) of the app"

    def sign3(self):
        testId = "SIGN3"
        keyPath = ''

        try:
            keyPath = self.gradle['android']['signingConfigs'][0]['release'][0]['storeFile'][0][0]
        except:
            result = "FAILED."
            additional = "There is no given path for release keystore file"
            return (testId, self.sign3_descp(), (result, additional))

        if path.exists(keyPath):
            if "/build/" in keyPath:
                result = "FAILED"
                additional = " Your release keystore is in build classpath."
            else:
                result = "SUCCEED."
                additional = "Your release keystore is not in build classpath."

            return (testId, self.sign3_descp(), (result, additional))
        else:
            result = "FAILED."
            additional = " There is no release keystore in the project."
            return (testId, self.sign3_descp(), (result, additional))

    def sign3_descp(self):
        return "Make sure that the release keystore is NOT included in build classpath i.e. Apk should never expose this file"

    def prg1(self):
        testId = "PRG1"
        if 'monitise' in self.gradleDict:
            result = "SUCCEED."
            additional = "Your gradle has \"monitise\" block."
        else:
            result = "FAILED."
            additional = "Your gradle file does not have \"monitise\" block.  You forgot deleting logs."

        return (testId, self.prg1_descp(), (result, additional))

    def prg1_descp(self):
        return "Make sure that logging is disabled on release builds."

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
                result = "SUCCEED."
                additional = "minifyEnabled and shrinkResources are set to true."
                return (testId, self.prg2_descp(), (result, additional))

        result = "FAILED."
        additional = "minifyEnabled and shrinkResources must be true."
        return (testId, self.prg2_descp(), (result, additional))

    def prg2_descp(self):
        return "Make sure that minifyEnabled and shrinkResoureces are set to true for release build type"
