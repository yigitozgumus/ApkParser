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
    def generate_report(self):
        #open a file
        with working_directory(self.output_dir):
            file = open("report.html","w")
        file.write(self.opening_string)
        # http://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_ref_table-responsive&stacked=h
        file.write(self.closing_string)
