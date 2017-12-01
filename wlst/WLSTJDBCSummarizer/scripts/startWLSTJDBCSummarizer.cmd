@ECHO ON

@REM Change the environment variables below to suit your target environment
@REM The WLST_OUTPUT_PATH and WLST_OUTPUT_FILE environment variables in this script 
@REM determine the output directory and file of the script
@REM The WLST_OUTPUT_PATH directory value must have a trailing slash. If there is no trailing slash 
@REM script will error and not continue.


SETLOCAL

set WL_HOME=C:\Oracle\MW11gR1\wlserver_10.3
set DOMAIN_HOME=C:\Oracle\MW11gR1\user_projects\domains\WT_Domain
set WLST_OUTPUT_PATH=C:\WLST\WLSTJDBCSummarizer\output\
set WLST_OUTPUT_FILE=WLST_JDBC_Summary_Via_MBeans.html

call "%WL_HOME%\common\bin\wlst.cmd" WLS_JDBC_Summary_Online.py



pause

ENDLOCAL