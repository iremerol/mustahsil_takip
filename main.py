
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * #QWidgets.QApplication gibi yazımdan kurtulmak için bu şekilde import ettik
from mustahsil_anasayfa import*

Uygulama=QApplication(sys.argv) 
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna
penAna.show()
#VERİTABANI OLUŞTURMA 
import sqlite3
global curs
global conn
conn=sqlite3.connect('veritabanı.db')
curs=conn.cursor() #connection adlı değişkenin cursor fonksiyonundan bir tane "curs" adlı nesne örnekliyoruz
sorguCreTblMustahsil=("CREATE TABLE IF NOT EXISTS mustahsil(        \
                     Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    \
                TARİH TEXT NOT NULL UNIQUE,                        \
                TC TEXT NOT NULL,                       \
                AD TEXT NOT NULL,                           \
                SOYAD TEXT NOT NULL,                              \
                IKAMETGAH TEXT NOT NULL,                            \
                URUN TEXT NOT NULL,                               \
                BIRIM TEXT NOT NULL,                              \
                MIKTAR TEXT NOT NULL)")

curs.execute(sorguCreTblMustahsil)
conn.commit() 

#VERİTABANINA KAYDET
def ekle(): 
    _clnTarih=ui.clntarih.selectedDate().toString(QtCore.Qt.ISODate)
    _lneTck=ui.lneTck.text()
    _lneAd=ui.lneAd.text()
    _lneSoyad=ui.lneSoyad.text()
    _lneIkametgah=ui.lneIkametgah.text()
    _cmbUrun=ui.cmbUrun.currentText()
    _spnBirim=ui.spnBirim.value()
    _spnMiktar=ui.spnMiktar.value()
    curs.execute("INSERT INTO mustahsil \
                    (TARİH,TC,AD,SOYAD,IKAMETGAH,URUN,BIRIM,MIKTAR) \
                    VALUES(?,?,?,?,?,?,?,?)", \
                    (_clnTarih,_lneTck,_lneAd,_lneSoyad,_lneIkametgah, _cmbUrun,_spnBirim,
                    _spnMiktar))
    conn.commit()
    listele()
