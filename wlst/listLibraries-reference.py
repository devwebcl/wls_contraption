"""
---------------------------------------------------------------------------------------------------
Script  : ListLibraries.py
Author  : Mark Piller
Date    : 2015-01-06
Purpose : Create 2 separate files > 
          1) list of libraries in the targeted WebLogic server
          2) List of applications in the targeted server

run this with > java weblogic.WLST ListLibraries.py
or by execfile('<drive>:<directory>/ListLibraries.py') when in the WLST command prompt
---------------------------------------------------------------------------------------------------
"""

import java.io as javaio 



"""
---------------------------------------------------------------------
Global Variables
---------------------------------------------------------------------
"""
username = 'weblogic'
password = 'welcome1'

# tiene que ser URL de algun Managed Server
URL = 't3://127.0.0.1:7001'


outputDir = '/Users/German/tmp'

# get the date to add to the file name
from datetime import date
today = date.today()
filedate = today.isoformat()

# libraries output saved to this file
libraryOutputFile = outputDir + "/" + "libraries-in-wls-" + filedate + ".txt"
libraryOutputFileWriter=javaio.FileWriter(libraryOutputFile)

# applications output saved to this file
appOutputFile = outputDir + "/" + "app-deployments-in-wls-" + filedate + ".txt"
appOutputFileWriter=javaio.FileWriter(appOutputFile)


"""
---------------------------------------------------------------------
Function to find the libraries
---------------------------------------------------------------------
"""
def getLibraryListing(mbeanPosition):
  cd(mbeanPosition)
  libraryListing = ls('c', returnMap='true')
  print(libraryListing.size())

  if libraryListing.size() > 0 :
    # print file headings

    libraryOutputFileWriter.write("Library Listing " + filedate)
    libraryOutputFileWriter.write(System.getProperty("line.separator"))
    libraryOutputFileWriter.write(System.getProperty("line.separator"))

    libraryOutputFileWriter.write("Domain    : " + domainName)
    libraryOutputFileWriter.write(System.getProperty("line.separator"))

    libraryOutputFileWriter.write("Server    : " + serverName)
    libraryOutputFileWriter.write(System.getProperty("line.separator"))

    libraryOutputFileWriter.write("MBean path: " + pwd())
    libraryOutputFileWriter.write(System.getProperty("line.separator"))
    libraryOutputFileWriter.write(System.getProperty("line.separator"))

    libraryOutputFileWriter.write("Libary\tVersion\tServer(s) Deployed To")
    libraryOutputFileWriter.write(System.getProperty("line.separator"))

    libraryOutputFileWriter.write("-------\t-------\t-----------------------------")
    libraryOutputFileWriter.write(System.getProperty("line.separator"))

    for library in libraryListing :

      #mio:
      #cd('ReferencingRuntimes')
      #ls()
      #cd('..')


      # separate the library name from the version number
      libraryArray = library.split('#')
      myoutput = ""

      itemCount = 0
      for libraryItem in libraryArray :
        itemCount = itemCount + 1
        # item 1 is Library Name
        # item 2 - if exists - is Library Version
        if itemCount > 1:
          myoutput = myoutput + "\t"
        myoutput = myoutput + libraryItem

      # if a library version is not included then add a tab character
      if itemCount < 2:
        myoutput = myoutput + "\t"

      # identify the servers that the library is deployed to
      serverArray = getTargetServers(library)
      srvrCnt = 0
      myoutput = myoutput + "\t"
      for srvrNm in serverArray :
        srvrCnt = srvrCnt + 1
        myoutput = myoutput + srvrNm
        if srvrCnt < len(serverArray) :
          myoutput = myoutput + ', '
        
      # print to the file
      libraryOutputFileWriter.write(myoutput)
      libraryOutputFileWriter.write(System.getProperty("line.separator"))
      
  return


"""
---------------------------------------------------------------------
Function to find the servers deployed to
---------------------------------------------------------------------
"""
def getTargetServers(childNodeName):
  serverArray = []
  cd(childNodeName)
  childNodeListing = ls(returnMap='true',returnType='c')
  if childNodeListing.size() > 0 :
    for childNode in childNodeListing :
      if childNode == 'Targets' :
        cd('Targets')
        serverNames = ls(returnMap='true',returnType='c')
        if serverNames.size() > 0 :
          for srvrNm in serverNames :
            serverArray.append(srvrNm)
        # navigate to parent of Targets node
        cd('..')
  # navigate back to parent attribute
  cd('..')
  return serverArray



"""
---------------------------------------------------------------------
Main Routine
---------------------------------------------------------------------
"""
try:
  try:
    connect(username, password, URL)
    serverRuntime()
    getLibraryListing('/LibraryRuntimes')
   
  except Exception, e:
    print 'Unable to print libraries and applications'
    print e
finally:
  disconnect()
  libraryOutputFileWriter.close()
  appOutputFileWriter.close()

