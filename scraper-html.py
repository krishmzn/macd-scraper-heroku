import email
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.policy import SMTP
from msilib.schema import File
import smtplib
import os

from email.message import EmailMessage
import ssl

from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #wating for content to load
from selenium.webdriver.support import expected_conditions as EC #required for passing 
from selenium.webdriver.common.keys import Keys
import pandas as pd

# email list of people we want ot email to
# emaillist = ['angelamaharjan96@gmail.com', 'kimmhrz@gmail.com', 'supalamhrzn@gmail.com']
emaillist = ['kimmhrz@gmail.com']


path = 'C:\\Users\Krish Maharjan\Downloads\edgedriver_win64\msedgedriver.exe'
driver = webdriver.Edge(executable_path=path)

driver.get("https://nepsealpha.com/trading-signals/tech")

tkr = [ ]
macds = [ ]

driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

# selecting 100 rows on the table from the default 10
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#funda-table_length > label > select"))).click()
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#funda-table_length > label > select > option:nth-child(4)"))).click()

# loop for 2 pages
for j in range(2):
    # For Ticker
    driver.implicitly_wait(5)
    tickers = driver.find_elements_by_css_selector("#funda-table > tbody > tr > td.fixed-left-header")
    for ticker in tickers:
        tkr.append(ticker.text)
        
    # For MACD
    macd = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div/div/div[3]/div[2]/table/tbody/tr/td[11]")
    for i in macd:
        macds.append(i.text)
        
    # Navigate to Next Page    
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div/div/div/div[2]/div/div/div/div[5]/a[2]"))).click()

# Creating a dataframe
df = {'TICKER': tkr, 'MACD': macds}
dataset = pd.DataFrame.from_dict(df, orient = 'index')
dataset = dataset.transpose()

# Removing duplicate entries
dataset = dataset.drop_duplicates()

# Filtering Data
bullish = dataset.loc[dataset['MACD'] == 'Bullish']
bullish_list = bullish['MACD']

# Creating Variables
EMAIL_FROM = 'krishmzn69@gmail.com'
SMTP_PASSWORD = 'iciilcvizsgdtqsv'
EMAIL_TO = 'kimmhrz@gmail.com'

EMAIL_SUBJECT = 'Positive MACD breakouts of the day'
MESSAGE_BODY = 'MACD technical analysis summary'


def send_mail():
    
    msg = MIMEMultipart("alternative")
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    
    # Create the plain-text and HTML version of your message
    html = """\
        <!DOCTYPE html>
<html lang="en">
<head>
    <!-- css -->
    <style>
        h2, h4{
            color:#000;
        }
    </style>
</head>
<body>
    <!-- body -->
    <h2>Tickers with positive breakouts today</h2>
    <h4>$(data)</h4>
</body>
</html>
            """
        
    html = html.replace("$(data)", bullish_list)
    part1 = MIMEText(html, "html")

    # HTML/plain-text parts to MIMEMultipart message
    msg.attach(part1)
    # Converting the message to a string and send it
    context = ssl.create_default_context()
    
    # looping through email list
    for mail_loop in emaillist:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_FROM, SMTP_PASSWORD)
            smtp.sendmail(EMAIL_FROM, mail_loop, msg.as_string())
     
send_mail()