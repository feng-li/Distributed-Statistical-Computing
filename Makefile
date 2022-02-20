all: slides

slides:
	jupyter-nbconvert **/L*.ipynb  --to slides  --SlidesExporter.reveal_theme=solarized --SlidesExporter.reveal_scroll=True --SlidesExporter.reveal_transition=fade

html:
	jupyter-nbconvert **/**.ipynb  --to html

zip:
	git archive --output=distcomp-slides.zip HEAD

sync:
	git checkout-index -a -f --prefix=$HOME/nextcloud/feng.li/distcomp/
	rsync -av distcomp-slides.zip $HOME/nextcloud/feng.li/distcomp/
