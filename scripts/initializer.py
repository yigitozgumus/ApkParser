#!/usr/bin/env python


import argparse
import os
import sys
import urllib2
from contextlib import contextmanager
from subprocess import call

from apk_parse import apk
from berker import ChecklistBerker

# Context manager function for changing directory if necessary
@contextmanager
def working_directory(directory):
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)

def main():
    project, apk = parse_parameters(sys.argv)
    berku = ChecklistBerker(project, apk)

    berku.B4()
    berku.B6()
    berku.MAN2()
    berku.MAN5()
    berku.SEC1()
#    apktool_loading()
#    printManifest(apk)
#    executeGradlewSigning(project)
#    apkfReport(apk)


#function for loading apktool to the system
#TODO maintanence for the jar version
def apktool_loading():
    scriptFile = urllib2.urlopen("https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/osx/apktool")
    jarFile = urllib2.urlopen("https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.2.0.jar")
    filename_script = "apktool"
    filename_jar = "apktool.jar"

    with working_directory("/tmp"):
        print "Downloading script..."
        with open(filename_script, "wb") as output_script:
            output_script.write(scriptFile.read())
        print "Downloading jar file..."
        with open(filename_jar, "wb") as output_jar:
            output_jar.write(jarFile.read())
        call(["mv",filename_script,"/usr/local/bin"])
        call(["mv", filename_jar, "/usr/local/bin"])

    with working_directory("/usr/local/bin"):
        print "Changing the mod of the script..."
        call(["chmod","+x",filename_script])
        print "Changing the mod of the jar..."
        call(["chmod", "+x", filename_jar])

#This function parses paramenters
def parse_parameters(argv):
    apk_location = ''
    project_location = ''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir',help='Directory location')
    parser.add_argument('-a','--apk',help='Apk file location')
    args = parser.parse_args()
    project_location = args.dir
    apk_location = args.apk
    return project_location,apk_location


def printManifest(apk_location):
    with working_directory("/tmp"):
        call(["apktool", "d", apk_location])
    # Print AndroidManifest.xml file
    with working_directory("/tmp" + "/app-release"):
        f = open("AndroidManifest.xml", "rw")
        for line in f:
            print line,

def executeGradlewSigning(project_location):
    with working_directory(project_location):
        call(["./gradlew", "signingReport"])


def apkfReport(apk_location):
    apk_inspect = apk.APK(apk_location)
    print apk_inspect.cert_text
    print apk_inspect.file_md5
    print apk_inspect.cert_md5
    print apk_inspect.file_size
    print apk_inspect.androidversion
    print apk_inspect.package
    print apk_inspect.get_android_manifest_xml()
    print apk_inspect.get_android_manifest_axml()
    print apk_inspect.is_valid_APK()
    print apk_inspect.get_filename()
    print apk_inspect.get_package()
    print apk_inspect.get_androidversion_code()
    print apk_inspect.get_androidversion_name()
    print apk_inspect.get_max_sdk_version()
    print apk_inspect.get_min_sdk_version()
    print apk_inspect.get_target_sdk_version()
    print apk_inspect.get_libraries()
    print apk_inspect.get_files()
    print apk_inspect.get_files_types()
    # print apkf.get_dex()
    print apk_inspect.get_main_activity()
    print apk_inspect.get_activities()
    print apk_inspect.get_services()
    print apk_inspect.get_receivers()
    print apk_inspect.get_providers()
    print apk_inspect.get_permissions()
    print apk_inspect.show()








if __name__ == "__main__":
    main()



