from bs4 import BeautifulSoup
import requests,json,os,random,time
from pprint import pprint

url = "https://www.imdb.com/india/top-rated-indian-movies/"

page = requests.get(url)
soup = BeautifulSoup(page.text,"html.parser")

movie_names = []
movie_ranks =[]
ratings = []
movie_urls =[]
years = []
def scrape_top_list():
    main_div = soup.find("div",class_="lister")
    tbody = main_div.find("tbody",class_="lister-list")
    trs = tbody.find_all("tr")

    for tr in trs:
        position = tr.find("td",class_="titleColumn").get_text().strip()
        rank = ""
        for i in position:
            if "." not in i:
                rank += i
            else:
                break

        movie_ranks.append(rank)
        title = tr.find("td",class_="titleColumn").a.get_text()
        movie_names.append(title)
        year = tr.find("td",class_="titleColumn").span.get_text()
        years.append(year)
        imdb_rating = tr.find("td",class_="ratingColumn imdbRating").strong.get_text()
        ratings.append(imdb_rating)
        link = tr.find("td",class_="titleColumn").a["href"]
        movie_link = "https://www.imdb.com"+ link
        movie_urls.append(movie_link)

    Top_movies = []
    for i in range(0,len(ratings)):
        details = {"name" : "","position" : "","year" : "","rating" : "","url" : ""}

        details["name"] = str(movie_names[i])
        details["position"] = int(movie_ranks[i])
        details["rating"] = float(ratings[i])
        years[i] = years[i][1:5]
        details["year"] = int(years[i])
        details["url"] = movie_urls[i]
        Top_movies.append(details)
    return(Top_movies)
scraping = scrape_top_list()
# print(scraping)

def group_by_year(movies):
    years = []
    for i in movies:
        year = i["year"]
        if year not in years:
            years.append(year)
    movie_dic = {i:[]for i in years}
    for i in movies:
        name = i
        year = i["year"]
        for j in movie_dic:
            if str(j)== str(year):
                movie_dic[j].append(name)
    return (movie_dic)
dec_arg = (group_by_year(scraping))
# print(dec_arg)

def group_by_year(movies):
    list = []
    movie_dict = {}
    for i in movies:
        mod  = i%10
        decade = i-mod
        if  decade not in list:
            list.append(decade)
    for i in list:
        movie_dict[i]=[]
    for i in movie_dict:
        dec10 = i+9
        for x in movies:

            if x <= dec10 and x>=i:
                for j in movies[x]:
                    movie_dict[i].append(j)
    return movie_dict


# print(group_by_year(dec_arg))




def scrape_movie_details(movie_url):
    movie_id = ""
    random_sleep = random.randint(1,3)
    for _id in movie_url[27:]:
        if "/" not in _id:
            movie_id += _id
        else:
            break
    file_name = movie_id +".json"

    # text = None
    if os.path.exists(file_name):
        # print("hello")
        with open(file_name,"r") as f:
            text = json.load(f)
        return text
    # if text is None:

    else:
        time.sleep(random_sleep)
        # print("sorry")
        page = requests.get(movie_url)
        soup = BeautifulSoup(page.text,"html.parser")
        title_div = soup.find("div",class_="title_wrapper").h1.get_text()
        movie_name = ""
        for i in title_div:
            if "(" not in i:
                movie_name = (movie_name + i).strip()
            else:
                break
        # print(movie_name)
        sub_div = soup.find("div",class_="subtext")
        runtime = sub_div.find("time").get_text().strip()
        runtime_hours = int(runtime[0])*60
        if "min" in runtime:
            runtime_minutes = int(runtime[3:].strip("min"))
            movie_runtime = runtime_hours + runtime_minutes
        else:
            movie_runtime = runtime_hours
        # print(movie_runtime)
        gener = sub_div.find_all("a")
        gener.pop()
        movie_gener = [i.get_text() for i in gener]
        # print(movie_gener)
        sumery = soup.find("div",class_="plot_summary")
        movie_bio = sumery.find("div",class_="summary_text").get_text().strip()
        # print(movie_bio)
        director = sumery.find("div",class_="credit_summary_item")
        director_list = director.find_all("a")
        movie_director = [i.get_text().strip() for i in director_list]
        # pri-nt(movie_director)
        extra_details = soup.find("div",attrs={"class":"article","id":"titleDetails"})
        list_of_divs = extra_details.find_all("div")
        for div in list_of_divs:
            tag_h4 = div.find_all("h4")
            for text in tag_h4:
                if 'Language:' in text:
                    tag_ancheor = div.find_all("a")
                    movie_language = [language.get_text() for language in tag_ancheor]
                elif 'Country:' in text:
                    tag_ancheor = div.find_all("a")
                    movie_country = ''.join([contry.get_text() for contry in tag_ancheor])
        See_more = soup.find("div",attrs={'class':'article','id':'titleCast'})
        more = See_more.find('div',class_="see-more").a['href']

        see_all_cast = movie_url + more

        def scrape_movie_cast(cast_url):
            page = requests.get(cast_url)
            soup = BeautifulSoup(page.text,"html.parser")
            table_data = soup.find("table",class_="cast_list")
            actors = table_data.findAll("td",class_= "")
            all_cast_list = []
            for actor in actors:
                All_cast_dict = {}
                imdb_id = actor.find("a").get("href")[6:15]
                All_cast_dict["imdb_id"] = imdb_id
                main_actor = actor.get_text().strip()
                All_cast_dict["actor_name"] = main_actor
                all_cast_list.append(All_cast_dict)

            return all_cast_list
        cast_all = scrape_movie_cast(see_all_cast)
        # print(more)                # elif "Runtime:" in text:
                #     movie_runtime = div.find("time").get_text()
        # print(movie_runtime)

        # print(type(movie_country))
        # print(type(movie_language))
        movie_poster_link = soup.find("div",class_="poster").a["href"]
        movie_poster = "https://www.imdb.com" + movie_poster_link
        # print(movie_poster)
        movie_details_dict = {'Name':'','Derector':'','Runtime':'','Gener':'','Bio':'','Language':'','Country':'','Poster_image_url':'',' Cast':''}

        movie_details_dict['Name'] = movie_name
        movie_details_dict['Director'] = movie_director
        movie_details_dict['Runtime'] = movie_runtime
        movie_details_dict['Gener'] = movie_gener
        movie_details_dict['Bio'] = movie_bio
        movie_details_dict['Language'] = movie_language
        movie_details_dict['Country'] = movie_country
        movie_details_dict['Poster_image_url'] = movie_poster
        movie_details_dict[' Cast'] = cast_all


        with open(file_name,"w") as file1:
            raw = json.dump(movie_details_dict,file1)

        return movie_details_dict


