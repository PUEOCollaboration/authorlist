#!/usr/bin/env python 

## PUEO Author Tool to save time on author lists... 
#  Cosmin Deaconu <cozzyd@kicp.uchicago.edu> 
#  apologies for the semicolons, it's a reflex at this point... 
#  This is about as brute force as it gets :)

import sys
from datetime import date

prefix = "pueo"  #prefix for all output files  (first argument overrideS) 
collaboration = "PUEO"  # (second argument overrides) 


if len(sys.argv) > 1: 
  prefix = sys.argv[1] 

if len(sys.argv) > 2: 
  collaboration = sys.argv[2] 


## may need to do more here! 
def tex_escape(string): 
  escapes = ( ("&","\&"), ("ı́","\\'i") )
  escaped = string
  for escape in escapes:
      escaped = escaped.replace(escape[0],escape[1])

  return escaped

def html_escape(string):
    escapes = ( ("&","&amp;"), ("\~n", "&ntilde;") )

    escaped = string; 
    for escape in escapes: 
        escaped = escaped.replace(escape[0],escape[1])
    return escaped

def xml_escape(string):
    escapes = (('\~n','ñ'),)
    escaped = string; 
    for escape in escapes: 
        escaped = escaped.replace(escape[0],escape[1])
    return escaped



# Start by opening the institutes.in 
finst = open("institutes.in") 

institutes = {} 
for line in finst.readlines(): 


  line = line.strip()
  if len(line) == 0:
    continue
  if line[0] == "#": 
    continue

  tokens = line.split("|"); 
  if len(tokens) < 2:
    continue 

  inst_id = tokens[0].strip() 
  inst_addr = tokens[1].strip() 
  inst_short = inst_addr if len(tokens) < 3 else tokens[2].strip() 

  if inst_id in institutes: 
    print( "WARNING: duplicate ID \"%s\" found! Replacing existing." % (inst_id))

  institutes[inst_id] = (inst_addr, inst_short) 



# Then open the authors list 

fauth = open("authors.in")

lineno = 0

orcids = [] 
authors = [] 
sorted_institutes = [] 
sorted_short_institutes = [] 
institute_numbers = {}
short_institute_numbers = {}

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"; 
institute_letters = {}
short_institute_letters = {}



for line in fauth.readlines(): 
  line = line.strip()
  lineno+=1 
  if len(line) == 0:
    continue
  if line[0] == "#": 
    continue

  orcid = None
  orcid_split = line.split('<') 
  if len(orcid_split) > 1:
      orcid = orcid_split[1].strip() 
  line = orcid_split[0] 
  tokens = line.split("|"); 
  if len(tokens) == 1: 
    print(" WARNING: No affiliation on line %d" % (lineno))

  author = tokens[0].strip()
  affiliations = []
  short_affiliations = []

  for t in tokens[1:]: 
    aff = t.strip() 
    if aff not in institutes: 
      print(" WARNING, no key for %s found in institutes.in" % (aff))
    else: 
      if aff not in sorted_institutes: 
        sorted_institutes.append(aff) 
        institute_numbers[aff] = len(sorted_institutes) 
        institute_letters[aff] = letters[len(sorted_institutes)-1]
      affiliations.append(aff) 

      if institutes[aff][1] != "":
          if aff not in sorted_short_institutes: 
              sorted_short_institutes.append(aff)
              short_institute_numbers[aff] = len(sorted_short_institutes)
              short_institute_letters[aff] = letters[len(sorted_short_institutes)-1]
          short_affiliations.append(aff)



  authors.append((author,affiliations,short_affiliations, orcid)) 



# authors.txt 

f_authors_txt = open(prefix +"authors.txt","w") 

first = True
for author in authors: 

  if not first: 
    f_authors_txt.write(", "); 
  f_authors_txt.write(author[0] + " "); 

  for aff in author[1]:
    f_authors_txt.write("[%d]" % (institute_numbers[aff]) ); 

  first = False

f_authors_txt.write("\n\n"); 
for i in range(len(sorted_institutes)): 
  f_authors_txt.write("%d: %s\n"%( i+1, institutes[sorted_institutes[i]][0])) 


f_authors_txt.close()

# authors.csv 

f_authors_csv = open(prefix +"authors.csv","w") 
f_authors_csv.write("First: Last: Affiliation \n")

for author in authors: 

  f_authors_csv.write(" ".join(author[0].split()[0:-1]) + ": " + author[0].split()[-1] + ": " + institutes[author[1][0]][0] + "\n"); 


f_authors_txt.close()


# authors.html 

f_authors_html = open(prefix +"authors.html","w") 

f_authors_html.write("<p align='center'>") 
first = True
for author in authors: 

  if not first: 
    f_authors_html.write(", \n"); 
  if author[3] is not None: 
      f_authors_html.write('<a href="https://orcid.org/' + author[3] +'">' + html_escape(author[0])+ '</a>'); 
  else: 
      f_authors_html.write(html_escape(author[0])); 

  f_authors_html.write("<sup>"); 
  first_aff = True
  for aff in author[1]:
    if not first_aff:
      f_authors_html.write(","); 
    f_authors_html.write("<a href='#%s'>%d</a>" % (aff, institute_numbers[aff]) ); 

    first_aff = False 
  f_authors_html.write("</sup>"); 

  first = False

