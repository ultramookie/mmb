# mmb
mookie's mini blog

make a blog using python only. fun.

i did not want to run mysql or php or whatever. i just wanted to write then render html files.

create an input directory where the config.json, header.jinja, footer.jinja and style.css will live.

this is the directory that you'll put all your blog entry files in also.

edit the config.json file to your liking.

naming format of blog entry files:

YYYY-MM-DD-title.md

example:

2016-06-21-happy-birthday-to-mookie.md

run this to render:

mmb.py -i INPUT_DIR
