'''Python package to crawl the publicly available forms filed with the Securities and Exchange Commission (SEC) 
    under the new Electronic Data Gathering, Analysis and Retrieval System (EDGAR).
    Copyright (C) 2013  Sreecharan Sankaranarayanan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
  
    Full License can be viewed at https://github.com/sreecharan93/FormCrawl/blob/master/LICENSE
    Contact : sreecharan93@gmail.com											'''




from bs4 import BeautifulSoup
import re
import requests
import os


# Procedure to retrieve the CIK codes with the entered SEC Code
sec = input("Enter the SEC Code : ")
count = 0 # Count for displaying 40 elements on the Company Search page
tddoc=[1] # Initialize to any non-empty list
companyList = []
while(len(tddoc)!=0):
	base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC="+str(sec)+"&owner=include&match=&start="+str(count)+"&count=40&hidefilings=0"
	r = requests.get(base_url)
	data = r.text
	soup = BeautifulSoup(data)
	tddoc = soup.find_all("td")
	for i in range(0,len(tddoc)):
		companyList.append(tddoc[i].string)
		i+=2
	count+=40
# `companyList` now contains the list of companies corresponding to the entered SEC code.
cikList = []
for i in range(0,len(companyList),3):
	cikList.append(companyList[i])
# List of CIK codes to be crawled has been extracted into `cikList`

# Below procedure creates the required folders if they don't already exist.
if not os.path.exists("Crawled Data/"):
	os.makedirs("Crawled Data/")
if not os.path.exists("Crawled Data/"+str(sec)):
	os.makedirs("Crawled Data/"+str(sec))
for j in range(len(cikList)):
	if not os.path.exists("Crawled Data/"+str(sec)+"/"+str(cikList[j])):
		os.makedirs("Crawled Data/"+str(sec)+"/"+str(cikList[j]))

for i in range(len(cikList)):
	base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cikList[i])+"&type=10-K&dateb=&owner=exclude&output=xml&count=100"	
	r = requests.get(base_url)
	data = r.text
	soup = BeautifulSoup(data) # Initializing to crawl again
	linkList=[] # List of all links from the CIK page
	# If the link is .htm convert it to .html
	for link in soup.find_all('filinghref'):
		URL = link.string
		if link.string.split(".")[len(link.string.split("."))-1] == "htm":
			URL+="l"
    		linkList.append(URL)
	linkListFinal = linkList
	docList = [] # List of URL to the text documents
	docNameList = [] # List of document names

	for k in range(len(linkListFinal)):
		requiredURL = str(linkListFinal[k])[0:len(linkListFinal[k])-11]
		txtdoc = requiredURL+".txt"
		docname = txtdoc.split("/")[len(txtdoc.split("/"))-1]
		docList.append(txtdoc)
		docNameList.append(docname)
	# Save every text document into its respective folder
	for j in range(len(docList)):
		base_url = docList[j]
		r = requests.get(base_url)
		data = r.text
		path = "Crawled Data/"+str(sec)+"/"+str(cikList[i])+"/"+str(docNameList[j])
		filename = open(path,"a")
		filename.write(data)
