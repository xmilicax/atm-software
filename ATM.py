import random
import os
import sys
from tkinter import messagebox

with open ("baza.txt", "r", encoding="utf-8") as fajl :
        lista = [red.split() for red in fajl]
        i = len(lista)
        
## odabirrandom korisnika iz baze podataka
brRac = random.randint(0, i-1) 
print('Redni broj računa je: ', brRac)

def br_racuna():
    global brRac
    global brojRacuna
    
    ## štampanje broja računa korisnika
    brojRacuna = lista[brRac][2]  
    return brojRacuna

br = 0  
def provera():
    global br
    global brRac
    izlaz = False

    while True:
         ## provera unosa PIN-a
         if PIN.get() == lista[brRac][3]:
            ## ukoliko je PIN ispravan
            raise_frame(meni_str)         
            break
         else:
            ## ukoliko PIN nije ispravan
            br += 1                           
            PIN.set('')
            ## ako je korisnik iskoristio dozvoljeni broj unosa PIN-a
            if br == 3:                     
                obavestenje_login_label['text']="Uneli ste netačan PIN maksimalni broj puta. \nMolimo pokušajte kasnije."
                login_button.grid_forget()
                return False
            ## ako korisnik nije iskoristio dozvoljeni broj unosa PIN-a
            else:                           
               obavestenje_login_label['text']='Uneli ste netačan PIN. Pokušajte ponovo.'
               break

            
def ime_korisnika():
    global brRac
    global korisnik

    ## štampanje imena korisnika kojeg ćemo prikazati na meni strani
    korisnik = lista[brRac][1]  
    return korisnik

## automatski unos u Entry polje na strani za uplatu
def automatski_unos_uplata(unos): 
    UplataEntry.delete(0, END)
    UplataEntry.insert(0, unos)
    return

## automatski unos u Entry polje na strani za isplatu
def automatski_unos_isplata(unos): 
    IsplataEntry.delete(0, END)
    IsplataEntry.insert(0, unos)
    
## uzimanje vrednosti koju korisnik ima na računu
stanje_iznos = lista[brRac][4]  

## funkcija za uplatu na račun
def uplata():              
    global stanje_iznos
    global brRac
    uplata_iznos = UplataEntry.get()
    
    uplata_iznos = float(uplata_iznos)
    stanje_iznos = float(stanje_iznos)
    
    stanje_iznos += uplata_iznos
    ## formatiranje iznosa na dve decimale
    stanje_iznos = "{:.2f}".format(stanje_iznos) 
    ## ažuriranje vrednosti stanja na računu
    lista[brRac][4] = stanje_iznos               

    a=0
    ## ažuriranje baze podataka 
    with open("baza.txt", "w", encoding="utf-8") as fajl:  
        for a in range(0, i):
            for x in range(4):
                fajl.write(lista[a][x]+ ' ')
            fajl.write(str(lista[a][4])+ '\n')

            
    messagebox.showinfo('Potvrda o uplati', 'Uplata je izvršena.')
    
    ## čišćenje Entry polja i slanje korisnika na meni stranu
    UplataEntry.delete(0, END)   
    raise_frame(meni_str)
    
    ## vraćanjd vrednost stanja na računu kao rezultat funkcije
    return stanje(stanje_iznos) 
    
                   
def isplata():
    global stanje_iznos
    global brRac
    
    while True:
        isplata_iznos = IsplataEntry.get()
        
        stanje_iznos = float(stanje_iznos)
        isplata_iznos = float(isplata_iznos)

        ## provera da li korisnik ima mogućnost da izvrši željenu isplatu
        if isplata_iznos > stanje_iznos:  
            messagebox.showinfo('Greška pri isplati', 'Nije moguće izvršiti isplatu, jer je uneti iznos je veći od trenutnog na računu.\nPokušajte ponovo.')
        else:
            ## izvršavanje isplate
            stanje_iznos -= isplata_iznos  
            stanje_iznos = "{:.2f}".format(stanje_iznos)
            lista[brRac][4] = stanje_iznos

            a=0
            ## ažuriranje baze podataka 
            with open("baza.txt", "w", encoding="utf-8") as fajl:  
                for a in range(0, i):
                    for x in range(4):
                        fajl.write(lista[a][x]+ ' ')
                    fajl.write(str(lista[a][4])+ '\n')
                
                        
            messagebox.showinfo('Potvrda o isplati', 'Isplata je izvršena.')

            ## čišćenje Entry polja i slanje korisnika na meni stranu
            IsplataEntry.delete(0, 'end')   
            raise_frame(meni_str)
        ## vraćanje vrednosti stanja na računu kao rezultat funkcije
        return stanje(stanje_iznos)   

def stanje(stanje_iznos):
    ## menjanje Label na stani Stanje
    stanje_label['text']= str(stanje_iznos)  


