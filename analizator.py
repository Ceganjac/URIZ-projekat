import base64  # Koristi se za pretvaranje slike u base64 format koji može da se pošalje modelu.
import os  # Koristi se za čitanje OPENAI_API_KEY i opcionog LLM_MODEL iz .env fajla.
from pathlib import Path  # Koristi se za rad sa putanjama do slika.
from typing import Any  # Koristi se da funkcija može da primi objekat slike iz klijent_slike.py.

from langchain_core.output_parsers import StrOutputParser  # Pretvara odgovor modela u običan string.
from langchain_core.prompts import ChatPromptTemplate  # Omogućava pravljenje prompt šablona.
from langchain_openai import ChatOpenAI  # LangChain klasa za rad sa OpenAI chat modelima.


# Prompt koji objašnjava modelu kako treba da poredi dve slike.
PROMPT_ZA_POREDJENJE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "Ti si stručnjak za vizuelnu analizu slika, 3D rendera i AI generisanih slika. "
                "Tvoj zadatak je da uporediš AI generisanu sliku sa Blender renderovanom slikom. "
                "Analiziraj samo ono što je vidljivo na slikama. "
                "Ako nešto nije moguće jasno proceniti, to jasno napiši."
            ),
        ),
        (
            "user",
            [
                {
                    "type": "text",
                    "text": (
                        "Uporedi sledeće dve slike.\n\n"
                        "Prva slika je AI generisana slika.\n"
                        "Druga slika je Blender renderovana slika.\n\n"
                        "Poređenje uradi po sledećim kriterijumima:\n\n"
                        "1. Oblik i proporcije - Da li objekat ima sličan oblik, veličinu, siluetu i proporcije.\n"
                        "2. Kompozicija i položaj - Da li je objekat slično postavljen u kadru, pod sličnim uglom i na sličnoj pozadini.\n"
                        "3. Boje i osvetljenje - Da li su boje, tonovi, svetlo, kontrast i senke slični.\n"
                        "4. Teksture, materijali i detalji - Da li materijal izgleda slično i da li su važni detalji očuvani.\n"
                        "5. Ukupna vizuelna sličnost - Konačna procena koliko slike ukupno liče jedna na drugu.\n\n"
                        "Za svaki kriterijum dodeli ocenu od 1 do 5:\n"
                        "- 1 znači veoma različito\n"
                        "- 2 znači uglavnom različito\n"
                        "- 3 znači delimično slično\n"
                        "- 4 znači veoma slično\n"
                        "- 5 znači skoro identično\n\n"
                        "Odgovor napiši na srpskom jeziku u Markdown formatu.\n\n"
                        "Obavezno uključi sledeće sekcije:\n"
                        "# Analiza poređenja slika\n"
                        "## Tabela ocena\n"
                        "## Glavne razlike\n"
                        "## Zaključak\n"
                        "## Preporuke za poboljšanje\n\n"
                        "U tabeli koristi kolone: Kriterijum, Ocena, Objašnjenje."
                    ),
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "{ai_slika_url}"
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "{blender_slika_url}"
                    },
                },
            ],
        ),
    ]
)


def analiziraj_slike(
    ai_slika: Any,
    blender_slika: Any,
    model: str | None = None,
) -> str:
    # Kreiramo OpenAI model koji će analizirati slike.
    llm = napravi_openai_model(model=model)

    # Povezujemo prompt, model i parser u LangChain lanac.
    lanac = PROMPT_ZA_POREDJENJE | llm | StrOutputParser()

    # Pretvaramo AI sliku u data URL format koji OpenAI vision model može da pročita.
    ai_slika_url = pretvori_sliku_u_data_url(ai_slika)

    # Pretvaramo Blender sliku u data URL format koji OpenAI vision model može da pročita.
    blender_slika_url = pretvori_sliku_u_data_url(blender_slika)

    # Pokrećemo lanac i vraćamo tekstualni rezultat analize.
    return lanac.invoke(
        {
            "ai_slika_url": ai_slika_url,
            "blender_slika_url": blender_slika_url,
        }
    )


def napravi_openai_model(model: str | None = None) -> ChatOpenAI:
    # Proveravamo da li je OpenAI API ključ postavljen u .env fajlu ili sistemskom okruženju.
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY nije postavljen. Dodajte ga u .env fajl pre pokretanja programa."
        )

    # Kreiramo i vraćamo OpenAI model koji podržava analizu slika.
    return ChatOpenAI(
        model=model or os.getenv("LLM_MODEL", "gpt-4o"),
        temperature=0.2,
    )


def pretvori_sliku_u_data_url(slika: Any) -> str:
    # Pokušavamo da pročitamo MIME tip slike iz objekta, a ako ne postoji, koristimo image/png.
    mime_tip = getattr(slika, "mime_tip", "image/png")

    # Ako objekat slike već ima base64 sadržaj, koristimo ga direktno.
    if hasattr(slika, "sadrzaj_base64"):
        return f"data:{mime_tip};base64,{slika.sadrzaj_base64}"

    # Ako objekat ima atribut putanja, koristimo tu putanju.
    putanja_slike = getattr(slika, "putanja", slika)

    # Pretvaramo putanju u Path objekat.
    putanja_slike = Path(putanja_slike)

    # Proveravamo da li fajl slike postoji.
    if not putanja_slike.exists():
        raise ValueError(f"Slika ne postoji: {putanja_slike}")

    # Čitamo binarni sadržaj slike.
    bajtovi_slike = putanja_slike.read_bytes()

    # Pretvaramo binarni sadržaj slike u base64 tekst.
    sadrzaj_base64 = base64.b64encode(bajtovi_slike).decode("utf-8")

    # Vraćamo sliku u data URL formatu koji OpenAI može da obradi.
    return f"data:{mime_tip};base64,{sadrzaj_base64}"