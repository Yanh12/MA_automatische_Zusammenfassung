import spacy, pickle, re
from spacy.symbols import dobj,pobj,punct,NOUN,pcomp
nlp = spacy.load('en',disable = ['ner'])

with open ('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/titles.p','rb' ) as filehandle:
    titles = pickle.load(filehandle)
with open('/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_sentsV2.p', 'rb') as filehandle:
    abstracts = pickle.load(filehandle)


def relation_extration_from_title (titles):
   """
   this function is used to extract the main concerned domain in the article and (possible) also the technique used
   with the dependency grammar and semantic relation analysis
   """
   domains = []
   techs = []
   tech_triggers = ['via','with','across','through','base','use','using','by','from','employing','employ']
   stops = ['study','research','approach','method','dataset','semeval','application','investigation','web',
            'paper','article','science','microblog']
   domain_triggers = ['for', 'of', 'to','on']
   for i in range (len(titles)):
       titles[i] = titles[i].lower()
       domain = []
       tech = []
       doc = nlp(titles[i])
       tech_str = ""
       """
       based on the types of formulizing a title, some titles explicity indicated zhe topic domain with the with of
       trigging prepositions like 'for' or 'of', then we need to extract the prep-object (the whole noun chunk) of the
       preposition. If there was no such prepositions, the assumption is that the topic domain is the first noun chunk
       after deleting some useless patterns.
       """
       if not titles[i]:
           domain.append("")
           tech.append("")

       elif any (token.lemma_ == t for t in domain_triggers for token in doc):
           for chunk in doc.noun_chunks:
               if any (t in str(chunk.text) for t in stops):
                   continue

               #elif len(str(chunk.text.strip('the')).split()) <= 1:
                   #continue

               elif any (t == chunk.root.head.lemma_ for t in tech_triggers):
                   tech_str = str(chunk.text)
                   tech_str = re.sub(r'\b(the|a|an)\b', '', tech_str)
                   tech_str = tech_str.strip()
                   tech.append(tech_str)

               #deal with "based on" type
               elif chunk.root.head.lemma_ == 'on' and doc[chunk.root.head.i-1].lemma_ == "base":
                   tech_str = str(chunk.text)
                   tech.append(tech_str)

               elif any (chunk.root.head.lemma_ == t for t in domain_triggers) and chunk.root.dep == pobj:
                   d_str = str(chunk.text)
                   d_str = re.sub(r'\b(the|a|an)\b', '', d_str)
                   d_str = d_str.strip()
                   domain.append(d_str)

           #part-of-speech tagging or parsing or named entity recognition not correctly marked:
           for token in doc:
               if token.text == "tagging" and "part-of-speech tagging" in titles[i]:
                   text = doc[token.i-5 : token.i+1]
                   if not any (t in doc[token.i-6].lemma_ for t in tech_triggers):
                       domain.append(str(text))
                   else:
                       tech.append(str(text))
               elif token.text == "tagging" and "part of speech tagging" in titles[i]:
                   text = doc[token.i - 3 : token.i+1]
                   if not any(t in doc[token.i - 6].lemma_ for t in tech_triggers):
                       domain.append(str(text))
                   else:
                       tech.append(str(text))
               elif token.text == "induction" and "part of speech induction" in titles[i]:
                   text = doc[token.i - 3 : token.i+1]
                   if not any(t in doc[token.i - 6].lemma_ for t in tech_triggers):
                       domain.append(str(text))
                   else:
                       tech.append(str(text))
               elif token.text == "parsing" and "dependency parsing" in titles[i]:
                   text = doc[token.i-1 : token.i+1]
                   if not any(t in doc[token.i-2].lemma_ for t in tech_triggers):
                       domain.append(str(text))
                   else:
                       tech.append(str(text))
               elif token.text == "named" and "named entity recognition" or "named entity recognizer" in titles[i]:
                   text = doc[token.i: token.i+3]
                   if not any(t in doc[token.i-1].lemma_ for t in tech_triggers):
                       domain.append(str(text))
                   else:
                       tech.append(str(text))
               elif token.text == "parsing" or token.text == "bootstrapping" or token.text == 'chunking':
                   n = doc[token.i].n_lefts
                   text = doc[token.i-n : token.i+1]
                   if not any(t in doc[token.i-n-1].lemma_ for t in tech_triggers):
                       domain.append(str(text))
                   else:
                       tech.append(str(text))

       else:
           for chunk in doc.noun_chunks:
               if any(t in str(chunk.text) for t in stops):
                   continue

               elif len(str(chunk.text.strip('the')).split()) <= 1:
                   continue

               elif any(t == chunk.root.head.lemma_ for t in tech_triggers):
                   tech_str = str(chunk.text)
                   tech_str = re.sub(r'\b(the|a|an)\b', '', tech_str)
                   tech_str = tech_str.strip()
                   tech.append(tech_str)

               # deal with "based on" type
               elif chunk.root.head.lemma_ == 'on' and doc[chunk.root.head.i - 1].lemma_ == "base":
                   tech_str = str(chunk.text)
                   tech.append(tech.str)

               else:
                   d_str = str(chunk.text)
                   d_str = re.sub(r'\b(the|a|an)\b', '', d_str)
                   d_str = d_str.strip()
                   if not domain:
                       domain.append(d_str)

       """
       due to the limitation of the dependency analysis of Spacy, some noun chunks cannot be identified properly, for
       example, XXX for part-of-speech tagging. tagging cannot be appropriately marked as the object of 'for' because Spacy
       have problems with -ing nouns.
       This and such problems should be dealt with some extra rules to maximally improve the results.
       """
       if not domain:
           for token in doc:
               if token.lemma_ == 'for':
                   if list(token.children):
                       d = [child for child in token.children][0]
                       if not d.dep == punct and not d.dep == pcomp:
                           d_str = str(doc[token.i + 1: d.i + 1])
                           d_str = re.sub(r'\b(the|a|an)\b', '', d_str)
                           d_str = d_str.strip()
                           domain.append(d_str)
                   """
                   to deal with cases like "xxx for integrating natural language processing techniquwa" when "integratubf"
                   the first child of "for" is
                   """
                   if d.dep == pcomp:
                       d_children = [child for child in d.children]
                       if len(d_children) != 0:
                           d1 = d_children[0]
                           d1_str = str(doc[d.i : d1.i+1])
                           d1_str = re.sub(r'\b(the|a|an)\b', '', d1_str)
                           d1_str = d1_str.strip()
                           domain.append(d1_str)

       #if no domian information can be extracted from the methods described above, then:
       if not domain:
           if not any (token.lemma_ == t for t in tech_triggers for token in doc):
               if not list(doc.noun_chunks):
                   domain.append(titles[i])
               else:
                   for chunk in doc.noun_chunks:
                       if any(t in str(chunk.text) for t in stops):
                           continue
                       elif len(str(chunk.text.strip('the')).split()) <= 1:
                           continue
                       else:
                           domain.append(str(chunk.text))
               if not domain:
                   domain.append(titles[i])
           #if tech triggers exist, should delete the tech phrases
           else:
               d_str1 = titles[i].replace (tech_str, '')
               d_str1 = re.sub(r'\b(via|using|with|across|through|base|use|by|from)\b','',d_str1)
               d_str1 = d_str1.strip()
               doc1 = nlp(d_str1)
               if not list(doc1.noun_chunks):
                   domain.append(d_str1)
               else:
                   for chunk in doc1.noun_chunks:
                       if any(t in str(chunk.text) for t in stops):
                           continue
                       elif len(str(chunk.text.strip('the')).split()) <= 1:
                           continue
                       else:
                           domain.append(str(chunk.text))
               if not domain:
                   domain.append(d_str1)

       #removing dulicates
       domain = list(set(domain))
       tech = list(set(tech))

       techs.append(tech)
       domains.append(domain)
       #print("title: " + str(titles[i]))
       #print('topic: ' + str(domain))
       #print('tech :' + str(tech))
       #print('/n')

   return domains, techs