for i in scraping:
    url1 = i["url"]
    movies_details = scrape_movie_details(url1)
    pprint(movies_details)




def get_movie_list_details(movies_list):
    new_list = []
    count = 0
    for i in range(len(movies_list)):
        url1 = movies_list[i]["url"]
        movies_details = scrape_movie_details(url1)
        new_list.append(movies_details)
        # count += 1
        # if count == 9:
        #     break
    return new_list

# all_movie_detail = (get_movie_list_details(scraping))

# def analyse_movies_language(movies_list):
#     language_dic = {}
#     sample_list = []
#     for i in movies_list:
#         sample_list.append(i["Language"])
#     new_list =[]
#     for j in sample_list:
#         for x in j:
#             new_list.append(x)
#     language_dic = {}
#
#     for lang in new_list:
#         if lang not in language_dic:
#             language_dic[lang] = 1
#         else:
#             language_dic[lang] +=1
#     return(language_dic)
#
#
# # movies_language_analyse =  (analyse_movies_language(movie_detail))
# # pprint (movies_language_analyse)
#
# def analyse_movies_directors(movies_list):
#     director_dic = {}
#     sample_list = []
#     for i in movies_list:
#         sample_list.append(i["Director"])
#     new_list =[]
#     for j in sample_list:
#         for x in j:
#             new_list.append(x)
#     director_dic = {}
#
#     for lang in new_list:
#         if lang not in director_dic:
#             director_dic[lang] = 1
#         else:
#             director_dic[lang] +=1
#     return(director_dic)
# # movies_director_analyse =  (analyse_movies_directors(movie_detail))
# # pprint (movies_director_analyse)


def analyse_movies_language_and_director(movies_list):
    director_dic = {}
    for movie in movies_list:
        for directors in movie["Director"]:
            director_dic[directors] = {}
    for i in range(len(movies_list)):
        for director in director_dic:
            if director in movies_list[i]["Director"]:
                for language in movies_list[i]["Language"]:
                    director_dic[director][language] = 0
    for x in range(len(movies_list)):
        for direc in director_dic:
            if direc in movies_list[x]["Director"]:
                for language in movies_list[x]["Language"]:
                    director_dic[direc][language] += 1
    return director_dic


# directors_by_language = analyse_movies_language_and_director(all_movie_detail)
# print(directors_by_language)

def analyse_movies_gener(movies_list):
    gener_list = []
    for movie in movies_list:
        gener = movie["Gener"]
        for i in gener:
            if i not in gener_list:
                gener_list.append(i)
    analyse_gener = {gener_type : 0 for gener_type in gener_list}
    for gener_type in gener_list:
        for movie in movies_list:
            if gener_type in movie["Gener"]:
                analyse_gener[gener_type] += 1
    return analyse_gener

# gener_analysis = analyse_movies_gener(all_movie_detail)
# print(gener_analysis)
