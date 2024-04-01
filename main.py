import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import ssl
import streamlit as st 

ssl._create_default_https_context = ssl._create_unverified_context

sehirler=["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
]

st.title('İmsakiye')
sehir=st.sidebar.selectbox('Şehir Seçiniz',sehirler,sehirler.index('Denizli'))
yedekSehir=sehir

islemler=['İmsakiye','İftara Kalan Süre']
islem=st.sidebar.selectbox('İşlem Seçiniz',islemler,islemler.index('İftara Kalan Süre'))

sehir=sehir.lower()
sehir=sehir.replace('ı','i')
sehir=sehir.replace('ç','c')
sehir=sehir.replace('ö','o')
sehir=sehir.replace('ü','u')
sehir=sehir.replace('ş','s')
sehir=sehir.replace('ğ','g')

df=pd.read_html(f'https://www.milliyet.com.tr/ramazan/imsakiye/{sehir}-iftar-vakti/')[0]
df['Tarih']=df['Tarih'].str.split('Gün ').str[1]
df['Tarih']=df['Tarih'].str.split(' ').str[0]+' '+df['Tarih'].str.split(' ').str[1]+' '+df['Tarih'].str.split(' ').str[2]

df['Tarih']=df['Tarih'].str.replace(' Mart ','-3-').str.replace(' Nisan ','-4-')
df['Tarih']=df['Tarih'].str.split('-').str[2]+'-'+df['Tarih'].str.split('-').str[1]+'-'+df['Tarih'].str.split('-').str[0]

df['Tarih']=df['Tarih'].astype(np.datetime64)
date=str(datetime.today().year)+'-'+str(datetime.today().month)+'-'+str(datetime.today().day)

simdi=datetime.now(pytz.timezone('Europe/Istanbul'))
simdi=simdi.strftime('%H:%M:%S')
simdi=pd.to_datetime(simdi)

iftar=df[date==df['Tarih']]['Akşam'].values[0]
iftar=pd.to_datetime(iftar)

iftaraKalanSure=pd.Timedelta(iftar-simdi)
check=str(iftaraKalanSure)
iftaraKalanSure=str(iftaraKalanSure).split('days ')[1]

saat=iftaraKalanSure.split(':')[0]+' Saat'
if iftaraKalanSure.split(':')[0]=='00':
    saat=''
elif saat[0]=='0':
    saat=saat.replace('0','')

dakika=iftaraKalanSure.split(':')[1]+' Dakika'
if iftaraKalanSure.split(':')[1]=='00':
    dakika=''
elif dakika[0]=='0':
    dakika=dakika.replace('0','')

saniye=iftaraKalanSure.split(':')[2]+' Saniye'

if saniye[0]=='0':
    saniye=saniye.replace('0','')

if '-1 days' not in check:
  if islem=='İftara Kalan Süre':
    st.subheader(f'{yedekSehir} şehri için iftara kalan süre: \n{saat} {dakika} {saniye}')  
else:
    st.success(f'{yedekSehir} Şehri için iftar saati gelmiştir.')   
if islem=='İmsakiye':
    st.subheader('Bugün')
    st.table(df[df['Tarih']==date])
    st.subheader(f'{yedekSehir} şehri için imsakiye')
    st.table(df)


 