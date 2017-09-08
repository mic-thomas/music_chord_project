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
import sys
import pandas as pd

# 2. Define functions

# Function to extract chords from a website
# Input: A URL with chords of a song from Ultimate Guitar 
# Output: The chords of the song as a Python list
def extract_chords (url):
    final_chord_list = []
    # extract artist and song name
    temp_artist = re.sub("https://tabs.ultimate-guitar.com/./", "", url)
    temp_artist = re.sub(".htm", "", temp_artist)
    #final_chord_list = re.split("/", temp_artist)[0]
    #final_chord_list[1] = re.split("/", temp_artist)[1]
    #final_chord_list.extend(re.split("/", temp_artist)[0])
    #final_chord_list.extend(re.split("/", temp_artist)[1])
    from urllib.request import urlopen
    song_url = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(song_url)
    content = soup.find_all("pre", {"class":"js-tab-content js-init-edit-form js-copy-content js-tab-controls-item"}) # distills the important stuff better
    content_str = str(content)
    # isolate the chords:
    temp_chords = re.findall('<span>(.*)</span>', content_str)
    temp_chords_2 = [re.sub("<span>", "", line) for line in temp_chords]
    temp_chords_3 = [re.sub("</span>", "", line) for line in temp_chords_2]
    # convert into a list of chords
    for i in range(0,len(temp_chords_3)):
        final_chord_list.extend(temp_chords_3[i].split())
    #final_chord_list = re.split("/", temp_artist)[0] + re.split("/", temp_artist)[1] + final_chord_list
    final_chord_list.insert(0, re.split("/", temp_artist)[1]) # include song name
    final_chord_list.insert(0, re.split("/", temp_artist)[0]) # include artist name
    return final_chord_list;

extract_chords("https://tabs.ultimate-guitar.com/g/g_love_special_sauce/free_at_last_crd.htm")

# 3. Get a list with all artists out there

from urllib.request import urlopen
d={} 
for letter in string.ascii_lowercase: # string.ascii_lowercase gives you all lower case letters in the alphabet    
    d["artist_page_" + letter] = [] # You are creating a dictionary entry with key {artist_page_<index>: NULL}, e.g. artist_page_a, artist_page_b
    print("We are at letter:" + letter)
    for page_count in range(0,3): # for every artist_page_<letter> you are opening up artist_page_<letter>_<page_number> and perform operations
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
        artist_list_temp_3 = [re.split("\">", line)[0] for line in artist_list_temp_2] # delete the sub string that comes after the ">
        d["artist_page_" + letter].extend(artist_list_temp_3)
        print(str(datetime.datetime.now()) + " Within letter " + letter + " this is page number: "+ str(page_count))
# Result: dictionary d that contains URL endings to all artist per letter

# convert the dictionay into a list
artist_list_urls = []
for x in string.ascii_lowercase:
    artist_list_urls.extend(d["artist_page_" + x])
    print ("The number of artists in the arti_list_urls is: " + str(len(artist_list_urls)))
# Results: List "artist_list" that contains URL endings to all artists

# 4. Loop through songs of a given artist and create data frame with chords
song_list = []
for artists in artist_list_urls:
    url = urlopen("https://www.ultimate-guitar.com"+artists) # open site of a given artist
    soup = bs4.BeautifulSoup(url) 
    temp_song_list = soup.find_all("tr", {"class":"tr__lg"}) # extract relevant information, i.e. links to songs
    temp_song_list_str = [str(x) for x in temp_song_list] # convert object to string to filter out unnecessary stuff
    temp_song_list_str_2 = [x for x in temp_song_list_str if "<b>Chords</b>" in x] #only take those songs, where chords are vailable (i.e. we dont want tabs or lyrics or bass tabs etc.)
    temp_song_list_str_3 = [re.split("href=\"", x)[-1] for x in temp_song_list_str_2] # filter out stuff
    temp_song_list_str_4 = [re.split("\">", x)[0] for x in temp_song_list_str_3] # filter out stuff to get clean html
    artist_name = re.sub("/tabs/", "", artists)
    artist_name = re.sub("_tabs.htm", "", artist_name)
    print ("Appending songs of: " + artist_name)
    song_list.extend(temp_song_list_str_4) # append the links of songs from the artist to the song list
    print ("The number of songs in the list is: " + str(len(song_list)))
