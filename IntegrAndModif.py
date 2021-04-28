import csv
from xml.etree import ElementTree as etree
from xml.dom import minidom

### opens the specified csv file and reads the file row by row
f = open('example_thesis2.csv')
csv_f = csv.reader(f)

### A list where all the generated test cases will be saved
inputCases = []
### A list where all method names are saved
method_names = []
i=0
###Expected Outcome is set to be zero for all the test cases
expectedOut = '0'
###--------------This part needs to be changed manually for every new FB----------------###

### goes through every row in csv file, extracts the input values and creates new test cases
for row in csv_f:
    ### generates the name for every new test case with individual numbering that is equal to the row number where inputs have been taken from
    i=i+1
    m_name = "NEW_Test" + str(i)
    #print(m_name)

    ###...TODO...add the test case name (m_name) to FB body-ST part as well, so that it gets called and executed

    ### separate variable that integrates the input values and then gets added into text_data
    case_to_add = """ TEST('"""+m_name+"""');
                         Sum(one := """+row[0]+""", two := """+row[1]+""", result =&gt; Result);
                          AssertEquals(Expected := ExpectedSum,
                                     Actual := Result,
                                     Message := 'The calculation is not correct');
                      TEST_FINISHED();"""

    text_data = """<data handleUnknown="implementation" name="http://www.3s-software.com/plcopenxml/method">
                      <Method name='"""+m_name+"""' ObjectId="071ba4c3-fe0d-4b0b-be72-a320c9d403a4">
                       <interface>
                          <localVars>
                          <variable name="Sum">
                            <type>
                              <derived name="FB_Sum" />
                            </type>
                          </variable>
                          <variable name="Result">
                            <type>
                              <UINT />
                            </type>
                          </variable>
                          <variable name="ExpectedSum">
                            <type>
                              <UINT />
                            </type>
                            <initialValue>
                              <simpleValue value='"""+expectedOut+"""' /> 
                            </initialValue>
                            </variable>
                        </localVars>
                        <addData>
                          <data name="http://www.3s-software.com/plcopenxml/accessmodifiers" handleUnknown="implementation">
                            <AccessModifiers Private="true" />
                          </data>
                        </addData>
                      </interface>
                      <body>
                        <ST>
                          <xhtml xmlns="http://www.w3.org/1999/xhtml">
                          """+case_to_add+"""
                          </xhtml>
                        </ST>
                      </body>
                      <addData />
                    </Method>
                </data>"""
                  
    method_names.append(m_name+'();')
    inputCases.append(etree.fromstring(text_data)) #new test cases are added in the list parsed as tree Elements
   
f.close()

###--------- Modification and Update of an XML file -----------###

file_n = "Just_tests2.xml"
elem = etree.parse(file_n) 

### Removes namespaces from the parsed xml file
def remove_namespace(doc, namespace):
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

remove_namespace(elem, u"http://www.plcopen.org/xml/tc6_0200")

root = elem.getroot()
#print(root.tag)

### Adds all the newly created test-case method names into FB body
fb_body = root.find('./types/pous/pou/body/ST/')
names = ' '.join(method_names)
fb_body.text = names   
print(fb_body.text)

### Finds a place where test cases as new methods will be added
place_for_case = elem.findall('./types/pous/pou/addData')
place_for_case[0].extend(inputCases)

#place_for_case.remove()


### Writes changes to a new XML file
elem.write("New_Just_Tests2.xml", encoding="us-ascii", xml_declaration = True)