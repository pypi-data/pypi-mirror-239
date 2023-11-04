import subprocess
import sys
package_names=['requests','BeautifulSoup4','pandas','openpyxl','selenium','datetime','termcolor']
for package_name in package_names:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", package_name])
    except subprocess.CalledProcessError:
        print(f"Failed to install '{package_name}'. Please install it manually.")
        sys.exit(1)
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime



sys.stdout.reconfigure(encoding='utf-8')
class TopMoviesScraper:
    def __init__(self):
        self.headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}     
        self.movie_link=[]
        self.movie_name=[]
        self.all_video_link=[]
        self.all_photo_link=[]
        self.movie_poster_link=[]
        self.movie_year=[]
        self.movie_time=[]
        self.movie_rating=[]
        self.genre=[]
        self.short_description=[]
        self.how_many_people_rated=[]
        self.popularity_score=[]
        self.dirctor_name=[]
        self.writer_name=[]
        self.star=[]
        self.user_review=[]
        self.critic_viewers=[]
        self.meta_score=[]
        self.wins_and_nomination=[]
        self.oscar_link=[]
        self.top_cast_name_and_link=[]
        self.all_cast_crew_link=[]
        self.additional_desciption=[]
        self.more_like_movie_link=[]
        self.aspect_ratio=[]
        self.sound_mix_company=[]
        self.box_office=[]
        self.production_company=[]
        self.also_known_as=[]
        self.language=[]
        self.country_of_origin=[]
        self.release_date=[]
        self.faq_link=[]
        self.user_review_link=[]
        self.facts_and_link=[]

 
     
# #--------store genre______________
    def get_genre(self,soup1):
        genre_title=[]
        for gen in soup1.find_all('a',class_="ipc-chip ipc-chip--on-baseAlt"):
            genre=gen.find('span',class_="ipc-chip__text")
            if genre==None:
                genre_title=None
            else:
                genre_title.append(genre.text)
        self.genre.append(genre_title)

# #------store short description------
    def get_short_description(self,soup1):
        short_description_element=soup1.find('span',class_="sc-466bb6c-0 kJJttH")
        if short_description_element==None:
            short_description=None
        else:
            short_description=short_description_element.text
        self.short_description.append(short_description)
# #----  store how_many_people_rated______

    def get_how_many_people_rated(self,soup1):
        how_many_people_rated_element=soup1.find('div',class_="sc-bde20123-3 bjjENQ")
        if how_many_people_rated_element==None:
            how_many_people_rated=None
        else:
            how_many_people_rated=how_many_people_rated_element.text
        self.how_many_people_rated.append(how_many_people_rated)
# #-----store movie popularity score
    def get_movie_popularity_score(self,soup1):
        popularity_score_element=soup1.find('div',class_="sc-5f7fb5b4-1 bhuIgW")
        if popularity_score_element:
            popularity_score=popularity_score_element.text
        else:
            popularity_score=None
        self.popularity_score.append(popularity_score)
