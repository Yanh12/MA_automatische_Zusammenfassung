import os
import glob
import pickle
from xml.etree import ElementTree as ET
from collections import OrderedDict


#At first to get all xml-files
"""
recursively get all xml-files under the given directory, since the structure of the original corpus is quite complex.
the corpus has many sub-sections, each such-section contains a directory, which has a number of xml-files.
for example, a specific xml-file's path is like "..//P 15/P15/P15/P15-4003-parscit.130908.xml.
so, it needs basically 3-times of recursion to get to the file level
"""
def get_data_recursive (path, data):
    """
    :param path: the main path of the corpus
    :param data: firstly an empty list for storing file names
    :return: full file names
    """
    dir = os.listdir(path)
    for d in dir:
        if not os.path.isdir(d):
            try:
                get_data_recursive (path + "/" + d, data)
            except NotADirectoryError:
                data.append(path + "/" + d)
    return data

#a brief look at data
xmls = get_data_recursive ("/Users/yanqinghu/Downloads", [])
print("There are " +str(len(xmls)) + " texts in the original data set.")
#print(type(xmls[:10]))

def get_labeled_texts (files):
    #create a dictionary to store the texts
    labeled_texts = []

    #a list to store exceptions
    exceptions = []

    for file in files:
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            #for the structure of data: root[0][0]begings with the text contents
            text = root[0][0]
            #section label: document the child nodes in the text
            sectLabel = []
            for child in text:
                sectLabel.append(str(child))

            #if a section, it will be marked as 'sectionHeader'. This step is to extract all sections (their position ida)
            sectionHeader_id = []
            for i in range(len(sectLabel)):
                #to delete subsection like 1.1 mistagged as section header
                if " 'sectionHeader' " in sectLabel[i] and '\.' not in sectLabel[i]:
                    #or to say when the confidence score is higher than 0.8
                    #float(text[i].attrib['confidence']) > 0.8:
                    sectionHeader_id.append(i)

            #if a node is about a body text, it is marked as 'bodyText'.  Find out their positions.
            bodyText_id = []
            for i in range(len(sectLabel)):
                if " 'bodyText' " in sectLabel[i] and float(text[i].attrib['confidence']) > 0.9:
                    bodyText_id.append(i)

            #becuse body texts of a same section may be interrupted by figures, notes etcs, this step is to find out all
            #body texts of the same section by finding out all position ids between 2 sections and concatenating them.

            #get the titles
            title = ""
            for i in range(len(sectLabel)):
                if " 'title' " in sectLabel[i]:
                    title = text[i].text

            #make the dict to store the texts an ordered dict that keeps insertion order, so we can get ordered text
            textWithSecLabel = OrderedDict()
            textWithSecLabel['Title'] = title

            j = 0
            for i in range(len(sectionHeader_id)):
                secName = text[sectionHeader_id[i]].text  # type: object
                bodyText = ""  # type: str
                while j < len(bodyText_id) and i < (len(sectionHeader_id) - 1):
                    if sectionHeader_id[i] < bodyText_id[j] < sectionHeader_id[i + 1]:
                        bodyText += text[bodyText_id[j]].text
                        j += 1
                    else:
                        break
                #for each section, key is their section name and value is the body text
                d = {secName:bodyText}
                textWithSecLabel.update(d)

            #append each text to the whole text file
            labeled_texts.append(textWithSecLabel)

        #what if the xml is not well-formed and cannot be parsed
        except Exception as e:
            exceptions.append(e)

    return labeled_texts

labeled_texts = get_labeled_texts(xmls)
print("Deleting not well-formed texts, there are now " +str(len(labeled_texts)) + " texts.")

#some texts are only general intro of a book, they should be deleted.
labeled_texts_selected = []
for text in labeled_texts:
    if ('\nAbstract\n') not in text.keys():
        continue
    else:
        labeled_texts_selected.append(text)
print("They are finally " + str(len(labeled_texts_selected)) + " texts in the corpus.")


#pickel the texts list
if os.path.exists("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts.p"):
    os.remove("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts.p")
with open ("/Users/yanqinghu/Desktop/Masterarbeit/CL_data/texts.p",'wb') as filehandle:
    pickle.dump(labeled_texts_selected,filehandle)