def izlaz():
    ## ažuriramo bazu podataka 
    with open("baza.txt", "w", encoding="utf-8") as fajl:  
        for brRac in range(i):
            for x in range(4):
                fajl.write(lista[brRac][x]+ ' ')
            fajl.write(str(lista[brRac][4])+ '\n')
    ## restartovanje programa za novog korisnika, moguće da ne radi na svim Python verzijama    
    os.execl(sys.executable, sys.executable, *sys.argv)  
    

## MASTER -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from tkinter import *
from tkinter import ttk
import tkinter as tk


## Master izgled prozora
root = Tk()
root.title('Ablanco ATM')
root.iconbitmap('slike/icon.ico')
root.geometry('1280x829')
root.resizable(False, False)

#frame-ovi
pocetna_str = Frame(root)
login_str = Frame(root)
meni_str = Frame(root)
uplata_str = Frame(root)
isplata_str = Frame(root)
stanje_str = Frame(root)
izlaz_str = Frame(root)

#definisanje funkcije za pozivanje frame-ova
def raise_frame(frame):
    frame.tkraise()

for frame in (pocetna_str, login_str, meni_str, uplata_str, isplata_str, stanje_str, izlaz_str):
    frame.grid(row=0, column=0, sticky='news')

##POČETNA STRANA--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
img = PhotoImage(file='slike/background.png')
Button(pocetna_str,
       image = img,
       command = lambda:raise_frame(login_str)).grid(row=0, column=0)  


##LOGIN STRANA----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
img_logo = PhotoImage(file='slike/ablanco-mala.png')
logo_meni = Label(login_str, image=img_logo).grid(row=0, column=0)

br_racuna()

Label(login_str,
      text='Broj računa: ' + str(brojRacuna),
      font= ('Arial', 25)).grid(row=1, column=1, pady=80)

PINLabel = Label(login_str,
           text="Unesite PIN",
           font= ('Montserrat', 20)).grid(row=2, column=1)

PIN = StringVar()

PINEntry = Entry(login_str,
           show='*',
           textvariable = PIN,
           font= ('Montserrat', 30),
           width=15,
           justify=CENTER).grid(row=3, column=1, pady=20)  


login_button = Button(login_str,
               text='O K',
               font= ('Montserrat', 14),
               relief='raised',
               bg='#FDEB30',
               activebackground="blue",
               activeforeground='white',
               borderwidth=1.5,
               width=20,
               height=3,
               command=provera)

## odvojeno pozicioniranje Login dugmeta, odnosno .grid jer prethodno, tj. zajedno sa prethodnim blokom vraća 'NoneType', što nije odgovarajuće
login_button.grid(row=5, column=1, pady=30)   

obavestenje_login_label = Label(login_str,
                          text=" ",
                          fg ='red',
                          font= ('Arial', 14,))
obavestenje_login_label.grid(row=6, column=1)

nazad_button = Button(login_str,
               text='Nazad',
               font= ('Montserrat', 14),
               relief='raised', 
               bg='#FDEB30',
               activebackground='orange',
               activeforeground='white',
               borderwidth=1.5,
               width=20,
               height=3,
               command = izlaz).place(x=950, y=630)


##MENI STRANA-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
logo_meni = Label(meni_str, image=img_logo).place(x=0, y=0)

dobrosli_label = Label(meni_str,
                 text='Dobrodošli ' + str(ime_korisnika()) + '!',
                 anchor='center',
                 font= ('Montserrat', 42)).place(x=380, y=90)

naslov_label = Label(meni_str,
               text='Izaberite uslugu',
               anchor='center',
               font= ('Montserrat', 30)).place(x=460, y=210)


uplata_button = Button(meni_str,
                text='U P L A T A',
                font= ('Montserrat', 14),
                relief='raised',
                bg='#FDEB30',
                activebackground='blue',
                activeforeground='white',
                borderwidth=1.5,
                width=38,
                height=4,
                command = lambda:raise_frame(uplata_str)).place(x=100, y=320)

isplata_button = Button(meni_str,
                 text='I S P L A T A',
                 font= ('Montserrat', 14),
                 relief='raised',
                 bg='#FDEB30',
                 activebackground='blue',
                 activeforeground='white',
                 borderwidth=1.5,
                 width=38,
                 height=4,
                 command = lambda:raise_frame(isplata_str)).place(x=100, y=520)

stanje_button = Button(meni_str,
                text='S T A N J E',
                font= ('Montserrat', 14),
                relief='raised',
                bg='#FDEB30',
                activebackground='blue',
                activeforeground='white',
                borderwidth=1.5,
                width=38,
                height=4,
                command = lambda:raise_frame(stanje_str)).place(x=710, y=320)

