from datetime import datetime  # Koristi se za dodavanje datuma i vremena kada je izveštaj napravljen.
from pathlib import Path  # Koristi se za rad sa putanjama do fajlova.


def generisi_izvestaj(
    analiza: str,
    putanja_ai_slike: Path,
    putanja_blender_slike: Path,
) -> str:
    # Kreiramo datum i vreme kada je izveštaj generisan.
    datum_generisanja = datetime.now().strftime("%d.%m.%Y. %H:%M")

    # Kreiramo Markdown izveštaj koji uključuje osnovne podatke i AI analizu.
    izvestaj = f"""# Izveštaj o poređenju slika

*Datum generisanja:* {datum_generisanja}

## Ulazne slike

*AI generisana slika:* {putanja_ai_slike}

*Blender renderovana slika:* {putanja_blender_slike}

---

{analiza}

---

## Napomena

Ovaj izveštaj je automatski generisan pomoću AI modela.  
Ocene predstavljaju vizuelnu procenu na osnovu vidljivih elemenata na slikama.
"""

    # Vraćamo gotov Markdown tekst.
    return izvestaj


def sacuvaj_izvestaj(izvestaj: str, putanja_izlaza: Path) -> None:
    # Proveravamo da li folder za čuvanje postoji.
    if putanja_izlaza.parent != Path("."):
        # Ako folder ne postoji, kreiramo ga.
        putanja_izlaza.parent.mkdir(parents=True, exist_ok=True)

    # Upisujemo izveštaj u fajl koristeći UTF-8 encoding zbog srpskih karaktera.
    putanja_izlaza.write_text(izvestaj, encoding="utf-8")