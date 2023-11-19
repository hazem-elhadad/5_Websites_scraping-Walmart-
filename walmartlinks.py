import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd
from selenium.webdriver.chrome.options import Options
driver = uc.Chrome()
inputurl = input("Enter category url: ")
links_list=[]
file=open('walmartlinks.csv','w',encoding='utf-8',newline='')
csv_writer=csv.writer(file)
csv_writer.writerow(['Link'])
i=0
v=0
if ('page=') in inputurl:
    print(f"We are now in {inputurl[inputurl.find('page='):]}")
    needed_page = int(input("Enter a page to start from: "))
    inputurl = inputurl.replace(inputurl[inputurl.find('page='):],f'page={needed_page}')
driver.get(inputurl)
while True:
    if ('page=') in inputurl:
        inputurl = inputurl.replace(inputurl[inputurl.find('page='):],f'page={needed_page}')
        print(inputurl)
        driver.get(inputurl)
        print(f"We are now in page {needed_page}")
    driver.get(inputurl)
    try:
        if driver.find_element(By.CSS_SELECTOR, '#px-captcha'):
            sleep(1)
            element = driver.find_element(By.CSS_SELECTOR, '#px-captcha')
            action = ActionChains(driver)
            action.click_and_hold(element)
            action.perform()
            sleep(10)
            action.release()
            action.perform()
            sleep(5)

    except:
        pass
    try:
        print("stage 0")
        table_data = driver.find_element(By.CSS_SELECTOR,
                                         '#maincontent > main > div > div > div > div > div.w-100.relative-m.pl4.pr4.flex.pt2 > div.relative.w-80 > div > section').find_element(
            By.XPATH, './div').find_elements(By.TAG_NAME, 'div')
        print("stage 1")
        for product in table_data:
            try:
                element_sku = product.find_element(By.XPATH, './div').find_element(By.XPATH,
                                                                                   './div/a').get_attribute(
                    'link-identifier')
                if element_sku != "itemClick":
                    element_href = product.find_element(By.XPATH, './div').find_element(By.XPATH,
                                                                                        './div/a').get_attribute(
                        'href')
                    print("stage 2")

                    csv_writer.writerow([element_href])
            except:
                pass

    except:
        pass
    try:
        next_butt = driver.find_element(By.CSS_SELECTOR,
                                 '#maincontent > main > div > div > div > div > div:nth-child(9) > nav > ul > li > a[data-testid="NextPage"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", next_butt)
    except:
        print("No more page")
        break
    needed_page+=1
x=0
file.close()
# driver.close()
main_data_frame = pd.read_csv("walmartlinks.csv")
writer = pd.ExcelWriter(r'walmartlinks.xlsx', engine='xlsxwriter')
main_data_frame.to_excel(writer, index=False)
writer.close()

# for alink in links_list:
#     x+=1
#     y = 0
#     while True:
#         try:
#             if driver.find_element(By.CSS_SELECTOR,'#px-captcha'):
#                 element = driver.find_element(By.CSS_SELECTOR,'#px-captcha')
#                 action = ActionChains(driver)
#                 click = ActionChains(driver)
#                 action.click_and_hold(element)
#                 action.perform()
#                 sleep(10)
#                 action.release(element)
#                 action.perform()
#                 sleep(2)
#                 action.release(element)
#             if driver.find_element(By.CSS_SELECTOR, 'head > script:nth-child(18)').get_attribute("innerHTML"):
#                 break
#         except:
#             y+=1
#             if y ==5:
#                 print("limit of try")
#                 break
#     sku="None"
#     gtin="None"
#     price="None"
#     brand = "None"
#     availability="None"
#     driver.get(alink)
#     print(f"Scraping product number {x}")
#     # if x == 5:
#     #     break
#     try:
#         data = driver.find_element(By.CSS_SELECTOR, 'head > script:nth-child(18)').get_attribute("innerHTML")
#     except:pass
#     try:
#         required_string_gtin = data[data.find('gtin13') + len('gtin13'):data.find('gtin13') + 60]
#         gtin_string_mark1 = required_string_gtin.find(':')
#         gtin_string_mark2 = required_string_gtin.find(',')
#
#         gtin=required_string_gtin[gtin_string_mark1 + 1:gtin_string_mark2].replace('"', '')
#         required_string_sku = data[data.find('sku') + len('sku'):data.find('sku') + 60]
#         sku_string_mark1 = required_string_sku.find(':')
#         sku_string_mark2 = required_string_sku.find(',')
#         sku=required_string_sku[sku_string_mark1 + 1:sku_string_mark2].replace('"', '')
#
#         name = driver.find_element(By.CSS_SELECTOR ,'#main-title').text
#         depprice = data[data.find('price') + len('price'):data.find('price') + 60]
#         the_price = re.findall(r'\d+', depprice)
#         if len(the_price) > 1:
#             price = the_price[0] + ',' + the_price[1]
#         else:
#             price=the_price[0]
#         try:
#             # brand_table1 = driver.find_element(By.CSS_SELECTOR,'#maincontent > section > main > div.flex.undefined.flex-column.h-100 > div:nth-child(2) > div > div.w_aoqv.w_wRee.w_p0Zv > div > div > section[aria-describedby="delivery-instructions"]')
#             # brand_table2 = brand_table1.find_element(By.XPATH ,'./div[@data-testid="ui-collapse-panel"]').find_element(By.XPATH,'./div').find_element(By.XPATH ,'./div').find_elements(By.TAG_NAME ,'div')
#             # print(len(brand_table2))
#             # print("HOLLLLLLLLAAAAAA")
#             # for a_product in brand_table2 :
#             #     print("For LOOOOOOOOOOOOOOPP")
#             #     [print(a_product.text)]
#             #     if "Brand" in a_product.find_element(By.TAG_NAME,'h3').text:
#             #         print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
#             required_string_brand = data[data.find('Brand') + len('Brand'):data.find('Brand') + 60]
#             brand_string_mark1 = required_string_brand.find(':')
#             brand_string_mark2 = required_string_brand.find('}')
#             brand =required_string_brand[brand_string_mark1 + 1:brand_string_mark2].replace('"', '')
#         except:pass
#         try:
#             avail = data[data.find('availability') + len('availability'):data.find('availability') + 80]
#             if "InStock" in avail:
#                 availability ="In stock"
#         except:pass
#         csv_writer.writerow([alink, sku ,gtin ,name ,price , brand , availability])
#     except:pass
# file.close()
# main_data_frame = pd.read_csv("walmart.csv")
# writer = pd.ExcelWriter(r'walmartdata.xlsx', engine='xlsxwriter')
#
# main_data_frame.to_excel(writer, index=False)
# writer.close()