izlaz_button = Button(meni_str,
               text='I Z L A Z',
               font= ('Montserrat', 14),
               relief='raised',
               bg='#FDEB30',
               activebackground='orange',
               activeforeground='white',
               borderwidth=1.5,
               width=38,
               height=4,
               command = lambda:raise_frame(izlaz_str)).place(x=710, y=520)



##UPLATA STRANA-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
logo_meni = Label(uplata_str, image=img_logo).place(x=0, y=0)

naslov_uplata_label = Label(uplata_str,
                      text='UPLATA NA RAČUN',
                      anchor='center',
                      font= ('Arial', 30)).place(x=440, y=120)

suma_uplate_label = Label(uplata_str,
                    text='Izaberite ili unesite sumu koju želite da uplatite na Vaš račun',
                    anchor='center',
                    font= ('Arial', 20)).place(x=270, y=210)

uplata_iznos = IntVar()

UplataEntry = Entry(uplata_str,
              width=20,
              font= ('Montserrat', 20),
              justify=CENTER)
UplataEntry.place(x=460, y=410)

uplata_button = Button(uplata_str,
                text='Uplati',
                font= ('Montserrat', 14),
                relief='raised',
                bg='#FDEB30',
                activebackground='blue',
                activeforeground='white',
                borderwidth=1.5,
                width=20,
                height=3,
                command=uplata)
uplata_button.place(x=528, y=510)

uplata500_button = Button(uplata_str,
                   text='500',
                   font= ('Montserrat', 14),
                   relief='raised',
                   bg='#FDEB30',
                   activebackground='#333333',
                   activeforeground='white',
                   borderwidth=1.5,
                   width=20,
                   height=2,
                   command = lambda:automatski_unos_uplata(500)).place(x=90, y=280)

uplata1000_button = Button(uplata_str,
                    text='1000',
                    font=('Montserrat', 14),
                    relief='raised',
                    bg='#FDEB30',
                    activebackground='#333333',
                    activeforeground='white',
                    borderwidth=1.5,
                    width=20,
                    height=2,
                    command = lambda:automatski_unos_uplata(1000)).place(x=90, y=360)

uplata1500_button = Button(uplata_str,
                    text='1500',
                    font= ('Montserrat', 14),
                    relief='raised',
                    bg='#FDEB30',
                    activebackground='#333333',
                    activeforeground='white',
                    borderwidth=1.5,
                    width=20,
                    height=2,
                    command = lambda:automatski_unos_uplata(1500)).place(x=90, y=440)

uplata2000_button = Button(uplata_str,
                    text='2000',
                    font= ('Montserrat', 14),
                    relief='raised',
                    bg='#FDEB30',
                    activebackground='#333333',
                    activeforeground='white',
                    borderwidth=1.5,
                    width=20,
                    height=2,
                    command = lambda:automatski_unos_uplata(2000)).place(x=90, y=520)

uplata5000_button = Button(uplata_str,
                    text='5000',
                    font= ('Montserrat', 14),
                    relief='raised',
                    bg='#FDEB30',
                    activebackground='#333333',
                    activeforeground='white',
                    borderwidth=1.5,
                    width=20,
                    height=2,
                    command = lambda:automatski_unos_uplata(5000)).place(x=90, y=600)

uplata10000_button = Button(uplata_str,
                    text='10000',
                    font= ('Montserrat', 14),
                    relief='raised',
                    bg='#FDEB30',
                    activebackground='#333333',
                    activeforeground='white',
                    borderwidth=1.5,
                    width=20,
                    height=2,
                    command = lambda:automatski_unos_uplata(10000)).place(x=90, y=680)

nazad_button = Button(uplata_str,
               text='Nazad',
               font= ('Montserrat', 14),
               relief='raised',
               bg='#FDEB30',
               activebackground='orange',
               activeforeground='white',
               borderwidth=1.5,
               width=20,
               height=3,
               command = lambda:raise_frame(meni_str)).place(x=950, y=630)


##ISPLATA STRANA--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
logo_meni = Label(isplata_str, image=img_logo).place(x=0, y=0)

naslov_isplata_label = Label(isplata_str,
                       text='ISPLATA SA RAČUNA',
                       anchor='center',
                       font= ('Arial', 30)).place(x=440, y=120)

suma_isplate_label = Label(isplata_str,
                     text='Izaberite ili unesite sumu koju želite da podignete sa Vašeg računa',
                     anchor='center',
                     font= ('Arial', 20)).place(x=270, y=210)

isplata_iznos = IntVar()

IsplataEntry = Entry(isplata_str,
               width=20,
               font= ('Montserrat', 20),
               justify=CENTER)
IsplataEntry.place(x=460, y=410)

