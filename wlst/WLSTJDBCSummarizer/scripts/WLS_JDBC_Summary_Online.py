# Prototype Script to perform WLST online collection of JDBC System Resource and JTA MBeans
# The values are printed as part of a HTML file which is built dynamically by this script.
# Author: Daniel Mortimer
# Proactive Support Delivery
# Date: 2nd July 2013
# Version 003

#IMPORTS

# import types;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import os;
import string;
from java.lang import *
from java.util import Date


# START OF FUNCTIONS

# function to help locate whether MBean directory exists. 
# This does not perform a global search. It just checks whether a given MBean directory exists at the level the script is currently in 
def findMBean(v_pattern):
        # get a listing of everything in the current directory
	mydirs = ls(returnMap='true');
 
        v_compile_pattern = java.util.regex.Pattern.compile(v_pattern);
	
	found = 'Nope not here';
        
	for mydir in mydirs:
		x = java.lang.String(mydir);
		v_matched = v_compile_pattern.matcher(x);
		if v_matched.find():
			found = 'true';
                 
        return found;

# function to strip the Bean Value which is returned as tuple (list). 
# We only want to return and print the target name and type

		
def stripMBeanValue (v_mbeanvalue,v_type):
	
	v_check_value = str(v_mbeanvalue);
	v_strippedValue01 = String.replace(v_check_value,'[MBeanServerInvocationHandler]','');
	v_strippedValue02 = String.replace(v_strippedValue01,'com.bea:Name=','');
	#v_strippedValue03 = "Strip Function Failed";
	
	if v_type == 'Cluster':
		v_strippedValue = String.replace(v_strippedValue02,',Type=Cluster','');
	
	if v_type == 'Machine':
		v_strippedValue = String.replace(v_strippedValue02,',Type=Machine','');
		
	if v_type == 'JDBC_Server':
		v_strippedValue03 = String.replace(v_strippedValue02,'Location=','');
		v_strippedValue04 = String.replace(v_strippedValue03,',Type=ServerRuntime','');
		v_strippedValue05 = String.replace(v_strippedValue04,',',' ');
		v_strippedValue = v_strippedValue05.split();
		# Pick v_strippedValue[1]	
	
	if v_type == 'JDBC_DataSource':
		
		v_strippedValue03 = String.replace(v_strippedValue02,'com.bea:ServerRuntime=','');
		v_strippedValue04 = String.replace(v_strippedValue03,'Name=','');
		v_strippedValue05 = String.replace(v_strippedValue04,',Type=JDBCDataSourceRuntime','');
		v_strippedValue06 = String.replace(v_strippedValue05,',',' ');
		v_strippedValue = v_strippedValue06.split();	
		# Pick v_strippedValue[1]	
	

	if v_type == 'JTA_RuntimeSource':
		
		v_strippedValue03 = String.replace(v_strippedValue02,'[MBeanServerInvocationHandler]com.bea:Name=','');
		v_strippedValue04 = String.replace(v_strippedValue03,'Location=','');
		v_strippedValue05 = String.replace(v_strippedValue04,',Type=ServerRuntime','');
		v_strippedValue06 = String.replace(v_strippedValue05,',',' ');
		v_strippedValue = v_strippedValue06.split();

		
	if v_type == 'HealthCheck':
		
		v_strippedValue03 = String.replace(v_strippedValue02,'Component:ServerRuntime,State:','');
		v_strippedValue04 = String.replace(v_strippedValue03,'MBean:','');
		v_strippedValue05 = String.replace(v_strippedValue04,'Component:','');
		v_strippedValue06 = String.replace(v_strippedValue05,'null','');
		v_strippedValue07 = String.replace(v_strippedValue06,'State:','');
		v_strippedValue08 = String.replace(v_strippedValue07,'ReasonCode:[]','');
		v_strippedValue09 = String.replace(v_strippedValue08,',',' ');
		v_strippedValue = v_strippedValue09.split();
		
	if v_type == 'Target':
		
		v_strippedValue03 = String.replace(v_strippedValue02,'array(weblogic.management.configuration.TargetMBean,','');
		v_strippedValue04 = String.replace(v_strippedValue03,'[[MBeanServerInvocationHandler]','');
		v_strippedValue05 = String.replace(v_strippedValue04,'com.bea:Name=','');
		v_strippedValue06 = String.replace(v_strippedValue05,'array(javax.management.ObjectName,[','');
		v_strippedValue07 = String.replace(v_strippedValue06,'Type=','');
		v_strippedValue08 = String.replace(v_strippedValue07,'])','');
		v_strippedValue09 = String.replace(v_strippedValue08,',',' ');
		v_strippedValue = v_strippedValue09.split();
		

					
	
	return v_strippedValue;		

