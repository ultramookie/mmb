#!/usr/bin/env python

import json
import markdown
import optparse
import glob
import os
import re
import jinja2
import shutil
import feedgenerator

# Get me my config values!
def read_config(input_dir):
  config_location = input_dir + '/config.json'
  if os.path.isfile(config_location):
    with open(config_location) as config_file:    
      config = json.load(config_file)
    return config
  else:
    print 'config file %s is missing' % config_location

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

# Create metadata from the markdown filename
def get_meta_data(base_filename):
  path,filename = os.path.split(base_filename)
  filename_split = re.split('-', filename)
  return filename_split

# Make the date
def get_date(metadata):
  date = '-'.join(metadata[0:3])
  return date

# Make the year
def get_year(metadata):
  year = int(metadata[0])
  return year

# Make the title
def get_title(metadata):
  title = ' '.join(metadata[3:])
  return title

# Given the jinja for header or footer, render it to html
def render_jinja(incoming_template,metadata,config):
  date = get_date(metadata)
  title = get_title(metadata).title()
  blog_name = config['blog_name']
  meta_keywords = config['meta_keywords']
  meta_description = config['meta_description']
  language = config['language']
  author = config['author']
  base_url = config['base_url']
  url_location = config['url_location']
  template = jinja2.Template(incoming_template)
  rendered_jinja = template.render(
    title=title,
    date=date,
    blog_name=blog_name,
    meta_keywords=meta_keywords,
    meta_description=meta_description,
    language=language,
    base_url=base_url,
    url_location=url_location,
    author=author
  )
  return rendered_jinja

# Copy the style sheet into place
def copy_style(config):
  css_file = config['css_file'] 
  path,filename = os.path.split(css_file)
  dest_file = config['output'] + '/' + filename
  shutil.copyfile(css_file,dest_file)

# Copy the latest html file to be index file
def copy_index_into_place(config):
  index_file = config['output'] + '/index.html'
  html_files = sorted(glob.glob(config['output'] + '/*.html'), reverse=True)
  for html_file in html_files:
    path,filename = os.path.split(html_file)
    filename_pattern = re.compile(r'^(\d{4})-(\d{2})-(\d{2})(-\w*)*\.html$')
    if (filename_pattern.match(filename)):
      shutil.copyfile(html_file,index_file)
      break

# Do the doing
def process_entries(input_dir,config):
  header_template = open(config['header_file']).read()
  footer_template = open(config['footer_file']).read()
  entry_files = glob.glob(input_dir + '/*.md')
  for entry_file in entry_files:
    base_filename = os.path.splitext(entry_file)[0]
    metadata = get_meta_data(base_filename)
    if not os.path.isfile(base_filename + '.done'):
      path,filename = os.path.split(base_filename)
      filename_pattern = re.compile(r'^(\d{4})-(\d{2})-(\d{2})(-\w*)*$')
      if (filename_pattern.match(filename)):
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
          print '%s has been processed.' % entry_file

# Let people find their way around
def create_archive_page(input_dir,config):
  index_filename = config['output'] + '/archive.html'
  author = config['author']
  metadata = ['','','',author]
  prev_year = -1
  output_dir = config['output']
  header_template = open(config['header_file']).read()
  footer_template = open(config['footer_file']).read()
  header_html = render_jinja(header_template,metadata,config)
  footer_html = render_jinja(footer_template,metadata,config)
  entry_files = sorted(glob.glob(input_dir + '/*.done'), reverse=True)
  index_filecontents = '%s<h1>Archive</h1>' % header_html 
  for entry_file in entry_files:
    base_filename = os.path.splitext(entry_file)[0]
    metadata = get_meta_data(base_filename)
    path,filename = os.path.split(base_filename)
    html_filename = filename + '.html'
    date = get_date(metadata)
    title = get_title(metadata).title()
    cur_year = get_year(metadata)
    if cur_year != prev_year:
      index_filecontents = '%s <h1>%s</h1>' % (index_filecontents,cur_year)
      prev_year = cur_year
    index_filecontents = '%s <a href="%s">%s</a> (%s) <br />' % (index_filecontents,html_filename,title,date)
  index_filecontents = index_filecontents + footer_html
  index_file = open(index_filename,'w')
  index_file.write(index_filecontents)
  index_file.close()

# Generator those fancy rss feeds
def create_rss_feed(input_dir,config):
  counter = 0
  rss_filename = config['output'] + '/feed.rss'
  blog_name = config['blog_name']
  author = config['author']
  language = config['language']
  url = config['base_url'] + config['url_location']
  meta_description = config['meta_description']
  feed_entries = int(config['feed_entries'])
  feed = feedgenerator.Rss201rev2Feed(
    title=blog_name,
    link=url,
    description=meta_description,
    language=language,
    feed_guid=url,
    feed_url='%sfeed.rss' % url
  )
  entry_files = sorted(glob.glob(input_dir + '/*.done'), reverse=True)
  for entry_file in entry_files:
    counter = counter + 1
    if counter > feed_entries:
      break
    else:
      base_filename = os.path.splitext(entry_file)[0]
      metadata = get_meta_data(base_filename)
      path,filename = os.path.split(base_filename)
      html_filename = filename + '.html'
      date = get_date(metadata)
      title = get_title(metadata).title()
      feed.add_item(
        title=title,
        link='%s%s' % (url,html_filename),
        description=title,
        author_name=author,
        unique_id='%s%s' % (url,html_filename),
        unique_id_is_permalink="true"
      )

  with open(rss_filename, 'w') as rss_file:
    feed.write(rss_file, 'utf-8')

# Go Speed Go
def run():
  input_dir = get_input_dir()
  config = read_config(input_dir)
  copy_style(config)
  process_entries(input_dir,config)
  create_archive_page(input_dir,config)
  copy_index_into_place(config)
  create_rss_feed(input_dir,config)

# Make it so!
run()
