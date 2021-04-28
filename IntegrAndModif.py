import csv
from xml.etree import ElementTree as etree

###-------FILE NAMES NEED TO BE CHANGED FOR EVERY FB--------###

input_file = "example_thesis2.csv"      # file with generated input values from SEAFOX
file_to_parse = "testing3.xml"          # exported PLCopenXML file from CODESYS with FB_Test_suite as an example test case
new_file_name = "testing3_new.xml"      # File that will be imported back to CODESYS with new test cases 

f = open(input_file)         # opens and loads the specified csv-file
csv_f = csv.reader(f)        # Reads the csv-file row by row

inputCases = []              # A list where all the generated test cases will be saved
method_names = []            # A list where all method names are saved
i=0

### goes through every row in csv-file, extracts the input values and creates new test cases with them
for row in csv_f:
    i=i+1

    ###--------------The following parts need to be changed manually for every new FB----------------###

    m_name = "FB_SafeCraneNumber" + str(i)       #----CHANGE THE METHOD NAME----#

    ###-----COPY/PASTE IN THE STRING------from xml file. The whole <data> Element located at './types/pous/pou/addData/'.-----###
    ### String that will create a new Element in xml file.  Every Element matches a single test case in CODESYS program
    text_data = """<data name="http://www.3s-software.com/plcopenxml/method" handleUnknown="implementation">
            <Method name="New_Method_name" ObjectId="cc6b36d7-5497-4911-81b5-9c5d048b7581">
              <interface>
                <localVars>
                  <variable name="Fun">
                    <type>
                      <derived name="ccsSafeCraneNumberSuperv" />
                    </type>
                  </variable>
                  <variable name="Result">
                    <type>
                      <BOOL />
                    </type>
                  </variable>
                  <variable name="ExpectedResult">
                    <type>
                      <BOOL />
                    </type>
                    <initialValue>
                      <simpleValue value="FALSE" />
                    </initialValue>
                  </variable>
                  <variable name="Condition">
                    <type>
                      <BOOL />
                    </type>
                  </variable>
                </localVars>
              </interface>
              <body>
                <ST>
                  <xhtml xmlns="http://www.w3.org/1999/xhtml">TEST('"""+m_name+"""');
Fun(in_CraneNoSet1 := """+row[0]+""", in_CraneNoSet2 := """+row[1]+""", out_S_CraneNoSupervOk =&gt; Result);    
AssertTrue(Condition := (Result = ExpectedResult),
           Message := 'Result is True');
                                                                                      
TEST_FINISHED();</xhtml>
                </ST>
              </body>
              <addData />
            </Method>
          </data>"""
                  
    method_names.append(m_name)                         # method names are saved in a list to later add in FB body
    inputCases.append(etree.fromstring(text_data))      # new test cases are added in the list while parsed as tree Elements
   
f.close()

###--------- Modification and Update of an XML file -----------###

### Parses the file where new test cases will be addded
elem = etree.parse(file_to_parse) 
root = elem.getroot()
#print(root.tag)

### Removes namespaces from the parsed xml file
def remove_namespace(doc, namespace):
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

name_space = u"http://www.plcopen.org/xml/tc6_0200" 
remove_namespace(elem, name_space)

### Sets new method names in each Element <data><Method 'name'= 'new_name'>
for i in range(len(method_names)):
    inputCases[i][0].set('name', method_names[i]) 
    #print(inputCases[i][0].attrib)

#### Adds all newly created (test cases) method names into FB body (as function calls in CODESYS)
fb_body = root.find('./types/pous/pou/body/ST/')
names = '(); \n'.join(method_names)+'(); '
fb_body.text = names   
print(""+str(len(method_names))+" new test cases were created:\n",fb_body.text)

### Finds a place where new test cases will be added
### clears the existing list and adds in new list of cases
place_for_case = elem.findall('./types/pous/pou/addData/')
place_for_case[0].clear()
place_for_case[0].extend(inputCases)

### Changes are written to a new XML file
elem.write(new_file_name, encoding="us-ascii", xml_declaration = True)
print('The new file was created successfully!:', new_file_name)