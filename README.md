mmb
===
mookie's mini blog
------------------

my weekend project to write a script to generate a blog using only python.

i did not want to run mysql or php or whatever; all i want are static html files that can be served from a cheap service and cached easily by a caching service. i just want to write then have something render that into html files.

getting started
---------------

create an input directory and move the config.json file there. this is the directory that you'll also put all your blog entry markdown files in.

create a template directory where header.jinja, footer.jinja and style.css will live.

edit the config.json file to your liking. remember to change the directories for the output and templates.

some of the metadata for blog entries is embedded in the markdown's filename (date in the format YYYY-MM-DD and title). be sure to name the blog entry files in this format (complete with the file extension .md):

YYYY-MM-DD-title.md

example:

2016-06-21-happy-birthday-to-mookie.md

in order to render html files, the index file and the rss feed file from new markdown files, run this command:

mmb.py -i INPUT_DIR

where INPUT_DIR is the one that was created above.

header and footer templates
---------------------------

these variables based on the filename metadata and the config file are passed into the header and footer templates:

* title
* date
* blog_name
* meta_keywords
* meta_description
* language
* base_url
* url_location
* author

