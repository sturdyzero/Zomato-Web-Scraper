# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 05:12:08 2019

@author: sturd
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

#Extracting Bangalore Restaurants Data

#Browser Header for Firefox
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'}

#URL
url = r'https://www.zomato.com/bangalore/restaurants?page='


def bee(url, number, header):
    '''Data is read line by line from Template'''
    count = 1
    
    output = list()
    
    #Form Query
    query = url + str(number)
    print(query)
    
    #Get Webpage
    page = requests.get(query, headers = header)

    #Parse Webpage with BeautifulSoup
    soup = BeautifulSoup(page.text, 'lxml')
    
    #Find Label
    matches = soup.find_all('article', class_='search-result')

    #Find Tag in Label
    for match in matches:
        #print(count)
        tag = match.find('div', class_='row').text.strip().split(' ')[0].split('\n')[0]
        #print('Tag : {0}'.format(tag))
        
        try:
            
            type_sub = match.find('a', class_ = 'zdark ttupper fontsize6').text
            #print('Sub-Type : {0}'.format(type_sub))
            
            name = match.find('a', class_ = 'result-title hover_feedback zred bold ln24 fontsize0').text.strip()
            #print('Name : {0}'.format(name))
            
            location = match.find('a', class_ = 'ln24 search-page-text mr10 zblack search_result_subzone left').b.text
            #print('Location : {0}'.format(location))
            
            addr = match.find('div', class_ = 'col-m-16 search-result-address grey-text nowrap ln22').text        
            #print('Address : {0}'.format(addr))
            
            line6 = match.find_all('div', class_ = 'ta-right floating search_result_rating col-s-4 clearfix')
                
            for value in line6:
                rating = value.find('div').text.strip()
                votes = value.find('span').text.strip()
            
            #print('Rating : {0}, Votes : {1}'.format(rating, votes))
            
            #Extraction of Data from Bottom Categories
            line7 = match.find('div', class_ = 'search-page-text clearfix row')
            
            #Cuisines
            cuisine_container = list()
            cuisines = line7.find_all('a')
            for value in cuisines:
                cuisine = value.text
                cuisine_container.append(cuisine)
            #print('Cuisines : {0}'.format(cuisine_container))
            
            #Cost
            cost = line7.find_all('span', 'col-s-11 col-m-12 pl0')
            for value in cost:
                inr = value.text
                #print('Cost for 2 People : {0}'.format(inr))
                
            featured = line7.find_all('div', 'col-s-11 col-m-12 pl0 search-grid-right-text')
            
            feature_container = list()
            #Time and Featured
            for features in featured:
                list1 = features.text.strip()
                feature_container.append(list1)
            #print('Features : {0}\n\n'.format(feature_container))
            
            #print('Cuisines : {0} \n Cost : {1} \n Featured : {2}'.format(cuisine, inr, list1))
            
# =============================================================================
#             output[count] = [tag, type_sub, name, location, addr, rating, votes,
#                                      cuisine_container, inr, feature_container]
# =============================================================================
            output.append([name, tag, type_sub, location, addr, rating, votes,
                          cuisine_container, inr, feature_container])
            
            count += 1
        
        except:
            raise ValueError('Data Read Error!')
        
    return output


my_list = list()
#Iteration Begins
for i in range(1, 877):
    reception = bee(url, i, header)
    my_list.append(reception)

consolidated = list()
    
for ls in my_list:
    for values in ls:
        consolidated.append(values)


column_names = ['Name', 'Tag', 'Type', 'Location', 'Address', 'Rating',
                'Votes', 'Cuisines', 'Cost for 2', 'Features']        
df = pd.DataFrame(consolidated, columns = column_names)
df.to_excel('Zomato.xlsx')


        
    
    



    