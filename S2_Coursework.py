import os
from typing import Dict, List
from pathlib import Path

class StudentuPriemimoSistema:
    def __init__(self):
        self.kodo_aplankas = Path(__file__).parent.absolute()
        self.studentu_failas = self.kodo_aplankas / "studentai.txt"
        self.kursu_failas = self.kodo_aplankas / "kursai.txt"
        
        self.studentai = self.uzkrauti_studentus()
        self.kursai = self.uzkrauti_kursus()
        
        self.dalykai = ["Lietuvių kalba", "Matematika", "Anglų kalba", "IT", "Fizika", "Istorija", "Biologija"]
    
    def uzkrauti_studentus(self) -> List[Dict]:
        studentai = []
        try:
            if self.studentu_failas.exists():
                with open(self.studentu_failas, 'r', encoding='utf-8') as failas:
                    eilutes = failas.readlines()
                    
                for eilute in eilutes:
                    eilute = eilute.strip()
                    if eilute and not eilute.startswith('#'):
                        dalys = eilute.split('|')
                        if len(dalys) >= 10:  # vardas|pavarde|vidurkis|7_dalykų_pažymiai|kursas
                            studentas = {
                                'vardas': dalys[0].strip(),
                                'pavarde': dalys[1].strip(),
                                'pilnas_vardas': f"{dalys[0].strip()} {dalys[1].strip()}",
                                'vidurkis': float(dalys[2].strip()),
                                'lietuviu_kalba': int(dalys[3].strip()) if dalys[3].strip().isdigit() else 0,
                                'matematika': int(dalys[4].strip()) if dalys[4].strip().isdigit() else 0,
                                'anglu_kalba': int(dalys[5].strip()) if dalys[5].strip().isdigit() else 0,
                                'it': int(dalys[6].strip()) if dalys[6].strip().isdigit() else 0,
                                'fizika': int(dalys[7].strip()) if dalys[7].strip().isdigit() else 0,
                                'istorija': int(dalys[8].strip()) if dalys[8].strip().isdigit() else 0,
                                'biologija': int(dalys[9].strip()) if len(dalys) > 9 and dalys[9].strip().isdigit() else 0,
                                'kursas': dalys[10].strip() if len(dalys) > 10 else ""
                            }
                            studentai.append(studentas)
        except Exception as e:
            print(f"Klaida užkraunant studentus: {e}")
        return studentai
    
    def uzkrauti_kursus(self) -> List[Dict]:
        kursai = []
        try:
            if self.kursu_failas.exists():
                with open(self.kursu_failas, 'r', encoding='utf-8') as failas:
                    eilutes = failas.readlines()
                    
                for eilute in eilutes:
                    eilute = eilute.strip()
                    if eilute and not eilute.startswith('#'):
                        dalys = eilute.split('|')
                        if len(dalys) >= 9:  # pavadinimas|bendras_vidurkis|7_dalykų_kriterijai
                            kursas = {
                                'pavadinimas': dalys[0].strip(),
                                'bendras_vidurkis': float(dalys[1].strip()) if dalys[1].strip() else 0,
                                'lietuviu_kalba': float(dalys[2].strip()) if dalys[2].strip() else 0,
                                'matematika': float(dalys[3].strip()) if dalys[3].strip() else 0,
                                'anglu_kalba': float(dalys[4].strip()) if dalys[4].strip() else 0,
                                'it': float(dalys[5].strip()) if dalys[5].strip() else 0,
                                'fizika': float(dalys[6].strip()) if dalys[6].strip() else 0,
                                'istorija': float(dalys[7].strip()) if dalys[7].strip() else 0,
                                'biologija': float(dalys[8].strip()) if len(dalys) > 8 and dalys[8].strip() else 0
                            }
                            kursai.append(kursas)
        except Exception as e:
            print(f"Klaida užkraunant kursus: {e}")
        return kursai
    
    def issaugoti_studentus(self):
        try:
            with open(self.studentu_failas, 'w', encoding='utf-8') as failas:
                failas.write("# Studentų duomenys: Vardas|Pavardė|Vidurkis|Lietuvių|Matematika|Anglų|IT|Fizika|Istorija|Biologija|Kursas\n")
                for studentas in self.studentai:
                    eilute = f"{studentas['vardas']}|{studentas['pavarde']}|{studentas['vidurkis']}|"
                    eilute += f"{studentas['lietuviu_kalba']}|{studentas['matematika']}|{studentas['anglu_kalba']}|"
                    eilute += f"{studentas['it']}|{studentas['fizika']}|{studentas['istorija']}|{studentas['biologija']}|"
                    eilute += f"{studentas['kursas']}\n"
                    failas.write(eilute)
            print("Studentų duomenys išsaugoti sėkmingai!")
        except Exception as e:
            print(f"Klaida saugant studentų duomenis: {e}")
    
    def issaugoti_kursus(self):
        try:
            with open(self.kursu_failas, 'w', encoding='utf-8') as failas:
                failas.write("# Kursų kriterijai: Pavadinimas|Bendras_vidurkis|Lietuvių|Matematika|Anglų|IT|Fizika|Istorija|Biologija\n")
                for kursas in self.kursai:
                    eilute = f"{kursas['pavadinimas']}|{kursas['bendras_vidurkis']}|"
                    eilute += f"{kursas['lietuviu_kalba']}|{kursas['matematika']}|{kursas['anglu_kalba']}|"
                    eilute += f"{kursas['it']}|{kursas['fizika']}|{kursas['istorija']}|{kursas['biologija']}\n"
                    failas.write(eilute)
            print("Kursų duomenys išsaugoti sėkmingai!")
        except Exception as e:
            print(f"Klaida saugant kursų duomenis: {e}")
    
    def skaiciuoti_vidurki(self, pazymai: Dict) -> float:
        visi_pazymai = []
        dalyku_kodai = ['lietuviu_kalba', 'matematika', 'anglu_kalba', 'it', 'fizika', 'istorija', 'biologija']
        
        for kodas in dalyku_kodai:
            if pazymai[kodas] > 0:
                visi_pazymai.append(pazymai[kodas])
        
        if not visi_pazymai:
            return 0.0
        
        return round(sum(visi_pazymai) / len(visi_pazymai), 2)
    
    def tikrinti_kurso_kriterijus(self, studentas: Dict, kursas: Dict) -> bool:
        if kursas['bendras_vidurkis'] > 0 and studentas['vidurkis'] < kursas['bendras_vidurkis']:
            return False
        
        # Tikrinti dalykų pažymius
        dalyku_kodai = ['lietuviu_kalba', 'matematika', 'anglu_kalba', 'it', 'fizika', 'istorija', 'biologija']
        for kodas in dalyku_kodai:
            if kursas[kodas] > 0:
                # Jei studentas neturi pažymio (0), bet kursas reikalauja
                if studentas[kodas] == 0:
                    return False
                # Jei pažymys per mažas
                if studentas[kodas] < kursas[kodas]:
                    return False
        
        return True
    
    def rasti_tinkamus_kursus(self, studentas: Dict) -> List[Dict]:
        """Randa kursus, į kuriuos studentas gali patekti."""
        tinkami_kursai = []
        for kursas in self.kursai:
            if self.tikrinti_kurso_kriterijus(studentas, kursas):
                tinkami_kursai.append(kursas)
        return tinkami_kursai
    
    def prideti_studenta(self):
        print("\n=== PRIDĖTI STUDENTĄ ===")
        
        if not self.kursai:
            print("Nėra sukurtų kursų! Pirmiau pridėkite kursus.")
            return
        
        try:
            vardas = input("Įveskite studento vardą: ").strip()
            if not vardas:
                print("Vardas negali būti tuščias!")
                return
            
            pavarde = input("Įveskite studento pavardę: ").strip()
            if not pavarde:
                print("Pavardė negali būti tuščia!")
                return
            
            # Tikrinti ar studentas jau egzistuoja
            pilnas_vardas = f"{vardas} {pavarde}"
            for studentas in self.studentai:
                if studentas['pilnas_vardas'].lower() == pilnas_vardas.lower():
                    print("Studentas su tokiu vardu jau egzistuoja!")
                    return
            
            print("\nĮveskite galutinių pažymių duomenis (1-10 arba Enter jei nėra pažymio):")
            dalyku_pazymai = {}
            dalyku_kodai = ['lietuviu_kalba', 'matematika', 'anglu_kalba', 'it', 'fizika', 'istorija', 'biologija']
            
            for i, dalykas in enumerate(self.dalykai):
                while True:
                    pazymys_str = input(f"{dalykas}: ").strip()
                    if not pazymys_str:
                        dalyku_pazymai[dalyku_kodai[i]] = 0
                        break
                    try:
                        pazymys = int(pazymys_str)
                        if 1 <= pazymys <= 10:
                            dalyku_pazymai[dalyku_kodai[i]] = pazymys
                            break
                        else:
                            print("Pažymys turi būti tarp 1 ir 10!")
                    except ValueError:
                        print("Įveskite skaičių arba palikite tuščią!")
            
            vidurkis = self.skaiciuoti_vidurki(dalyku_pazymai)
            
            naujas_studentas = {
                'vardas': vardas,
                'pavarde': pavarde,
                'pilnas_vardas': pilnas_vardas,
                'vidurkis': vidurkis,
                'kursas': "",
                **dalyku_pazymai
            }
            
            print(f"\nApskaičiuotas vidurkis: {vidurkis}")
            
            tinkami_kursai = self.rasti_tinkamus_kursus(naujas_studentas)
            
            if not tinkami_kursai:
                print("\n Studentas neatitinka nė vieno kurso kriterijų!")
                print("Studentas nebus įrašytas į sistemą.")
                return
            
            print(f"\n Studentas {pilnas_vardas} gali patekti į šiuos kursus:")
            for i, kursas in enumerate(tinkami_kursai, 1):
                print(f"{i}. {kursas['pavadinimas']}")
            
            while True:
                try:
                    pasirinkimas = input(f"\nPasirinkite kursą (1-{len(tinkami_kursai)}): ").strip()
                    numeris = int(pasirinkimas)
                    
                    if 1 <= numeris <= len(tinkami_kursai):
                        pasirinktas_kursas = tinkami_kursai[numeris - 1]
                        naujas_studentas['kursas'] = pasirinktas_kursas['pavadinimas']
                        break
                    else:
                        print("Neteisingas pasirinkimas!")
                except ValueError:
                    print("Įveskite skaičių!")
            
            self.studentai.append(naujas_studentas)
            self.issaugoti_studentus()
            print(f"\n Studentas {pilnas_vardas} sėkmingai įrašytas į kursą '{naujas_studentas['kursas']}'!")
            
        except Exception as e:
            print(f"Klaida pridedant studentą: {e}")
    
    def istrinti_studenta(self):
        print("\n=== IŠTRINTI STUDENTĄ ===")
        
        if not self.studentai:
            print("Studentų sąrašas tuščias!")
            return
        
        print("Studentų sąrašas:")
        print("-" * 80)
        for i, studentas in enumerate(self.studentai, 1):
            print(f"{i}. {studentas['pilnas_vardas']} (vidurkis: {studentas['vidurkis']}, kursas: {studentas['kursas']})")
        
        print("-" * 80)
        
        try:
            pasirinkimas = input("Įveskite studento numerį, kurį norite ištrinti (arba 'q' grįžti): ").strip()
            
            if pasirinkimas.lower() == 'q':
                return
            
            numeris = int(pasirinkimas)
            
            if numeris < 1 or numeris > len(self.studentai):
                print("Neteisingas studento numeris!")
                return
            
            istrinamas_studentas = self.studentai[numeris - 1]
            
            patvirtinimas = input(f"Ar tikrai norite ištrinti studentą {istrinamas_studentas['pilnas_vardas']}? (t/n): ").strip().lower()
            
            if patvirtinimas == 't' or patvirtinimas == 'taip':
                self.studentai.pop(numeris - 1)
                self.issaugoti_studentus()
                print(f"Studentas {istrinamas_studentas['pilnas_vardas']} ištrintas sėkmingai!")
            else:
                print("Trynimas atšauktas.")
                
        except ValueError:
            print("Neteisingas numerio formatas!")
        except Exception as e:
            print(f"Klaida trinant studentą: {e}")
    
    def prideti_kursa(self):
        print("\n=== PRIDĖTI KURSĄ ===")
        
        try:
            pavadinimas = input("Įveskite kurso pavadinimą: ").strip()
            if not pavadinimas:
                print("Pavadinimas negali būti tuščias!")
                return
            
            for kursas in self.kursai:
                if kursas['pavadinimas'].lower() == pavadinimas.lower():
                    print("Kursas su tokiu pavadinimu jau egzistuoja!")
                    return
            
            print("Įveskite minimalius kriterijus (Enter jei kriterijus nereikalingas):")
            
            bendras_str = input("Bendras vidurkis: ").strip()
            bendras_vidurkis = float(bendras_str.replace(',', '.')) if bendras_str else 0
            
            dalyku_kriterijai = {}
            dalyku_kodai = ['lietuviu_kalba', 'matematika', 'anglu_kalba', 'it', 'fizika', 'istorija', 'biologija']
            
            for i, dalykas in enumerate(self.dalykai):
                kriterijus_str = input(f"{dalykas}: ").strip()
                if kriterijus_str:
                    try:
                        kriterijus = float(kriterijus_str.replace(',', '.'))
                        if 1 <= kriterijus <= 10:
                            dalyku_kriterijai[dalyku_kodai[i]] = kriterijus
                        else:
                            print(f"Neteisingas kriterijus dalykui {dalykas}, praleista.")
                            dalyku_kriterijai[dalyku_kodai[i]] = 0
                    except ValueError:
                        print(f"Neteisingas formatas dalykui {dalykas}, praleista.")
                        dalyku_kriterijai[dalyku_kodai[i]] = 0
                else:
                    dalyku_kriterijai[dalyku_kodai[i]] = 0
            
            naujas_kursas = {
                'pavadinimas': pavadinimas,
                'bendras_vidurkis': bendras_vidurkis,
                **dalyku_kriterijai
            }
            
            self.kursai.append(naujas_kursas)
            self.issaugoti_kursus()
            print(f"Kursas '{pavadinimas}' pridėtas sėkmingai!")
            
        except ValueError:
            print("Neteisingas skaičiaus formatas!")
        except Exception as e:
            print(f"Klaida pridedant kursą: {e}")
    
    def rodyti_studentu_sarasa(self):
        print("\n=== STUDENTŲ SĄRAŠAS ===")
        
        if not self.studentai:
            print("Studentų sąrašas tuščias!")
            return
        
        print("-" * 100)
        print(f"{'Vardas Pavardė':<20} {'Vidurkis':<10} {'Lietuvių':<10} {'Matemat.':<10} {'Anglų':<8} {'IT':<5} {'Fizika':<8} {'Istorija':<10} {'Biologija':<10} {'Kursas':<15}")
        print("-" * 100)
        
        for studentas in self.studentai:
            print(f"{studentas['pilnas_vardas']:<20} {studentas['vidurkis']:<10} "
                  f"{studentas['lietuviu_kalba'] if studentas['lietuviu_kalba'] > 0 else '-':<10} "
                  f"{studentas['matematika'] if studentas['matematika'] > 0 else '-':<10} "
                  f"{studentas['anglu_kalba'] if studentas['anglu_kalba'] > 0 else '-':<8} "
                  f"{studentas['it'] if studentas['it'] > 0 else '-':<5} "
                  f"{studentas['fizika'] if studentas['fizika'] > 0 else '-':<8} "
                  f"{studentas['istorija'] if studentas['istorija'] > 0 else '-':<10} "
                  f"{studentas['biologija'] if studentas['biologija'] > 0 else '-':<10} "
                  f"{studentas['kursas']:<15}")
        
        print("-" * 100)
    
    def istrinti_kursa(self):
        print("\n=== IŠTRINTI KURSĄ ===")
        
        if not self.kursai:
            print("Kursų sąrašas tuščias!")
            return
        
        print("Kursų sąrašas:")
        print("-" * 80)
        for i, kursas in enumerate(self.kursai, 1):
            studentu_skaicius = len([s for s in self.studentai if s['kursas'] == kursas['pavadinimas']])
            print(f"{i}. {kursas['pavadinimas']} (studentų: {studentu_skaicius})")
        
        print("-" * 80)
        
        try:
            pasirinkimas = input("Įveskite kurso numerį, kurį norite ištrinti (arba 'q' grįžti): ").strip()
            
            if pasirinkimas.lower() == 'q':
                return
            
            numeris = int(pasirinkimas)
            
            if numeris < 1 or numeris > len(self.kursai):
                print("Neteisingas kurso numeris!")
                return
            
            istrinamas_kursas = self.kursai[numeris - 1]
            
            kurso_studentai = [s for s in self.studentai if s['kursas'] == istrinamas_kursas['pavadinimas']]
            
            if kurso_studentai:
                print(f"\n  Šiame kurse yra {len(kurso_studentai)} studentų:")
                for studentas in kurso_studentai:
                    print(f"   • {studentas['pilnas_vardas']}")
                print("\nJei ištrinsite kursą, šie studentai liks be kurso!")
            
            patvirtinimas = input(f"\nAr tikrai norite ištrinti kursą '{istrinamas_kursas['pavadinimas']}'? (t/n): ").strip().lower()
            
            if patvirtinimas == 't' or patvirtinimas == 'taip':
                self.kursai.pop(numeris - 1)
                
                for studentas in self.studentai:
                    if studentas['kursas'] == istrinamas_kursas['pavadinimas']:
                        studentas['kursas'] = ""
                
                self.issaugoti_kursus()
                self.issaugoti_studentus()
                
                print(f"Kursas '{istrinamas_kursas['pavadinimas']}' ištrintas sėkmingai!")
                if kurso_studentai:
                    print(f"Studentai, kurie mokėsi šiame kurse, dabar liko be kurso.")
            else:
                print("Trynimas atšauktas.")
                
        except ValueError:
            print("Neteisingas numerio formatas!")
        except Exception as e:
            print(f"Klaida trinant kursą: {e}")
    
    def rodyti_kursus(self):
        print("\n=== KURSŲ SĄRAŠAS ===")
        
        if not self.kursai:
            print("Kursų sąrašas tuščias!")
            return
        
        for kursas in self.kursai:
            print(f"\n{'='*60}")
            print(f" {kursas['pavadinimas'].upper()}")
            print(f"{'='*60}")
            
            kurso_studentai = [s for s in self.studentai if s['kursas'] == kursas['pavadinimas']]
            
            if kurso_studentai:
                print("Studentai:")
                for studentas in kurso_studentai:
                    print(f"  • {studentas['pilnas_vardas']} (vidurkis: {studentas['vidurkis']})")
            else:
                print("Studentai: Nėra įstojusiųjų")
            
            print("\nReikalavimai:")
            if kursas['bendras_vidurkis'] > 0:
                print(f"  • Bendras vidurkis: {kursas['bendras_vidurkis']}")
            
            dalyku_kodai = ['lietuviu_kalba', 'matematika', 'anglu_kalba', 'it', 'fizika', 'istorija', 'biologija']
            for i, dalykas in enumerate(self.dalykai):
                if kursas[dalyku_kodai[i]] > 0:
                    print(f"  • {dalykas}: {kursas[dalyku_kodai[i]]}")
            
            if not any(kursas[kodas] > 0 for kodas in dalyku_kodai) and kursas['bendras_vidurkis'] == 0:
                print("  • Nėra specifinių reikalavimų")
    
    def rodyti_meniu(self):
        print("\n" + "=" * 50)
        print("    STUDENTŲ PRIĖMIMO VALDYMO SISTEMA")
        print("=" * 50)
        print("1. Pridėti studentą")
        print("2. Ištrinti studentą") 
        print("3. Pridėti kursą su kriterijais")
        print("4. Ištrinti kursą")
        print("5. Rodyti studentų sąrašą")
        print("6. Rodyti kursų sąrašą")
        print("7. Išeiti")
        print("=" * 50)
    
    def paleisti(self):
        """Paleidžia pagrindinį programos ciklą."""
        print("Sveiki atvykę į Studentų priėmimo valdymo sistemą!")
        print(f"Duomenys saugomi: {self.kodo_aplankas}")
        print(f"Studentų failas: {self.studentu_failas}")
        print(f"Kursų failas: {self.kursu_failas}")
        
        while True:
            self.rodyti_meniu()
            
            try:
                pasirinkimas = input("Pasirinkite veiksmą (1-7): ").strip()
                
                if pasirinkimas == '1':
                    self.prideti_studenta()
                elif pasirinkimas == '2':
                    self.istrinti_studenta()
                elif pasirinkimas == '3':
                    self.prideti_kursa()
                elif pasirinkimas == '4':
                    self.istrinti_kursa()
                elif pasirinkimas == '5':
                    self.rodyti_studentu_sarasa()
                elif pasirinkimas == '6':
                    self.rodyti_kursus()
                elif pasirinkimas == '7':
                    print("Ačiū, kad naudojotės sistema. Viso gero!")
                    break
                else:
                    print("Neteisingas pasirinkimas! Pasirinkite skaičių nuo 1 iki 7.")
                
                if pasirinkimas in ['1', '2', '3', '4', '5', '6']:
                    input("\nPaspauskite Enter, kad tęsti...")
                    
            except KeyboardInterrupt:
                print("\n\nProgramos darbas nutrauktas.")
                break
            except Exception as e:
                print(f"Netikėta klaida: {e}")

def main():
    """Pagrindinė programos funkcija."""
    sistema = StudentuPriemimoSistema()
    sistema.paleisti()

if __name__ == "__main__":
    main()