#--------store director 
    def get_director_name(self,soup1): 
        dir_name_element = soup1.find('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        if dir_name_element:
            dir_name = dir_name_element.text
        else:
            dir_name =None
        self.dirctor_name.append(dir_name)
# # #-------------store writer nam
    def get_writer_name(self,soup1):
        wri=soup1.find_all('li')
        wri_name=[]
        for i in wri:
            lir=i.find('a')
            if lir==None:
                pass
            else:
                if lir.text.startswith('Writer'):
                    nam=i.find_all('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                    for i in nam:
                        if i==None:
                            pass
                        else:
                            wri_name.append(i.text)
                    break
                else:
                    lir=i.find('span')
                    if lir==None:
                        pass
                    else:
                        if lir.text.startswith('Writer'):
                            nam=i.find_all('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                            for i in nam:
                                if i==None:
                                    pass
                                else:
                                    wri_name.append(i.text)
                            break

        max_writer_names = 5  # Assuming the maximum number of writers for any movie is 5, you can adjust this based on your data
        wri_name.extend([''] * (max_writer_names - len(wri_name)))
        self.writer_name.append(wri_name)
#--------store stars name________________
    def get_stars_name(self,soup1):
        st=soup1.find_all('div',class_="sc-bfec09a1-7 dpBDvu")
        star=[]
        for i in st:
            if i==None:
                star=None
            else:
                alt=i.find('a',class_="sc-bfec09a1-1 fUguci")
                if alt:
                    star.append(alt.text)
                else:
                    star=None
        self.star.append(star)
#store user_review___
    def User_review(self,soup1):
        section=soup1.find('section',attrs={'data-testid':'UserReviews'})
        numeric_value=None
        ffff=section.find('a',class_="ipc-title-link-wrapper").get('href')
        link="https://www.imdb.com"+ffff
        response1=requests.get(link,headers=self.headers)
        soup22=BeautifulSoup(response1.text,'html.parser')
        div=soup22.find('div',class_="header")
        input_string=div.find('span').text
        numeric_value=int(''.join(filter(str.isdigit, input_string)))
        self.user_review.append(numeric_value)

# store _______user views,critic reviews,metascore________
    def get_userviews_criticreviews_metascore(self,soup1):
        lis=[]
        a1=soup1.find_all('span',class_="three-Elements")
        for i in a1:
            score1=i.find('span',class_='score')
            if score1:
                lis.append(score1.text)
            else:
                lis.append('N/A')

        critic_viewers=None
        meta_score =None
        num=None
        if len(lis) >= 3:
            if lis[0]==None:
                pass
            
            else:
                pass
            if lis[1]==None:
                critic_viewers='N/A'
                self.critic_viewers.append(critic_viewers)
            else:
                critic_viewers =lis[1]
                self.critic_viewers.append(critic_viewers)
            if lis[2]==None:
                meta_score ='N/A'
                self.meta_score.append(meta_score)
            else:
                meta_score = lis[2]
                self.meta_score.append(meta_score)
        else:    
            critic_viewers='N/A'
            meta_score ='N/A'
            
            self.critic_viewers.append(critic_viewers)
            self.meta_score.append(meta_score)
# # store awards_and_nomination- {'wins	': <int>, 'nominations': <int>}
    def get_store_awards_and_nomination(self,soup1):
        a=soup1.find('span',class_="ipc-metadata-list-item__list-content-item")
        if a==None:
            wins=None
            nominations=None
        else:
            win_nom=a.text.split()
            wins=0
            nominations=0
            if len(win_nom) >= 4:
                try:
                    wins = int(win_nom[0])
                    nominations = int(win_nom[3])
                except ValueError:
                    pass
        dict={'wins':wins,'nominations':nominations}
        self.wins_and_nomination.append(dict)
# # #--------store oscar link
    def get_oscar_link(self,soup1):
        w=soup1.find_all('a',class_="ipc-metadata-list-item__label ipc-metadata-list-item__label--link")
        if w is not None:
            
            oscar_hub=None
            for k in w:
                if k is not None:
                    lin=k.get('href')
                    if 'awards' in lin:
                        oscar_hub="https://www.imdb.com"+lin
                    else:
                        pass
                else:
                    oscar_hub=None
            if oscar_hub is not None:
                responsep= requests.get(oscar_hub, headers=self.headers)
                soupp= BeautifulSoup(responsep.text, 'html.parser')
                oscar_data=soupp.find('a',class_="ipc-metadata-list-summary-item__t")
                link=oscar_data.get('href')
                oscar_link="https://www.imdb.com"+link
            else:
                oscar_link="N/A"
        else:
            oscar_link="N/A"
        self.oscar_link.append(oscar_link)
# # #_--------top_cast - {1:{'char_name':<href>,'original_name':<href>},2:{...},3:{...},...}
    def get_top_cast_name_and_link(self,soup1):
        top_cast_name_and_link={}
        count=0
        org_cast=soup1.find_all('a',class_="sc-bfec09a1-1 fUguci")
        char_cast=soup1.find_all('a',class_="sc-bfec09a1-2 sc-bfec09a1-3 iDdzXP gKnTQh title-cast-item__char")
        if org_cast and char_cast is not None: 
            for org, char in zip(org_cast, char_cast):
                org_name = org.text
                org_link = "https://www.imdb.com" + org.get('href')
                char_name = char.find('span').text
                char_link = "https://www.imdb.com" + char.get('href')
                entry_dict = {'org_name': org_name,'org_link': org_link,'char_name': char_name,'char_link': char_link}
                count=count+1
                top_cast_name_and_link[count] = entry_dict
        else:
            top_cast_name_and_link[0] = 0
        self.top_cast_name_and_link.append(top_cast_name_and_link)
# #----all cast and crew________________________
    def get_all_cast_crew_link(self,soup1):
        all=soup1.find('a',class_="ipc-metadata-list-item__icon-link")
        if all is not None:
            all_cast_crew_link="https://www.imdb.com"+all.get('href')
        else:
            all_cast_crew_link="N/A"
        self.all_cast_crew_link.append(all_cast_crew_link)
# #------additional_desciption---------
    def get_additional_description(self,soup1):
        story=soup1.find('div',class_="ipc-html-content-inner-div")
        if story is not None:
            additional_desciption=story.text
        else:
            additional_desciption="N/A"
        self.additional_desciption.append(additional_desciption)
# # # ===more_movies_like_this - dictionary {movie_name:<href>,...}
    def get_more_like_movie_link(self,soup1):
        more=soup1.find_all('a',class_="ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable")
        if more is not None:
            more_like_movie_link={}
            count=0
            for d in more:
                if d is not None:  
                    link3=d.get("href")
                    name3=d.find('span').text
                    dict3={"movie_name":name3,'movie_link':link3}
                    count=count+1
                    more_like_movie_link[count]=dict3
                else:
                    more_like_movie_link="N/A"
        else:
            more_like_movie_link="N/A"
        self.more_like_movie_link.append(more_like_movie_link)
    
#---------storyline___________

# ______keywords - list of tags ['key1','key2','key3',...]


# 22. plot_summary - link str


# 23. plot_synopsis - link str


# 24. tagline - str


# 25. motion_micture_rating - str


# 26. parents_guide_

# # 27. fact_and_link- {'trivia':[text, link], 'goofs': [text, link],...} 
    def get_fact_and_link(self,soup1):
        div=soup1.find_all('section')
        facts_and_links={}
        for i in div:
            if i.get('data-testid')=="DidYouKnow":
                manydiv=i.find_all('div',class_="ipc-list-card--border-line ipc-list-card--tp-none ipc-list-card--bp-none ipc-list-card sc-c3661566-1 hhEqPz ipc-list-card--base")
                if manydiv is not None:
                    for li in manydiv:
                        tag=li.find('a',class_="ipc-metadata-list-item__label ipc-metadata-list-item__label--link")
                        if tag is not None:
                            tag_link="https://www.imdb.com"+tag.get('href')
                            tag_name=tag.text
                            tag_text=li.find('div',class_='ipc-html-content-inner-div').text
                            facts_and_links[tag_name]=[tag_text,tag_link]
                        else:
                            pass
                else:
                    facts_and_links[0]=[0,0]
        self.facts_and_link.append(facts_and_links)


# 28. user_review_link - str
    def get_user_review_link(self,soup1):
        div=soup1.find_all('div')
        user_review_link=None

        if div is not None:

            for i in div:
                if i.get('data-testid')=="reviews-header":
                    userr=i.find('a',)
                    if userr is not None:
                        user_review_link="https://www.imdb.com"+userr.get('href')
                    else:
                        pass
        else:
            user_review_link=None
        self.user_review_link.append(user_review_link)
# # 29. faq_link - str
    def get_faq_link(self,soup1):
        div=soup1.find_all('div')
        if div is not None:
            faq_link = None
            for i in div:
                if i is not None:
                    if i.get('data-testid')=="faq-content":
                        faq_link="https://www.imdb.com"+i.find('a',).get('href')
                else:
                    pass
        else:
            faq_link="N/A"
        self.faq_link.append(faq_link)
# # 30. release_date - Month/Date/Year (12/30/1990)
    def get_release_date(self,soup1):
        release_date=None
        div=soup1.find_all('div')
        for i in div:
            if i.get('data-testid')=="title-details-section":
                lio=i.find_all('li',class_="ipc-metadata-list__item ipc-metadata-list-item--link")
                if lio is not None:
                    new=lio[0].find("li",class_="ipc-inline-list__item") 
                    if new is not None:             
                        a=new.find('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                        if a is not None:
                            date1=(str(a.text))
                        else:   
                            pass                
                    else:
                         pass
                else:
                    release_date="N/A"
                
        if date1 is not None:
            try:
                parsed_date = datetime.strptime(date1, '%B %d, %Y (India)')
                # Use strftime to format the parsed date in the desired format 'MM/DD/YYYY'
                release_date = parsed_date.strftime('%m/%d/%Y')
            except ValueError:
                date_string =date1
                release_date= re.search(r'\d{4}', date_string).group()
        else:
             release_date="N/A"
        self.release_date.append(release_date)
        # If parsing fails (invalid date format), return a default value or handle it  
# 31. country_of_origin - str
    def get_country_of_origin(self,soup1):
        div=soup1.find_all('div')
        country_of_origin=[]
        for i in div:
            if i.get('data-testid')=="title-details-section":
                lio=i.find_all('li',class_="ipc-metadata-list__item")
                if lio is not None:
                    new=lio[1].find_all("li",class_="ipc-inline-list__item")
                    if new is not None:
                        for i in new:                
                            a=i.find('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                            if a is not None:
                                country_of_origin.append(str(a.text))
                            else:  
                                pass  
                    else:
                        country_of_origin="N/A"     
                else:
                    country_of_origin="N/A"  
        self.country_of_origin.append(country_of_origin)         
# 32. language -str
    def get_language(self,soup1):
        div=soup1.find_all('div')
        language_list=[]
        for i in div:
            if i.get('data-testid')=="title-details-section":
                lio=i.find_all('li',class_="ipc-metadata-list__item")
                if lio is not None:
                    new=lio[3].find_all("li",class_="ipc-inline-list__item")
                    if new is not None:
                        for i in new:                
                            a=i.find('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                            if a is not None:
                                language_list.append(str(a.text))
                            else:  
                                pass  
                    else:
                        language_list="N/A"
                else:
                    language_list="N/A"
        self.language.append(language_list)
    
# # # 33. als_knows_as - list of words 
    def get_also_known_as(self,soup1):
        div=soup1.find_all('div')
        also_name_list=[]
        for i in div:
            if i.get('data-testid')=="title-details-section":
                lio=i.find_all('li',class_="ipc-metadata-list__item ipc-metadata-list-item--link")
                if lio is not None:

                    new=lio[-4].find_all("li",class_="ipc-inline-list__item")
                    if new is not None:
                        for i in new:
                            a=i.find('span',class_="ipc-metadata-list-item__list-content-item")
                            if a is not None:
                                also_name_list.append(str(a.text))
                            else:  
                                pass                 
                                # href="https://www.imdb.com"+a.get('href')
                    else:
                        also_name_list="N/A"
                else:
                    also_name_list="N/A"
        self.also_known_as.append(also_name_list)
# # 34. production_company -  [list]
    def get_production_company(self,soup1):
        div=soup1.find_all('div')
        company_list=[]
        for i in div:
            if i.get('data-testid')=="title-details-section":
                lio=i.find_all('li',class_="ipc-metadata-list__item ipc-metadata-list-item--link")
                if lio is not None:
                    new=lio[-2].find_all("li",class_="ipc-inline-list__item")
                    if new is not None:
                        for i in new:
                            a=i.find('a',class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
                            if a is not None:
                                company_list.append(a.text)
                            else: 
                                pass                  
                                # href="https://www.imdb.com"+a.get('href')
                    else:
                        company_list="N/A"
                else:
                    company_list="N/A"
        self.production_company.append(company_list)
    
# # # 35. box_office_no - {'budget':<int>,'gross_us_canad_income':<>,...}
    def get_box_office_no(self,soup1):
        box_office={}
        budget=soup1.find('ul',class_="ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact sc-6d4f3f8c-0 VdkJY ipc-metadata-list--base")
        if budget is not None:
            lin=budget.find_all("li")   
            for g in lin:  
                label=g.find('span',class_="ipc-metadata-list-item__label")
                if label is not None:
                    lab=label.text
                else:
                    continue
                a=g.find('li',class_="ipc-inline-list__item")
                if a is not None:
                    number=a.find('span',class_="ipc-metadata-list-item__list-content-item")
                    if number is not None:
                        num=number.text
                        box_office[lab]=num
                    else:
                        box_office[lab]="n/a"
                    
                else:
                    box_office[lab]="n/a"
        self.box_office.append(box_office)
# # 36. sound_mix_company - list
    def get_sound_mix_company(self,soup1):
        name=None
        link=None
        nam=None
        lin=None
        sound=soup1.find_all('ul',class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
        if sound is not None:
            li=sound[-2].find_all("li")
            sound_list=[]
            for a in li:
                if a is not None:
                    nam=a.find("a")
                    if nam is not None:
                        name=nam.text
                    else:
                        pass
                    lin=a.find("a")
                    if lin is not None:
                        link=lin="https://www.imdb.com"+lin.get('href')

                    else:
                        pass
                    sound_list.extend([name,link])
                else:
                    sound_list="n/a"
        else:
            sound_list="n/a"
        self.sound_mix_company.append(sound_list)
    
# #  store  37. aspect_ratio -  str/
    def get_ratio(self,soup1):
        ratio=None
        ratio_element=None
        aspect=soup1.find_all('ul',class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
        if aspect is not None:

            ratio_element=aspect[-1].find('span',class_="ipc-metadata-list-item__list-content-item")
            if ratio_element is not None:
                ratio=ratio_element.text
            else:
                ratio ="N/A" 
        else:
            ratio="N/A"
        self.aspect_ratio.append(ratio)

# # #------------------------start>>>>>>>>>  store video link------------------------------------------------------------
    def get_video_list_link(self,soup1):
        hub_video_link=None
        response2=None
        soup2=None
        store_video_heading=None
        store_anchor=None
        y=None
        a=soup1.find('a',class_="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-onBase ipc-secondary-button sc-d0440aee-3 jUntGU")
        if a is not None:
            hub_video_link="https://www.imdb.com"+a.get('href')
            response2= requests.get(hub_video_link, headers=self.headers)
            soup2=BeautifulSoup(response2.text, 'html.parser')
            store_video_heading=soup2.find_all("h2")
            video_list=[]
            for i in store_video_heading:
                store_anchor=i.find('a',class_="video-modal")
                if store_anchor is not None:
                    y=store_anchor.get('href')          
                    video_list.append("https://www.imdb.com"+y)
                else:
                    pass
            soi=soup2
            for l in range(200):
                for i in soi.find_all('a'):
                    if i.text=="Next »":
                        t="https://www.imdb.com"+i.get('href')
                        response= requests.get(t, headers=self.headers)
                        soup=BeautifulSoup(response.text, 'html.parser')
                        soi=soup
                        store_video_heading1=soi.find_all("h2")
                        for i in store_video_heading1:    
                            store_anchor1=i.find('a',class_="video-modal")
                            if store_anchor1 is not None:
                                video_list.append("https://www.imdb.com"+store_anchor1.get('href'))
                            else:
                                pass
                        break           
        else:
            video_list=None
        self.all_video_link.append(video_list)
    
    def get_photo_list_link(self,soup1):
        hub_photos_link=None
        photo_list=None
        a_tag=soup1.find_all('a',class_="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-onBase ipc-secondary-button sc-d0440aee-3 jUntGU")
        if a_tag is not None:
        
            for i in a_tag:
                if i is None:
                    hub_photos_link=None

                    continue
                elif 'video' in i.get('href'):
                    continue              
                else:    
                    hub_photos_link="https://www.imdb.com"+i.get('href')
                    break
            if hub_photos_link is not None:
                            
                if 'rm' in hub_photos_link:
                    response4= requests.get(hub_photos_link, headers=self.headers)
                    soup4=BeautifulSoup(response4.text, 'html.parser')
                    half=soup4.find('a',class_="ipc-icon-link ipc-icon-link--baseAlt ipc-icon-link--onBase")
                    if half is not None:
                        half_link=half.get('href')
                    else:
                        pass

                    hub_photos_link='https://www.imdb.com'+half_link
                else:
                    pass  
                photo_list=[]
                response5= requests.get(hub_photos_link, headers=self.headers)
                soup5=BeautifulSoup(response5.text, 'html.parser')
                store_photo_heading=soup5.find("div",class_="media_index_thumb_list")
                if store_photo_heading is not None:
                    image=store_photo_heading.find_all('img')
                    for store_photo in image:
                        if store_photo==None:
                            pass
                        else:
                            y=store_photo.get('src')          
                            photo_list.append(y)
                sou=soup5
                for k in range(200):
                    for i in sou.find_all('a'):
                            if i.text=="Next »":
                                j="https://www.imdb.com"+i.get('href')
                                response= requests.get(j, headers=self.headers)
                                soup=BeautifulSoup(response.text, 'html.parser')
                                sou=soup
                                store_photo_heading1=sou.find("div",class_="media_index_thumb_list")
                                image1=store_photo_heading1.find_all('img')
                                for store_photo1 in image1:
                                    if store_photo1==None:
                                        pass
                                    else:
                                        y=store_photo1.get('src')          
                                        photo_list.append(y)
                                break
            else:
                photo_list=hub_photos_link
        else:
            photo_list="N/A"
        self.all_photo_link.append(photo_list)  
   
        
#---------stop<<<<<<<<< photos src----------------------------
    def get_data_from_each_link(self,li_tag):
        self.get_movie_link(li_tag)
        self.get_movie_name(li_tag)
        self.get_movie_poster_link(li_tag)
        self.get_movie_year(li_tag)
        self.get_movie_time(li_tag)        
        self.get_movie_rating(li_tag)

    
    def get_movie_link(self,li_tag):
        movie_link= "https://www.imdb.com" +li_tag.find('a', class_="ipc-title-link-wrapper").get('href')
        self.movie_link.append(movie_link)
        response1= requests.get(movie_link, headers=self.headers)
        soup1= BeautifulSoup(response1.text, 'html.parser')
        self.get_photo_list_link(soup1)
        self.get_video_list_link(soup1)
        self.get_ratio(soup1)
        self.get_sound_mix_company(soup1)
        self.get_box_office_no(soup1)
        self.get_production_company(soup1)
        self.get_also_known_as(soup1)
        self.get_language(soup1)
        self.get_country_of_origin(soup1)
        self.get_release_date(soup1)
        self.get_faq_link(soup1)
        self.get_user_review_link(soup1)
        self.get_more_like_movie_link(soup1)
        self.get_additional_description(soup1)
        self.get_genre(soup1)
        self.get_short_description(soup1)
        self.get_how_many_people_rated(soup1)
        self.get_movie_popularity_score(soup1)
        self.get_director_name(soup1)
        self.get_writer_name(soup1)
        self.get_stars_name(soup1)
        self.get_userviews_criticreviews_metascore(soup1)
        self.get_store_awards_and_nomination(soup1)
        self.get_oscar_link(soup1)
        self.get_top_cast_name_and_link(soup1)
        self.get_all_cast_crew_link(soup1)
        self.get_fact_and_link(soup1)
        self.User_review(soup1)

    def get_movie_name(self,li_tag):
        title=li_tag.find('h3').text
        movie_name=re.sub(r'^\d+\.\s*', '', title)
        self.movie_name.append(movie_name)
    def get_movie_poster_link(self,li_tag):                     
            movie_poster_link=li_tag.find('img').get('src')
            self.movie_poster_link.append(movie_poster_link)
    def get_movie_year(self,li_tag):
            movie_year= li_tag.find('span', class_="sc-14dd939d-6 kHVqMR cli-title-metadata-item")
            if movie_year:
                movie_year = movie_year.text.strip('()')
            else:
                movie_year =None
            self.movie_year.append(movie_year)
    def get_movie_time(self,li_tag):
            movie_time = li_tag.find('span', class_="sc-14dd939d-6 kHVqMR cli-title-metadata-item")
            if movie_time:
                movie_time = movie_time.find_next_sibling().text.strip()
            else:
                movie_time =None
            self.movie_time.append(movie_time)
    def get_movie_rating(self,li_tag):
            movie_rating=li_tag.find('span',class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").text
            self.movie_rating.append(movie_rating)
    def get_top_250_movies(self):
        
        main_url = "https://www.imdb.com/chart/top/"
        response=requests.get(main_url, headers=self.headers)
        soup=BeautifulSoup(response.text, 'html.parser')
        # movie_rows = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-3a353071-0 wTPeg compact-list-view ipc-metadata-list--base")
        movie_rows = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 ckQYbL compact-list-view ipc-metadata-list--base")

        
        count=0
        for row in movie_rows.find_all('li'):            
            self.get_data_from_each_link(row)   
            count=count+1
            print(f"Processing movie {count}")  # Example output        
    def generate_excel(self, filename):
        movie_data = {'movie_link':self.movie_link,'movie_name': self.movie_name,'movie_poster_link':self.movie_poster_link,'movie_year':self.movie_year,
 'movie_time': self.movie_time,'movie_rating': self.movie_rating,'genre':self.genre,'short_description':self.short_description ,'how_many_people_rated': self.how_many_people_rated,'movie_popularity_score':self.popularity_score,
'director_name':self.dirctor_name,'writer_name':self.writer_name,'star_name':self.star,'user_review':self.user_review,'critic_viewers':self.critic_viewers,'meta_score':self.meta_score,'wins_and_nominations': self.wins_and_nomination,
'oscar_link':self.oscar_link,'top_cast_name_and_link':self.top_cast_name_and_link,'all_cast_crew_link':self.all_cast_crew_link,'additional_desciption':self.additional_desciption,'more_like_movie_link':self.more_like_movie_link ,
            'aspect_ratio':self.aspect_ratio,'sound_mix_company':self.sound_mix_company,'box_office':self.box_office,'production_company':self.production_company,
            'also_known_as':self.also_known_as,
            'language':self.language,
            'country_of_origin':self.country_of_origin,
            'release_date':self.release_date,
            'faq_link':self.faq_link,
            'user_review_link':self.user_review_link,
            'facts_and_links':self.facts_and_link,
            'all_video_link':self.all_video_link,
            'all_photo_link':self.all_photo_link,
            
        }              
        df = pd.DataFrame(movie_data)
        df.to_excel(filename, index=False)        




