#!/usr/bin/env python

import json
import markdown
import optparse
import glob
import os
import re
import jinja2
import shutil
import time

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

def get_date(metadata):
  date = '-'.join(metadata[0:3])
  return date

def get_title(metadata):
  title = ' '.join(metadata[3:])
  return title

def render_jinja(incoming_template,metadata,config):
  date = get_date(metadata)
  title = get_title(metadata).title()
  blog_name = config['blog_name']
  meta_keywords = config['meta_keywords']
  base_url = config['base_url']
  url_location = config['url_location']
  template = jinja2.Template(incoming_template)
  rendered_jinja = template.render(title=title,date=date,blog_name=blog_name,meta_keywords=meta_keywords,base_url=base_url,url_location=url_location)
  return rendered_jinja

def copy_style(config):
  css_file = config['css_file'] 
  path,filename = os.path.split(css_file)
  dest_file = config['output'] + '/' + filename
  shutil.copyfile(css_file,dest_file)

# Do the doing
def process_entries(input_dir,config):
  header_template = open(config['header_file']).read()
  footer_template = open(config['footer_file']).read()
  entry_files = sorted(glob.glob(input_dir + '/*.md'))
  for entry_file in entry_files:
    base_filename = os.path.splitext(entry_file)[0]
    metadata = get_meta_data(base_filename)
    if not os.path.isfile(base_filename + '.done'):
      path,filename = os.path.split(base_filename)
      html_filename = config['output'] + '/' + filename + '.html'
      done_filename = base_filename + '.done'
      header_html = render_jinja(header_template,metadata,config)
      footer_html = render_jinja(footer_template,metadata,config)
      body_html = read_body(entry_file)
      html_doc = header_html + body_html + footer_html
      blog_file = open(html_filename,'w')
      blog_file.write(html_doc)
      blog_file.close()
      if os.path.isfile(html_filename):
        open(done_filename,'a').close()

# Let people find their way around
def create_index_page(input_dir,config):
  index_filename = config['output'] + '/index.html'
  blog_name = config['blog_name']
  year = time.strftime("%Y")
  month = time.strftime("%m")
  day = time.strftime("%d")
  metadata = [year,month,day,blog_name]
  output_dir = config['output']
  header_template = open(config['header_file']).read()
  footer_template = open(config['footer_file']).read()
  header_html = render_jinja(header_template,metadata,config)
  footer_html = render_jinja(footer_template,metadata,config)
  entry_files = sorted(glob.glob(input_dir + '/*.done'))
  index_filecontents = header_html
  for entry_file in entry_files:
    base_filename = os.path.splitext(entry_file)[0]
    metadata = get_meta_data(base_filename)
    path,filename = os.path.split(base_filename)
    html_filename = filename + '.html'
    date = get_date(metadata)
    title = get_title(metadata).title()
    index_filecontents = '%s <a href="%s">%s</a> (%s) <br />' % (index_filecontents,html_filename,title,date)
  index_filecontents = index_filecontents + footer_html
  index_file = open(index_filename,'w')
  index_file.write(index_filecontents)
  index_file.close()

# Go Speed Go
def run():
  input_dir = get_input_dir()
  config = read_config(input_dir)
  copy_style(config)
  process_entries(input_dir,config)
  create_index_page(input_dir,config)

run()
