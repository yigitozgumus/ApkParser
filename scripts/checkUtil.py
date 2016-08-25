#!/usr/bin/env python

from contextlib import contextmanager
import os
import subprocess
import xmltodict
import ConfigParser
import json, ast


# Context manager function for changing directory if necessary
@contextmanager
def working_directory(directory):
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)


# def extractXML(project_dir, apk_location):
#     """
#     Parses AndroidManifest file and returns a dictionary object
#     :param project_dir: Project Location
#     :param apk_location: Apk location
#     :return: Parsed AndroidManifest Dictionary
#     """
#     with working_directory(project_dir):
#         subprocess.check_output(["./gradlew", "assembleRelease"])
#     with working_directory("/tmp"):
#         subprocess.call(["apktool", "d", apk_location])
#     with working_directory("/tmp" + "/app-release/"):
#         with open("AndroidManifest.xml") as fd:
#             obj_file = xmltodict.parse(fd.read())
#             return ast.literal_eval(json.dumps(obj_file))

def extractXML(apk_location,config_location):
    """

    @param project_dir:
    @param apk_location:
    @return:
    """
    with working_directory("/tmp"):
        subprocess.call(["apktool", "d", apk_location])
    config = ConfigParser.ConfigParser()
    config.read(config_location)
    app_name = "app-external-release"
    temp = config.get("APP_NAME","app_flavor_name")
    if temp != None:
        app_name = temp
    with working_directory("/tmp/" + app_name):
        with open("AndroidManifest.xml") as fd:
            obj_file = xmltodict.parse(fd.read())
            return ast.literal_eval(json.dumps(obj_file))
