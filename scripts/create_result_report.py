#!/usr/bin/env python

from checkUtil import working_directory
from subprocess import check_output
import style_files as style

class CreateReport(object):

    def __init__(self,test_results,output_directory):
        self.test_results = test_results
        self.output_dir = output_directory
        self.opening_string = "<!DOCTYPE html>\n" \
                              "<html>\n" \
                              "<head>\n" \
                              "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" \
                              "<link rel=\"stylesheet\" href=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">\n" \
                              "<link href=\"css/base-style.css\" rel=\"stylesheet\" type=\"text/css\"/>"\
                              "<link href=\"css/style.css\" rel=\"stylesheet\" type=\"text/css\"/"\
                              "<script src=\"js/report.js\" type=\"text/javascript\"></script>"\
                              "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js\">\n" \
                              "</script><script src=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\">\n" \
                              "</script>\n" \
                              "</head>\n" \
                              "<body>\n"
        self.closing_string = " </body>\n" \
                              "</html>\n"

    def generate_report(self,title,description):
        #open a file
        with working_directory(self.output_dir):
            check_output(["mkdir","-p","Report"])
        with working_directory(self.output_dir+"/Report"):
            check_output(["mkdir","-p", "js"])
            check_output(["mkdir","-p", "css"])
        with working_directory(self.output_dir + "/Report/js"):
            f = open("report.js", "w")
            f.write(style.report_js)
            f.close()
        with working_directory(self.output_dir + "/Report/css"):
            f = open("style.css", "w")
            f.write(style.style_css)
            f.close()
            f = open("base-style.css", "w")
            f.write(style.base_style_css)
            f.close()
        # Statistics
        total_tests = len(self.test_results)
        failures = 0
        for element in self.test_results:
            if(type(element[2]) == tuple):
                if(element[2][0] == "FAILED."):
                    failures +=1
            elif(type(element[2]) == list):
                list0 = [val1 for val1,val2 in element[2]]
                if "FAILED." in list0:
                    failures +=1
        successes = 0
        for element in self.test_results:
            if(type(element[2]) == tuple):
                if(element[2][0] == "SUCCEED."):
                    successes +=1
            elif(type(element[2]) == list):
                list0 = [val1 for val1,val2 in element[2]]
                if "FAILED." not in list0:
                    successes +=1
        confirms = total_tests - successes - failures
        success_rate = int(float((successes + confirms)) / total_tests * 100)



        with working_directory(self.output_dir + '/Report'):

            file = open("report.html","w")
        file.write(self.opening_string)
        table_setup = "<div class=\"container\">\n" \
                      "<h1><b>Test Summary</b></h1>\n" \
                      "<div id=\"summary\">\n" \
                      "<table>\n" \
                      "<tr>\n" \
                      "<td>\n" \
                      "<div class=\"summaryGroup\">\n" \
                      "<table>\n" \
                      "<tr>\n" \
                      "<td>\n" \
                      "<div class=\"infoBox\" id=\"tests\">\n" \
                      "<div class=\"counter\">"+str(total_tests)+"</div>\n" \
                      "<p>Total number of tests</p>\n" \
                      "</div>\n" \
                      "</td>\n" \
                      "<td>\n" \
                      "<div class=\"infoBox\" id=\"failures\">\n" \
                      "<div class=\"counter\">"+str(failures)+"</div>\n" \
                      "<p>Failures</p>\n" \
                      "</div>\n" \
                      "</td>\n" \
                      "<td>\n" \
                      "<div class=\"infoBox\" id=\"failures\">\n" \
                      "<div class=\"counter\">" + str(confirms) + "</div>\n" \
                      "<p>Needs Confirmation</p>\n" \
                      "</div>\n" \
                      "</td>\n" \
                      "<td>\n" \
                      "<div class=\"infoBox\" id=\"failures\">\n" \
                      "<div class=\"counter\">" + str(successes) + "</div>\n" \
                      "<p>Passed</p>\n" \
                      "</div>\n" \
                      "</td>\n" \
                      "</tr>\n" \
                      "</table></div></td><td><div class=\"infoBox failures\" id=\"successRate\">\n" \
                      "<div class=\"percent\">"+str(success_rate)+"%</div>\n" \
                      "<p>successful</p>\n" \
                      "</div>\n" \
                      "</td>\n" \
                      "</tr>\n" \
                      "</table>\n" \
                      "</div>"\
                      "<h1><b>" + title +"</b></h1>\n" \
                      "<p>" + description +"</p>\n" \
                      "<div class=\"table\" >\n" \
                      "<table class=\"table table-hover table-cond\" border=\"4px\">\n" \
                      "<thead>\n" \
                      "<tr>\n" \
                      "<th>Test Id</th>\n" \
                      "<th>Description</th>\n" \
                      "<th>Result</th>\n" \
                      "<th>Additional Information</th>\n" \
                      "</tr>\n" \
                      "</thead>\n"
        file.write(table_setup)
        file.write("<tbody>\n")
        for elements in self.test_results:
            if type(elements[2]) == list:
                is_succeed = False
                is_failed=False
                for element in elements[2]:
                    if element[0] == "SUCCEED.":
                        is_succeed = True
                    elif element[0] == "FAILED.":
                        is_failed = True
                if(is_succeed and not(is_failed)):
                    file.write("<tr class=\"success\">")
                elif(is_succeed and is_failed):
                    file.write("<tr class=\"warning\">")
                elif(not(is_succeed) and is_failed):
                    file.write("<tr class=\"danger\">")
            elif "FAILED." in elements[2]:
                file.write("<tr class=\"danger\">")
            elif "CONFIRM:" in elements[2]:
                file.write("<tr class=\"info\">")
            elif "SUCCEED." in elements[2]:
                file.write("<tr class=\"success\">")
            for index in range(len(elements)):
                if type(elements[index]) == str:
                    file.write("<td>\n")
                    if index == 0:
                        file.write("<b>" +elements[index].replace("\n","<br />")+ "</b>\n")
                    else:
                        file.write(elements[index])
                    file.write("</td>\n")
                elif type(elements[index]) == tuple:
                    file.write("<td>\n")
                    file.write("<b>" +elements[index][0].replace("\n","<br />")+ "</b>\n")
                    file.write("</td>\n")
                    file.write("<td>\n")
                    file.write(elements[index][1].replace("\n","<br />\n"))
                    file.write("</td>\n")
                elif type(elements[index]) == list:
                    file.write("<td>\n")
                    file.write("<b>\n")
                    for sub_sub in elements[index]:
                        file.write(sub_sub[0].replace("\n","<br />") + "<br />\n")
                    file.write("</b>\n")
                    file.write("</td>\n")
                    file.write("<td>\n")
                    for sub_sub in elements[index]:
                        file.write(sub_sub[1].replace("\n","<br />")+"<br />\n")
                    file.write("</td>\n")
            file.write("</tr>\n")
        file.write("</tbody>\n</table>\n</div>\n</div>\n")
        file.write(self.closing_string)
        file.close()

