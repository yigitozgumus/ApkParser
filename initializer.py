#!/usr/local/bin/python


import argparse
import sys
import urllib2
from scripts.checkUtil import working_directory
from subprocess import call
from subprocess import check_output
import scripts.CheckList as cl

def main():
    args = parse_parameters(sys.argv)
    project = args.dir
    config = args.config
    tasks = ''
    if args.tasks :
        tasks = args.tasks
        print tasks
    apk_extension= "/app/build/outputs/apk/app-external-release.apk"
    try:
        check_output(["apktool"])
    except:
        apktool_loading()
    tester = cl.Checklist(project,project+apk_extension)
    tester.executeTests(config)
    with working_directory("/tmp"):
        check_output(["rm","-rf","/app-release"])



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
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir',
                        nargs='?',
                        help='Directory location')
    parser.add_argument('-c', '--config',
                        nargs='?',
                        help='Config File Location')
    parser.add_argument('-t','--tasks',
                        nargs=1,
                        help='Optional task file to import check functions')

    return parser.parse_args()


if __name__ == "__main__":
    main()
