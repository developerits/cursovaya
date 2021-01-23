from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException        
from time import sleep, ctime
from collections import namedtuple
import csv



listDetailsProducts = [['title', 'price', 'rating', 'numberOfSales', 'seller']]

class crawlerAliexpress():
    #global numberItem
    def __init__(self, searchName, numberPage = 1):
        # Инициализация браузера.
        opts = Options()
        #opts.set_headless()     
        self.browser = Firefox(options=opts)
        self.searchName = searchName
        self.numberPage = numberPage 
        self.listDetailsProducts = []

        currentUrl = f'https://aliexpress.ru/wholesale?SearchText={self.searchName}&page={self.numberPage}'
        self.browser.get(currentUrl)
        cookie = {'name': 'aep_usuc_f', 'value': 'isfm=y&site=rus&c_tp=RUB&isb=y&region=RU&b_locale=ru_RU', 'domain': '.aliexpress.ru'}
        self.browser.add_cookie(cookie)
        self.browser.get(currentUrl)
        sleep(1)

    def scroll_down_page(self, speed=8):
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            self.browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self.browser.execute_script("return document.body.scrollHeight")

    def getProductsDetail(self, countPage):
        #scrollPauseTime = 2
        self.countPage = countPage
        self.scroll_down_page()
        title = self.browser.find_elements_by_xpath("//li[@class='list-item']//div[@class='item-title-wrap']//a[@class='item-title']")
        price = self.browser.find_elements_by_xpath("//li[@class='list-item']//div[@class='hover-help']//div[@class='item-price-row']")
        rating = self.browser.find_elements_by_xpath("//li[@class='list-item']//div[@class='hover-help']//span[@class='rating-value']")
        numberOfSales = self.browser.find_elements_by_xpath("//li[@class='list-item']//div[@class='hover-help']//a[@class='sale-value-link']")
        seller = self.browser.find_elements_by_xpath("//li[@class='list-item']//div[@class='hover-help']//a[@class='store-name']")
        itemsTitle = len(title)
        itemsPrice = len(price)
        itemsRating = len(rating)
        itemsNumberOfSales = len(numberOfSales)
        itemsSeller = len(seller)

        for i in range(min(itemsTitle, itemsPrice, itemsRating, itemsNumberOfSales, itemsSeller)):
            itemProduct = [title[i].text, price[i].text, rating[i].text, numberOfSales[i].text, seller[i].text]
            listDetailsProducts.append(itemProduct)

        self.paginator(self.countPage)
        
    def saveInCsv(self, nameFile):
        self.nameFile = nameFile
        with open(self.nameFile, "w", newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(listDetailsProducts)
 
    
    def check_exists_by_xpath(self, xpath):
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def paginator(self, countPage):
        sleep(2)
        isPaginator = self.check_exists_by_xpath("//button[@class='next-btn next-medium next-btn-normal next-pagination-item next-next' and not(@disabled)]")
        self.numberPage += 1
        currentUrl = f'https://aliexpress.ru/wholesale?SearchText={self.searchName}&page={self.numberPage}'
        if isPaginator and (countPage>1):
            self.browser.get(currentUrl)
            self.getProductsDetail(countPage-1)
        else:
            print('\nВсе страницы обработали')
            self.browser.close()



if __name__ == '__main__':
    test = crawlerAliexpress('собачка', 1)
    test.getProductsDetail(4)
    test.saveInCsv('out.csv')
