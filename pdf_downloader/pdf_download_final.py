import requests
from bs4 import BeautifulSoup
# to use webdriver you need chromedriver.exe in the same folder as the .py script
from selenium import webdriver
import time
from PyPDF2 import PdfFileMerger
import os
import csv
import random


def get_html_source(url, sleep_time=10):
    browser = webdriver.Chrome()
    # get web page
    browser.get(url)
    # execute script to scroll down the page
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # sleep for time
    time.sleep(sleep_time)
    return browser.page_source

# returns list of links of all pdf on a page
def get_all_hrefs(list_of_page_number_on_website, sleep_time=10):
    browser = webdriver.Chrome()
    final_all_pdf_links = []
    for number in list_of_page_number_on_website:
        # get web page
        browser.get(f"https://registry.verra.org/app/projectDetail/VCS/{number}")
        # execute script to scroll down the page( copy from internet )
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        # sleep for time
        if number == list_of_page_number_on_website[0]:
            time.sleep(20)
        else:
            time.sleep(sleep_time)
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        a_tags = soup.find_all(name="a")
        all_pdf_links_of_page = []
        for a_tag in a_tags:
            if a_tag.text[-3:] == "pdf":
                all_pdf_links_of_page.append(a_tag["href"])
        del a_tags
        final_all_pdf_links.append(all_pdf_links_of_page)
    
    return final_all_pdf_links

# Create and merge pdfs
def create_and_merge_pdfs(links_list, start_page, end_page):
    pdf_name_list = []
    initial_start_page = start_page
    merger = PdfFileMerger()
    for a_page in links_list:
        for index_link, a_link in enumerate(a_page):
            content = requests.get(a_link).content
            with open(f"pdf_downloader_folder/{start_page}_{index_link}.pdf", 'wb') as my_data:
                my_data.write(content)
            pdf_name_list.append(f"pdf_downloader_folder/{start_page}_{index_link}.pdf")
            
            try:
                merger.append(f"pdf_downloader_folder/{start_page}_{index_link}.pdf")
                print(f"Fetched & Merged PageNumber_PDFindex-- {start_page}_{index_link}")
            except:
                print(f"------------{start_page}_{index_link}.pdf was not merged due to some reason!!!")
                print("Visit the folling link for it:")
                print(f"Link--- {a_link}")
        time.sleep(random.random()*3)
        # Forcing correct name of pdf according to the start_page and end page 
        start_page += 1

    my_data.close()
    merger.write(f"pdf_downloader_folder/Compiled_{initial_start_page}_{end_page}.pdf")
    merger.close()
    for pdf in pdf_name_list:
        os.remove(pdf)
    print("Compiled PDF Created")
    return


#-------------------- MAIN SCRIPT IMPLEMENTATION------------------------------
print("-- Enter the Page number of the website ,i.e, what you write after / . P.S. Both are included")
start_page= int(input("Start_page - "))
end_page= int(input("End_page - "))
mylist = list(range(start_page, end_page+1))
print("-- Whether to read from previously saved CSV or not (saved inside pdf_downloader_folder) ----")
print("-- Use 'w' if you have no idea about this ----")
mode = input("r for read or w for write mode: ") # read or write mode

try:
    os.mkdir("pdf_downloader_folder")
except FileExistsError:
    pass
  
if mode == "w" :
    # ----- Writing to csv file
    linksss = get_all_hrefs(mylist, sleep_time=10)

    # data to be written row-wise in csv fil
    data = linksss
    # opening the csv file in 'w+' mode
    file = open('pdf_downloader_folder/links.csv', 'w+', newline ='')

    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(data)
    file.close()
    print("links.csv created")

elif mode == "r":
    # ------- Reading From csv file
    with open('pdf_downloader_folder/links.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    f.close()
    print("links.csv read")
    linksss = data
# --------


create_and_merge_pdfs(links_list=linksss, start_page=start_page, end_page=end_page)
