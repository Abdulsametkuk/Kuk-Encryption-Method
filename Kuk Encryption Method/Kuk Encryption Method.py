import customtkinter as ctk  # GUI arayüzü için customtkinter kütüphanesini import ettik
from tkinter import messagebox 

# EBOB hesaplama fonksiyonu. a ve n'nin aralarında asal olup olmadığını kontrol etmek için ebob işlemi gerçekleştirdik
# Affin de olan bir kuraldır.
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Modüler tersini bulma fonksiyonu
# Deşifreleme sırasında çarpma anahtarının tersi var mı yok mu diye kontrol edip eğer varsa çarpma anahtarının tersini aldık. 3^-1 = 9 gibi
def mod_ters(a, n):
    t, yeni_t = 0, 1
    r, yeni_r = n, a
    while yeni_r != 0:
        bolum = r // yeni_r
        t, yeni_t = yeni_t, t - bolum * yeni_t
        r, yeni_r = yeni_r, r - bolum * yeni_r
    if r > 1:
        raise ValueError("{} sayısının mod {} için tersi yok".format(a, n))
    if t < 0:
        t = t + n
    return t

def kukari_sifrele(duz_metin, m, a, b, n=26):  # m: anahtar uzunluğu, a: çarpma anahtarı, b: kaydırma anahtarı 
    k = [i+1 for i in range(m)]   # anahtar uzunluğu kadar bir başlangıç anahtar oluşturduk. m = 5 ise k = [1, 2, 3, 4, 5]  
    sifreli_metin = ''
    for i in range(0, len(duz_metin), m): # metnin hangi yerden bloklara ayrılacağını belirledik ve bloklara ayırdık
        blok = duz_metin[i:i+m] # Burada metne ait blokları sırası ile aldık 
        for j in range(len(blok)): # Blok uzunluğu kadar döngü oluşturduk 
            kaydir = (ord(blok[j]) - ord('A') + k[j]) % 26 # ord(blok[j]) - ord('A') fonksiyonu her bir harfin alfabedeki sırasını bulduk ve k[j] ile kaydırma işlemi yaptık
            sifreli_metin += chr(kaydir + ord('A'))   # kaydırma sonucunda elde ettiğimiz harfleri sifreli_metin'e ekledik
        k = [(x + 1) % 26 for x in k] # Anahtarları birer birer kaydırarak gücelledik
    if gcd(a, n) != 1:
        raise ValueError("Çarpma anahtarı ve alfabe boyutu aralarında asal olmalı")
    sonuc = ''
    for char in sifreli_metin:
        P = ord(char) - ord('A')
        C = (a * P + b) % n
        sonuc += chr(C + ord('A'))
    return sonuc

def kukari_desifre(sifreli_metin, m, a, b, n=26): # Burada da şifreleme işlemine ait adımların tam tersini yaptık
    a_tersi = mod_ters(a, n)
    desifreli_metin = ''
    for char in sifreli_metin:
        C = ord(char) - ord('A')
        P = (a_tersi * (C - b)) % n  
        desifreli_metin += chr(P + ord('A'))
    k = [i+1 for i in range(m)]
    sonuc = ''
    for i in range(0, len(desifreli_metin), m):
        blok = desifreli_metin[i:i+m]
        for j in range(len(blok)):
            kaydir = (ord(blok[j]) - ord('A') - k[j]) % 26
            sonuc += chr(kaydir + ord('A'))
        k = [(x + 1) % 26 for x in k]
    return sonuc

def sifrele(): 
    try:
        metin = entry_text.get().upper()
        m = int(entry_m.get())
        a = int(entry_a.get())
        b = int(entry_b.get())
        sonuc = kukari_sifrele(metin, m, a, b)
        result_label.configure(text="Şifrelenmiş Metin: {}".format(sonuc))

    except Exception as e:
        messagebox.showerror("Hata", str(e))

def desifrele():  
    try:
        metin = entry_text.get().upper()
        m = int(entry_m.get())
        a = int(entry_a.get())
        b = int(entry_b.get())
        sonuc = kukari_desifre(metin, m, a, b)
        result_label.configure(text="Deşifrelenmiş Metin: {}".format(sonuc))

    except Exception as e:
        messagebox.showerror("Hata", str(e))

# Arayüzü oluşturduk
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Kuk Şifreleme")
root.geometry("500x400")

ctk.CTkLabel(root, text="Metin:").pack()
entry_text = ctk.CTkEntry(root, width=300)
entry_text.pack()

ctk.CTkLabel(root, text="Anahtar Uzunluğu (m):").pack()
entry_m = ctk.CTkEntry(root)
entry_m.pack()

ctk.CTkLabel(root, text="Çarpma Anahtarı (a):").pack()
entry_a = ctk.CTkEntry(root)
entry_a.pack()

ctk.CTkLabel(root, text="Kaydırma Anahtarı (b):").pack()
entry_b = ctk.CTkEntry(root)
entry_b.pack()

sifrele_button = ctk.CTkButton(root, text="Şifrele", command=sifrele)
sifrele_button.pack(pady=5)

desifrele_button = ctk.CTkButton(root, text="Deşifrele", command=desifrele)
desifrele_button.pack(pady=5)

result_label = ctk.CTkLabel(root, text="Sonuç:")
result_label.pack()

root.mainloop() # Arayüzü çalıştırdık