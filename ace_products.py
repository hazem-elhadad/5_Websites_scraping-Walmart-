import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import re
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import csv
from time import sleep
driver = uc.Chrome()
file=open('ace.csv','w',encoding='utf-8',newline='')
csv_writer=csv.writer(file)
csv_writer.writerow(['URL' ,'UPC','Name','Price' ,'Brand','Availability'])
df=pd.read_excel('acelinks.xlsx')
print(len(df['URL']))
i=0
for index, row in df.iterrows():
    i+=1
    print(f"Scraping product {i}")
    if i == 10 :
        break
    name = "NULL"
    the_price = ""
    brand = "NULL"
    upc = "NULL"
    availability = "NULL"
    try:
        driver.get(row['URL'])
        try:
            upc_dt = re.search(r'"upc":"(.*?)"', driver.page_source)
            upc = upc_dt.group(1)
        except:pass
        try:
            sku_dt = re.search(r'"productCode":"(.*?)"', driver.page_source)
            sku = sku_dt.group(1)
        except:pass
        try:
            price_pattern = r'"price":\s*{"onSale":\s*(true|false),\s*"msrp":\s*([\d.]+),\s*"price":\s*([\d.]+),\s*"priceType":\s*"(.*?)",\s*"catalogListPrice":\s*([\d.]+),\s*"effectivePricelistCode":\s*"(.*?)",\s*"priceListEntryCode":\s*"(.*?)",\s*"priceListEntryMode":\s*"(.*?)"'

            # Search for the price pattern in the JSON data
            match = re.search(price_pattern, driver.page_source)
            if match:
                on_sale, msrp, price, price_type, catalog_list_price, effective_pricelist_code, price_list_entry_code, price_list_entry_mode = match.groups()
                the_price= price
            # price_dt = re.search(r'"catalogListPrice":"(.*?)"', driver.page_source)
            # price = driver.find_element(By.CSS_SELECTOR ,'.custom-price mz-price').text
        except:pass
        try:
            if the_price =="":
                the_price = driver.find_element(By.CSS_SELECTOR ,'#product-actions-wrap > div.product-pricing-info.product-info-section.row > div > div').text
        except:pass
        try:
            name_dt = re.search(r'"productName":"(.*?)"', driver.page_source)
            name = name_dt.group(1)
        except:
            pass
        try:
            brand_dt = re.search(r'"tenant~brand-name-attribute":"(.*?)"', driver.page_source)
            brand = brand_dt.group(1)
        except:pass
        try:
            # driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR , '#product-actions-wrap > div.product-fullfillment-info.product-info-section'))
            # driver.execute_script("window.scrollBy(0, 200);")
            availability = row['Availability']
        except:pass
        csv_writer.writerow([row['URL'], upc, name, price, brand, availability])
    except:pass


driver.close()
file.close()
main_data_frame = pd.read_csv("ace.csv")
writer = pd.ExcelWriter(r'ace.xlsx', engine='xlsxwriter')

main_data_frame.to_excel(writer, index=False)
writer.close()