f_authors_html.write("<br>(<b>%s Collaboration</b>)\n" % (collaboration)); 
f_authors_html.write("</p>\n\n"); 
for i in range(len(sorted_institutes)): 
  f_authors_html.write("<br> <a name='%s'\\> <sup>%d</sup> %s\n"%(sorted_institutes[i],  i+1, html_escape(institutes[sorted_institutes[i]][0]))) 


f_authors_html.close()


# revtex_authors.tex 
f_revtex_authors = open(prefix + "revtex_authors.tex","w")
f_revtex_authors.write("%% Collaboration author file for %s in revtex format\n" % (collaboration)) 
f_revtex_authors.write("%% \\input this file in main body (make sure you also do the institutes file in the preamble!) \n\n" ) 

for author in authors: 
  name = author[0].replace(" ","~")
  f_revtex_authors.write(" \\author{%s}" % (name)) 
  if author[1] is not None: 
    for aff in author[1]: 
      f_revtex_authors.write("\\at%s" % (aff)) 
  f_revtex_authors.write("\n") 

f_revtex_authors.write("\\collaboration{%s Collaboration}\\noaffiliation\n" % (collaboration)); 

f_revtex_authors.close()


# revtex_institutes.tex 
f_revtex_institutes = open(prefix + "revtex_institutes.tex","w")
f_revtex_institutes.write("%% Collaboration institute file for %s in revtex format\n" % (collaboration)) 
f_revtex_institutes.write("%% \\input this file in the preamble (make sure you also do the author file in the body!) \n\n") 

for key in sorted_institutes: 
  addr = tex_escape(institutes[key][0]) ; 
  f_revtex_institutes.write("\\newcommand{\\at%s}{\\affiliation{%s}}\n" % (key, addr)); 

f_revtex_institutes.close()

# aas_authors.tex 
f_aas_authors = open(prefix + "aas_authors.tex","w")
f_aas_authors.write("%% Collaboration author file for %s in aas format\n" % (collaboration)) 
f_aas_authors.write("%% \\input this file in main body (make sure you also do the institutes file in the preamble!) \n\n" ) 

for author in authors: 
  name = author[0].replace(" ","~")
  f_aas_authors.write("\\author{%s}" % (name)) 
  if author[1] is not None: 
    for aff in author[1]: 
      f_aas_authors.write("\n\\at%s" % (aff)) 
  f_aas_authors.write("\n") 

f_aas_authors.write("\\collaboration{1000}{%s Collaboration}\n" % (collaboration)); 
f_aas_authors.close()


# aas_institutes.tex 
f_aas_institutes = open(prefix + "aas_institutes.tex","w")
f_aas_institutes.write("%% Collaboration institute file for %s in aas format\n" % (collaboration)) 
f_aas_institutes.write("%% \\input this file in the preamble (make sure you also do the author file in the body!) \n\n") 

for key in sorted_institutes: 
  addr = tex_escape(institutes[key][0]) ; 
  f_aas_institutes.write("\\newcommand{\\at%s}{\\affiliation{%s}}\n" % (key, addr)); 

f_aas_institutes.close()



#elsarticle_authors.tex 

f_elsarticle_authors = open(prefix + "elsarticle_authors.tex","w"); 

f_elsarticle_authors.write("%% authorlist for elsarticle publications for %s collaboration\n\n" % (collaboration) ); 

f_elsarticle_authors.write("\\collaboration{%s Collaboration}\n\n" % (collaboration)); 

for key in sorted_institutes: 
  num = institute_numbers[key]; 
  addr = tex_escape(institutes[key][0]) ; 
  f_elsarticle_authors.write("\\address[%d]{%s}\n" % (num, addr)); 

f_elsarticle_authors.write("\n\n"); 

for author in authors: 
  name = author[0].replace(" ","~")
  affs = "" 
  for aff in author[1]: 
    if affs != "": 
      affs += ","
    affs += str(institute_numbers[aff])
  f_elsarticle_authors.write("\\author[%s]{%s}\n" % (affs,name)) 

f_elsarticle_authors.close()

#sissa_authors.tex 

f_sissa_authors = open(prefix + "sissa_authors.tex","w"); 

f_sissa_authors.write("%% authorlist for elsarticle publications for %s collaboration\n\n" % (collaboration) ); 


for author in authors: 
  name = author[0].replace(" ","~")
  affs = "" 
  for aff in author[1]: 
    if affs != "": 
      affs += ","
    affs += str(institute_letters[aff])
  f_sissa_authors.write("\\author[%s]{%s}\n" % (affs,name)) 


f_sissa_authors.write("\n\n"); 

