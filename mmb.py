#!/usr/bin/env python

import json
import markdown
import optparse
import glob
import pprint

# Get me my config values!
def read_config(input_dir):
  config_location = input_dir + '/config.json'
  with open(config_location) as config_file:    
    config = json.load(config_file)
  return config

# What am I trying to translate?
def read_body():
  mdfile = open('test.md').read()
  html = markdown.markdown(mdfile)
  return html

# Where is the stuff?
def get_input_dir():
  parser = optparse.OptionParser()
  parser.add_option('-i', action="store", help="Where are your input files located?", dest="input_dir", default="./")
  (options, args) = parser.parse_args()
  return options.input_dir

# Do the doing
def process_entries(input_dir,config):
  entry_files = glob.glob(input_dir + '/*.md')
  done_files = glob.glob(input_dir + '/*.done')
  pprint.pprint(entry_files)
  pprint.pprint(done_files)

# Go Speed Go
def run():
  input_dir = get_input_dir()
  config = read_config(input_dir)
  pprint.pprint(config)
  for k in config:
    print "%s: %s" % (k,config[k])
  process_entries(input_dir,config)

run()
