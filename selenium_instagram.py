from instagram import username,password    #giriş bilgilerinin saklandığı modül
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class Instagram:
    def __init__(self,username,password):
        self.browserProfile=webdriver.ChromeOptions()        #web driver profiline yeni özellik eklicez
        self.browserProfile.add_experimental_option('prefs',{'intl.accept_languages' :'tr'})  #dil ayarlarını yapıyoruz
        self.browser=webdriver.Chrome('chromedriver.exe',chrome_options=self.browserProfile)  #web driver ile optionsu ilişkilendirmiş olduk
        self.username=username
        self.password=password

    def sigIn(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(2)
        self.browser.maximize_window()
        usernameInput=self.browser.find_element_by_name("username")
        passwordInput=self.browser.find_element_by_name("password")

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(4)
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]").click()
        time.sleep(1)


    def getFollowers(self, max):    #max kaç takipçi getirmesini istiyorsak ona göre değer verdik
        self.browser.get(f"https://www.instagram.com/{username}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)
        dialog=self.browser.find_element_by_css_selector("div[role=dialog] ul")    #bazı clasların değişme ihtimali olduğundan dolayı role yi bu şekilde kullandık
        followerCount = len(dialog.find_elements_by_css_selector("li"))
        print(f"first : {followerCount}")

        action=webdriver.ActionChains(self.browser)  
                                                      
        while followerCount < max:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).key_down(Keys.SPACE).key_up(Keys.SPACE).perform()    #istediğimiz tuşları bu şekilde basabiliyoruz.
                                        #https://sqa.stackexchange.com/questions/36732/how-do-you-press-two-keys-at-the-same-time-with-python-selenium. tuşların yazımı ile ilgili site
            time.sleep(2)

            newCount=len(dialog.find_elements_by_css_selector("li"))

            if newCount !=followerCount:
                followerCount=newCount
                print(f"update count: {newCount}")
                time.sleep(3)
            else:
                break

        followers=dialog.find_elements_by_css_selector("li")

        followersList=[]
        i=0
        for user in followers:
            link=user.find_element_by_css_selector("a").get_attribute("href")
            followersList.append(link)

            i += 1
            if i == max:
                break

        with open('followers.txt','w',encoding='utf-8') as file:
            for item in followersList:
                file.write(item+'\n')

    def followUser(self,username):
        self.browser.get("https://www.instagram.com/"+username)
        time.sleep(2)

        followButton=self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/button")
        if followButton.text !="Mesaj Gönder":
            followButton.click()
            time.sleep(2)
        else:
            print("Zaten takiptesin")


    def unFollowUser(self,username):
        self.browser.get("https://www.instagram.com/" + username)
        time.sleep(2)

        followButton=self.browser.find_elements_by_tag_name('button')[1]
        if followButton.text !="Takip Et":
            followButton.click()
            time.sleep(2)
            self.browser.find_element_by_xpath('//button[text()="Takibi Bırak"]').click()
        else:
            print("takip etmiyorsunuz")


    def likedPhotos(self,username):
        self.browser.get("https://www.instagram.com/" + username)
        time.sleep(2)
        photo=self.browser.find_elements_by_xpath("//*[@id='react-root']/section/main/div/div[3]/article/div[1]/div/div")
        print(photo)
        for like in photo:

            for i in like.find_elements_by_xpath("//*[@id='react-root']/section/main/div/div[3]/article/div[1]/div/div/div"):
                i.find_element_by_css_selector("a").click()
                time.sleep(2)
                self.browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()
                time.sleep(2)
                self.browser.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()





instagram=Instagram(username,password)
instagram.sigIn()
#instagram.getFollowers(50)    
#instagram.followUser('')
#instagram.unFollowUser('')
#instagram.likedPhotos('')