#listelee
def listele():
    ui.tblwBilgiler.clear()
    ui.tblwBilgiler.setHorizontalHeaderLabels(('No','TARİH','TC','AD','SOYAD','IKAMETGAH','URUN','FIYAT','MIKTAR'))#sütunların isimleri belirlenir
    ui.tblwBilgiler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#sıkıştırılmış halde alcak
    curs.execute("SELECT * FROM mustahsil")#cursor e sorgu atayacağız
    for satırIndeks,satırVeri in enumerate(curs):#sorgumuzu enumerate e veriyoruz
         for sutunIndeks,sutunVeri in enumerate(satırVeri):
            ui.tblwBilgiler.setItem(satırIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.lneTck.clear()
    ui.lneAd.clear()
    ui.lneSoyad.clear()
    ui.lneIkametgah.clear()
    ui.cmbUrun.setCurrentIndex(-1)
    ui.spnBirim.setValue(55)
    ui.spnMiktar.setValue(55)
    curs.execute("SELECT  COUNT(*) FROM mustahsil"
    kayitSayisi=curs.fetchone()
    ui.lblKayitSayisi.setText(str(kayitSayisi[0]))
      
listele()

#cıkıs 
def cikis():
     cevap=QMessageBox.question(penAna,"CIKIS","Programdan cıkmak istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
     
     if cevap==QMessageBox.Yes:
         conn.close()#veritabanı bağlantısını kapatsın
         sys.exit(Uygulama.exec_())#sistemden çıksın
     else:
        penAna.show()#pencereyi tekrardan göstersin

#sil
def sil():
       cevap=QMessageBox.question(penAna,"KAYIT SİL","Kaydı silmek  istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
       if cevap==QMessageBox.Yes:
           secili=ui.tblwBilgiler.selectedItems()  
      
           silinecek=secili[1].text() 
         
           try:
               curs.execute("DELETE FROM mustahsil WHERE TC='%s'"%(silinecek))
               conn.commit()
               listele() 
              
               ui.statusbar.showMessage("KAYIT SİLME BASARIYLA GERCEKLESTİ",10000) #10sn ekranda bu mesaj gösterilecek
               
           except Exception as Hata:
                ui.statusbar.showMessage("Söyle bir hata ile karsılasıldı.."+str(Hata)) #hata string olduğu için mesajla gösterilecek
       else:
           ui.statusbar.showMessage("SİLME İSLEMİ İPTAL EDİLDİ",10000)
def ara():
    aranan1=ui.lneTck.text()
    aranan2=ui.lneAd.text()
    aranan3=ui.lneSoyad.text()
    curs.execute("SELECT * FROM mustahsil WHERE TC=? OR AD=? OR SOYAD=? OR (AD=? AND SOYAD=? )",
                 (aranan1,aranan2,aranan3,aranan2,aranan3)) 
    conn.commit() 
    #table widget içerisine gerekli bilgileri getiricez
    ui.tblwBilgiler.clear()
    for satırIndeks,satırVeri in enumerate(curs):
         for sutunIndeks,sutunVeri in enumerate(satırVeri):
            ui.tblwBilgiler.setItem(satırIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
def doldur():
#mesela tablewidgettan seçtiğimiz müşteride  güncelleme yapacağğız ve seçili olan müşterilerin bilgilerini yukarıdakş boş alanlara doldurmak istiyoruz bu yüzden doldur adlı fonksiyonu kullanıcaz
      secili=ui.tblwBilgiler.selectedItems() #tablewidgettan seçmiş olduğumuz kaydı(ui.tblwBilgiler.selectedItems())  secili adlı bir değişkene atayalım
      yil=int(secili[1].text()[0:4]) 
     
      ay=int(secili[1].text()[5:7]) 
      gun=int(secili[1].text()[8:10]) 
      ui.clntarih.setSelectedDate(QtCore.QDate(yil,ay,gun)) 
      
     
      ui.lneTck.setText(secili[2].text()) 
    
      ui.lneAd.setText(secili[3].text()) #ad 2.indiste
      
      ui.lneSoyad.setText(secili[4].text())
      
      ui.lneIkametgah.setText(secili[5].text())
      
      ui.cmbUrun.setCurrentText(secili[6].text()) 
   
     
      ui.spnBirim.setValue(int(secili[7].text()))
     
      ui.spnMiktar.setValue(int(secili[8].text()))

def guncelle():
     cevap=QMessageBox.question(penAna,"KAYIT GUNCELLE","Kaydı güncellmek  istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
     if cevap==QMessageBox.Yes:
         try:
             secili=ui.tblwBilgiler.selectedItems()
             _Id=int(secili[0].text()) 
             _clnTarih=ui.clntarih.selectedDate().toString(QtCore.Qt.ISODate)
             _lneTck=ui.lneTck.text()
             _lneAd=ui.lneAd.text()
             _lneSoyad=ui.lneSoyad.text()
             _lneIkametgah=ui.lneIkametgah.text()
             _cmbUrun=ui.cmbUrun.currentText()
             _spnBirim=ui.spnBirim.value()
             _spnMiktar=ui.spnMiktar.value()
             curs.execute("UPDATE mustahsil SET  TARİH=?,TC=?,AD=?,SOYAD=?,IKAMETGAH=?,URUN=?,BIRIM=?,MIKTAR=? WHERE Id=?" ,\
                         (_clnTarih,_lneTck,_lneAd,_lneSoyad,_lneIkametgah, _cmbUrun,_spnBirim,\
                          _spnMiktar,_Id))
                    
             conn.commit()
             listele()
         except Exception as Hata:
             ui.statusbar.showMessage("Şöyle bit hata meydana geldi"+str(Hata))
             
     else:
        ui.statusbar.showMessage("Güncelleme iptal edildi",10000)    
          
#butonlar
ui.btnekle.clicked.connect(ekle)
ui.btnlistele.clicked.connect(listele)
ui.btncikis.clicked.connect(cikis)
ui.btnsil.clicked.connect(sil)
ui.btnara.clicked.connect(ara)
ui.tblwBilgiler.itemSelectionChanged.connect(doldur)
ui.btnguncelle.clicked.connect(guncelle)

sys.exit(Uygulama.exec_())
