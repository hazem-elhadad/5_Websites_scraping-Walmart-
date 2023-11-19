import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import csv
from selenium import webdriver

import re
import pandas as pd
driver = uc.Chrome()
x=0
file=open('walmartmaindatasample.csv','w',encoding='utf-8',newline='')
csv_writer=csv.writer(file)
csv_writer.writerow(['URL','SKU','UPC','Name','Price','Brand','Availability'])
df=pd.read_excel('walmartlinks.xlsx')
for row in df['Link']:
    alink=row
    driver.get(row)
    x+=1
    if x ==20:break
    y = 0
    while True:
        try:
            if driver.find_element(By.CSS_SELECTOR,'#px-captcha'):
                element = driver.find_element(By.CSS_SELECTOR,'#px-captcha')
                action = ActionChains(driver)
                click = ActionChains(driver)
                action.click_and_hold(element)
                action.perform()
                sleep(10)
                action.release(element)
                action.perform()
                sleep(2)
                action.release(element)
            if driver.find_element(By.CSS_SELECTOR, 'head > script:nth-child(18)').get_attribute("innerHTML"):
                break
        except:
            y+=1
            if y ==5:
                print("limit of try")
                break
    sku="None"
    gtin="None"
    price="None"
    brand = "None"
    availability="None"
    print(f"Scraping product number {x}")
    # if x == 20:
    #     break
    try:
        data = driver.find_element(By.CSS_SELECTOR, 'head > script:nth-child(18)').get_attribute("innerHTML")
    except:pass
    try:
        required_string_gtin = data[data.find('gtin13') + len('gtin13'):data.find('gtin13') + 60]
        gtin_string_mark1 = required_string_gtin.find(':')
        gtin_string_mark2 = required_string_gtin.find(',')

        gtin=required_string_gtin[gtin_string_mark1 + 1:gtin_string_mark2].replace('"', '')
        if gtin =="":
            gtin="NULL"
        required_string_sku = data[data.find('sku') + len('sku'):data.find('sku') + 60]
        sku_string_mark1 = required_string_sku.find(':')
        sku_string_mark2 = required_string_sku.find(',')
        sku=required_string_sku[sku_string_mark1 + 1:sku_string_mark2].replace('"', '')

        name = driver.find_element(By.CSS_SELECTOR ,'#main-title').text
        depprice = data[data.find('price') + len('price'):data.find('price') + 60]
        the_price = re.findall(r'\d+', depprice)
        if len(the_price) > 1:
            price = the_price[0] + '.' + the_price[1]
        else:
            price=the_price[0]+'.00'
        try:
            # brand_table1 = driver.find_element(By.CSS_SELECTOR,'#maincontent > section > main > div.flex.undefined.flex-column.h-100 > div:nth-child(2) > div > div.w_aoqv.w_wRee.w_p0Zv > div > div > section[aria-describedby="delivery-instructions"]')
            # brand_table2 = brand_table1.find_element(By.XPATH ,'./div[@data-testid="ui-collapse-panel"]').find_element(By.XPATH,'./div').find_element(By.XPATH ,'./div').find_elements(By.TAG_NAME ,'div')
            # print(len(brand_table2))
            # print("HOLLLLLLLLAAAAAA")
            # for a_product in brand_table2 :
            #     print("For LOOOOOOOOOOOOOOPP")
            #     [print(a_product.text)]
            #     if "Brand" in a_product.find_element(By.TAG_NAME,'h3').text:
            #         print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
            required_string_brand = data[data.find('Brand') + len('Brand'):data.find('Brand') + 60]
            brand_string_mark1 = required_string_brand.find(':')
            brand_string_mark2 = required_string_brand.find('}')
            brand =required_string_brand[brand_string_mark1 + 1:brand_string_mark2].replace('"', '')
            if brand =="":
                brand="NULL"
        except:pass
        try:
            avail = data[data.find('availability') + len('availability'):data.find('availability') + 80]
            if "InStock" in avail:
                availability ="In stock"
        except:
            try:
                if availability == "None" :
                    availability_dt =  re.search(r'"availabilityStatus":"(.*?)"', driver.page_source)
                    availability = availability_dt.group(1)
            except:pass

        csv_writer.writerow([alink, sku ,gtin ,name ,price , brand , availability])
    except:
        pass
    sleep(2)
file.close()
main_data_frame = pd.read_csv("walmartmaindatasample.csv")
writer = pd.ExcelWriter(r'walmartmaindatasample.xlsx', engine='xlsxwriter')

main_data_frame.to_excel(writer, index=False)
writer.close()