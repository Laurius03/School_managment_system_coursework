"""
Objektinio programavimo kursinis darbas: E-Dienyno sistema
Laurynas Raščius IS24
2025-12-15
"""

import json
import os
from datetime import datetime

# ==================== 1. OBJEKTAI IR KLASĖS ====================

class Asmuo:
    def __init__(self, vardas, pavarde, asmens_kodas):
        self.vardas = vardas
        self.pavarde = pavarde
        self.asmens_kodas = asmens_kodas

    def gauti_pilna_varda(self):
        return f"{self.vardas} {self.pavarde}"

    def __str__(self):
        return f"{self.gauti_pilna_varda()} (AK: {self.asmens_kodas})"


class Mokinys(Asmuo):
    mokyklos_pavadinimas = "Vilniaus Kolegija"

    def __init__(self, vardas, pavarde, asmens_kodas, klase):
        super().__init__(vardas, pavarde, asmens_kodas)
        self.klase = klase
        self.pazymiai = []
        self.lankomumas = []
        self.aktyvus = True

    def prideti_pazymi(self, dalykas, pazymys, data=None):
        
        if not isinstance(pazymys, int) or pazymys < 1 or pazymys > 10:
            print("Klaida: Pažymys turi būti skaičius nuo 1 iki 10")
            return False

        if data is None:
            data = datetime.now().strftime("%Y-%m-%d")

        pazymio_objektas = {
            'dalykas': dalykas,
            'pazymys': pazymys,
            'data': data
        }
        self.pazymiai.append(pazymio_objektas)
        return True

    def skaiciuoti_vidurki(self):
        if not self.pazymiai:
            return 0.0

        suma = 0
        for p in self.pazymiai:
            suma += p['pazymys']
        return round(suma / len(self.pazymiai), 2)

    # 8. REKURSIJA - Rekursyvus pažymių sumos skaičiavimas pagal dalyką
    def skaiciuoti_dalyko_suma_rekursyviai(self, dalykas, indeksas=0, suma=0):
        if indeksas >= len(self.pazymiai):
            return suma

        if self.pazymiai[indeksas]['dalykas'].lower() == dalykas.lower():
            suma += self.pazymiai[indeksas]['pazymys']

        return self.skaiciuoti_dalyko_suma_rekursyviai(dalykas, indeksas + 1, suma)

    def gauti_dalyko_vidurki(self, dalykas):
        dalyko_pazymiai = [p for p in self.pazymiai if p['dalykas'].lower() == dalykas.lower()]
        
        if not dalyko_pazymiai:
            return 0.0
        
        suma = self.skaiciuoti_dalyko_suma_rekursyviai(dalykas)
        return round(suma / len(dalyko_pazymiai), 2)

    """ Norėjau padaryti, jog būtų galima žymėti lankomumą, tačiau atmečiau idėja ir pamiršau ištrinti. Prisiminiau tik padares word failą
    def pazymeti_lankomuma(self, data, ar_dalyvavo):
        self.lankomumas.append([data, ar_dalyvavo])

    def gauti_lankomumo_statistika(self):
        if not self.lankomumas:
            return 100.0
        dalyvavo = 0
        for irasas in self.lankomumas:
            if irasas[1]:
                dalyvavo += 1
        return round((dalyvavo / len(self.lankomumas)) * 100, 2) """    

    def __str__(self):
        return f"Mokinys: {self.gauti_pilna_varda()}, Klasė: {self.klase}, Vidurkis: {self.skaiciuoti_vidurki()}"


class Mokytojas(Asmuo):
    def __init__(self, vardas, pavarde, asmens_kodas, dalykas, patirtis_metais=0):
        super().__init__(vardas, pavarde, asmens_kodas)
        self.dalykas = dalykas
        self.patirtis_metais = patirtis_metais  
        self.destomos_klases = [] 

    def prideti_klase(self, klase):
        if klase not in self.destomos_klases:
            self.destomos_klases.append(klase)

    def __str__(self):
        return f"Mokytojas: {self.gauti_pilna_varda()}, Dalykas: {self.dalykas}"


