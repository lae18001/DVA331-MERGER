# DVA331-Script_SEAFOX_CODESYS
The implementation of the script is a process of the  new test case creation while processing the  rows  from  a  csv-file.
Input  values  for  those test cases are set during the iteration process over each created data element’s variable tags. 
The  script uses  a  well  established  python  library  called xml.etree.ElementTree that is made especially for parsing, creating and modifying xml files.  For the merging process to begin, the user first needs to specify the names of the input files for the script (See the picture below). 
![TheScript](https://user-images.githubusercontent.com/48024044/117944797-ebfb6500-b30d-11eb-9460-30f03de20f65.JPG)

The csv-file, holding all the input values and the PLCopen XML file that will be parsed and used as a template for the new test case creation.  
The name of the output PLCopen XML file, that will be created holding all the newly generated test cases also requires user specified name.
In order to execute the script, all the previous mentioned input files and the script itself needs to be located in the same file folder on the users computer.  
Then the user needs to open the Command Prompt and specify the path to this folder or  simply  open  the  Windows  Power  Shell  from  the  folder  and  run  the  python  script using python command.  
If the execution of the script went as expected,  the number of created test cases will be printed out on the screen as well as the message of successfully created xml-file.
The main task of the script is to merge together two files with the most important information taken from both of them and create the new file, hence the name of the script - Merger.  
