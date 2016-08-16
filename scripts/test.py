#!/usr/bin/env python

import gradleParser as gr

test = gr.GradleParser(".")

test2 = test.parse()

import json
print json.dumps(test2,sort_keys=True,indent=2)