# END OF FUNCTIONS

# START OF SCRIPT

#Some WLST commands throw output to stdout
#For a cleaner user experience we redirect that stuff to log.
#Only print commands will display to the console - print >>f commands are redirecting to the HTML output file

# You can use a properties file as an alternative method for obtaining parameters such as domain URL and username 
# loadProperties('summarizer.properties')

redirect('wlstonlinedomainsummarizer.log', 'false');


v_chooseMode = raw_input('Is your domain Admin Server up and running and do you have the connection details? (Y /N ): ').lower();

if v_chooseMode == 'y':
		
	try:
		#We obtain connecton details interactively. An alternative is store these properties values in a properties file
		URL = raw_input('Enter connection URL to Admin Server e.g t3://mymachine.acme.com:7001 : ');
		username = raw_input('Enter weblogic username: ');
		password = "".join(java.lang.System.console().readPassword("Enter weblogic username password %s", [prompt]));
		connect(username, password,URL);
	except:
		print "There has been a problem connecting to the Admin Server. This script will not work unless WLST can establish a connection to the Admin Server.";
		exit();
else:
	print "Sorry, for this script to work your Admin Server needs to be up and running. Please start your Admin Server and try again.";
	exit();


v_domainHome = os.environ["DOMAIN_HOME"];
v_outputFilePath = os.environ["WLST_OUTPUT_PATH"];
v_outputFile = os.environ["WLST_OUTPUT_FILE"];


if v_domainHome == '':
	v_domainHome = raw_input('Enter DOMAIN_HOME, specify full path: ');
	
if v_outputFilePath== '':	
	v_outputFilePath = raw_input('Enter output directory, specify full path including final trailing slash: ');

if v_outputFile== '':	
	v_outputFile = raw_input('Enter output file name, specify .html as the file extension: ');

if os.path.isdir(v_domainHome) == false:
 	raise Exception ('Invalid Domain Home. The path does not exist. Check the start summarizer cmd or sh file.')

if os.path.isdir(v_outputFilePath) == false:
 	raise Exception ('Invalid Output Directory. The path does not exist')







# OPEN the output HTML file and start to write to it

f = open(v_outputFilePath  + v_outputFile, 'w');

# Work out what is available for capture

v_JDBCfound = findMBean('JDBCSystemResources');
v_JTAfound = findMBean('JTA');


# BUILD the HTML, header includes javascript and css to enable table styling and sorting

print >>f, "<html>"

print >>f, "<head>"

print >>f, "<script src=\"spry.js\"></script>"
print >>f, "<script type=\"text/javascript\" src=\"jquery-ui.js\"></script>"
print >>f,"<link href=\"WLSTSummarizer.css\" type=\"text/css\" rel=\"stylesheet\">"


print >>f, "</head>"

print >>f, "<body>"


print >>f, "<div id=\"divContainer\">"
print >>f, "<h1 class=\"headline3\">Introduction</h1>"
print >>f, "<p>This is the output from a WLST script run in <u><strong>ONLINE mode</strong></u>. The script retrieves JDBC System Resource and JTA (Java Transaction API) MBean values. </p>"
print >>f, "<p>Note: Make sure the spry.js, jquery-ui.js and WLSTSummarizer.css are located in same local directory as this HTML file"
print >>f, "</p>"
print >>f, "</div>"
print >>f, "<p></p>"


