from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import os
import requests
import urllib.request
from models import News
class Taotiao_Spider():
    def __init__(self):
        self.url="https://www.toutiao.com"
        self.driver=webdriver.Chrome()
        self.path="django/3.8/BrainPower/static/src/images/news"
        self.img_path="/src/images"


    #获取url
    def get_url(self,url_houzhi):
        return self.url+"/"+url_houzhi

    def get_respons(self,url_start):
        self.driver.get(url_start)
        time.sleep(2)
        items=[]
        items_url=[]
        # data = self.driver.find_element_by_class_name("channel").text
        # #items.append(data)
        # items_lise=list(data.split("\n"))
        # print(items_lise)
        par_urls=self.driver.find_elements_by_xpath("//a[@class='channel-item']")
        print(par_urls)
        for urls in par_urls:
            url_list=urls.get_attribute('href')
            if url_list.startswith(self.url):
                items_url.append(url_list)
            title=urls.find_element_by_xpath("./span").text
            if title!="阳光宽频" and title!="更多" and title !="直播":
                items.append(title)
        items=[x for x in items if x !='']
        # ac=self.driver.find_element_by_xpath("//li[@class='channel-more']/a")
        # ActionChains(self.driver).move_to_element(ac).perform()
        iteme_son=["军事","国际","时尚","旅游","探索","育儿","养生","美文","历史","美食"]
        items.extend(iteme_son)
        print(items_url,items)
        print(len(items_url), len(items))
        return items_url, items


        # for item in items:
        #     print(item)
        #     url_list=self.driver.find_element_by_partial_link_text(item)
        #     print(url_list)
        # element_list=self.driver.page_source
        # print(element_list.encode("utf-8"))
        # for ele in element_list:
        #     print(ele)wcommonFeed
        #     parsernUrl=ele.find_element_by_xpath("./a/@href")
        #     print(parsernUrl)


    def parse(self,parent_urls,parent_titles):
        print(parent_urls,parent_titles)
        print(len(parent_urls),len(parent_titles))

        for i in range(0,len(parent_urls)):
            items=[]
            self.driver.get(parent_urls[i])
            js = "var q=document.documentElement.scrollTop=10000"
            time.sleep(2)
            self.driver.save_screenshot("redbaidu.png")
            self.driver.execute_script(js)
            time.sleep(5)
            self.driver.save_screenshot("redbaidu1.png")
            element_list=self.driver.find_elements_by_xpath("//div[@class='wcommonFeed']/ul/li")
            for element in element_list:
                try:
                    news={}
                    news['parentTitles']=parent_titles[i]
                    news['sonUrls']=element.find_element_by_xpath(".//div[@class='title-box']/a").get_attribute('href')
                    news['news_title']=element.find_element_by_xpath(".//div[@class='title-box']/a").text
                    news['news_image']=element.find_element_by_xpath(".//a[@class='img-wrap']/img").get_attribute('src')
                    news['news_img_path']=self.download(news['news_image'],news['news_title'][0:2],news['parentTitles'])
                    print(news)
                except Exception as re:
                    print(re)
    #图片下载
    def download(self,image_url,filename,parent_title):
        paths = self.path + "/" + parent_title
        if not os.path.isdir(paths):
            os.makedirs(paths)
        try:
            with requests.get(url=image_url) as r:
                with open(paths+"/"+'%s.jpg'%filename,'ab+')as f:
                    for chunk in r.iter_content():
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            print("下载完成")
        except Exception as e:
            print(e)
        finally:
            f.close()
            return self.img_path+'/'+parent_title+'/'+filename+'.jpg'

    def downimg2(self,img_url,img_title,parent_title):
        path="/scrapy/3.23/image"+"/"+parent_title
        print(path)
        if not os.path.isdir(path):
            os.makedirs(path)
        try:
            f=open(path+"/"+parent_title+".jpg","wb")
            f.write((urllib.request.urlopen(img_url)).read())

            #urllib.request.urlretrieve(img_url,'{}{}.jpg'.format(path,img_title))
            print("下载完成")
        except Exception as e:
            print(e)
        finally:
            f.close()















    #主程序
    def run(self):
        pass

        #1获取url
        url_start=self.url

        #2发送请求，获取响应
        parent_urls,parent_title=self.get_respons(url_start)



        #3获取数据
        self.parse(parent_urls,parent_title)


        #4保存到数据库


if __name__=='__main__':
    taotiao=Taotiao_Spider()
    taotiao.run()

