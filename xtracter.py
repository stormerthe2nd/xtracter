from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException, ElementClickInterceptedException
from bs4 import BeautifulSoup

# find element by id, name, link text, css selector


class Xtracter:
    def __init__(self, _city, _std_code, _shop_category):
        self.city = _city
        self.std_code = _std_code
        self.shop_category = "+".join(tuple(_shop_category.split(" ")))
        self.url = f"https://www.google.com/search?q={self.shop_category}+in+{self.city}&rlz=1C1CHBD_enIN877IN877&oq=mobi&aqs=chrome.1.69i57j35i39j69i59j0i67l3j0i20i263i457j0i402.3502j0j7&sourceid=chrome&ie=UTF-8"
        self.contacts = []
        self.page = 1
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            '../chromedriver.exe')  # , options=self.options)
        try:
            self.driver.get(self.url)
            sleep(1)
            self.driver.find_element(
                By.XPATH, "//span[text()='View all']").click()
        except NoSuchElementException as err:
            print("Error ignored: ", err)
            self.driver.get(self.url)
            sleep(1)
            self.driver.find_element(
                By.XPATH, "//span[text()='View all']").click()
        except WebDriverException:
            self.driver.close()
            raise Exception("no internet connection")
        sleep(2)

    def xtract_page(self):
        print("Extracting Page ", self.page, "\n")
        elements_list = self.driver.find_elements_by_class_name(
            "rllt__details")
        for element in elements_list:
            html = element.get_attribute(
                "innerHTML")
            soup = BeautifulSoup(
                html, "lxml")
            try:
                contact = soup.find_all("div")[2].text[-11:].replace(" ", "")
                int(contact)  # this will return an error if not int
                if contact.startswith(self.std_code, 0, 5) or len(contact) < 10:
                    continue
                self.contacts.append(contact)
            except (IndexError, ValueError) as err:
                continue
        sleep(1)

    def next(self):
        while True:
            try:
                sleep(1)
                self.driver.find_element(
                    By.XPATH, "//span[text()='Next']").click()
                sleep(3)
                self.page += 1
                self.xtract_page()
            except NoSuchElementException:
                print("Extraction Completed without any Errors\n")
                break
            except (StaleElementReferenceException, ElementClickInterceptedException):
                print("Staled Element\n")
                if input("Continue ? (y/n)\n") == "y":
                    continue
                break

    def end(self):
        print("---Ending Session---\n")
        self.driver.close()
        sleep(1)
        with open(f"{self.city}.txt", "w") as contact_list:
            for i in self.contacts:
                contact_list.write(f"+91{i}\n")
            print("Contacts Printed\n")


city = input("Enter City :- ")
std_code = input("STD Code:- ")
shop_category = input("Shop:- ")

if __name__ == "__main__":
    x = Xtracter(city, std_code, shop_category)
    x.xtract_page()
    x.next()
    x.end()
