#!/usr/bin/env python

import yigit
import berker
import ConfigParser
import create_result_report


class Checklist(object):
    def __init__(self, project_dir, apk_dir):
        self.project_dir = project_dir
        self.apk_dir = apk_dir
        self.checklist_yigit = yigit.ChecklistYigit(self.project_dir, self.apk_dir)
        self.checklist_berker = berker.ChecklistBerker(self.project_dir, self.apk_dir)

    def executeTests(self,config_location):
        config = ConfigParser.ConfigParser()
        config.read(config_location)
        result_loc = config.get("OUTPUT","outputLocation")

        test_results = self.checklist_yigit.execute_test_batch(config_location)
        test_results2 = self.checklist_berker.execute_test_batch(config_location)
        test_res = test_results + test_results2
        results = create_result_report.CreateReport(test_res,result_loc)
        results.generate_report("Checklist Tests","This report shows the Checklist test results")