print >>f, "<div id=\"divContainer\">"
print >>f, "<p></p>"
print >>f, "<div id=\"TabbedPanels001\" class=\"TabbedPanels\">"
print >>f,  "<ul class=\"TabbedPanelsTabGroup\">"
print >>f,	"<li class=\"TabbedPanelsTab\" tabindex=\"0\">JDBC</li>"
print >>f,	"<li class=\"TabbedPanelsTab\" tabindex=\"0\">JTA</li>"
print >>f,  "</ul>"
print >>f, "<div class=\"TabbedPanelsContentGroup\">"	


print >>f, "<div class=\"TabbedPanelsContent\">"


print >>f, "<h3 class=\"headline1\">JDBC System Resources - Configuration</h3>"
print >>f, "<p>"
print >>f, "</p>"

# Check if JDBC System Resource MBean Directory exists


if v_JDBCfound == 'true':

	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining System JDBC Resource configuration information"
	print "++++++++++++++++++++++++++"
	print ""



	cd ('JDBCSystemResources');
	myjdbcresources = ls(returnMap='true');
	v_MultiSourceFlag = 'false';
	
	
	
	print >>f, "<table id=\"my_JDBC_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th rowspan=2>Name</th>"
	print >>f, "<th rowspan=2>Type</th>"
	print >>f, "<th colspan=2>Target(s)</th>"
	print >>f, "<th rowspan=2>Driver</th>"
	print >>f, "<th rowspan=2>Global Transactions Protocol</th>"
	print >>f, "<th rowspan=2>JDBC URL</th>"
	print >>f, "<th colspan=3>Connection Pool Capacity</th>"
	print >>f, "</tr>"
	print >>f, "<tr>"
	print >>f, "<th>Name</th>"
	print >>f,  "<th>Type</th>"
	print >>f, "<th>Init</th>"
	print >>f,  "<th>Min</th>"
	print >>f, "<th>Max</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"
	
	
	for myjdbcresource in myjdbcresources:
		x_jdbc = java.lang.String(myjdbcresource);
		
		# Change to the JDBC Resource
		cd(x_jdbc);
		
		# If a resource has no targets, the get will fail with an error, so we need to code for this scenario 
		try:
			v_any_targets = '';
			v_jdbc_target = get('Targets');
			v_no_of_targets = len(v_jdbc_target);
					
		except:
			
			v_no_of_targets = 0;
			
			# The exception will still display to standard out, which may cause alarm
			# So adding this message telling the user the exception is expected and can be ignored
			print "IGNORE this exception";	
		
			
		
		
		# Get the other attribute values
		cd ('JDBCResource')
		cd (x_jdbc);
		cd ('JDBCDriverParams');
		cd (x_jdbc);
		
		v_JDBCType = 'Generic';
		
		v_DriverName = get('DriverName');
		v_JDBC_URL = get('Url');
		
		
		
		cd ('../../');
		
		cd ('JDBCDataSourceParams');
		cd (x_jdbc);
		
		v_GlobalTransactionsProtocol = get('GlobalTransactionsProtocol');
		v_DataSourceList = get('DataSourceList');
		
		#Checking to see if this is Gridlink Data Source Type. If OneNodeList returns a value then we can assume yes it is
		cd ('../../JDBCOracleParams');
		cd (x_jdbc);
		v_OnsNodeList = get('OnsNodeList'); 
		
		
		
		# Get Connection Pool Capacity Configuration
		cd ('../../JDBCConnectionPoolParams');
		cd (x_jdbc);
		
		v_ConnectPoolInitial = get('InitialCapacity');
		v_ConnectPoolMin = get('MinCapacity');
		v_ConnectPoolMax = get('MaxCapacity');
		
		cd ('../../../../../');
		
		
		
		# If the Data Source is Multi, set the Type to Multi. Driver Name and URL are not applicable
		# as a multi data source is like a cluster i.e it consists of multi generic data sources
		if str(v_DriverName) == 'None':
			
			v_JDBCType = 'Multi';
			v_DriverName = 'n/a';
			v_JDBC_URL = 'n/a';
			v_GlobalTransactionsProtocol = 'n/a';
			v_MultiSourceFlag = 'true';
		else:
			v_DataSourceList = 'n/a';	
		
		
		
		#We can determine whether a data source is GridLink by checking whether it has a ONS Nodes
		
		if str(v_OnsNodeList)  != 'None':
			v_JDBCType = 'GridLink';
			v_OnsNodeList = '';
		
		
		
		
		
		
		
		
		if v_JDBCType != 'Multi':
		
			# Now we are ready to print the HTML, setting rowspan
			print >>f, "<tr>";
			print >>f, "<td";
			print >>f, "rowspan=";
			print >>f, v_no_of_targets;
			print >>f, ">";
			print >>f, x_jdbc;
			print >>f, "</td>";
			print >>f, "<td";
			print >>f, "rowspan=";
			print >>f, v_no_of_targets;
			print >>f, ">";
			print >>f, v_JDBCType;
			print >>f, "</td>";
		
		
		
			if v_no_of_targets > 0:
			
				v_count02 = 'false';
			
				for value in v_jdbc_target:
					value = stripMBeanValue(value, 'Target');
					if v_count02 == 'true':
						print >>f, "<tr>";
						print >>f, "<td>";
						print >>f, value[0];
						print >>f, "</td>";
						print >>f, "<td>";
						print >>f, value[1];
						print >>f, "</td>";
						print >>f, "</tr>";
					else:	
						print >>f, "<td>";
						print >>f, value[0];
						print >>f, "</td>";
						print >>f, "<td>";
						print >>f, value[1];
						print >>f, "</td>";
						
					
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_DriverName;
						print >>f, "</td>";
					
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_GlobalTransactionsProtocol;
						print >>f, "</td>";
					
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_JDBC_URL;
						print >>f, "</td>";
						
						
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_ConnectPoolInitial;
						print >>f, "</td>";
						
						
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_ConnectPoolMin;
						print >>f, "</td>";
						
						print >>f, "<td";
						print >>f, "rowspan=";
						print >>f, v_no_of_targets;
						print >>f, ">";
						print >>f, v_ConnectPoolMax;
						print >>f, "</td>";
						
				
						print >>f, "</tr>";
						v_count02 = 'true';
			else:
				v_any_targets = 'None';
				print >>f, "<td>";
				print >>f, 	v_any_targets;
				print >>f, "</td>";
				
				print >>f, "<td>";
				print >>f, 	"n/a";
				print >>f, "</td>";
				
				
				print >>f, "<td>";
				print >>f, v_DriverName;
				print >>f, "</td>";
					
				print >>f, "<td>";
				print >>f, v_GlobalTransactionsProtocol;
				print >>f, "</td>";
					
				print >>f, "<td>";
				print >>f, v_JDBC_URL;
				print >>f, "</td>";
				
				print >>f, "<td";
				print >>f, "rowspan=";
				print >>f, v_no_of_targets;
				print >>f, ">";
				print >>f, v_ConnectPoolInitial;
				print >>f, "</td>";
						
						
				print >>f, "<td";
				print >>f, "rowspan=";
				print >>f, v_no_of_targets;
				print >>f, ">";
				print >>f, v_ConnectPoolMin;
				print >>f, "</td>";
						
				print >>f, "<td";
				print >>f, "rowspan=";
				print >>f, v_no_of_targets;
				print >>f, ">";
				print >>f, v_ConnectPoolMax;
				print >>f, "</td>";
				
				
				print >>f, "</tr>";
		
	

	print >>f, "</tbody></table>"
	print >>f, "<p></p>"		
	
	
	v_didyoufindit = '';
	# Return to MBean Tree Root
	cd ('..');

