from bs4 import BeautifulSoup
import requests
import smtplib

sender_email = 'youemailaddresss'
# app password to login
python = "secure_code_to_sendemail"
# list of receivers mails
receivers = []

#list of item you want to buy

list_of_url = [
    "https://www.amazon.in/gp/product/B09TTSM8HB/ref=sw_img_1?smid=A14CZOWI0VEHLG&psc=1"
]
# list of corresponding minimum price
to_buy_price = [7000]
for i in range(len(list_of_url)):
    item = list_of_url[i]
    response = requests.get(url=item)
    soup = BeautifulSoup(response.text, "html.parser")
    t = soup.find(name="span", class_="a-price-whole")
    print(t.getText)
    l = t.get_text()
    final_price = l.replace(",", "")
    final_price = int(float(final_price.removesuffix(".")))
    print(final_price)
    if final_price < to_buy_price[i]:
        for receviers_address in receivers:
            connection = smtplib.SMTP("smtp.gmail.com")
            connection.starttls()
            connection.login(user=sender_email, password=python)
            connection.sendmail(from_addr=sender_email, to_addrs=receviers_address, msg=f"price-alert/n/n/n {item} to buy")
            connection.close()
