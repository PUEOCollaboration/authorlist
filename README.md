# PUEO Author List

This is a centralized store for PUEO author lists. 

There are two files used as input, authors.in and institutions.in

Running make will then generate the other files (using a python script). 

institutions.txt defines a mapping of institution id's to addresses in a |-separated manner, e.g., including an optional short name (used for PoS) 

`UC | Dept. of Physics, Enrico Fermi Inst., Kavli Inst. for Cosmological Physics, Univ. of Chicago, Chicago, IL 60637. | University of Chicago` 


The format of authors.txt is 


`NAME  | INSTITUTION_ID1 | [ INSTIUTION_ID2 | etc.. ] [ < orcidid ]  `

e.g. 

`C. Deaconu | UC < 0000-0002-4953-6397`


Output is generated in several formats: 

  - `pueo_revtex_authors.tex` and `pueo_revtex_institutes.txt` for use with revtex journals
  - `pueo_aas_authors.tex` and `pueo_aas_institutes.txt` for use with AAS journals
  - `pueo_elsarticle_authors.tex`  for use with elsevier journals
  - `pueo_pos_authors.tex` for use with PoS (a sort of raw format)
  - `pueo_icrc_authors.tex` for use with the 2019 ICRC authorlist format. 
  - `pueo_sissa_authors.tex` for use with sissa journals (JCAP/JINST/etc.) 
  - `pueo_authors.html` for web display, this is used to generate an index.html that we can use for gh-pages (you should commit this if it changed!) 
  - `pueo_authors.txt` for text
  - `pueoauthors.csv` for a general use csv file (used to generate an xml file using ICRC's submission tool). Entries are colon-separated and of the form `First: Last: Affiliation`
  - `pueo_inspire.xml` inspire xml format for arxiv/inspirehep

TODO:
  - ORCID support in more formats (right not just used for inspire.xml) 












