from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib.parse
import time

baseURL = 'https://myanimelist.net/anime.php?cat=0&q=&type=0&score=0&status=2&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c%5B0%5D=a&c%5B1%5D=b&c%5B2%5D=c&c%5B3%5D=f&gx=0&o=3&w=1'

# opening up connection
baseClient = uReq(baseURL)
pageHTML = baseClient.read()
baseClient.close()

pageSoup = soup(pageHTML, "html.parser")

containers = pageSoup.findAll("a", {"class":"hoverinfo_trigger fw-b fl-l"})

filename = "How Long To Watch Every Anime.csv"
f = open(filename, "w")

pageNum = 50

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
		title = title.replace(",", "|")

		#finds the table for the information
		data = animePageSoup.find("td")

		# this is the anime type (TV, Movie, etc.)
		if "Music" in data.find("span", string ="Type:").find_parent().text:
			animeType = "Music"
		else:
			animeType = data.find("span", string="Type:").find_next_sibling().text

		#this is the number of episodes
		numEpisodes = [int(s) for s in (data.find("span", string="Episodes:").find_parent().text).split() if s.isdigit()]

		#check is finished
		airing = data.find("span", string="Status:").find_parent().text
		finished = False
		if 'Finished Airing' in airing:
			finished = True

		#Genre List
		genreFinder = data.find("span", string="Genres:").find_parent().findAll("a")
		genreList = []
		for genres in range(len(genreFinder)):
			genreList.append(genreFinder[genres].text)
		genreString = ' '.join(map(str, genreList))

		#this is the time per episode
		timePerEpisode = []
		if "Unknown" in data.find("span", string="Duration:").find_parent().text:
			timePerEpisode.append(0)
		elif "hr" in data.find("span", string="Duration:").find_parent().text:
			timePerEpisode = [int(times) for times in (data.find("span", string="Duration:").find_parent().text).split() if times.isdigit()]
			timePerEpisode.append(0)
			timePerEpisode[0] = (timePerEpisode[0] * 60) + (timePerEpisode[1])
		else:
			timePerEpisode = [int(times) for times in (data.find("span", string="Duration:").find_parent().text).split() if times.isdigit()]

		#this is the score
		score = data.find("span", string="Score:").find_next_sibling().text
		if score == "N/A":
			keepGoing = False
		else:
			print("Title: " + title)
			print("Type: " + animeType)
			print("Number of Episodes: " + str(numEpisodes[0]))
			print("Finished Airing: " + str(finished))
			print("Genres: " + genreString)
			print("Time Per Episode: " + str(timePerEpisode[0]))
			print("Score: " + score)
			print("\n")

			importString = (title + "," + animeType + "," + str(numEpisodes[0]) + "," + str(finished) + "," + genreString + "," + str(timePerEpisode[0])+ "," + score + "\n")
			f.write(importString)

	time.sleep(90)
	baseURL = baseURL + "&show=" + str(pageNum)
	pageNum = pageNum + 50

	# opening up connection
	baseClient = uReq(baseURL)
	pageHTML = baseClient.read()
	baseClient.close()

	pageSoup = soup(pageHTML, "html.parser")

	containers = pageSoup.findAll("a", {"class":"hoverinfo_trigger fw-b fl-l"})

f.close()