domains, techs = relation_extration_from_title(titles)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/domains.p",'wb') as filehandle:
     pickle.dump(domains,filehandle)
with open("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/techs.p", 'wb') as filehandle:
    pickle.dump(techs, filehandle)


#extracting core information from abstracts, i.e. main concerns & method (optional) & results/achivements/improvements optional)
def info_extraction_from_abs (abstracts):
   triggers_main = ['present','propose','provide','introduce', 'study','address','examine','describe','explore',
                    'consider', 'construct', 'carry out', 'put forward', 'report on', 'work on','investigate',
                    'develop','focus on', 'represent','suggest']
   #trigger_techs = ['use','apply','employ','utilize']
   #trigger_results = ['outperform', 'show']
   topics = []
   techs = []
   results = []
   for i in range (len(abstracts)):
       topic = []
       #tech = []
       #result = []
       for s in abstracts[i]:
           doc = nlp(s)
           root = [token for token in doc if token.head == token][0]
           if any (root.lemma_ in t for t in triggers_main):
               #print(doc)
               if list(root.rights):
                   child_p = list(root.rights)[-1]
                   topic.append(str(doc[root.i+1 : child_p.i]))
                   #print(topic)
                   #print('\n')
       if not topic:
           topic.append(abstracts[i][0])
       topics.append(topic)

       """
           elif any (root.lemma_ == t for t in trigger_results):
               print (doc)
               children = [child for child in root.children if child.dep == dobj and child.i > root.i]
               if children:
                   child_p == children[0]
                   result.append(doc[root.i+1 : child_p.i+1])
                   print(result)
                   results.append(result)
           else:
               for token in doc:
                   if any (token.lemma_ == t for t in trigger_techs):
                       children = [child for child in token.children]
                       for child in children:
                           if child.dep == dobj or child.dep == pobj:
                               print (doc)
                               tech.append(doc[token.i+1 : child.i+1])
                               print(tech)
                               topics.append(topic)
       """

   return topics


info_from_abs = info_extraction_from_abs(abstracts)
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/info_from_abstract.p",'wb') as filehandle:
     pickle.dump(info_from_abs,filehandle)

#to merge the core information to form the new abstract
core_infos = []
for i in range(len(info_from_abs)):
    info1 = "This article focuses on "
    if len(domains[i])==0:
        continue
    elif len(domains[i])>1:
        for j in range(len(domains[i])):
            if j < len(domains[i])-1:
                info1 += (domains[i][j] + " and ")
            else:
                info1 += (domains[i][j] + ". ")
    else:
        info1 += (domains[i][0] + ". ")

    if not info1:
        info2 = "This articles presents "
    else:
        info2 = "It presents "

    if len(info_from_abs[i]) > 1:
        for j in range(len(info_from_abs[i])):
            #more than one concern and not exceeds max_summary_len (default = 40)
            if j < len(info_from_abs[i])-1 and (len(info1) + len(info2)) < 30:
                info2 += (info_from_abs[i][j] + " and ")
            else:
                info2 += (info_from_abs[i][j] + ". ")
    else:
        info2 += (info_from_abs[i][0] + ". ")

    info3 = ""
    if techs[i]:
        info3 += "It uses " + techs[i][0] + ". "

    info = info1 + info2 + info3

    core_infos.append(info)

with open("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/abs_infos.p", 'wb') as filehandle:
    pickle.dump(core_infos, filehandle)

