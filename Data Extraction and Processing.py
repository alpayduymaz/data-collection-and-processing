### web sitesine istek yaparak içeriği soup değişkenine atandı.####
import requests

from bs4 import BeautifulSoup

url = "https://www.arabam.com/ikinci-el/otomobil/bmw-3-serisi"

r = requests.get(url)

soup = BeautifulSoup(r.content,"html.parser")

#web sitesininde araçların table kısmı gelen veri değişkenine atandı#
gelenveri = soup.find_all("table",{"class":"table listing-table w100 border-grey2"})
#araç tablosundaki tbody kısmı gelen veriden araçtablosu değişkenine atandı#
aractablosu = (gelenveri[0].contents)[len(gelenveri[0].contents)-1]

aractablosu = aractablosu.find_all("tr",{"class":"listing-list-item pr should-hover bg-white"})

import xlsxwriter

#cekilen veriler ön işleme yapılmadan excele yazdiriliyor
outworkbook  = xlsxwriter.Workbook('Veri.xlsx')
outsheet = outworkbook.add_worksheet()
outsheet.write("A1","RENK")
outsheet.write("B1","YIL")
outsheet.write("C1","KM")
outsheet.write("D1","FİYAT")
item = 0
for i in range(len(aractablosu)):
    kolon = aractablosu[i].find_all("td",{"class":"pl8 pr8 tac pr"})
    fiyat = kolon[0].text
    fiyat = fiyat.split()[0]
    outsheet.write(item+1, 3, fiyat)
    item += 1


item = 0
for i in range(len(aractablosu)):
    kolon = aractablosu[i].find_all("td",{"class":"listing-text pl8 pr8 tac pr"})
    yıl = kolon[0].text
    km = kolon[1].text
    renk = kolon[2].text
    renk = renk.split()[0]
    outsheet.write(item+1, 0, renk)
    outsheet.write(item+1, 1, yıl)
    outsheet.write(item+1, 2, km)
    item += 1

outworkbook.close() 

# Kütüphanelerin eklenmesi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Veri setinin okunarak bağımlı ve bağımsız değişkenlere ayrılması
dataset = pd.read_excel('Veri.xlsx', encoding = 'iso-8859-9')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 3].values
y = y.reshape(-1, 1) 

# Kategorik verilerin sayısallaştırılması
#One hot encoding
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

# Veri setinin eğitim ve test olarak bölünmesi
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Özellik ölçekleme
from sklearn.preprocessing import MinMaxScaler
sc_X = MinMaxScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = MinMaxScaler()
y_train = sc_y.fit_transform(y_train) 
y_test = sc_y.fit_transform(y_test) 

# Eğitim verileri ile modelin eğitilmesi
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Test verileri kullanılarak tahmin yapılması
y_pred = regressor.predict(X_test)




#Test değerleri ile tahmin değerleri arasındaki hata farkının hesaplanması
#Modelin başarısının ölçüldüğü kısım.
from sklearn.metrics import r2_score
r2_score(y_test, y_pred)

print(r2_score(y_test, y_pred))

print(y_pred)

#ön işleme yapılmış veriler excele yazdiriliyor
import xlsxwriter 

workbook = xlsxwriter.Workbook('ÖnislenmisVeri.xlsx') 
worksheet = workbook.add_worksheet()
row = 1

#önce kolon isimleri yazdiriliyor
worksheet.write("A1","RENK")
worksheet.write("B1","RENK")
worksheet.write("C1","RENK")
worksheet.write("D1","RENK")
worksheet.write("E1","RENK")
worksheet.write("F1","RENK")
worksheet.write("G1","RENK")
worksheet.write("H1","RENK")
worksheet.write("I1","YIL")
worksheet.write("J1","KM")

#veriler yazdiriliyor
for col,data in enumerate(X.T):
    worksheet.write_column(row, col, data)
       
    
workbook.close()
