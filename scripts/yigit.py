#!/usr/bin/env python

import os
import re
import subprocess
from subprocess import check_output
import gradleParser_v2 as gr
import os.path as path
from apk_parse import apk
from checkUtil import extractXML
from checkUtil import working_directory


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

    def showResults(self, testId, res_add_tuples):
        print "\n\n============ " + testId + " Test ==========================================="
        for result, additional in res_add_tuples:
            print "=="
            print "==\t" + result + additional
            print "=="
            print "=================================================================="

    def b2(self):
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

    def create_apk(self):
        """
        :return:
        """
        with working_directory(self.project_dir):
            subprocess.check_output(["./gradlew", "assembleRelease"])
        self.is_apk_created = True
        # print "Apk file is created"

    def b5(self, config_minSdk):
        """
        :return:
        """
        testId = "B5"
        if (not self.is_apk_created):
            self.create_apk()
        min_sdk = self.apkf_inspect.get_min_sdk_version()
        if (min_sdk == config_minSdk):
            result = "SUCCEED."
            additional = "Minimum sdk version is " + config_minSdk + ". Test successful."
        else:
            result = "FAILED."
            additional = "Test failed. Your project's minimum sdk is not " + config_minSdk + ", it is " + min_sdk + ". "

        self.showResult(testId, result, additional)

    def b7(self):
        """
        :return:
        """
        testId = "B7 Test"
        # TODO ask the checklist item
        if (not self.is_apk_created):
            self.create_apk()
        compile_sdk = self.gradle["android"]["compileSdkVersion"][0][0]
        result = "SUCCEED."
        additional = "Project compileSdkVersion is " + compile_sdk + ". Check for behavioral changes accordingly"

        self.showResult(testId, result, additional)

    def b8(self):
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

    def man1(self):
        """
        :return:
        """
        testId = "MAN1"
        # TODO How to read previous version code ?
        versionCode = self.gradle['android']['defaultConfig'][0]['versionCode'][0][0]
        result = "CONFIRM:"
        additional = "Current version code is " + versionCode

        self.showResult(testId, result, additional)

    def man3(self):
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

    def sign4(self):
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

    def perm3(self):
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
                        if not (feature['@android:required'].lower() == "false"):
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

    def prg3(self, proguard_list):
        """
        :return:
        """
        # todo change print version
        testId = "PRG3"
        result = "\n"
        additional = ""
        proguard_files = self.gradle["android"]["buildTypes"][0]["release"][0]["proguardFiles"][0]
        proguard_list_filtered = proguard_list.split(",")
        proguard_list_filtered = [x.strip(" ") for x in proguard_list_filtered]
        isValid = True
        proguard_files.remove("getDefaultProguardFile")
        for file in proguard_files:
            if file in proguard_list_filtered:
                isValid = False
                result = result + "==\tWARNING: " + file + " is added to the build.gradle\n"
        if isValid:
            result += "==\tSUCCEED.\n"
        else:
            result += "==\tFAILED.\n"

        result += "==\tAdded proguard files listed below:"
        for i in range(len(proguard_files)):
            result = result + "\n==\t{0}-) {1}".format(str(i + 1), proguard_files[i]) + ""

        self.showResult(testId, result, additional)

    def apk2(self):
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

    def sec4(self):
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
                        if check['@android:exported'].lower() == 'false' in check:
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
                        if check['@android:exported'].lower() == 'false' in check:
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
                        if check['@android:exported'].lower() == 'false' in check:
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

        self.showResult(testId, result, "")

    def gen2(self):
        """

        @return:
        """
        testId = "GEN2"

    def gen4(self, apk_location, sdk_location):
        """
        runs aapt command and verifies permissions, locales and densities supported
        @return:
        """
        testId = "GEN4"
        res_add = []
        with working_directory(sdk_location):
            output = check_output(["./aapt", "d", "badging", self.project_dir + apk_location])
        # information extraction
        list = output.split("\n")
        permission_aapt = [re.search("\'[\s\S]+\'", x).group(0).strip("'") for x in list if "permission" in x]
        permission_annotate = [re.search("^[\s\S]+:", x).group(0).strip(":") for x in list if "permission" in x]
        permission_manifest = [x["@android:name"] for x in self.manifest['manifest']['uses-permission']]

        densitiy_info = [x for x in list if "densities" in x]
        densities_supported = map(lambda x: x.strip("'"), densitiy_info[0].split(" ")[1:])

        any_density = [x for x in list if "supports-any-density" in x]
        locales = [x for x in list if "locales"]
        locales_supported = map(lambda x: x.strip("'"), locales[0].split(" ")[1:])
        try:
            locales_gradle = self.gradle['android']['defaultConfig'][0]['resConfigs'][0]

        except:
            pass
        # Verify permissions
        aapt_length = len(permission_aapt)
        manifest_length = len(permission_manifest)
        if (aapt_length != manifest_length):
            result = "FAILED."
            len_long = permission_aapt if aapt_length > manifest_length else permission_manifest
            len_short = permission_manifest if len_long == permission_aapt else permission_aapt
            additional = "The number of permissions in manifest and aapt result are different." \
                         ""
            differences = ''
            for i in len_long:
                if i < len(len_short):
                    if (len_long[i] != len_short[i]):
                        differences = differences + permission_annotate[i] + "->"
            res_add.append((result, additional))
        # Verify Densities
        if "true" in any_density[0]:
            result = "SUCCEED."
            additional = "Application supports all densities. Here are the defined ones: " \
                         + " ".join(densities_supported)
            res_add.append((result, additional))
        else:
            result = "WARNING."
            additional = "Support any density option is false. Here are the defined densities: " \
                         + " ".join(densities_supported)
            res_add.append(result, additional)
        # Verify Locales
        locale_check = True
        if (len(locales_gradle) == 0 or len(locales_supported) == 0):
            result = "FAILED."
            additional = "Your locale definitions are empty. Check your Project"
            res_add.append((result, additional))
        for locale in locales_supported:
            if locale not in locales_gradle:
                locale_check = False
        if (locale_check):
            result = "SUCCEED."
            additional = "Your locale definitions are consistent"
            res_add.append((result, additional))
        else:
            result = "FAILED."
            additional = "Your locale definitions are inconsistent. Check your Project"
            res_add.append((result, additional))

        self.showResults(testId, res_add)

    def man4(self):
        """
        Check android:Version name from manifest file
        @return:
        """
        testId = "MAN4"
        res_add = []
        version_name = ''
        try:
            version_name = self.manifest['manifest']['android:versionName']
        except:
            result = "FAILED."
            additional = "There is no defined android:VersionName in the AndroidManifest file"
            self.showResult(testId, result, additional)
        if len(version_name) != 0:
            version_coded = version_name.split(".")
            if len(version_coded) == 3:
                result = "SUCCEED."
                additional = "Version naming is correct"
                self.showResult(testId, result, additional)
            else:
                result = "FAILED."
                additional = "Please check your version name in the AndroidManifest file"
                self.showResult(testId, result, additional)

    def sign2(self):
        """
        This test makes sure the release keystore is included in source control
        @return:
        """
        testId = "SIGN2"
        keystore_path = ''
        try:
            keystore_path = self.gradle['android']['signingConfigs'][0]['release'][0]['storeFile'][0][0]
        except:
            result = "FAILED."
            additional = "There is no given path for Release Keystore file"
            self.showResult(testId, result, additional)
            return
        if path.exists(keystore_path):
            result = "SUCCEED."
            additional = "Keystore file is included in source Control."
            self.showResult(testId, result, additional)
        else:
            result = "FAILED."
            additional = "Keystore file isn't included in source Control"
            self.showResult(testId, result, additional)

    def cq1(self):
        """

        @return:
        """
        testId = "CQ1"

    def apk1(self, apk_folder):
        """
        Checks the apk for the <app-name>-<flavor>-<buildType>-<versionName>.apk convention
        @return:
        """
        testId = "APK1"
        with working_directory(self.project_dir + apk_folder):
            apk_names = check_output(["ls"]).split("\n")
        try:
            app_name = self.gradle['monitise']['appOptions'][0]['projectName'][0]
        except:
            result = "FAILED."
            additional = "There is no monitise section in gradle file"
            self.showResult(testId, result, additional)
            return
        flavors = self.gradle['android']['productFlavors'][0].keys()
        version_name = '1.2.3'
        try:
            version_name = self.manifest['manifest']['android:versionName']
        except:
            result = "FAILED."
            additional = "There is no defined android:VersionName in the AndroidManifest file"
            self.showResult(testId, result, additional)
            return
        build_types = self.gradle['android']['buildTypes'][0].keys()
        # name combinations
        apk_results = []
        if (len(flavors) == 0 or len(build_types) == 0 or version_name == ''):
            result = "FAILED."
            additional = "Check flavors, build types and version name declarations"
            self.showResult(testId, result, additional)
        else:
            for app in apk_names:
                check_app = app.split("-")
                if len(check_app) != 4:
                    result = "FAILED."
                    additional = app + " is not a valid name for the project"
                    apk_results.append((result, additional))
                else:
                    is_valid = True
                    additional = ''
                    if check_app[0] != app_name:
                        is_valid = False
                        additional = additional + "\n==\t" + app + "'s app name is not consistent with the project"
                    if check_app[1] not in flavors:
                        is_valid = False
                        additional = additional + "\n==\t" + app + "'s flavor value is not consistent with the project"
                    if check_app[2] not in build_types:
                        is_valid = False
                        additional = additional + "\n==\t" + app + "'s build type is not consistent with the project"
                    if check_app[3] != version_name:
                        is_valid = False
                        additional = additional + "\n==\t" + app + "'s version name is not consistent with the project"
                    if (is_valid):
                        result = "SUCCEED."
                        additional = app + "'s name is valid. "
                        apk_results.append((result, additional))
                    else:
                        result = "FAILED."
                        apk_results.append((result, additional))
            self.showResults(testId, apk_results)
