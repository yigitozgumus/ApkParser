#!/usr/bin/env python

import os
import re
import subprocess
import ConfigParser
from subprocess import check_output
import gradleParser_v2 as gr
import os.path as path
from apk_parse import apk
from checkUtil import extractXML
from checkUtil import working_directory
from bs4 import BeautifulSoup


class ChecklistYigit(object):
    """
    This class checks certain checklist items regarding the Android project
    Attributes:
        project_dir : Project directory of the Android app
    """
    is_apk_created = False
    apk_location = "/app/build/outputs/apk/app-external-release.apk"
    test_results = []

    def __init__(self, project_dir, apk_dir,config_location):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.manifest = extractXML(apk_dir,config_location)
        self.apkf_inspect = apk.APK(apk_dir)
        self.gradle = gr.GradleParserNew(self.project_dir + "/app").parse(False)

    def execute_test_batch(self,config_location):
        config = ConfigParser.ConfigParser()
        config.read(config_location)
        self.test_results.append(self.b2())
        minSdkVersion = config.get('B5', 'minSdkVersion')
        self.test_results.append(self.b5(minSdkVersion))
        self.test_results.append(self.b7())
        self.test_results.append(self.b8())
        self.test_results.append(self.man1())
        self.test_results.append(self.man3())
        self.test_results.append(self.sign4())
        self.test_results.append(self.perm3())
        proguardList = config.get('PRG3', 'proguardList')
        self.test_results.append(self.prg3(proguardList))
        self.test_results.append(self.apk2())
        self.test_results.append(self.sec4())
        flavor = config.get('GEN2','flavor')
        self.test_results.append(self.gen2(flavor))
        sdk_location = config.get('GEN4', 'sdkLocation')
        apk_location = config.get('GEN4', 'apkLocation')
        self.test_results.append(self.gen4(apk_location,sdk_location))
        self.test_results.append(self.man4())
        self.test_results.append(self.sign2())
        apk_folder_location = config.get('APK1', 'apkFolderLocation')
        self.test_results.append(self.apk1(apk_folder_location))
        return self.test_results

    def b2_desc(self):
        return "This test ensures the release apk is signed with release keystore; " \
               "verifies the signing information for each variant with gradle's signingReport" \
               " task"

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
            additional = "Please check assigned keys\n"
            for i in signing_report:
                additional = additional + i + '\n'
        return (testId,self.b2_desc(),(result,additional))

    def create_apk(self):
        """
        :return:
        """
        with working_directory(self.project_dir):
            subprocess.check_output(["./gradlew", "assembleRelease"])
        self.is_apk_created = True
        # print "Apk file is created"

    def b5_descp(self):
        return "This test makes sure that minSdkVersion is set to 16 for new projects. " \
               "Get approval from your PM, project's Technical Owner and your manager " \
               "before modifying this number on any ongoing project."


    def b5(self, config_minSdk):
        """
        :return:
        """
        testId = "B5"
        # if (not self.is_apk_created):
        #     self.create_apk()
        min_sdk = self.apkf_inspect.get_min_sdk_version()
        if (min_sdk == config_minSdk):
            result = "SUCCEED."
            additional = "Minimum sdk version is " + config_minSdk + ". Test successful."
        else:
            result = "FAILED."
            additional = "Test failed. Your project's minimum sdk is not " + config_minSdk + ", it is " + min_sdk + ". "

        return (testId,self.b5_descp(),(result,additional))

    def b7_descp(self):
        return "This test makes sure that compileSdkVersion is modified with " \
               "precaution and the app is fully tested against behavioral changes " \
               "with the new api version"

    def b7(self):
        """
        :return:
        """
        testId = "B7"
        # TODO ask the checklist item
        # if (not self.is_apk_created):
        #     self.create_apk()
        compile_sdk = self.gradle["android"]["compileSdkVersion"][0][0]
        result = "SUCCEED."
        additional = "Project compileSdkVersion is " + compile_sdk + ". Check for behavioral changes accordingly"

        return (testId,self.b7_descp(),(result,additional))

    def b8_descp(self):
        return "This test makes sure that each dependency injected has a specific " \
               "version specified"

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
            result += "SUCCEED."
            additional = "Every dependency injected has a specific version"
        else:
            result += "\nFAILED."
            additional = "Test failed."

        return (testId,self.b8_descp(),(result,additional))

    def man1_descp(self):
        return "This test returns the current version code for the project"

    def man1(self):
        """
        :return:
        """
        testId = "MAN1"
        # TODO How to read previous version code ?
        versionCode = self.gradle['android']['defaultConfig'][0]['versionCode'][0][0]
        result = "CONFIRM:"
        additional = "Current version code is " + versionCode
        return (testId,self.man1_descp(),(result,additional))

    def man3_descp(self):
        return "This test makes sure that android:versionName follows <major>." \
               "<minor>.<patch>.<buildNumber> convention."

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
        return (testId,self.man3_descp(),(result,additional))

    def sign4_descp(self):
        return "This test makes sure that storePassword, keyAlias, " \
               "keyPassword are set in the build.gradle file for release signing config."

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
                result = "FAILED."
                additional = "all values for the signingConfig are not defined.\n Defined are below:\n"
                for key in config_values.keys():
                    additional = additional + "\nthe key name is" + key + "and its value is" + config_values[key][0][1:-1]
                return
            for check in config_values.keys():
                if (len(config_values[check]) == 0):
                    result = result + "\nCheck " + check + " value"
                    isValid = False
            if (isValid):
                result = "SUCCEED. "
                additional = "All signingConfig values are valid"
        else:
            result = "FAILED."
            additional = "There is no config value in signingConfigs tag in your project."

        return (testId,self.sign4_descp(),(result,additional))

    def perm3_descp(self):
        return "This test makes sure to set android:required to false for hardware features e.g. " \
               "<uses-feature android:name=\"android.hardware.telephony\" android:required=\"true\"" \
               " /> will prevent Play Store to list the app to wifi only devices"

    def perm3(self):
        """
        :return:
        """
        testId = "PERM3"

        # if (not self.is_apk_created):
        #     self.createAPK()
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
                result = "SUCCEED."
                additional = "android:required attributes is false for all hardware features."
        else:
            result = "CONFIRM:"
            additional = "There is no uses-feature tag in this AndroidManifest.xml"

        return (testId,self.perm3_descp(),(result,additional))

    def prg3_descp(self):
        return "This test makes sure that default files like proguard-android.txt, " \
               "proguard-rules.pro is not in the project and project specific proguard " \
               "configurations files are added through proguardFiles property in the " \
               "release build type"

    def prg3(self, proguard_list):
        """
        :return:
        """
        # todo change print version
        testId = "PRG3"
        result = ""
        additional = ""
        proguard_files = self.gradle["android"]["buildTypes"][0]["release"][0]["proguardFiles"][0]
        proguard_list_filtered = proguard_list.split(",")
        proguard_list_filtered = [x.strip(" ") for x in proguard_list_filtered]
        isValid = True
        proguard_files.remove("getDefaultProguardFile")
        for file in proguard_files:
            if file in proguard_list_filtered:
                isValid = False
                additional = additional + "WARNING: " + file + " is added to the build.gradle\n"
        if isValid:
            result = "SUCCEED."
        else:
            result = "FAILED."

        additional += "Added proguard files listed below:\n"
        for i in range(len(proguard_files)):
            additional = additional + "{0}-) {1}".format(str(i + 1), proguard_files[i]) + "\n"

        return (testId,self.prg3_descp(),(result,additional))

    def apk2_descp(self):
        return "This test makes sure that the apk size for prod-release doesn't exceed 15 MB"

    def apk2(self):
        """
        :return:
        """
        testId = "APK2"
        # if (not self.is_apk_created):
        #     self.createAPK()
        apk_size = os.path.getsize(self.apk_dir)
        apk_rest = apk_size % (1024 * 1024)
        apk_size = apk_size / (1024 * 1024)

        if (apk_size < 15):
            result = "SUCCEED."
            additional = "Apk size is within limits.(" + str(apk_size) + "," + str(apk_rest) + "mb)."
        else:
            result = "FAILED."
            additional = "Apk size exceeds limits (>15mb)."

        return (testId,self.apk2_descp(),(result,additional))

    def sec4_descp(self):
        return "This test makes sure to set android:exported to false for services, " \
               "activities and broadcast receivers containing intent filters in order " \
               "to prevent other apps' components access if an activity doesn't have any " \
               "intent filter, android:exported is false by default; true otherwise, hence " \
               "it should be set to false explicitly in this case if any access from any other " \
               "application component is not expected or wanted."

    def sec4(self):
        """
        :return:
        """
        # todo change print version

        testId = "SEC4"
        result = "\n"
        # if (not self.is_apk_created):
        #     self.createAPK()
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
        additional = ''
        isValid = True
        if (activity_exist):
            for check in activities:
                if 'intent-filter' in check:
                    if '@android:exported' in check:
                        if check['@android:exported'].lower() == 'false' in check:
                            pass
                        else:
                            isValid = False
                            additional = additional + "CONFIRM: " + check[
                                '@android:name'] + "\t--> android:exported value should be set to false\n"
                    else:
                        isValid = False
                        radditional = additional + "CONFIRM: " + check[
                            '@android:name'] + "\t--> Please add android:exported=\"false\" attribute\n"
        if (service_exist):
            for check in services:
                if 'intent-filter' in check:
                    if '@android:exported' in check:
                        if check['@android:exported'].lower() == 'false' in check:
                            pass
                        else:
                            isValid = False
                            additional = additional + "CONFIRM: " + check[
                                '@android:name'] + "\t--> android:exported value should be set to false\n"
                    else:
                        isValid = False
                        additional = additional + "CONFIRM: " + check[
                            '@android:name'] + "\t--> Please add android:exported=\"false\" attribute\n"
        if (receiver_exist):
            for check in receivers:
                if 'intent-filter' in check:
                    if '@android:exported' in check:
                        if check['@android:exported'].lower() == 'false' in check:
                            pass
                        else:
                            isValid = False
                            additional = additional + "CONFIRM: " + check[
                                '@android:name'] + "\t--> android:exported value should be set to false\n"
                    else:
                        isValid = False
                        additional = additional + "CONFIRM: " + check[
                            '@android:name'] + "\t--> Please add android:exported=\"false\" attribute\n"

        if (isValid):
            result = "SUCCEED."
        else:
            result = "FAILED."

        return (testId,self.sec4_descp(),(result,additional))

    def gen2_descp(self):
        return "This test makes sure that basic functionality of the app is fully working "

    def gen2(self,flavor):
        """
        Runs all the tests including espressos and prints out the results
        @return:
        """
        testId = "GEN2"

        with working_directory(self.project_dir):
            output = check_output(["./gradlew", "connectedCheck"], shell=True,
                                  stderr=subprocess.STDOUT)
        flavor_list = []
        flavor_exist = True
        if ('productFlavors' in self.gradle['android'].keys()):
            test_locations = '/app/build/reports/androidTests/connected/flavors'
            with working_directory(self.project_dir + test_locations):
                flavors = check_output(["ls"]).split("\n")
                flavor_list = [x.strip("'") for x in flavors]
        else:
            test_locations = '/app/build/reports/androidTests/connected/'
            flavor_exist = False

        #Print external Report
        file = 'index.html'
        if(flavor_exist):
            report_location = '/app/build/reports/androidTests/connected/flavors/'+ flavor
        else:
            report_location = '/app/build/reports/androidTests/connected/'
            file_temp = check_output(["ls"]).split("\n")
            file = [x.strip("'") for x in file_temp if x != ' '][0]
        with working_directory(self.project_dir+report_location):
            soup = BeautifulSoup(open(file),'html.parser')
        success_rate = soup.find(id='successRate').div.get_text()
        tests = soup.find(id='tests').div.get_text().encode('utf-8')
        failures = soup.find(id='failures').div.get_text().encode('utf-8')
        links = [x.get('href') for x in soup.findAll('a') if ("tab" or ("gradle" or "html#s")) not in x.get('href')]
        if(success_rate != "100%"):
            result = "FAILED."
            additional = "Success rate is : "+success_rate +". "+ failures + " of "+ tests +" tests have failed. Please check :" + \
            "\n" + self.project_dir+report_location + "/index.html for more information."
        else:
            result = "SUCCEED."
            additional = "Success rate is : "+success_rate +". All of your tests have succeed. Please check :" + \
            "\n" + self.project_dir + report_location + "/index.html for more information."
        return (testId,self.gen2_descp(),(result,additional))


    def gen4_descp(self):
        return "Make sure to run following command to get brief information about the apk. " \
               "\"aapt d badging app/build/outputs/apk/app-prod-release.apk\" .Verify permissions, " \
               "locales and densities supported."

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
        locales = [x for x in list if "locales" in x]
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

        return (testId,self.gen4_descp(),res_add)

    def man4_descp(self):
        return "This test checks If MmP is requested instead of MmPb, make sure to hide " \
               "build number on android:VersionName attribute for prod-release config by " \
               "setting -PhideBuildNumber gradle parameter on jenkins job configuration."

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
            return (testId,self.man4_descp(),(result,additional))
        if len(version_name) != 0:
            version_coded = version_name.split(".")
            if len(version_coded) == 3:
                result = "SUCCEED."
                additional = "Version naming is correct"
            else:
                result = "FAILED."
                additional = "Please check your version name in the AndroidManifest file"
            return (testId,self.man4_descp(),(result,additional))

    def sign2_descp(self):
        return "This test makes sure that the release keystore is included in source control."

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
            return (testId,self.sign2_descp(),(result,additional))
        if path.exists(keystore_path):
            result = "SUCCEED."
            additional = "Keystore file is included in source Control."
        else:
            result = "FAILED."
            additional = "Keystore file isn't included in source Control"
        return (testId, self.sign2_descp(),(result, additional))

    def cq1(self):
        """

        @return:
        """
        print "This test will not be implemented."
        testId = "CQ1"

    def apk1_descp(self):
        return "Make sure that the apk available on dist.pozitron.com follows " \
               "<app-name>-<flavor>-<buildType>-<versionName>.apk name format"

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
            return(testId, self.apk1_descp(), (result, additional))
        flavors = self.gradle['android']['productFlavors'][0].keys()
        version_name = '1.2.3'
        try:
            version_name = self.manifest['manifest']['android:versionName']
        except:
            result = "FAILED."
            additional = "There is no defined android:VersionName in the AndroidManifest file"
            return (testId, self.apk1_descp(), (result, additional))
        build_types = self.gradle['android']['buildTypes'][0].keys()
        # name combinations
        apk_results = []
        if (len(flavors) == 0 or len(build_types) == 0 or version_name == ''):
            result = "FAILED."
            additional = "Check flavors, build types and version name declarations"
            return (testId,self.apk1_descp(),(result,additional))
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
            return (testId, self.apk1_descp(), apk_results)
