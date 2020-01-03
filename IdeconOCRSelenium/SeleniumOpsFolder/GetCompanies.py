from selenium import webdriver
import os

sign_in = "https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin"

driver_path = os.path.abspath("..\\SeleniumDriver\\chromedriver")
driver = webdriver.Chrome(executable_path=driver_path)

driver.get(sign_in)
username = driver.find_element_by_id("username")
username.clear()
username.send_keys(r"{LinkedInUsername}")

username = driver.find_element_by_id("password")
username.clear()
username.send_keys(r"{LinkedInPassword}")

driver.find_element_by_class_name("btn__primary--large").click()

harfler = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

for harf in harfler:
   for page in range(1,25):
       path = "https://www.linkedin.com/directory/companies-{}-{}".format(harf,page)

       driver.get(path)
       file_name = "company\\company-{}.txt".format(harf)
       with open(file_name, 'a') as file:
           for i in range(1,4000):
               try:
                   xPath = '//*[@id="seo-dir"]/div/div[3]/ul/li[{}]/a'.format(i)
                   text = driver.find_element_by_xpath(xPath).text
                   file.write(text + '\n')
               except:
                   break

driver.quit()