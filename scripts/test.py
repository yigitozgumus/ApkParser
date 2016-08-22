# import gradleParser as gr
#
# test = gr.GradleParser(".")
# test2 = test.parse()
#
# import json
# print json.dumps(test2,sort_keys=True,indent=2)

# import tokenize
#
# file = open("build.gradle")
#
# tokens = list()
# def handle_token(type, token, (srow, scol), (erow, ecol), line):
#     # print "%d,%d-%d,%d:\t%s\t%s" % \
#     #     (srow, scol, erow, ecol, tokenize.tok_name[type], repr(token))
#     tokens.append((tokenize.tok_name[type],repr(token).encode("utf-8")))
#
#
# tokenize.tokenize(
#     file.readline,
#     handle_token
#     )
#
# for el in tokens:
#     print el

import gradleParser_v2 as gr

test = gr.GradleParserNew(".")

test2 = test.parse(True)

print test2

