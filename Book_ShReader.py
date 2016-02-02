__author__ = 'Pavan'
__author__ = 'work-dady'

from bs4 import BeautifulSoup
import sys
import re
import time
import os

# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


bookmyshow_mainlk = 'http://in.bookmyshow.com'

filep = open(r'C:\Python34\file_shows1.txt','w')

with open(r'C:\Python34\listtt3.txt','r') as filelist_p:
  places_list = filelist_p.read().splitlines()

booking_link =""
mov_name =""

for tw in places_list:
    town = tw
    print('*****' + town + '************************')
    town_link = bookmyshow_mainlk + '/' + town + '/movies'
    print(town_link)

    town_movies_p = open(r'C:\Python34\towns_new\\' + town + '_'  + '_theater_list.txt','w')
    driver = webdriver.Firefox()


    try:
        new_lk = town_link

        driver.implicitly_wait(1)


        driver.get(new_lk)

        actionChain = ActionChains(driver).key_down(Keys.ALT)
        actionChain.send_keys(Keys.SPACE)
        actionChain.send_keys("n")
        actionChain.perform()

        wait = WebDriverWait(driver, 20)
        # username = wait.until(EC.presence_of_element_located((By.XPATH, u"//input[@id='id_username']/font[@color='red']")));
        loadmore_elem = wait.until(EC.presence_of_element_located((By.XPATH, u"//button[@data-pagination='movies' and text()='LOAD MORE']")));

        loadmore_elem.click()

        driver.implicitly_wait(2)

        f = driver.page_source
        soup= BeautifulSoup(f,'html.parser')
        movie_nowshowing = soup.find_all('div', {'class': '__col-now-showing'})

        print("***********************************************************")

        soup1 = BeautifulSoup(str(movie_nowshowing),'html.parser')
        movie_row = soup.find_all('div', {'class': 'wow fadeIn movie-card-container'})
        # print(movie_row)
        # filep.write(str(movie_row))

        i=0
        for element in movie_row:

            i = i + 1
            soup2= BeautifulSoup(str(element),'html.parser')
            movieList = soup2.find_all('a', {'class':'__movie-name'})
            language  = soup2.find_all('li', {'class':'__language'})

            bookbtn = soup2.find_all('div', {'class':'book-button'})
            soup3= BeautifulSoup(str(bookbtn),'html.parser')
            bookbutton = soup3.find_all('a')

            # Open movie list file for that town

            for mt in movieList:
                 mov_name =   str(mt.get('title'))
                 print("Movie Name : " + mov_name)

                 town_movies_p.write(mov_name + " ")

            for mt in language:
                lang = mt.string
                print("Language : " + str(lang))

                town_movies_p.write(lang + " ")

            for mt in bookbutton:
                btn_link =   mt.get('href')
                booking_link = bookmyshow_mainlk + str(btn_link)
                print("Booking Link : " + booking_link)

                town_movies_p.write(booking_link + "\n")

            # ######
            # For each movie in the town, go for booking link and find out all theater names and timings
            new_lk = booking_link
            driver_booking = webdriver.Firefox()
            driver_booking.implicitly_wait(1)


            driver_booking.get(new_lk)

            actionChain = ActionChains(driver).key_down(Keys.ALT)
            actionChain.send_keys(Keys.SPACE)
            actionChain.send_keys("n")
            actionChain.perform()


            user_text_1 = town

            popbox = driver_booking.find_element_by_xpath(u'//input[@id="inp_RegionSearch_top"]')

            if(popbox is not None):
                popbox.send_keys(user_text_1)
                popbox.send_keys(Keys.RETURN)

            driver_booking.implicitly_wait(1)

            wait_booking = WebDriverWait(driver_booking, 20)
            tktbook_elem = wait_booking.until(EC.presence_of_element_located((By.XPATH, u"//a[@class='__showtime-link ' and contains(@href,'booktickets')]")));
            driver_booking.implicitly_wait(1)

            booking_f = driver_booking.page_source

            booking_soup= BeautifulSoup(booking_f,'html.parser')
            theaters_running = booking_soup.find_all('a', {'class': '__venue-name'})

            bktheater_soup= BeautifulSoup(str(theaters_running),'html.parser')
            theaters_running = bktheater_soup.find_all('strong')
            # print(theaters_running)

            theaters_list_p = open(r'C:\Python34\towns_new\\' + town + '_'  + mov_name + '_theater_list.txt','w')

            for thts in theaters_running:
                 theat_name =  str(thts.string)
                 print("Theater Name : " + theat_name)
                 theaters_list_p.write(theat_name + "\n")

            #  Quit the booking window
            driver_booking.quit()

            theaters_list_p.close()

    except Exception as e:
        print(e)

    town_movies_p.close()
    driver.quit()


filep.close()