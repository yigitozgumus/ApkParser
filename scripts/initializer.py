import urllib2
from subprocess import call
import os
from contextlib import contextmanager

@contextmanager
def working_directory(directory):
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)

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





