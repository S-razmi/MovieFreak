from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup
import os.path
#takes The name of the Movie from the user
movie_name=str(input("Enter The Name Of The Movie:"))
# movie_name="The Fight Club"
#Convert it to a google url format
movie_name_split=movie_name.split(' ')
search_phrase=''
for i in range(len(movie_name_split)):
    search_phrase=search_phrase+'+'+movie_name_split[i]
search_phrase=search_phrase[1:]
google_url="https://www.google.com/search?q=%s" %search_phrase
#scraps the info from google using urllib
req =Request(google_url,data=None, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
search_result=urlopen(req)
search_html=search_result.read()
search_result.close()
search_soup=soup(search_html, "html.parser")
# finds the rating out of the google info
ratings=search_soup.find("div" ,{"class":'yQ8hqd ksSzJd w6Utff'})
website=ratings.findAll("a")
# Now we search and store the scores
scores={}
for web in website:
    score={}
    score["Title"]=web.find("span",{"class":"wDgjf"}).text
    score["score"]=web.find("span", {"gsrt IZACzd"}).text
    score["URL"]=web["href"]

    scores[score["Title"]]=score["score"]
print(scores)
# shows the summry of the story
plot=search_soup.find("div" ,{"class":'SALvLe farUxc mJ2Mod'})
plot=plot.find("span")
plot = plot.text
def remove_end(thestring, ending):
    # this function removes the unnecessary MORE word at the ending
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring

plot = remove_end(plot, '… MORE')
print(plot)
# shows the Movie Information
movie_director=search_soup.find("div" ,{"data-attrid":'kc:/film/film:director'})
director=movie_director.find("span" ,{"class":"LrzXr kno-fv"}).text
print (director)
movie_info=search_soup.find("div" ,{"class":'Ftghae iirjIb'})
info=movie_info.find("div" ,{"class":"SPZz6b"})
info=info.find("div" , {"class":"wwUB2c kno-fb-ctx"}).text
info=info.split(" ‧ ")
info_year=info[0]
info_genre=info[1]
info_length=info[2]
# Creates a file for storing the data as csv file
filename = "MovieFreak.csv"

if not os.path.isfile("MovieFreak.csv"):
    headers = "name, year, genre, length, director, imdbscore, rottenscore, metascore, plot\n"
    file = open(filename, "w")
    file.write(headers)
    file.close()
else:
    # before writing the plot to the file first we should remove the commas contained in the text
    plot = plot.replace(",", "|")
    file = open(filename, "a+")
    file.write(movie_name + "," + info_year + "," + info_genre + "," + info_genre + "," + director + "," + scores[
        "IMDb"] + "," + scores["Rotten Tomatoes"] + "," + scores["Metacritic"] + "," + plot + "\n")

    file.close()