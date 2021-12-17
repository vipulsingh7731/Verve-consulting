import requests
from bs4 import BeautifulSoup
# to use webdriver you need chromedriver.exe in the same folder as the .py script
from selenium import webdriver
import time
import os
import csv
import random
from pikepdf import Pdf as PDF

# returns list of links of all pdf on a page
def get_all_hrefs(list_of_page_number_on_website, sleep_time=10):
    browser = webdriver.Edge(r"msedgedriver.exe")
    final_all_pdf_links = []
    for number in list_of_page_number_on_website:
        # get web page
        browser.get(f"https://registry.verra.org/app/projectDetail/VCS/{number}")
        # execute script to scroll down the page( copy from internet )
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        # sleep for time
        if number == list_of_page_number_on_website[0]:
            time.sleep(15)
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
    pdf_name_list_which_were_created = []
    initial_start_page = start_page
    for a_page in links_list:
        pdf_ = PDF.new()
        version = pdf_.pdf_version
        if len(links_list[start_page-initial_start_page]) == 0:
            print(f"---------Index {start_page} has no files")
            pdf_.close()
            start_page += 1
            continue
        for index_link, a_link in enumerate(a_page):
            content = requests.get(a_link).content
            with open(f"pdf_downloader_folder/{start_page}_{index_link}.pdf", 'wb') as my_data:
                my_data.write(content)
                my_data.close()
            pdf_name_list_which_were_created.append(f"pdf_downloader_folder/{start_page}_{index_link}.pdf")
            
            try:
                
                src = PDF.open(f"pdf_downloader_folder/{start_page}_{index_link}.pdf")
                version = max(version, src.pdf_version)
                pdf_.pages.extend(src.pages)
                src.close()
                print(f"Fetched & Merged PageNumber_PDFindex-- {start_page}_{index_link}")
            except:
                print(f"------------{start_page}_{index_link}.pdf was not merged due to some reason!!!")
                print("----It is written to a separate file")
                with open(f"pdf_downloader_folder/Compiled_{start_page}_{index_link}_was.pdf", 'wb') as f:
                    f.write(content)
                    f.close()
            time.sleep(random.random()*3)
        pdf_.remove_unreferenced_resources()
        pdf_.save(f"pdf_downloader_folder/Compiled_{start_page}_.pdf", min_version=version)
        pdf_.close()
        # merger.write(f"pdf_downloader_folder/Compiled_{start_page}_.pdf")
        # merger.close()
    
        start_page += 1

    
    for pdf in pdf_name_list_which_were_created:
        os.remove(pdf)
    print("Compiled PDF Created")
    return


#-------------------- MAIN SCRIPT IMPLEMENTATION------------------------------
print("-- Enter the Page number of the website ,i.e, what you write after / . P.S. Both are included")
start_page= int(input("Start_page - "))
end_page= int(input("End_page - "))
if start_page>end_page:
    new_var = start_page
    start_page = end_page
    end_page = new_var
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
    linksss = get_all_hrefs(mylist, sleep_time=7)

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
os.system("PAUSE")