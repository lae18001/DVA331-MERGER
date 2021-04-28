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
    ### generates the name for every new test case with individual numbering that is equal to the row number
    i=i+1
    m_name = "FB_CraneNumberSuperv_Test" + str(i)

    text_data = """<data name="http://www.3s-software.com/plcopenxml/method" handleUnknown="implementation">
            <Method name='"""+m_name+"""' ObjectId="cc6b36d7-5497-4911-81b5-9c5d048b7581">
              <interface>
                <inputVars>
                  <variable name="craneNoSet1">
                    <type>
                      <WORD />
                    </type>
                    <initialValue>
                      <simpleValue value='"""+row[0]+"""'/>
                    </initialValue>
                    <documentation>
                      <xhtml xmlns="http://www.w3.org/1999/xhtml"> First crane number </xhtml>
                    </documentation>
                  </variable>
                  <variable name="craneNoSet2">
                    <type>
                      <WORD />
                    </type>
                    <initialValue>
                      <simpleValue value='"""+row[1]+"""'/>
                    </initialValue>
                    <documentation>
                      <xhtml xmlns="http://www.w3.org/1999/xhtml"> Second crane number </xhtml>
                    </documentation>
                  </variable>
                </inputVars>
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
                  <xhtml xmlns="http://www.w3.org/1999/xhtml">TEST('"""+m_name+"""');      			      (* Naming the test case *)

Fun(in_CraneNoSet1 := craneNoSet1, in_CraneNoSet2 := craneNoSet2, out_S_CraneNoSupervOk =&gt; Result);    (* Calling the FB to be tested *)
AssertTrue(Condition := (Result = ExpectedResult),
           Message := 'Result is True');
                                                                                      
TEST_FINISHED();</xhtml>
                </ST>
              </body>
              <addData />
            </Method>
          </data>"""
                  
    method_names.append(m_name+'();')
    inputCases.append(etree.fromstring(text_data)) #new test cases are added in the list parsed as tree Elements
   
f.close()

###--------- Modification and Update of an XML file -----------###

### Specify the file name where new test cases will be addded
file_n = "just_t1.xml"
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

### Adds all newly created (test case) method names into FB body
fb_body = root.find('./types/pous/pou/body/ST/')
names = ' '.join(method_names)
fb_body.text = names   
print(fb_body.text)

### Finds a place where new test cases will be added
### clears the existing space and adds in new cases
place_for_case = elem.findall('./types/pous/pou/addData')
place_for_case[0].clear()
place_for_case[0].extend(inputCases)

### Changes are written to a new XML file, name needs to be specifyed
new_file_name = "just_t1_new1.xml"
elem.write(new_file_name, encoding="us-ascii", xml_declaration = True)
print('The new file was created!:', new_file_name)