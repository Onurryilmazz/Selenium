from twitter import username,password   #giris bilgilerinin saklandığı modül
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class Twitter:
    def __init__(self,username,password):
        self.browser=webdriver.Chrome()
        self.username=username
        self.password=password

    def sıgnIn(self):
        self.browser.get("https://twitter.com/login")
        time.sleep(2)
        usernameInput=self.browser.find_element_by_name("session[username_or_email]")
        passwordInput=self.browser.find_element_by_name("session[password]")

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/form/div/div[3]/div/div/span").click()
        time.sleep(2)


    def search(self,hashtag):
        searchInput=self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input")
        searchInput.send_keys(hashtag)
        time.sleep(2)

        searchInput.send_keys(Keys.ENTER)
        time.sleep(2)

        results=[]

        list = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]")
        time.sleep(2)
        print("count"+ str(len(list)))

        for i in list:
            results.append(i.text)

        loopCounter=0       #scrool barın kaç kere aşşağı iniceğini kontrol ederken oluşturduğumu değişken
        last_hight=self.browser.execute_script("return document.documentElement.scrollHeight")     #javascript kodunu çalıştırmamızı sağlıyor. Bu sayede sitede console kısmında javascript kullanabilicez.scrool barı en aşşağı indirebilicez
                                                #çalıştırmak istediğimiz javascript kodunu yazıyoruz
        while True:
            if loopCounter >5:   #scrool bar değişken
                break
            self.browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height=self.browser.execute_script("return document.documentElement.scrollHeight")
            if last_hight==new_height:
                break
            last_hight=new_height
            loopCounter=loopCounter+1   #scrool barın kaç kere aşşağı iniceğini söylemek için

            list = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]")#"//div[@data-testid='tweet']/div[2]/div[2]/div[1]"
            time.sleep(2)
            print("count" + str(len(list)))

            for i in list:
                try:
                    results.append(i.text)
                except:
                    continue

        #count=1      #console yerine dosyaya yazdırıyoruz
        #for item in results:
         #   print(f"{count}-{item}")
            #count+=1
            #print("***************")

        count=1
        with open("tweets.txt","w",encoding='utf-8') as file:
            for item in results:
                file.write(f" {count}--{item}\n")
                count+=1

twitter=Twitter(username,password)
twitter.sıgnIn()
twitter.search("python")