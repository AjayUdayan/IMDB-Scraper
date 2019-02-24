import requests 
from bs4 import BeautifulSoup
url = "https://www.imdb.com/india/top-rated-indian-movies/"
import pprint


# Task 1
def  scrape_top_list():
	url = "https://www.imdb.com/india/top-rated-indian-movies/"

	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	top_movies_list = []
	main_div = soup.find("div",class_ = "lister")

	tbody = main_div.find("tbody",class_ = "lister-list")
	trs = tbody.find_all("tr")
	# print(trs)
	for tr in trs:
		data=tr.find('td',class_='titleColumn')
		position = data.get_text().strip().split()
		
		name = data.find('a').get_text()
		year = data.find('span').get_text()
		movie_url = data.find('a').get('href')
		imdb_url = 'https://www.imdb.com' + movie_url
		movie_rating =  tr.find('td',class_="ratingColumn imdbRating").strong.get_text() 

		
		top_movies_dict = {'position':'','name':'','year':'','rating':'','url':''}
		top_movies_dict['position']= int(position[0].strip('.'))
		top_movies_dict['name']= name
		top_movies_dict['year']= int(year.strip('()'))
		top_movies_dict['rating'] = float(movie_rating)
		top_movies_dict['url']= imdb_url

		top_movies_list.append(top_movies_dict)
	return(top_movies_list)
	
top_movies = scrape_top_list()
# print(top_movies)



# Task 2
def group_by_year(movies_list): #Here movies is top_movies_list
	movie_by_year = {}
	for movie in movies_list:
		movie_by_year[movie['year']] = []
	for year_key in movie_by_year:
		for movie_ in movies_list:
			year = movie_['year']
			if year_key == year:
				movie_by_year[year_key].append(movie_)

	print(movie_by_year)

# group_by_year_analysis = group_by_year(top_movies)
# print(group_by_year_analysis)


# Task 3
 

def group_by_decade(movies_list):
	movie_by_decade = {}
	for movie in movies_list:
		
		division = movie['year'] // 10
		decade = division * 10
		movie_by_decade[decade] = []
	

	for decade_key in movie_by_decade:
		for movie_ in movies_list:
			_division = movie_['year'] // 10
			_decade = _division * 10
			if decade_key == _decade:
				movie_by_decade[decade_key].append(movie_)

	print(movie_by_decade)

# group_by_decade_analysis = group_by_decade(top_movies)
# print(group_by_decade_analysis)

# Task 4

def scrape_movie_details(movie_url):
	page = requests.get(movie_url)
	soup = BeautifulSoup(page.text,"html.parser")
	name = soup.find('div',class_= 'title_wrapper').h1.get_text().split()
	name.pop()
	movie_name = (''.join(name)).strip()

	movie_detail = soup.find('div',class_="plot_summary")
	movie_bio = movie_detail.find('div',class_='summary_text').get_text().strip()
	movie_directors =  movie_detail.find('div',class_='credit_summary_item')
	directors = movie_directors.find_all('a')
	directors_list = [director.get_text()for director in directors]
	poster_image_url=soup.find('div',class_='poster').a.img['src']
	movie_gener = soup.find('div',class_= 'title_wrapper')
	time_gener_div = movie_gener.find('div',class_= 'subtext')
	geners = time_gener_div.find_all('a')
	geners.pop()
	gener_list = [gener.get_text() for gener in geners]


	print(directors_list)

movie_details = scrape_movie_details(top_movies[0]['url'])
print(movie_details)