else:
	print >>f, "<p>No JDBC Data Sources are configured within this domain.</p>";
	v_didyoufindit = '';
	# Return to MBean Tree Root
	cd ('..');


# Print out the Multi Data Sources if they exist

if v_MultiSourceFlag == 'true':
	
	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining System JDBC (Multi Source) configuration information"
	print "++++++++++++++++++++++++++"
	print ""
	
	cd ('JDBCSystemResources');
	
	print >>f, "<h4 class=\"headline1\">Multi Data Sources</h4>"
	print >>f, "<p>"
	print >>f, "</p>"
	
	print >>f, "<table id=\"my_JDBCMulti_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th>JDBC Data Source Name</th>"
	print >>f, "<th>Contains</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"

	for myjdbcresource in myjdbcresources:
		x_jdbc = java.lang.String(myjdbcresource);
		
		
		# Find Data Sources
		cd(x_jdbc);
		cd ('JDBCResource')
		cd (x_jdbc);
		cd ('JDBCDataSourceParams');
		cd (x_jdbc);
		
		v_DataSourceList00 = get('DataSourceList');
		
		# Return to JDBCSystemResources Tree Root
		cd ('../../../../../');
		
		if str(v_DataSourceList00) != 'None':
			
			#Data Sources List is returned as a comma delimited string. 
			#We need to turn it into a list if we want to print the data in sub rows
			v_DataSourceList01 = String.replace(v_DataSourceList00,',',' ');
			v_DataSourceList = v_DataSourceList01.split();
			v_no_of_datasources = len(v_DataSourceList);
			v_count05 = 'false';
			
			
			print >>f, "<tr>";
			print >>f, "<td";
			print >>f, "rowspan=";
			print >>f, v_no_of_datasources;
			print >>f, ">";
			print >>f, x_jdbc;
			print >>f, "</td>";
			
			
			for value in v_DataSourceList:
				if v_count05 == 'true':
					print >>f, "<tr>";
					print >>f, "<td>";
					print >>f, value;
					print >>f, "</td>";
					print >>f, "</tr>";
				else:	
					print >>f, "<td>";
					print >>f, value;
					print >>f, "</td>";
								
					print >>f, "</tr>";
					v_count05 = 'true';
		
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"	
	
