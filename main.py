import argparse  # Biblioteka za rad sa argumentima iz komandne linije.
from pathlib import Path  # Omogućava lakši rad sa putanjama do fajlova.

from dotenv import load_dotenv as ucitaj_env_promenljive  # Učitava promenljive iz .env fajla.

from analizator import analiziraj_slike  # Funkcija koja šalje slike modelu na analizu.
from klijent_slike import KlijentSlika  # Klasa za validaciju i učitavanje slika.
from generator_izvestaja import generisi_izvestaj, sacuvaj_izvestaj  # Funkcije za pravljenje i čuvanje izveštaja.


def main() -> None:
    #Učitavamo API ključ i ostala podešavanja iz .env fajla.
    ucitaj_env_promenljive()

    # Čitamo argumente koje je korisnik eventualno uneo pri pokretanju programa.
    argumenti = parsiraj_argumente()

    # Ako korisnik nije uneo putanju kroz CLI argument, program je traži preko input-a.
    putanja_ai_slike = argumenti.ai_slika or input(
        "Unesite putanju do AI generisane slike: "
    ).strip()

    # Nakon AI slike, posebno se traži i putanja do Blender slike.
    putanja_blender_slike = argumenti.blender_slika or input(
        "Unesite putanju do Blender renderovane slike: "
    ).strip()

    try:
        # Ako korisnik nije tražio preskakanje obaveštenja, prikazujemo poruku o privatnosti.
        if not argumenti.preskoci_obavestenje_o_privatnosti:
            prikazi_obavestenje_o_privatnosti()

        # Kreiramo klijenta koji proverava da li slike postoje, da li su PNG i da li su odgovarajuće veličine.
        klijent_za_slike = KlijentSlika(
            maksimalna_velicina_mb=argumenti.maksimalna_velicina_mb,
            dozvoljene_ekstenzije=(".png",),
        )

        # Učitavamo i validiramo AI generisanu sliku.
        ai_slika = klijent_za_slike.ucitaj_sliku(
            putanja_ai_slike,
            naziv="AI generisana slika",
        )

        # Učitavamo i validiramo Blender renderovanu sliku.
        blender_slika = klijent_za_slike.ucitaj_sliku(
            putanja_blender_slike,
            naziv="Blender renderovana slika",
        )

        # Ispisujemo koje su slike uspešno izabrane za poređenje.
        print("Slike izabrane za poređenje:")
        print(f"- AI slika: {ai_slika.putanja}")
        print(f"- Blender slika: {blender_slika.putanja}")

        # Obaveštavamo korisnika da počinje analiza.
        print("\nAnaliziranje slika pomoću LangChain-a...\n")

        # Pozivamo funkciju koja koristi OpenAI model da uporedi dve slike.
        analiza = analiziraj_slike(
            ai_slika=ai_slika,
            blender_slika=blender_slika,
            model=argumenti.model,
        )

        # Na osnovu rezultata analize generišemo tekstualni izveštaj u Markdown formatu.
        izvestaj = generisi_izvestaj(
            analiza=analiza,
            putanja_ai_slike=ai_slika.putanja,
            putanja_blender_slike=blender_slika.putanja,
        )

        # Formiramo izlaznu putanju za čuvanje izveštaja.
        putanja_izlaza = Path(argumenti.izlaz)

        # Čuvamo izveštaj u fajl.
        sacuvaj_izvestaj(izvestaj, putanja_izlaza)

        # Ispisujemo izveštaj i lokaciju na kojoj je sačuvan.
        print(izvestaj)
        print(f"\nIzveštaj je sačuvan u: {putanja_izlaza.resolve()}")

    except (ValueError, RuntimeError, OSError) as greska:
        # Ako dođe do greške, korisniku prikazujemo jasnu poruku.
        print(f"Greška: {greska}")


def parsiraj_argumente() -> argparse.Namespace:
    # Definišemo CLI interfejs za pokretanje programa iz terminala.
    parser = argparse.ArgumentParser(
        description=(
            "Poredi AI generisanu sliku sa Blender renderovanom slikom "
            "korišćenjem jednostavnog LangChain/OpenAI agenta."
        )
    )

    # Opcioni argument za putanju do AI slike.
    parser.add_argument(
        "--ai-slika",
        dest="ai_slika",
        default=None,
        help="Putanja do AI generisane PNG slike.",
    )

    # Opcioni argument za putanju do Blender slike.
    parser.add_argument(
        "--blender-slika",
        dest="blender_slika",
        default=None,
        help="Putanja do Blender renderovane PNG slike.",
    )

    # Opcioni argument za izlazni Markdown fajl.
    parser.add_argument(
        "--izlaz",
        default="izvestaj_poredjenja_slika.md",
        help="Putanja na kojoj će Markdown izveštaj biti sačuvan.",
    )

    # Opcioni argument za maksimalnu dozvoljenu veličinu slike.
    parser.add_argument(
        "--maksimalna-velicina-mb",
        type=float,
        default=20.0,
        help="Maksimalna dozvoljena veličina svake slike u megabajtima.",
    )

    # Opcioni argument za naziv OpenAI modela.
    parser.add_argument(
        "--model",
        default=None,
        help="Naziv OpenAI modela koji će se koristiti za analizu slika.",
    )

    # Opcioni argument kojim korisnik može da preskoči obaveštenje o privatnosti.
    parser.add_argument(
        "--preskoci-obavestenje-o-privatnosti",
        action="store_true",
        help="Preskače prikaz obaveštenja o privatnosti pre analize.",
    )

    # Vraćamo obrađene argumente.
    return parser.parse_args()


def prikazi_obavestenje_o_privatnosti() -> None:
    # Kratko obaveštavamo korisnika da slike mogu biti poslate OpenAI servisu radi analize.
    print(
        "Obaveštenje o privatnosti:\n"
        "Izabrane slike mogu biti poslate OpenAI servisu radi analize. "
        "Nemojte koristiti privatne ili osetljive slike ako nemate dozvolu za njihovu obradu.\n"
    )


# Obezbeđujemo da se main funkcija pokrene samo kada se ovaj fajl izvršava direktno.
if _name_ == "_main_":
    main()