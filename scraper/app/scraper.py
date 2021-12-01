import os
import re
import requests
import csv
import time
import html
from parse import *
from compile import *
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

def create_csv():
    global csv_name
    global dir_name
    dir_name = r"%s" % os.path.abspath(os.getcwd())
    csv_name = dir_name + "/data.csv"
    with open(csv_name, mode="w") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["State", "City/County", "Ordinance", "Site"])

def write_entry(info):
    for i in range(0, len(info)):
        info[i] = info[i].replace("\n", "")
        info[i] = info[i].replace(",", " ")
    with open(csv_name, mode="a") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(info)

class Scraper:
    def make_driver(self):
        driver_path = dir_name + r"/app/chromedriver"
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options, executable_path=driver_path)
    def general_code(self):
        page = requests.get("https://www.generalcode.com/text-library/")
        soup = BeautifulSoup(page.text, "html.parser")
        states = soup.find_all("div", class_=re.compile("state"))
        for state in states:
            state_name = state.find("h2", class_="stateTitle").text
            cities = state.find_all("div", class_="listItem")
            for city in cities:
                try:
                    county = city.find("div", class_="codeCounty").text
                except Exception:
                    county = ""
                city_link = city.find("a", class_="codeLink")
                write_entry([state_name, city_link.text + county, city_link["href"], "General Code"])
    def municode(self):
        self.make_driver()
        self.driver.get("https://library.municode.com")
        state_links = []
        state_path = "/html/body/div[1]/div[2]/ui-view/div[2]/section/div/div[2]/div[{}]/ul/li[{}]/a"
        for i in range(3, 23):
            for j in range(1, 11):
                try:
                    state = self.driver.find_element(By.XPATH, state_path.format(i, j))
                    state_links.append(state.get_attribute("href"))
                except NoSuchElementException:
                    break
        for link in state_links:
            self.driver.get(link)
            county_path = "html/body/div[1]/div[2]/ui-view/div[2]/section/div/div/div[{}]/ul/li/a"
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, county_path.format(2))))
            except TimeoutException:
                continue
            for i in range(2, 29):
                try:
                    counties = self.driver.find_elements(By.XPATH, county_path.format(i))
                    state = link[len(link) - 2 : len(link)].upper()
                    for county in counties:
                        write_entry([state, county.text, county.get_attribute("href"), "Municode"])
                except NoSuchElementException:
                    break
        self.driver.quit()
    def alpc(self):
        page = requests.get("https://codelibrary.amlegal.com/")
        soup = BeautifulSoup(page.text, "html.parser")
        states = soup.find_all("a", href=re.compile("/regions"))
        for state in states:
            link = "https://codelibrary.amlegal.com" + state["href"]
            page = requests.get(link)
            soup = BeautifulSoup(page.text, "html.parser")
            counties = soup.find_all("a", href=re.compile("/codes"))
            for county in counties:
                link = "https://codelibrary.amlegal.com" + str(county["href"])
                write_entry([state.text, county.text, link, "ALPC"])
    def codebook(self):
        page = requests.get("https://www.codebook.com/listing/#")
        soup = BeautifulSoup(page.text, "html.parser")
        states = soup.find_all("div", class_="listing-region")
        states = states[3 : len(states)] # removes Canada, tribes, and special regions
        for state in states:
            state_name = state.find("h1", class_="state-name").text
            state_name = state_name[0] + state_name[ 1 : len(state_name)].lower()
            counties = state.find_all("a", rel="noreferrer noopener")
            for county in counties:
                write_entry([state_name, county.text, county["href"], "Codebook"])
    def franklin_legal(self):
        def check_exists(link):
            return True
        page = requests.get("http://www.franklinlegal.net/search-codes")
        soup = BeautifulSoup(page.text, "html.parser")
        counties = soup.find_all("option", target=re.compile("blank"))
        counties = counties[1 : len(counties)]
        for county in counties:
            if check_exists(county["value"]):
                write_entry(["Texas", county.text, county["value"], "Franklin Legal"])
    def mtas(self):
        page = requests.get("https://www.mtas.tennessee.edu/charters_bycity_files")
        soup = BeautifulSoup(page.text, "html.parser")
        counties = soup.find_all("a", href=re.compile("/city"))
        for county in counties:
            page = requests.get("https://www.mtas.tennessee.edu" + county["href"])
            soup = BeautifulSoup(page.text, "html.parser")
            try:
                link = soup.find_all("a", type=re.compile("application/pdf"))
                link = link[len(link) - 1]["href"]
                write_entry(["Tennessee", county.text, link, "MTAS"])
            except Exception:
                pass
    def quality_code(self):
        page = requests.get("https://www.qcode.us/codes.html")
        soup = BeautifulSoup(page.text, "html.parser")
        counties = soup.find_all("a", href=re.compile("view=desktop"))
        for county in counties:
            state = re.search('([A-Z]){2}', county.text).group(0)
            county_name = county.text[0 : county.text.index(",")]
            write_entry([state, county_name, county["href"], "Quality Code"])
    def clerkbase(self):
        self.make_driver()
        self.driver.get("https://clerkshq.com/")
        county_path = "/html/body/div/main/div/ul/li[{}]/a"
        counties = []
        for i in range(1, 100):
            try:
                county = self.driver.find_element(By.XPATH, county_path.format(i))
                state = str(county.get_attribute("href"))
                state = state[len(state) - 2 : len(state)].upper()
                write_entry([state, county.text, county.get_attribute("href"), "Clerkbase"])
            except NoSuchElementException:
                pass
        self.driver.quit()
    def ranson(self):
        self.make_driver()
        self.driver.get("https://www.ransonfinancial.com/code-library/")
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        counties = soup.find_all("a", href=re.compile(".citycode.net"))
        for county in counties:
            state = county.text
            state = state[state.index(",") + 2 : len(state)]
            county_name = county.text[0 : county.text.index(",")]
            write_entry([state, county_name, county["href"], "Ranson"])
        self.driver.quit()
    def drake(self):
        page = requests.get("https://libguides.law.drake.edu/c.php?g=150956&p=992837")
        soup = BeautifulSoup(page.text, "html.parser")
        counties = soup.find_all("a", target="_blank")
        for county in counties:
            write_entry(["Iowa", county.text, county["href"], "Drake"])
    def nebraska_access(self):
        self.make_driver()
        self.driver.get("http://nebraskaccess.nebraska.gov/municipalcodes.asp")
        county_path = "/html/body/div[2]/div/div/div[3]/div/div[1]/div/ul[1]/li[{}]/a"
        for i in range(1, 100):
            try:
                county = self.driver.find_element(By.XPATH, county_path.format(i))
                county_name = county.text
                if not "American Legal Publishing" in county_name:
                    if "Code" in county_name:
                        county_name = county_name[0 : county_name.index("Code") - 1]
                    if "Municipal" in county_name:
                        county_name = county_name[0 : county_name.index("Municipal") - 1]
                    if "Ordinances" in county_name:
                        county_name = county_name[0 : county_name.index("Ordinances") - 1]
                write_entry(["Nebraska", county_name, county.get_attribute("href"), "Nebraska Access"])
            except NoSuchElementException:
                break
        self.driver.quit()
    def run(self):
        self.general_code()
        self.municode()
        self.alpc()
        self.codebook()
        self.franklin_legal()
        self.mtas()
        self.quality_code()
        self.clerkbase()
        self.ranson()
        self.drake()
        self.nebraska_access()

def main():
    s = Scraper()
    create_csv()
    s.run()
    parse(csv_name)
    make_html(csv_name)

if __name__ == '__main__':
    main()
