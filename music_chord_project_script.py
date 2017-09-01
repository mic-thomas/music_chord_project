# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 19:35:55 2017

webscraping guitar chords

@author: michael.gramlich
"""

# 1. Define libraries

import urllib
import bs4
import re
import datetime
import string

# 2. get the URL

sementara_sendiri = urllib.request.urlopen("https://tabs.ultimate-guitar.com/g/geisha/sementara_sendiri_crd.htm")

from urllib.request import urlopen
sementara_sendiri_3 = urlopen("https://tabs.ultimate-guitar.com/g/geisha/sementara_sendiri_crd.htm") 
print(sementara_sendiri_3)

# 3. select the relevant stuff from it with beautiful soup

soup = bs4.BeautifulSoup(sementara_sendiri_3)

print(soup.prettify()) # look at nested structure of html

# 4. get the body (chords and lyrics) that are in tag <tb_ct>

# tb_ct_content = soup.find_all("pre", {"class":"js-tab-content js-copy-content js-tab-controls-item"}) # apparently this doesnt work anymore, try below code (30.08.2017)
tb_ct_content = soup.find_all("pre", {"class":"js-tab-content js-init-edit-form js-copy-content js-tab-controls-item"}) # distills the important stuff better


tb_ct_content_string = str(tb_ct_content)

# 5. isolate the chords

chord_list = re.findall('<span>(.*)</span>', tb_ct_content_string)
chord_list_2 = [re.sub("<span>", "", line) for line in chord_list]
chord_list_3 = [re.sub("</span>", "", line) for line in chord_list_2]



# Looping thorugh all of the songs --> For that one needs three nested loops
# WRONG: Get all the page names by crawling thorugh the 

# for i in {A-Z} https://www.ultimate-guitar.com/bands/{i}.htm



# 6. Get a list with all artists out there

from urllib.request import urlopen
d={} # create an empty dictionary
for letter in string.ascii_lowercase: # string.ascii_lowercase gives you all lower case letters in the alphabet    
    d["artist_page_" + letter] = [] # You are creating a dictionary with key {artist_page_<laufvariable>: NULL}, e.g. artist_page_a, artist_page_b
    print("We are at letter:" + letter)
    for page_count in range(1,300): # for every artist_page_<letter> you are opening up artist_page_<letter>_<page_number> and perform operations
            
    
        # if urlopen("https://www.ultimate-guitar.com/bands/"+ str(letter) + str(page_count)+".htm")  --> How to include if statement to only execute this if it exists?
        placeholder = urlopen("https://www.ultimate-guitar.com/bands/"+ str(letter) + str(page_count)+".htm")
        
        soup = bs4.BeautifulSoup(placeholder) # get file    
        artist_list = soup.find_all("tr", {"class":"tr"}) # Extract the relevant part
        artist_list_raw = soup.find_all("td", {"style":"color:#DDDDCC"}) # within the part try to only get the links --> All of them all in color:#DDD.. style
        artist_list_raw_str = str(artist_list_raw) # convert to string to substring stuff --> It splits elemtns by <space>
        artist_list_raw_list = artist_list_raw_str.split() # split up the string into a list of substrings
        
        from fnmatch import fnmatch, fnmatchcase
        artist_list_temp = [x for x in artist_list_raw_list if fnmatch(x, "href=*")]
        artist_list_temp_2 = [re.sub("href=\"", "", line) for line in artist_list_temp]
        artist_list_temp_3 = [re.sub("\">A", "", line) for line in artist_list_temp_2]
        d["artist_page_" + letter].append(artist_list_temp_3)
        print(str(datetime.datetime.now()) + "Within letter " + letter + " this is page number: "+ str(page_count))


''' 
stopped here 30.08.2017 --> 

FIRST SOLVE LINE 76 --> append new values, how to integrate that in loop?

loop over all of the artist_list_ to get all the songs if there are chords
'''    





'''
safety copy

from urllib.request import urlopen
a_artists_page = urlopen("https://www.ultimate-guitar.com/bands/a.htm")
print(a_artists_page)

soup = bs4.BeautifulSoup(a_artists_page)

print(soup.prettify()) # look at nested structure of html

artist_list = soup.find_all("tr", {"class":"tr"}) # Extract the relevant part
artist_list_raw = soup.find_all("td", {"style":"color:#DDDDCC"}) # within the part try to only get the links --> All of them all in color:#DDD.. style
artist_list_raw_str = str(artist_list_raw) # convert to string to substring stuff --> It splits elemtns by <space>
artist_list_raw_list = artist_list_raw_str.split() # split up the string into a list of substrings

from fnmatch import fnmatch, fnmatchcase
artist_list_temp = [x for x in artist_list_raw_list if fnmatch(x, "href=*")]
artist_list_temp_2 = [re.sub("href=\"", "", line) for line in artist_list_temp]
artist_list_temp_3 = [re.sub("\">A", "", line) for line in artist_list_temp_2]
artist_list_final = artist_list_temp_3
'''




'''
- - - - Stopped here - - - -

Next steps:
    - create a loop to crawl ALL songs on ultimate-guitar
    - Think of what to do with the data --> Predict next chord, simple statistics, association analysis, etc
    - identify what model to use for that
    - continue data prep and bring the data in the required form

Goal: 

	1. Descriptive statistics
		i) Ranking what chords are used most often
		ii) Ranking what chord prgoressions are most often played
		iii)
	2. Analytics
		i) What chord is played next?
		ii) Correlation between sentiment and chord progression or major/ minor chords

Challenges/ actions/ to do´s

	- Crawl through all songs
		- By alphabet
	- How to find the root --> to determine the progressions
	- Version issue (what if there are several versions)
	- Only take the chords sites, not the bass, tab pro, tabs kind of shit










# # # # # # # # # Spielwiese # # # # 

help(re.findall)

type(tb_ct_content_2)
type(test_6)
len(test_2)

print(soup.get_text())















# # # # # # # # # Archive # # # # 
 
tb_ct_content = soup.find_all("div", {"class":"tb_ct"}) # still contains heading and unnecessary stuff


test = re.sub("\n", "", tet)

test_2 = re.search('<span>(.*)</span>', test)

test_3 = str(test_2)


test_4 = re.compile('<span>(.*)</span>')

test_5 = test_4.search(tet)

if test_5:
    chords = test_5.group(1)
    
    
    
for line in test_6:
    test_7 = re.sub("<span> | </span>", "", line)
    #test_7 = re.sub("</span>", "", line)

