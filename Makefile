all: slides

slides:
	jupyter-nbconvert **/L*.ipynb  --to slides

html:
	jupyter-nbconvert **/**.ipynb  --to html

sync:
	rsync -av --del --exclude=".git/" . ~/nextcloud/feng.li/distcomp/
