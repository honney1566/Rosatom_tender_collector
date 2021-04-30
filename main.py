from bs4 import  BeautifulSoup
import pandas as pd
import cbmcodecs
import requests
names=[]
prices=[]
proccessed=[]
URL=[]
URLS=[]
df = pd.DataFrame({'ID' : ()})
source_code = requests.get('http://www.zakupki.rosatom.ru/Web.aspx?node=currentorders&ostate=P&page=2')
numberr=input('How many pages')
budget=input('What will be the budget')
i=1
while i<int(numberr)+1:
    source_code = requests.get('http://www.zakupki.rosatom.ru/Web.aspx?node=currentorders&ostate=P&page='+str(i))
    soup = BeautifulSoup(source_code.content, 'lxml')
    soup.select('tbody')
    containers = soup.find_all('tr', {'class': 'even'})
    for container in containers:
        if container.find('div', {'class': 'description'}) is not None:
            name = container.find('a')
            names.append(name.text)
            price=container.find('td',{'class':'price text-right'})
            prices.append(str(price.find('p')))
            URL='http://www.zakupki.rosatom.ru'+name.get('href')
            URLS.append(URL)
    containers = soup.find_all('tr', {'class': 'odd'})
    for container in containers:
        if container.find('div', {'class': 'description'}) is not None:
            name = container.find('a')
            names.append(name.text.encode('utf-8').decode('utf-8'))
            price=container.find('td',{'class':'price text-right'})
            prices.append(str(price.find('p')))
            URL='http://www.zakupki.rosatom.ru'+name.get('href')
            URLS.append(URL)
    i=i+1
df.insert(1, 'Name', pd.Series(names))
df.insert(2, 'Prices', pd.Series(prices))
df.insert(3, 'URL', pd.Series(URLS))
del df['ID']
for price in df.iloc[:,1]:
    x1=price.replace(" ", "")
    x2=x1.replace(',', '.')
    x3=x2.replace('<p>', '')
    x4=x3.replace('</p>', '')
    proccessed.append(x4)
df.insert(2,'Price', pd.Series(proccessed))
del df['Prices']
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
#print(df)
df = df.drop(df[df.Price < int(budget)].index)
print(df)
df.to_csv(r'C:\Users\Eduard\Desktop\projects.csv', encoding='utf-8-sig')