# Result: song_list is the final list of webpages to get the chords from     



# 5. Apply function to extract chords for every song and put it in a data frame
chord_list = []
for song in song_list:
    chord_list.append(extract_chords(song))
    print ("Appending song: " + str(song))
df_chords = pd.DataFrame(chord_list)

df_chords[5].value_counts()




  





'''


Archive/ safety copies



# 2. get the URL

sementara_sendiri = urllib.request.urlopen("https://tabs.ultimate-guitar.com/g/geisha/sementara_sendiri_crd.htm")

from urllib.request import urlopen
sementara_sendiri_3 = urlopen("https://tabs.ultimate-guitar.com/g/geisha/sementara_sendiri_crd.htm") 
# print(sementara_sendiri_3)

# 3. select the relevant stuff from it with beautiful soup

soup = bs4.BeautifulSoup(sementara_sendiri_3)

#print(soup.prettify()) # look at nested structure of html

# 4. get the body (chords and lyrics) that are in tag <tb_ct>

# tb_ct_content = soup.find_all("pre", {"class":"js-tab-content js-copy-content js-tab-controls-item"}) # apparently this doesnt work anymore, try below code (30.08.2017)
tb_ct_content = soup.find_all("pre", {"class":"js-tab-content js-init-edit-form js-copy-content js-tab-controls-item"}) # distills the important stuff better


tb_ct_content_string = str(tb_ct_content)

# 5. isolate the chords

chord_list = re.findall('<span>(.*)</span>', tb_ct_content_string)
chord_list_2 = [re.sub("<span>", "", line) for line in chord_list]
chord_list_3 = [re.sub("</span>", "", line) for line in chord_list_2]

# convert into a list of chords
final_chord_list = []
for i in range(0,len(chord_list_4)):
    #chord_list_4 = [re.sub("  ", " ", line) for line in chord_list_4]
    final_chord_list.extend(chord_list_3[i].split())








# This loop was necessary befre I knew extend command and used append which created a nested structure
artist_list_urls = []
for x in string.ascii_lowercase:
    d["artist_page_" + x]
    list_length_1 = len(d["artist_page_" + x])
    for y in range(0, list_length_1):
        if type(d["artist_page_" + x][y]) == str:
            artist_list_urls.append(d["artist_page_" + x][y])
        else:
            list_length_2 = len(d["artist_page_" + x][y])
            for z in range(0, list_length_2):
                if type(d["artist_page_" + x][y][z]) == str:
                    artist_list_urls.append(d["artist_page_" + x][y][z])
print ("The type of the object artist_list_urls is" + str(type(artist_list_urls)))
print ("The number of artists in the arti_list_urls is: " + str(len(artist_list_urls)))
# Results: List "artist_list" that contains URL endings to all artists


# Convert list of URLs into list of artists:
artist_list =[re.sub("/tabs/", "", x) for x in artist_list_urls]
artist_list =[re.sub("_tabs.htm", "", x) for x in artist_list]


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


# Pseudocode: 
# for every artists URL 
    # open the webpage and retrieve all song links where there are chords available
    
# Try with one webpage first

artist_songs_test = urlopen("https://www.ultimate-guitar.com/tabs/mac_demarco_tabs.htm")
soup = bs4.BeautifulSoup(artist_songs_test)
# print(soup.prettify())
song_list = soup.find_all("tr", {"class":"tr__lg"}) 
song_list_string= [str(x) for x in song_list ] # apply the functin str for every element in the list --> The results is a list of strings
test_2 = [x for x in song_list_string if "<b>Chords</b>" in x] # through out list elements, that do not contain <b>Chords</b>
test_3 = [re.split("href=\"", x)[-1] for x in test_2]
test_4 = [re.split("\">", x)[0] for x in test_3]
# The result of this --> test_4 is a list - partially of lists - that contain the links to songs. The next step is to merge possible lists within the list to get one big list with all the links.

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

