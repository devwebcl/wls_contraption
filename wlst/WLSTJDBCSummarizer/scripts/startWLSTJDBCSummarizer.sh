#!/bin/sh

#Change the environment variables below to suit your target environment
#The WLST_OUTPUT_PATH and WLST_OUTPUT_FILE environment variables in this script 
#determine the output directory and file of the script
#The WLST_OUTPUT_PATH directory value must have a trailing slash. If there is no trailing slash 
#script will error and not continue.

WL_HOME=/oracle/middleware/wlserver_10.3
DOMAIN_HOME=/oracle/middleware/user_projects/domains/MyDomain; export DOMAIN_HOME
WLST_OUTPUT_PATH=/oracle/WLSTDomainSummarizer/output/; export WLST_OUTPUT_PATH
WLST_OUTPUT_FILE=WLST_JDBC_Summary_Via_MBeans.html; export WLST_OUTPUT_FILE

${WL_HOME}/common/bin/wlst.sh WLS_JDBC_Summary_Online.py