for key in sorted_institutes: 
  letter = institute_letters[key]; 
  addr = tex_escape(institutes[key][0]) ; 
  f_sissa_authors.write("\\affiliation[%s]{%s}\n" % (letter, addr)); 

f_sissa_authors.write("\n\n"); 
f_sissa_authors.write("\\collaboration{%s Collaboration}\n\n" % (collaboration)); 

f_sissa_authors.close()

# inspire XML 

f_xml = open(prefix + "inspire.xml","w"); 


f_xml.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE collaborationauthorlist SYSTEM "http://inspirehep.net/info/HepNames/tools/authors_xml/author.dtd">
<collaborationauthorlist
   xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:cal="http://inspirehep.net/info/HepNames/tools/authors_xml/">
   <cal:creationDate>{thedate}</cal:creationDate>
   <!-- maybe replace with journal below?-->
   <cal:publicationReference>https://pueo.space/authorlist</cal:publicationReference>
   <cal:collaborations>
      <cal:collaboration id="c1">
         <foaf:name>{collab} Collaboration</foaf:name>
      </cal:collaboration>
   </cal:collaborations>
   <cal:organizations>
'''.format(thedate=date.today(), collab=collaboration))

xml_index = 1
xml_index_map = {} 
for institute in institutes.keys():

    # note, we could improve the format of institutes.in to fill this in better.. 
    f_xml.write("""
       <foaf:Organization id="a{index}">
         <foaf:name>{name}</foaf:name>
      </foaf:Organization>
    """.format(index=xml_index, name=institutes[institute][0]))
    xml_index_map[institute] = xml_index 
    xml_index+=1 

f_xml.write('''
  </cal:organizations>
  <cal:authors>
''')

# we should start gathering orcids? 
for author in authors: 

    name=xml_escape(author[0])
    f_xml.write('''
    <foaf:Person>
      <foaf:name>{name}</foaf:name>
      <foaf:familyName>{familyname}</foaf:familyName>
      <cal:authorNamePaper>{name}</cal:authorNamePaper>
      <cal:authorCollaboration collaborationid="c1"/>'''.format(name=name, familyname=name.rsplit('.',1)[1].strip()))


    f_xml.write('''
      <cal:authorAffiliations>''')
    
    for aff in author[1]: 
        f_xml.write('\n        <cal:authorAffiliation organizationid="a{index}"/>'.format(index=xml_index_map[aff]))
    f_xml.write('''
      </cal:authorAffiliations>''')
    if author[3] is not None:
        f_xml.write('''       
      <cal:authorids>
        <cal:authorid source="ORCID">{orcid}</cal:authorid> 
      </cal:authorids>'''.format(orcid=author[3]))
    f_xml.write('''
    </foaf:Person>
    ''')



f_xml.write('''
  </cal:authors>
</collaborationauthorlist>
''')







# pos_authors.tex 

f_pos_authors = open(prefix +"pos_authors.tex","w") 
f_pos_authors.write("%% PoS list for %s Collaboration\n\n" % (collaboration));  
first = True

f_pos_authors.write("\\author{\n"); 

f_pos_authors.write("  (%s Collaboration)\n" % (collaboration)); 

for author in authors: 
  name = author[0].replace(" ","~")
  if not first: 
    f_pos_authors.write(",\n"); 
  f_pos_authors.write("  %s" % (name)); 
  affs = "" 
  for aff in author[1]: 
    if affs != "": 
      affs += ","
    affs += str(institute_numbers[aff])
 
  f_pos_authors.write("$^{%s}$"%(affs))
  first = False

f_pos_authors.write("\n\n\\\\\n"); 
first = True
for i in range(len(sorted_institutes)): 
  if not first: 
    f_pos_authors.write(",\n") 
  f_pos_authors.write(" $^{%d}$%s"%( i+1, tex_escape(institutes[sorted_institutes[i]][1]))) 
  first = False 

f_pos_authors.write("\n}\n"); 
f_pos_authors.close()


## ICRC authors
f_icrc_authors = open(prefix + "icrc_authors.tex","w"); 
f_icrc_authors.write("%% ICRC list for %s Collaboration\n\n" % (collaboration));  


first = True
num_institutes = 0 
f_icrc_authors.write("\\noindent\n")
for author in authors: 

  name = author[0].replace(" ","~")

  if not first: 
    f_icrc_authors.write(", \n"); 
  f_icrc_authors.write(name); 

  first_aff = True
  for aff in author[2]:
    if not first_aff:
      f_icrc_authors.write("\\textsuperscript{,}"); 
    f_icrc_authors.write("\\textsuperscript{%d}" % (short_institute_numbers[aff]) ); 
    first_aff = False
  first = False
f_icrc_authors.write("\n\\\\\n\\noindent\n"); 
first = True
for i in range(len(sorted_short_institutes)): 
  if not first: 
    f_icrc_authors.write(",\n") 
  f_icrc_authors.write("$^{%d}$%s"%( i+1, tex_escape(institutes[sorted_short_institutes[i]][1]))) 
  first = False 


f_icrc_authors.close()






