isplata_button = Button(isplata_str,
                 text='Isplati',
                 font= ('Montserrat', 14),
                 relief='raised',
                 bg='#FDEB30',
                 activebackground='blue',
                 activeforeground='white',
                 borderwidth=1.5,
                 width=20,
                 height=3,
                 command=isplata)
isplata_button.place(x=528, y=510)

isplata500_button = Button(isplata_str,
                    text='500',
                    font= ('Montserrat', 14),
                    relief='raised',
                    bg='#FDEB30',
                    activebackground='#333333',
                    activeforeground='white',
                    borderwidth=1.5,
                    width=20,
                    height=2,
                    command = lambda:automatski_unos_isplata(500)).place(x=90, y=280)

isplata1000_button = Button(isplata_str,
                     text='1000',
                     font=('Montserrat', 14),
                     relief='raised',
                     bg='#FDEB30',
                     activebackground='#333333',
                     activeforeground='white',
                     borderwidth=1.5,
                     width=20,
                     height=2,
                     command = lambda:automatski_unos_isplata(1000)).place(x=90, y=360)

isplata1500_button = Button(isplata_str,
                     text='1500',
                     font= ('Montserrat', 14),
                     relief='raised',
                     bg='#FDEB30',
                     activebackground='#333333',
                     activeforeground='white',
                     borderwidth=1.5,
                     width=20,
                     height=2,
                     command = lambda:automatski_unos_isplata(1500)).place(x=90, y=440)

isplata2000_button = Button(isplata_str,
                     text='2000',
                     font= ('Montserrat', 14),
                     relief='raised',
                     bg='#FDEB30',
                     activebackground='#333333',
                     activeforeground='white',
                     borderwidth=1.5,
                     width=20,
                     height=2,
                     command = lambda:automatski_unos_isplata(2000)).place(x=90, y=520)

isplata5000_button = Button(isplata_str,
                     text='5000',
                     font= ('Montserrat', 14),
                     relief='raised',
                     bg='#FDEB30',
                     activebackground='#333333',
                     activeforeground='white',
                     borderwidth=1.5,
                     width=20,
                     height=2,
                     command = lambda:automatski_unos_isplata(5000)).place(x=90, y=600)

isplata10000_button = Button(isplata_str,
                     text='10000',
                     font= ('Montserrat', 14),
                     relief='raised',
                     bg='#FDEB30',
                     activebackground='#333333',
                     activeforeground='white',
                     borderwidth=1.5,
                     width=20,
                     height=2,
                     command = lambda:automatski_unos_isplata(10000)).place(x=90, y=680)

nazad_button = Button(isplata_str,
               text='Nazad',
               font= ('Montserrat', 14),
               relief='raised',
               bg='#FDEB30',
               activebackground='orange',
               activeforeground='white',
               borderwidth=1.5,
               width=20,
               height=3,
               command = lambda:raise_frame(meni_str)).place(x=950, y=630)

##STANJE STRANA-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
logo_meni = Label(stanje_str, image=img_logo).grid(row=0, column=0)

naslov_stanje_label = Label(stanje_str,
                      text='STANJE NA RAČUNU',
                      anchor='center',
                      font= ('Arial', 30)).grid(row=1, column=1, padx=40, pady=50)

stanje_label = Label(stanje_str,
               text= stanje_iznos,
               anchor='center',
               fg='blue',
               font= ('Arial', 40))
stanje_label.grid(row=2, column=1, pady=130)

nazad_button = Button(stanje_str,
               text='Nazad',
               font= ('Montserrat', 18),
               relief='raised',
               bg='#FDEB30',
               activebackground='orange',
               activeforeground='white',
               borderwidth=1.5,
               width=20,
               height=3,
               command = lambda:raise_frame(meni_str)).grid(row=3, column=2, pady=80)

##IZLAZ STRANA-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
logo_meni = Label(izlaz_str, image=img_logo).place(x=0, y=0)

naslov_izlaz_label = Label(izlaz_str,
                     text='Da li ste sigurni da želite da završite sesiju?',
                     font=('Arial', 28)).place(x=280, y=210)

izlazDA_button = Button(izlaz_str,
                 text='D A',
                 font= ('Montserrat', 18),
                 relief='raised',
                 bg='#FDEB30',
                 activebackground="red",
                 activeforeground='white',
                 borderwidth=1.5,
                 width=25,
                 height=3,
                 command = izlaz).place(x=170, y=420)

izlazNE_button = Button(izlaz_str,
                 text='N E',
                 font= ('Montserrat', 18),
                 relief='raised',
                 bg='#FDEB30',
                 activebackground="orange",
                 activeforeground='white',
                 borderwidth=1.5,
                 width=25,
                 height=3,
                 command = lambda:raise_frame(meni_str)).place(x=680, y=420)


##kraj programa ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
raise_frame(pocetna_str)
root.mainloop()
