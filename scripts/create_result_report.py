#!/usr/bin/env python

from checkUtil import working_directory

class CreateReport(object):

    def __init__(self,test_results,output_directory):
        self.test_results = test_results
        self.output_dir = output_directory
        self.opening_string = "<!DOCTYPE html>\n" \
                              "<html>\n" \
                              "<head>\n" \
                              "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n" \
                              "<link rel=\"stylesheet\" href=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">\n" \
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
            file = open("report.html","w")
        file.write(self.opening_string)
        table_setup = "<div class=\"container\">\n" \
                      "<h2>" + title +"</h2>\n" \
                      "<p>" + description +"</p>\n" \
                      "<div class=\"table\" >\n" \
                      "<table class=\"table\" border=\"5px\">\n" \
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
                    file.write("<td>")
                    if index == 0:
                        file.write("<b>" +elements[index]+ "</b>")
                    else:
                        file.write(elements[index])
                    file.write("</td>")
                elif type(elements[index]) == tuple:
                    file.write("<td>")
                    file.write(elements[index][0])
                    file.write("</td>")
                    file.write("<td>")
                    file.write(elements[index][1])
                    file.write("</td>")
                elif type(elements[index]) == list:
                    file.write("<td>")
                    for sub_sub in elements[index]:
                        file.write(sub_sub[0] + "\n")
                    file.write("</td>")
                    file.write("<td>")
                    for sub_sub in elements[index]:
                        file.write(sub_sub[1]+"\n")
                    file.write("</td>")
            file.write("</tr>")
        file.write("</tbody>\n</table>\n</div>\n</div>")
        file.write(self.closing_string)
        file.close()

