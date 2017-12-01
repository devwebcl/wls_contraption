Readme.txt
++++++++++

1. The python script files and the wrapper cmd / sh scripts can be found in the "scripts" directory

2. Edit the environment variables in the start wrapper script 

startWLSTJDBCSummarizer.sh (Unix) 

or 

startWLSTJDBCSummarizer.cmd (MS Windows) 

to suit your system

3. To run the "summarizer", launch the start cmd or .sh wrapper script. (You may need to use the chmod command on Unix to make the .sh file executable) 

4. Note - ensure the following files (found in the "output" directory) are located in the WLST_OUTPUT_PATH directory. 
If these javascript files are not local to the HTML file produced by the script, the HTML file will not render correctly. 

Tip: After the script has created the HTML output, you can manually edit the HTML to change the "href" to the .js and .css files. 
Or manually edit the python script (WLS_JDBC_Summary_Online.py) to change the link reference the script creates to these files. 
For example, you may want to do this if the output is to be accessed via a web server.