# Return to MBean Tree Root	
cd ('..');	
		

# Now if data sources are active get JDBC Runtime data

print >>f, "<h3 class=\"headline1\">JDBC Runtime Information</h3>"
print >>f, "<p>"
print >>f, "</p>"

v_JDBCRuntimeDataExists = 'false';		
servers = domainRuntimeService.getServerRuntimes();

for server in servers:
	jdbcRuntime = server.getJDBCServiceRuntime();
	datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
	
	
        v_no_of_datasources = len(datasources);
	
	if v_no_of_datasources > 0:
		v_JDBCRuntimeDataExists = 'true';


if v_JDBCRuntimeDataExists == 'true':
	
	
	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining System JDBC Resource runtime information"
	print "++++++++++++++++++++++++++"
	print ""
	
	
	
	print >>f, "<table id=\"my_JDBCRuntime_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th rowspan=2>Server Name</th>"
	print >>f, "<th rowspan=2>JDBC Data Source Name</th>"
	print >>f, "<th rowspan=2>State</th>"
	print >>f, "<th colspan=4>Connections</th>"
	print >>f, "</tr>"
	print >>f, "<tr>"
	print >>f, "<th>Active</th>"
	print >>f,  "<th>Waiting</th>"
	print >>f,  "<th>Leaked</th>"
	print >>f,  "<th>Current Capacity</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"


	for server in servers:
		jdbcRuntime = server.getJDBCServiceRuntime();
		datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
		v_no_of_datasources = len(datasources);
		
		if v_no_of_datasources > 0:
			v_count04 = 'false';
			
			print >>f, "<tr>";
			print >>f, "<td rowspan=";
			print >>f, v_no_of_datasources;
			print >>f, ">";
			print >>f, stripMBeanValue(server, 'JDBC_Server')[1];
			print >>f, "</td>";
			
			
			for datasource in datasources:
				v_ActiveConnections = datasource.getActiveConnectionsCurrentCount();
				v_WaitingConnections = datasource.getWaitingForConnectionCurrentCount();
				v_JDBCSource_State = datasource.getState();
				v_LeakedConnectionCount = datasource.getLeakedConnectionCount()
				v_CurrCapacity = datasource.getCurrCapacity()
		
				if v_count04 =='true':
					print >>f, "<tr>";
					print >>f, "<td>";
					print >>f, stripMBeanValue(datasource, 'JDBC_DataSource')[1];
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_JDBCSource_State;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_ActiveConnections;
					print >>f, "</td>";
					print >>f, "<td>";
					print >>f, v_WaitingConnections;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_LeakedConnectionCount;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_CurrCapacity;
					print >>f, "</td>";
					
					print >>f, "</tr>";
				else:
					print >>f, "<td>";
					print >>f, stripMBeanValue(datasource, 'JDBC_DataSource')[1];
					print >>f, "</td>"
					
					print >>f, "<td>";
					print >>f, v_JDBCSource_State;
					print >>f, "</td>";
			
					print >>f, "<td>";
					print >>f, v_ActiveConnections;
					print >>f, "</td>"
			
					print >>f, "<td>";
					print >>f, v_WaitingConnections;
					print >>f, "</td>"
					
					print >>f, "<td>";
					print >>f, v_LeakedConnectionCount;
					print >>f, "</td>";
					
					print >>f, "<td>";
					print >>f, v_CurrCapacity;
					print >>f, "</td>";
					
					print >>f, "</tr>";
					v_count04 ='true';
					
	
			
	print >>f, "</tbody></table>"
	print >>f, "<p></p>"		

