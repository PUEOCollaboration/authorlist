
.PHONY: all 

tgts=output/pueo_authors.html output/pueo_authors.txt output/pueo_authors_revtex.tex output/pueo_institutes_revtex.tex output/pueo_elsarticle_authors.tex output/pueo_icrc_authors.tex output/pueo_pos_authors.tex

all: index.html pueo_authors.xml

clean: 
	@rm -rf output 
	@rm -f index.html 

$(tgts): authors.in institutes.in pueo_author_tool.py Makefile | output 
	@echo Running pueo_author_tool.py
	@./pueo_author_tool.py output/pueo_ 

output: 
	@mkdir -p $@

index.html: output/pueo_authors.html 
	@echo "<!DOCTYPE html><html><head><title>PUEO Author List</title></head> <body><h1 align='center'>PUEO Author List</h1><hr/>" > $@
	@cat $^ >> $@ 
	@echo "<hr/><p><a href='pueo_authors.xml'>Download as INSPIRE XML</a>" >> $@
	@echo "</body></html>" >> $@
	@echo "Please considering committing/pushing your index.html if it differs from https://pueocollaboration.github.io/authorlist" 
	
pueo_authors.xml: output/pueo_inspire.xml 
	@cp $^ $@ 
	@echo "Please considering committing/pushing your pueo_authors.xml if it differs from https://pueocollaboration.github.io/authorlist/pueo_authors.xml" 
