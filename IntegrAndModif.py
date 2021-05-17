import csv
from xml.etree import ElementTree as etree
import copy

###-------FILE NAMES NEED TO BE CHANGED FOR EVERY FB--------###

input_file = "testcaseInputs.csv"		# file with generated input values from SEAFOX
file_to_parse = "testFB.xml"			# exported PLCopenXML file from CODESYS with FB_Test_suite as an example test case
new_file_name = "testcases.xml"			# File that will be imported back to CODESYS with new test cases 
m_name = "TC"							#----CHANGE THE METHOD NAME----#

f = open(input_file)         # opens and loads the specified csv-file
csv_f = csv.reader(f)        # Reads the csv-file row by row

inputCases = []              # A list where all the generated test cases will be saved
method_names = []            # A list where all method names are saved
inputtext = []
methodText = ""

### Parses the file where new test cases will be addded
xmlTree = etree.parse(file_to_parse) 
root = xmlTree.getroot()

name_space = u"http://www.plcopen.org/xml/tc6_0200" 
#remove_namespace(xmlTree, name_space)
ns = u'{%s}' % name_space
nsl = len(ns)
for elem in xmlTree.iter():
	if elem.tag.startswith(ns):
		elem.tag = elem.tag[nsl:]

i=0
k=1

### goes through every row in csv-file, extracts the input values and creates new test cases with them
for row in csv_f:
	i = 0
	methodText = ""

	# Update input values for test case
	for element in root.findall('types/pous/pou/addData/data/Method/interface/inputVars/variable'):
		isTIME = False
		for child in element:
			if child.tag == "type":
				if child[0].tag == "TIME":
					isTIME = True
			if child.tag == "initialValue":
				if child[0].tag == "simpleValue":
					if isTIME:
						child[0].set('value', 'T#'+str(row[i])+'ms')
						i = i + 1
					else:
						child[0].set('value', row[i])
						i = i + 1			

	# update test case name in method
	for element in root.findall('types/pous/pou/addData/data/Method'):
		element.set('name', m_name+str(k))
		
	# update test case body text
	p = root.findall('types/pous/pou/addData/data/Method/body/ST')
	for element in root.find('types/pous/pou/addData/data/Method/body/ST'):
		methodText = element.text
		methodText = methodText.split(';', 1)[1]
		methodText = "<xhtml xmlns='http://www.w3.org/1999/xhtml'>TEST('" + m_name + str(k) + "');" + methodText + "</xhtml>"	#Change test case name in body
		inputtext.append(etree.fromstring(methodText))
		method_names.append(m_name + str(k)) # method names are saved in a list to later add in FB body
		k = k + 1

	# update xml file with test case body
	p[0].clear()
	p[0].extend(inputtext)
	inputtext.clear()
	
	# new test cases are added in the list
	path = root.findall('types/pous/pou/addData/data')
	newData = xmlTree.find('types/pous/pou/addData/data')
	tc = copy.deepcopy(newData)
	inputCases.append(tc)

f.close()

#### Adds all newly created (test cases) method names into FB body (as function calls in CODESYS)
fb_body = root.find('./types/pous/pou/body/ST/')
names = '(); \n'.join(method_names)+'(); '
fb_body.text = names   
print(""+str(len(method_names))+" new test cases were created\n")

### Finds a place where new test cases will be added
### clears the existing list and adds in new list of cases
place_for_case = root.findall('types/pous/pou/addData')
place_for_case[0].clear()
place_for_case[0].extend(inputCases)

### Changes are written to a new XML file
xmlTree.write(new_file_name,encoding='UTF-8',xml_declaration=True)
print('The new file was created successfully!:', new_file_name)