else:
	print >>f, "There is no JDBC System Resource Runtime data available";
	print >>f, "<p>"
	print >>f, "</p>"

# End of JDBC Panel
print >>f, "</div>"





print >>f, "<div class=\"TabbedPanelsContent\">"


print >>f, "<h3 class=\"headline1\">JTA - Domain Level Configuration</h3>"
print >>f, "<p>"
print >>f, "</p>"

# Check if JTA MBean Directory exists



if v_JTAfound == 'true':

	print ""
	print "++++++++++++++++++++++++++"
	print "Obtaining JTA Domain Level configuration information"
	print "++++++++++++++++++++++++++"
	print ""



	cd ('JTA');
	myjtaresources = ls(returnMap='true');
	
	
	print >>f, "<table id=\"my_JTA_table\" border=\"1\" class=\"formatHTML5\">"
	print >>f, "<thead align=\"left\">"
	print >>f, "<tr>"
	print >>f, "<th>Domain Name</th>"
	print >>f, "<th>Abandon Timeout Seconds</th>"
	print >>f, "<th>Before Completion Iteration Limit</th>"
	print >>f, "<th>Checkpoint Interval Seconds</th>"
	print >>f, "<th>Forget Heuristics</th>"
	print >>f, "<th>Max Transactions</th>"
	print >>f, "<th>Two Phase Enabled</th>"
	print >>f, "<th>Timeout Seconds</th>"
	print >>f, "</tr>"
	print >>f,"</thead>"
	print >>f, "<tbody>"
	
	
	for myjtaresource in myjtaresources:
		x_jta = java.lang.String(myjtaresource);
		
		# Change to the JDBC Resource
		cd(x_jta);
		
		
		v_AbandonTimeoutSeconds = get('AbandonTimeoutSeconds');
		v_BeforeCompletionIterationLimit = get('BeforeCompletionIterationLimit');
		v_CheckpointIntervalSeconds = get('CheckpointIntervalSeconds');
		v_ForgetHeuristics = get('ForgetHeuristics');
		v_MaxTransactions = get('MaxTransactions');
		v_TwoPhaseEnabled = get('TwoPhaseEnabled');
		v_TimeoutSeconds = get('TimeoutSeconds');
	
		
		# Now we are ready to print the HTML, setting rowspan
		print >>f, "<tr>";
		print >>f, "<td>";
		print >>f, x_jta;
		print >>f, "</td>";
		
		print >>f, "<td>";
		print >>f, v_AbandonTimeoutSeconds;
		print >>f, "</td>";
		
		print >>f, "<td>";
		print >>f, v_BeforeCompletionIterationLimit;
		print >>f, "</td>";
		
		print >>f, "<td>";
		print >>f, v_CheckpointIntervalSeconds;
		print >>f, "</td>";
		
		print >>f, "<td>";
		print >>f, v_ForgetHeuristics;
		print >>f, "</td>";
		
		print >>f, "<td>";
		print >>f, v_MaxTransactions;
		print >>f, "</td>";
		
		print >>f, "<td>";
		print >>f, v_TwoPhaseEnabled;
		print >>f, "</td>";
		
		print >>f, "<td>";
		print >>f, v_TimeoutSeconds;
		print >>f, "</td>";
		
		print >>f, "</tr>";
		
		# Return to MBean JTA Root
		cd('..')		
		
	

	print >>f, "</tbody></table>"
	print >>f, "<p></p>"		
	
	
	# Return to MBean Tree Root
	cd ('..');