"""class Pamoka:
    def __init__(self, pavadinimas, mokytojas, klase):
        self.pavadinimas = pavadinimas
        self.mokytojas = mokytojas  
        self.klase = klase
        self.dalyviai = []  
        self.pamokos_data = datetime.now().strftime("%Y-%m-%d %H:%M")

    def prideti_dalyvius(self, mokinys):
        if mokinys not in self.dalyviai:
            self.dalyviai.append(mokinys)

    def pazymeti_lankomuma(self):
        print(f"\n--- Lankomumo žymėjimas pamokoje: {self.pavadinimas} ---")
        for i, mokinys in enumerate(self.dalyviai, 1):
            while True:
                print(f"{i}. {mokinys.gauti_pilna_varda()}")
                atsakymas = input("Ar dalyvavo? (t/n): ").lower()
                if atsakymas == 't':
                    mokinys.pazymeti_lankomuma(self.pamokos_data, True)
                    break
                elif atsakymas == 'n':
                    mokinys.pazymeti_lankomuma(self.pamokos_data, False)
                    break
                else:
                    print("Įveskite 't' arba 'n'")""" #Ta pati situacija, kaip su lankomumu


class EDienynas:
    def __init__(self):
        # 11. Dinaminiai kintamieji - sąrašai, kuriuose saugomi objektai
        self.mokiniai = []
        self.mokytojai = []
        self.pamokos = []
        
        programos_aplankas = os.path.dirname(os.path.abspath(__file__))
        self.failas = os.path.join(programos_aplankas, "dienyno_duomenys.json")

    def prideti_mokini(self, mokinys):
        self.mokiniai.append(mokinys)
        print(f"Mokinys {mokinys.gauti_pilna_varda()} pridėtas į sistemą")

    def prideti_mokytoja(self, mokytojas):
        self.mokytojai.append(mokytojas)
        print(f"Mokytojas {mokytojas.gauti_pilna_varda()} pridėtas į sistemą")

    # 12. PAIEŠKOS ALGORITMAS - Paprasta linijinė paieška
    def ieskoti_mokinio(self, paieškos_tekstas):
        rezultatai = []
        paieškos_tekstas = paieškos_tekstas.lower()  

        for mokinys in self.mokiniai:
            pilnas_vardas = mokinys.gauti_pilna_varda().lower()
            if paieškos_tekstas in pilnas_vardas:
                rezultatai.append(mokinys)

        return rezultatai

    # 12. RŪŠIAVIMO ALGORITMAS - Burbuliukinis rūšiavimas
    def rusiuoti_mokinius_pagal_vidurki(self):
        n = len(self.mokiniai)

        for i in range(n):
            for j in range(0, n - i - 1):
                if self.mokiniai[j].skaiciuoti_vidurki() < self.mokiniai[j + 1].skaiciuoti_vidurki():
                    self.mokiniai[j], self.mokiniai[j + 1] = self.mokiniai[j + 1], self.mokiniai[j]

        print("\nMokiniai surūšiuoti pagal vidurkį (nuo didžiausio):")
        for i, m in enumerate(self.mokiniai, 1):
            print(f"{i}. {m.gauti_pilna_varda()}: {m.skaiciuoti_vidurki()}")

    # 9. FAILŲ TVARKYMAS
    def issaugoti_duomenis(self):
        duomenys = {
            'mokiniai': [],
            'mokytojai': []
        }

        for m in self.mokiniai:
            mokinys_dict = {
                'vardas': m.vardas,
                'pavarde': m.pavarde,
                'asmens_kodas': m.asmens_kodas,
                'klase': m.klase,
                'pazymiai': m.pazymiai,
                'aktyvus': m.aktyvus
            }
            duomenys['mokiniai'].append(mokinys_dict)

        for m in self.mokytojai:
            mokytojas_dict = {
                'vardas': m.vardas,
                'pavarde': m.pavarde,
                'asmens_kodas': m.asmens_kodas,
                'dalykas': m.dalykas,
                'patirtis_metais': m.patirtis_metais,
                'destomos_klases': m.destomos_klases
            }
            duomenys['mokytojai'].append(mokytojas_dict)

        try:
            with open(self.failas, 'w', encoding='utf-8') as f:
                json.dump(duomenys, f, ensure_ascii=False, indent=4)
            print(f"\nDuomenys sėkmingai išsaugoti į {self.failas}")
        except Exception as e:
            print(f"Klaida išsaugant duomenis: {e}")

    def nuskaityti_duomenis(self):
        try:
            with open(self.failas, 'r', encoding='utf-8') as f:
                duomenys = json.load(f)

            for m_dict in duomenys.get('mokiniai', []):
                mokinys = Mokinys(
                    m_dict['vardas'],
                    m_dict['pavarde'],
                    m_dict['asmens_kodas'],
                    m_dict['klase']
                )
                mokinys.pazymiai = m_dict['pazymiai']
                mokinys.aktyvus = m_dict['aktyvus']
                self.mokiniai.append(mokinys)

            for m_dict in duomenys.get('mokytojai', []):
                mokytojas = Mokytojas(
                    m_dict['vardas'],
                    m_dict['pavarde'],
                    m_dict['asmens_kodas'],
                    m_dict['dalykas'],
                    m_dict['patirtis_metais']
                )
                mokytojas.destomos_klases = m_dict['destomos_klases']
                self.mokytojai.append(mokytojas)

            print(f"Duomenys nuskaityti iš {self.failas}")
            print(f"Įkelta mokinių: {len(self.mokiniai)}, mokytojų: {len(self.mokytojai)}")

        except FileNotFoundError:
            print(f"Failas {self.failas} nerastas. Pradedama su tuščia sistema.")
        except Exception as e:
            print(f"Klaida nuskaitant duomenis: {e}")

    # 7. DVIMAČIŲ MASYVŲ DEMONSTRACIJA
    def rodyti_pazymiu_lentele(self, mokinys):
        if not mokinys.pazymiai:
            print("Mokinys neturi pažymių")
            return

        print(f"\n--- Pažymių lentelė: {mokinys.gauti_pilna_varda()} ---")

        lentele = []
        lentele.append(['Nr.', 'Dalykas', 'Pažymys', 'Data'])  

        for i, p in enumerate(mokinys.pazymiai, 1):
            eilute = [i, p['dalykas'], p['pazymys'], p['data']]
            lentele.append(eilute)

        for eilute in lentele:
            print(f"{eilute[0]:4} | {eilute[1]:15} | {eilute[2]:7} | {eilute[3]:12}")

        print(f"\nBendras vidurkis: {mokinys.skaiciuoti_vidurki()}")

    def menu(self):
        while True:
            print("\n" + "="*50)
            print("E-DIENYNO SISTEMA")
            print("="*50)
            print("1. Pridėti mokinį")
            print("2. Pridėti mokytoją")
            print("3. Įvesti pažymį")
            print("4. Rodyti visus mokinius")
            print("5. Ieškoti mokinio")
            print("6. Rūšiuoti mokinius pagal vidurkį")
            print("7. Rodyti mokinio pažymių lentelę")
            print("8. Rodyti dalyko vidurkį (naudoja rekursiją)")
            print("9. Išsaugoti duomenis")
            print("0. Išeiti")

            pasirinkimas = input("\nPasirinkite veiksmą: ")

            if pasirinkimas == '1':
                vardas = input("Vardas: ")
                pavarde = input("Pavardė: ")
                ak = input("Asmens kodas: ")
                klase = input("Klasė: ")
                mokinys = Mokinys(vardas, pavarde, ak, klase)
                self.prideti_mokini(mokinys)

            elif pasirinkimas == '2':
                vardas = input("Vardas: ")
                pavarde = input("Pavardė: ")
                ak = input("Asmens kodas: ")
                dalykas = input("Dėstomas dalykas: ")
                patirtis = int(input("Patirtis metais: "))
                mokytojas = Mokytojas(vardas, pavarde, ak, dalykas, patirtis)
                self.prideti_mokytoja(mokytojas)

            elif pasirinkimas == '3':
                if not self.mokiniai:
                    print("Sistemoje nėra mokinių!")
                    continue

                print("\nMokiniai:")
                for i, m in enumerate(self.mokiniai, 1):
                    print(f"{i}. {m}")

                try:
                    nr = int(input("Pasirinkite mokinio nr.: ")) - 1
                    if 0 <= nr < len(self.mokiniai):
                        dalykas = input("Dalykas: ")
                        pazymys = int(input("Pažymys (1-10): "))
                        self.mokiniai[nr].prideti_pazymi(dalykas, pazymys)
                    else:
                        print("Neteisingas numeris!")
                except ValueError:
                    print("Įveskite skaičių!")

            elif pasirinkimas == '4':
                if not self.mokiniai:
                    print("Sistemoje nėra mokinių!")
                else:
                    print("\n--- MOKINIŲ SĄRAŠAS ---")
                    for m in self.mokiniai:
                        print(m)

            elif pasirinkimas == '5':
                tekstas = input("Įveskite vardą ar pavardę: ")
                rezultatai = self.ieskoti_mokinio(tekstas)
                if rezultatai:
                    print(f"\nRasta mokinių: {len(rezultatai)}")
                    for m in rezultatai:
                        print(m)
                else:
                    print("Mokinių nerasta")

            elif pasirinkimas == '6':
                if len(self.mokiniai) < 2:
                    print("Per mažai mokinių rūšiavimui!")
                else:
                    self.rusiuoti_mokinius_pagal_vidurki()

            elif pasirinkimas == '7':
                if not self.mokiniai:
                    print("Sistemoje nėra mokinių!")
                    continue

                print("\nMokiniai:")
                for i, m in enumerate(self.mokiniai, 1):
                    print(f"{i}. {m.gauti_pilna_varda()}")

                try:
                    nr = int(input("Pasirinkite mokinio nr.: ")) - 1
                    if 0 <= nr < len(self.mokiniai):
                        self.rodyti_pazymiu_lentele(self.mokiniai[nr])
                    else:
                        print("Neteisingas numeris!")
                except ValueError:
                    print("Įveskite skaičių!")

            elif pasirinkimas == '8':
                if not self.mokiniai:
                    print("Sistemoje nėra mokinių!")
                    continue

                print("\nMokiniai:")
                for i, m in enumerate(self.mokiniai, 1):
                    print(f"{i}. {m.gauti_pilna_varda()}")

                try:
                    nr = int(input("Pasirinkite mokinio nr.: ")) - 1
                    if 0 <= nr < len(self.mokiniai):
                        mokinys = self.mokiniai[nr]
                        dalykas = input("Įveskite dalyko pavadinimą: ")
                        vidurkis = mokinys.gauti_dalyko_vidurki(dalykas)
                        
                        if vidurkis > 0:
                            print(f"\n{mokinys.gauti_pilna_varda()} dalyko '{dalykas}' vidurkis: {vidurkis}")
                            print(f"(Apskaičiuota naudojant rekursyvią sumavimo funkciją)")
                        else:
                            print(f"Mokinys neturi pažymių iš dalyko '{dalykas}'")
                    else:
                        print("Neteisingas numeris!")
                except ValueError:
                    print("Įveskite skaičių!")

            elif pasirinkimas == '9':
                self.issaugoti_duomenis()

            elif pasirinkimas == '0':
                print("Iki pasimatymo!")
                break

            else:
                print("Neteisingas pasirinkimas!")


# ==================== PAGRINDINĖ PROGRAMA ====================

if __name__ == "__main__":
    print("Sveiki atvykę į E-dienyno sistemą!")
    print("\n1. Pradėti su tuščia sistema")
    print("2. Įkelti duomenis iš failo") #Ištraukia duomenis iš .json failo aplanke

    pasirinkimas = input("\nJūsų pasirinkimas: ")

    sistema = EDienynas()
    
    if pasirinkimas == '2':
        sistema.nuskaityti_duomenis()
    else:
        print("Pradedama su tuščia sistema.")

    sistema.menu()