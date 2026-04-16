import json
import csv


def ucitaj_filmove(filename="filmovi.txt"):
    filmovi = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for linija in f:
                podaci = linija.strip().split("/")
                if len(podaci) < 9: continue
                film = {
                    "id": int(podaci[0]),
                    "naziv": podaci[1],
                    "zanrovi": podaci[2].split("_"),
                    "trajanje": podaci[3],
                    "glumci": podaci[4].split("_"),
                    "godina": int(podaci[5]),
                    "status": podaci[6],
                    "ocena": int(podaci[7]) if podaci[7] != "None" else None,
                    "jezici": podaci[8].split("_")
                }
                filmovi.append(film)
    except FileNotFoundError:
        pass
    return filmovi


def sacuvaj_filmove(filmovi, filename="filmovi.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for fm in filmovi:
            linija = f"{fm['id']}/{fm['naziv']}/{'_'.join(fm['zanrovi'])}/{fm['trajanje']}/" \
                     f"{'_'.join(fm['glumci'])}/{fm['godina']}/{fm['status']}/{fm['ocena']}/" \
                     f"{'_'.join(fm['jezici'])}\n"
            f.write(linija)

# 1. Dodavanje novog filma
def dodaj_film(filmovi, naziv, zanrovi, trajanje, glumci, godina, status, jezici, ocena=None):
    novi_id = filmovi[-1]['id'] + 1 if filmovi else 1
    # Validacija ocene na osnovu statusa
    if status not in ["ODGLEDANO", "ODUSTAJANJE"]:
        ocena = None
    
    novi_film = {
        "id": novi_id, "naziv": naziv, "zanrovi": zanrovi, "trajanje": trajanje,
        "glumci": glumci, "godina": godina, "status": status, "ocena": ocena, "jezici": jezici
    }
    filmovi.append(novi_film)
    return filmovi


# 2. Brisanje po rednom broju
def obrisi_film(filmovi, id_filma):
    return [f for f in filmovi if f['id'] != id_filma]

# 3. Ispis po nazivu i godini

def ispisi_naziv_godina(filmovi):
    for f in filmovi:
        print(f"{f['naziv']} ({f['godina']})")

# 4. Opseg godina
def pronadji_u_opsegu(filmovi, od_god, do_god):
    return [f for f in filmovi if od_god <= f['godina'] <= do_god]

# 5. Ispis detalja po nazivu i godini
def detalji_filma(filmovi, naziv, godina):
    for f in filmovi:
        if f['naziv'].lower() == naziv.lower() and f['godina'] == godina:
            print(f)

# 6. Prosečno trajanje (hh:mm -> minute)
def prosek_trajanja(filmovi):
    ukupno_minuta = 0
    if not filmovi: return 0
    for f in filmovi:
        h, m = map(int, f['trajanje'].split(':'))
        ukupno_minuta += h * 60 + m
    return ukupno_minuta / len(filmovi)

# 7. Prosek po žanru
def prosek_po_zanru(filmovi, zanr):
    filtrirani = [f for f in filmovi if zanr in f['zanrovi']]
    return prosek_trajanja(filtrirani)

# 8. Prikaz filmova u opsegu trajanja (npr "01:30-02:00")
def trajanje_u_opsegu(filmovi, min_t, max_t):
    def to_min(t_str): h, m = map(int, t_str.split(':')); return h*60 + m
    min_m, max_m = to_min(min_t), to_min(max_t)
    return [f for f in filmovi if min_m <= to_min(f['trajanje']) <= max_m]

# 9. Pretraga po glumcu
def filmovi_glumca(filmovi, glumac):
    return [f for f in filmovi if glumac in f['glumci']]

# 10. Sortiranje po žanru
def sortiraj_po_zanru(filmovi):
    return sorted(filmovi, key=lambda x: x['zanrovi'][0])

# 11. Promena statusa
def promeni_status(filmovi, id_filma, novi_status):
    for f in filmovi:
        if f['id'] == id_filma:
            f['status'] = novi_status
            if novi_status not in ["ODGLEDANO", "ODUSTAJANJE"]:
                f['ocena'] = None

# 12. Unos ocene
def unesi_ocenu(filmovi, id_filma, ocena):
    for f in filmovi:
        if f['id'] == id_filma:
            if f['status'] in ["ODGLEDANO", "ODUSTAJANJE"]:
                f['ocena'] = ocena
            else:
                print("Greška: Film mora biti završen ili prekinut za ocenjivanje.")

# 13. Ispis po statusu
def filmovi_po_statusu(filmovi, status):
    return [f for f in filmovi if f['status'] == status]

# 14. Ispis po broju jezika
def sortiraj_po_broju_jezika(filmovi):
    return sorted(filmovi, key=lambda x: len(x['jezici']), reverse=True)

# 15. Zapis u JSON
def sacuvaj_json(filmovi, filename="filmovi.json"):
    with open(filename, "w") as f:
        json.dump(filmovi, f, indent=4)

# 16. Zapis u CSV
def sacuvaj_csv(filmovi, filename="filmovi.csv"):
    if not filmovi: return
    keys = filmovi[0].keys()
    with open(filename, "w", newline="") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(filmovi)