else:
	print >>f, "<p>No JTA is configured within this domain.</p>";



		

# Now if servers are active get JTA Runtime data

print >>f, "<h3 class=\"headline1\">JTA Runtime Information - Per Server</h3>"
print >>f, "<p>"
print >>f, "</p>"

		
servers = domainRuntimeService.getServerRuntimes();
	
	
print ""
print "++++++++++++++++++++++++++"
print "Obtaining JTA Runtime information"
print "++++++++++++++++++++++++++"
print ""
		
	
print >>f, "<table id=\"my_JTARuntime_table\" border=\"1\" class=\"formatHTML5\">"
print >>f, "<thead align=\"left\">"
print >>f, "<tr>"
print >>f, "<th>Server</th>"
print >>f, "<th>Active Transaction Total Count</th>"
print >>f, "<th>Transaction Abandoned Total Count</th>"
print >>f, "<th>Transaction Committed Total Count</th>"
print >>f, "<th>Transaction Total Count</th>"
print >>f, "</tr>"	
print >>f,"</thead>"
print >>f, "<tbody>"


for server in servers:
	# x_server = java.lang.String(server);
	x_server = stripMBeanValue(server, 'JTA_RuntimeSource');
	jtaRuntime = server.getJTARuntime();		
	v_ActiveTransactionsTotalCount = jtaRuntime.getActiveTransactionsTotalCount();
	v_TransactionAbandonedTotalCount = jtaRuntime.getTransactionAbandonedTotalCount();
	v_TransactionCommittedTotalCount = jtaRuntime.getTransactionCommittedTotalCount();
	v_TransactionTotalCount = jtaRuntime.getTransactionTotalCount();
		
	print >>f, "<tr>";
	print >>f, "<td>";
	print >>f, x_server[1];
	print >>f, "</td>";
		
	print >>f, "<td>";
	print >>f, v_ActiveTransactionsTotalCount;
	print >>f, "</td>";
		
	print >>f, "<td>";
	print >>f, v_TransactionAbandonedTotalCount;
	print >>f, "</td>";
		
	print >>f, "<td>";
	print >>f, v_TransactionCommittedTotalCount;
	print >>f, "</td>";
		
	print >>f, "<td>";
	print >>f, v_TransactionTotalCount;
	print >>f, "</td>";
		
	print >>f, "</tr>";
	
print >>f, "</tbody></table>"
print >>f, "<p></p>"		


# End of JTAPanel
print >>f, "</div>"



print >>f, "</div>"


print >>f, "</div>"
print >>f, "</div>"

# This piece of javascript enabled the Tabs to work
print >>f, "<script type=\"text/javascript\">"
print >>f, "var TabbedPanels001 = new Spry.Widget.TabbedPanels(\"TabbedPanels001\");"
print >>f, "</script>"

print >>f, "</body>"
print >>f, "</html>"

# CLOSE output file, program end

print ""
print "++++++++++++++++++++++++++"
print "Script end, closing output file, disconnect from Admin Server and exiting WLST session"
print "++++++++++++++++++++++++++"
print ""

f.close();
disconnect();
exit();



	


