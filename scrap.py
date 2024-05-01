from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


meta_report_column = ['Spent', 'Impressions', 'Cost Per Lead', 'Leads']
google_ads_column = ['Location', 'Cost', 'Clicks', 'Impressions', 'CTR', 'Leads', 'Phone Calls', 'Driving directions']

def is_header_present(table):
    header_elements = table.find_all(class_="headerRow")
    return header_elements[0] if header_elements else False

def get_header_columns(header_row):
    columns = header_row.find_all(class_="colName")
    return [column.text for column in columns]

def get_table_body(table):
    table_body = table.find(class_="tableBody")
    cells = table_body.find_all(class_="cell-value")
    return [cell.text for cell in cells]

def get_stats(tables, cloums):
    for table in tables:
        is_header = is_header_present(table)
        if is_header:
            header_colums = get_header_columns(is_header)
            if  header_colums == cloums:
                return(get_table_body(table))

def get_websites_analytics(kpis):
    return [kpi.find(class_='valueLabel').text for kpi in kpis]

def run_job(link):
    no_of_retries = 5
    try_no = 0
    while try_no < no_of_retries:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(options=options)
            driver.get(link)
            wait = WebDriverWait(driver, 10)
            tables = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "table")))
            buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tab-button")))
            meta_stats = []
            google_stats = []
            website_analytics = []
            for button in buttons:
                if button.text in ["Facebook Ads", "Google Ads"]:
                    button.click() 
                    time.sleep(10)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    tables = soup.find_all(class_="table")
                    if button.text == "Facebook Ads":
                        meta_stats = get_stats(tables, meta_report_column)
                    else:
                        google_stats = get_stats(tables, google_ads_column)
                elif button.text == "Website Analytics":
                    button.click()
                    time.sleep(10)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    kpis = soup.find_all(class_="kpimetric")
                    website_analytics = get_websites_analytics(kpis)
            email_template = f"""
                Dear Franchise Partner,
                As part of our ongoing monthly reporting process, I am reaching out to provide you with the necessary link for accessing your latest reports. You can access the report via the following link: {link}.
                Outlined below are the key highlights for your review:
                Facebook Ads Analytics: Budget Spent: {meta_stats[0]}, Impressions: {meta_stats[1]}, Cost per lead: {meta_stats[2]}, Leads: {meta_stats[3]}
                Google Ads Analytics: Budget Spent: {google_stats[1]}, Clicks: {google_stats[2]}, Impressions: {google_stats[3]}, CTR: {google_stats[4]}, Leads: {google_stats[5]}, Phone Calls: {google_stats[6]}, Driving Directions: {google_stats[7]}
                Booker Analytics: Total Budget Spent: {website_analytics[0]}, Advertising Conversions: {website_analytics[1]}, Cost per paid booking: {website_analytics[2]}
                Should you require a more detailed examination of our Customer Relationship Management (CRM) system, I am more than happy to schedule a thorough review session at your convenience.
                Additionally, please remember to utilize our text/email blast request form, accessible through the following link: Blast Request Form.
                Looking forward to discussing these insights with you further.
            """
            return(email_template)
        except:
            try_no = try_no + 1


run_job("https://lookerstudio.google.com/u/0/reporting/1490e4cc-bb28-4ce7-987b-5f6cb4cb2201/page/p_e3u5ash12c")

