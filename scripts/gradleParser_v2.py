#!/usr/bin/env python

from checkUtil import working_directory
from collections import defaultdict
import tokenize
from io import BytesIO


class gradleParserNew(object):
    """

    This class will parse standard build gradle file and create a nested dictionary
    """
    dictionary_list = ["outside"]
    gradle_dict = dict()
    tokens_initial = list()
    token_list = list()

    def __init__(self, gradle_dir):
        with working_directory(gradle_dir):
            self.file = open("build.gradle", "r")

        def handle_token(type, token, (srow, scol), (erow, ecol), line):
            self.tokens_initial.append((tokenize.tok_name[type], repr(token).strip("\"\'")))

        tokenize.tokenize(self.file.readline, handle_token)
        # Delete rogue newlines between dict names and {'s
        self.token_list.append(self.tokens_initial[0])
        for i in range(1, len(self.tokens_initial) - 1):
            if (not (self.tokens_initial[i - 1][0] == "NAME" and self.tokens_initial[i + 1][1] == "{")):
                self.token_list.append(self.tokens_initial[i])
        self.token_list.reverse()

    def parse(self):
        # first dictionary initialization
        self.gradle_dict[self.dictionary_list[0]] = defaultdict(list)
        while not (len(self.token_list) == 0):
            parse_line = []
            while True:
                parse_line.append(self.token_list.pop())
                if (parse_line[-1][0] == 'NEWLINE' or parse_line[-1][0] == 'NL' or len(self.token_list) == 0):
                    break;
            # containment checks
            if (len(parse_line) == 1 and self.checkElements(parse_line, ['\\n'])):
                pass

            elif (self.checkElements(parse_line, ["{"]) and self.checkElements(parse_line, ["}"])):

                new_dict = parse_line[0][1]
                parent_node = self.dictionary_list[-1]

                if (not (new_dict in self.gradle_dict[parent_node].keys())):
                    self.gradle_dict[parent_node][new_dict] = defaultdict(list)

                element_list = self.purifyElements(parse_line, ["{", "}"])
                self.gradle_dict[parent_node][new_dict][element_list[1]].append(element_list[2:-1])

            elif (self.checkElements(parse_line, ["{"])):
                if (self.checkElements(parse_line, ["(", ")"])):
                    element_list = self.purifyElements(parse_line, ["(", ")"])
                    new_dict = element_list[1]
                    self.dictionary_list.append(new_dict)
                    self.gradle_dict[new_dict] = defaultdict(list)
                else:
                    new_dict = parse_line[0][1]
                    self.dictionary_list.append(new_dict)
                    self.gradle_dict[new_dict] = defaultdict(list)
            elif (not (self.checkElements(parse_line, ["{", "}"]))):
                current_node = self.gradle_dict[self.dictionary_list[-1]]
                element_list = self.purifyElements(parse_line, ["=", ":", ",", ";", "file", "(", ")"])

                if (self.checkElements(element_list, ["."])):
                    self.purifyElements(element_list, ["."])
                    joined_element = ".".join(element_list[1:-1])
                    current_node[element_list[0]].append(joined_element)

                elif (len(element_list) == 2):
                    current_node[element_list[0]].append(element_list[0])

                else:
                    current_node[element_list[0]].append(element_list[1:-1])

            elif (self.checkElements(parse_line, ["}"])):

                current_node = self.dictionary_list.pop()

                if (len(self.dictionary_list) > 1):
                    parent_node = self.dictionary_list[-1]
                    self.gradle_dict[parent_node][current_node].append(self.gradle_dict[current_node])
                    del self.gradle_dict[current_node]

        if("ext" in self.gradle_dict.keys()):
            self.parse_versions()

        return self.gradle_dict

    def parse_versions(self):
        """
        extract versions from the ext block if exists
        @return:
        """
        #first the normal libraries
        base_annotation = "$rootProject.ext."
        ext_list = self.gradle_dict["ext"]
        library_node = self.gradle_dict["dependencies"]["compile"]
        library_extract = [ x for x in self.gradle_dict["dependencies"]["compile"] if len(x) == 1]
        for lib in library_extract:
            version_placeholder = ''
            if base_annotation in lib[0]:
                temp_lib = lib[0][:lib[0].index("$")]
                version_placeholder = lib[0][lib[0].index("$"):]
                required = version_placeholder.strip(base_annotation)
                required_version = ext_list[required][0][0]
                #TODO add check for versions
                library_node.remove(lib)
                library_node.append([temp_lib+required_version])

    def checkElements(self, elements, target_list):
        """
        Checks whether any element in target_list exists in elements
        @param element:
        @param target_list:
        @return:
        """
        elements_check = []
        if type(elements[0]) == tuple:
            elements_check = [val2 for (val1, val2) in elements]
        else:
            elements_check = elements
        for target in target_list:
            if target in elements_check:
                return True
        return False

    def getElements(self, elements):
        """
        returns list of real elements without token tags
        @param elements:
        @return:
        """
        if type(elements[0]) == tuple:
            return [val2 for (val1, val2) in elements]
        else:
            return elements

    def purifyElements(self, elements, filter_list):
        """
        removes unwanted elements from the list if they exist
        @param elements:
        @param filter_list:
        @return:
        """
        el_lst = self.getElements(elements)
        for el in filter_list:
            if el in el_lst:
                el_lst.remove(el)
        return el_lst
