#!/usr/bin/env python

from checkUtil import working_directory
from checkUtil import extractXML
from apk_parse import apk
from collections import defaultdict
import subprocess
import gradleParser_v2 as gr
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

    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.manifest = extractXML(project_dir, apk_dir)
        self.apkf_inspect = apk.APK(apk_dir)
        self.gradle = gr.GradleParserNew(self.project_dir + "/app").parse(False)

    def showResult(self, testId, result, additional):
        print "\n\n============ " + testId + " Test ==========================================="
        print "=="
        print "==\t" + result + additional
        print "=="
        print "==================================================================\n"

    def B2(self):
        """
        This test executes gradle signing Report
        :param project_dir: Project location
        :return: to be documented
        """
        testId = "B2"
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
        for i in signing_report:
            print i

    def createAPK(self):
        """
        :return:
        """
        with working_directory(self.project_dir):
            subprocess.check_output(["./gradlew", "assembleRelease"])
        self.is_apk_created = True
        # print "Apk file is created"

    def B5(self, config_minSdk):
        """
        :return:
        """
        testId = "B5"
        if (not self.is_apk_created):
            self.createAPK()
        min_sdk = self.apkf_inspect.get_min_sdk_version()
        if (min_sdk == config_minSdk):
            result = "SUCCEED."
            additional = "Minimum sdk version is " + config_minSdk + ". Test successful."
        else:
            result = "FAILED."
            additional = "Test failed. Your project's minimum sdk is not " + config_minSdk + ", it is " + min_sdk + ". "

        self.showResult(testId, result, additional)

    def B7(self):
        """
        :return:
        """
        testId = "B7 Test"
        # TODO ask the checklist item
        if (not self.is_apk_created):
            self.createAPK()
        compile_sdk = self.gradle["android"]["compileSdkVersion"][0][0]
        result = "SUCCEED."
        additional = "Project compileSdkVersion is " + compile_sdk + ". Check for behavioral changes accordingly"

        self.showResult(testId, result, additional)

    def B8(self):
        """
        :return:
        """
        # TODO print
        testId = "B8"
        dependencies = [x for x in self.gradle["dependencies"]["compile"] if len(x) == 1]
        result = ""
        is_valid = True
        for dependency in dependencies:
            if not (re.search("\d+.\+", dependency[0]) == None):
                is_valid = False
                result = "CONFIRM: Please check the latest version of " + dependency[1:-1]
        if is_valid:
            result += "\n==\tSUCCEED."
            additional = "Every dependency injected has a specific version"
        else:
            result += "\nFAILED."
            additional = "Test failed."

        self.showResult(testId, result, additional)

    def MAN1(self):
        """
        :return:
        """
        testId = "MAN1"
        # TODO How to read previous version code ?
        versionCode = self.gradle['android']['defaultConfig'][0]['versionCode'][0][0]
        result = "CONFIRM:"
        additional = "Current version code is " + versionCode

        self.showResult(testId, result, additional)

    def MAN3(self):
        """
        :return:
        """
        testId = "MAN3"
        version_name = self.gradle["android"]["defaultConfig"][0]["versionName"][0]
        versions = version_name[0].split(".")
        if (not (len(versions) == 4)):
            result = "FAILED."
            additional = "Version name does not follow <major>.<minor>.<patch>.<buildNumber> convention."
        else:
            result = "SUCCEED."
            additional = "Version name is valid"
        self.showResult(testId, result, additional)

    def SIGN4(self):
        """
        :return:
        """
        testId = "SIGN4"
        # TODO improve test logic.
        # todo change print version
        if "config" in self.gradle['android']['signingConfigs']:
            config_values = self.gradle["android"]["signingConfigs"]["config"]
            num_configs = len(config_values.keys())
            isValid = True
            if (num_configs < 4):
                result = "FAILED. all values for the signingConfig are not defined.\n Defined are below:\n"
                for key in config_values.keys():
                    result = result + "==\tthe key name is" + key + "and its value is" + config_values[key][0][1:-1]
                return
            for check in config_values.keys():
                if (len(config_values[check]) == 0):
                    result = result + "\n==\tCheck " + check + " value"
                    isValid = False
            if (isValid):
                result = "SUCCEED. All signingConfig values are valid"
        else:
            result = "FAILED. There is no config value in signingConfigs tag in your project."

        self.showResult(testId, result, "")

    def PERM3(self):
        """
        :return:
        """
        testId = "PERM3"

        if (not self.is_apk_created):
            self.createAPK()
        isValid = True
        feature_list = self.manifest['manifest']
        if 'uses-feature' in feature_list.keys():
            uses_f = feature_list['uses-feature']
            if (not (type(uses_f) == list)):
                uses_f = [uses_f]
            for feature in uses_f:
                if "@android:name" in feature:
                    feature_name = feature['@android:name']
                    if "hardware" in feature_name:
                        if not (feature['@android:required'] == "False"):
                            isValid = False
                            result = "FAILED."
                            additional = "Please change " + feature['@android:name'] + " requirement to False"
            if isValid:
                result = "SUCCESS."
                additional = "Test is successful"
        else:
            result = "CONFIRM:"
            additional = "There is no uses-feature tag in this AndroidManifest.xml"

        self.showResult(testId, result, additional)

    def PRG3(self, proguard_list):
        """
        :return:
        """
        # todo change print version
        testId = "PRG3"
        result = "\n"
        additional = ""
        proguard_files = self.gradle["android"]["buildTypes"][0]["release"][0]["proguardFiles"][0]
        isValid = True
        proguard_files.remove("getDefaultProguardFile")
        for file in proguard_files:
            if file in proguard_list:
                isValid = False
                result = result + "==\tWARNING: " + file + " is added to the build.gradle\n"
        if isValid:
            result += "==\tSUCCEED.\n"
        else:
            result += "==\tFAILED.\n"

        result += "==\tAdded proguard files listed below:\n"
        for i in range(len(proguard_files)):
            result = result + "==\t{0}-) {1}".format(str(i + 1), proguard_files[i]) + "\n"

        self.showResult(testId, result, additional)

    def APK2(self):
        """
        :return:
        """
        testId = "APK2"
        if (not self.is_apk_created):
            self.createAPK()
        apk_size = os.path.getsize(self.apk_dir)
        apk_rest = apk_size % (1024 * 1024)
        apk_size = apk_size / (1024 * 1024)

        if (apk_size < 15):
            result = "SUCCEED."
            additional = "Apk size is within limits.(" + str(apk_size) + "," + str(apk_rest) + "mb)."
        else:
            result = "FAILED."
            additional = "Apk size exceeds limits (>15mb)."

        self.showResult(testId, result, additional)

    def SEC4(self):
        """
        :return:
        """
        # todo change print version

        testId = "SEC4"
        result = "\n"
        if (not self.is_apk_created):
            self.createAPK()
        activities, services, receivers = object(), object(), object()
        activity_exist, service_exist, receiver_exist = False, False, False
        if 'activity' in self.manifest['manifest']['application'].keys():
            activity_exist = True
            activities = self.manifest['manifest']['application']['activity']
        if 'service' in self.manifest['manifest']['application'].keys():
            service_exist = True
            services = self.manifest['manifest']['application']['service']
        if 'receiver' in self.manifest['manifest']['application'].keys():
            receiver_exist = True
            receivers = self.manifest['manifest']['application']['receiver']
        isValid = True
        if (activity_exist):
            for check in activities:
                if 'intent-filter' in check:
                    if '@android:exported' in check:
                        if check['@android:exported'] == 'false' in check:
                            pass
                        else:
                            isValid = False
                            result = result + "==\tCONFIRM: " + check[
                                '@android:name'] + "\t--> android:exported value should be set to false\n"
                    else:
                        isValid = False
                        result = result + "==\tCONFIRM: " + check[
                            '@android:name'] + "\t--> Please add android:exported=\"false\" attribute\n"
        if (service_exist):
            for check in services:
                if 'intent-filter' in check:
                    if '@android:exported' in check:
                        if check['@android:exported'] == 'false' in check:
                            pass
                        else:
                            isValid = False
                            result = result + "==\tCONFIRM: " + check[
                                '@android:name'] + "\t--> android:exported value should be set to false\n"
                    else:
                        isValid = False
                        result = result + "==\tCONFIRM: " + check[
                            '@android:name'] + "\t--> Please add android:exported=\"false\" attribute\n"
        if (receiver_exist):
            for check in receivers:
                if 'intent-filter' in check:
                    if '@android:exported' in check:
                        if check['@android:exported'] == 'false' in check:
                            pass
                        else:
                            isValid = False
                            result = result + "==\tCONFIRM: " + check[
                                '@android:name'] + "\t--> android:exported value should be set to false\n"
                    else:
                        isValid = False
                        result = result + "==\tCONFIRM: " + check[
                            '@android:name'] + "\t--> Please add android:exported=\"false\" attribute\n"

        if (isValid):
            result = result + "==\tSUCCEED."
        else:
            result = result + "==\tFAILED."

        self.showResult(testId,result,"")