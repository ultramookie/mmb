#!/usr/bin/env python

import json
import markdown
import optparse
import glob
import os
import re
import pprint

# Get me my config values!
def read_config(input_dir):
  config_location = input_dir + '/config.json'
  with open(config_location) as config_file:    
    config = json.load(config_file)
  return config

# What am I trying to translate?
def read_body(entry_file):
  mdfile = open(entry_file).read()
  html = markdown.markdown(mdfile)
  return html

# Where is the stuff?
def get_input_dir():
  parser = optparse.OptionParser()
  parser.add_option('-i', action="store", help="Where are your input files located?", dest="input_dir", default="./")
  (options, args) = parser.parse_args()
  return options.input_dir

def get_meta_data(base_filename):
  path,filename = os.path.split(base_filename)
  filename_split = re.split('-', filename)
  return filename_split

def create_header():
  
# Do the doing
def process_entries(input_dir,config):
  footer = open(config['footer_file']).read()
  entry_files = sorted(glob.glob(input_dir + '/*.md'))
  for entry_file in entry_files:
    base_filename = os.path.splitext(entry_file)[0]
    metadata = get_meta_data(base_filename)
    if not os.path.isfile(base_filename + '.done'):
      body_html = read_body(entry_file)
      html_doc = body_html + footer
      print html_doc

# Go Speed Go
def run():
  input_dir = get_input_dir()
  config = read_config(input_dir)
  pprint.pprint(config)
  for k in config:
    print "%s: %s" % (k,config[k])
  process_entries(input_dir,config)

run()
