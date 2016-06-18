#!/usr/bin/env python

import json
import markdown
import pprint

def read_config():
  with open('config.json') as config_file:    
    config = json.load(config_file)
  return config

def read_body():
  mdfile = open('test.md').read()
  html = markdown.markdown(mdfile)
  return html

def run():
  config = read_config()
  pprint.pprint(config)
  for k in config:
    print "%s: %s" % (k,config[k])
  body = read_body()
  print(body)

run()


