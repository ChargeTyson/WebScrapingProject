from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib.parse
import time

pageNum = 9300

baseTempURL = 'https://myanimelist.net/anime.php?cat=0&q=&type=0&score=0&status=2&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c[0]=a&c[1]=b&c[2]=c&c[3]=f&gx=0&o=3&w=1'

baseURL = baseTempURL + "&show=" + str(pageNum)

# opening up connection
baseClient = uReq(baseURL)
pageHTML = baseClient.read()
baseClient.close()

pageSoup = soup(pageHTML, "html.parser")

containers = pageSoup.findAll("a", {"class":"hoverinfo_trigger fw-b fl-l"})

filename = "Anime Desctriptions Part 4.txt"
f = open(filename, "w", encoding='utf-8', errors='ignore')



keepGoing = True

while keepGoing:

	for container in containers:

		#loads the anime's webpage on MAL
		anime_url = container["href"]
		anime_url = urllib.parse.urlsplit(anime_url)
		anime_url = list(anime_url)
		anime_url[2] = urllib.parse.quote(anime_url[2])
		anime_url = urllib.parse.urlunsplit(anime_url)

		animeClient = uReq(anime_url)
		animeHTML = animeClient.read()
		animeClient.close()
		animePageSoup = soup(animeHTML, "html.parser")

		#finds the title of the anime
		title =(container.text).encode("utf-8")
		title = str(title).replace("'", "")
		title = title[1:]

		#finds the table for the information
		data = animePageSoup.find("td")

		#this is the score
		score = data.find("span", string="Score:").find_next_sibling().text
		if score == "N/A":
			keepGoing = False
		else:
			description = (animePageSoup.find("p", {"itemprop":"description"}).text)
			print(title)

			# this is the anime type (TV, Movie, etc.)
			if "Music" in data.find("span", string ="Type:").find_parent().text:
				animeType = "Music"
			else:
				animeType = data.find("span", string="Type:").find_next_sibling().text


			if animeType == "TV" or animeType == "Movie" or animeType == "ONA":
				f.write(description)
				f.write("\n")
				f.write("<|endoftext|>")
				f.write("\n")

	time.sleep(90)
	pageNum = pageNum + 50
	baseURL = baseURL + "&show=" + str(pageNum)

	# opening up connection
	baseClient = uReq(baseURL)
	pageHTML = baseClient.read()
	baseClient.close()

	pageSoup = soup(pageHTML, "html.parser")

	containers = pageSoup.findAll("a", {"class":"hoverinfo_trigger fw-b fl-l"})

f.close()