# AI Agent za poređenje AI generisanih i Blender renderovanih slika

## Opis projekta

Ovaj projekat predstavlja AI agenta razvijenog u Python programskom jeziku koji koristi OpenAI Vision model za poređenje dve slike:

- AI generisane slike
- Blender renderovane slike

Cilj sistema je da proceni koliko su slike međusobno slične i da generiše strukturisan izveštaj sa rezultatima analize.

Analiza se vrši na osnovu unapred definisanih kriterijuma, a rezultat se čuva u Markdown dokumentu koji korisniku omogućava pregled ocena, glavnih razlika i preporuka za unapređenje.

---

## Funkcionalnosti

AI agent omogućava:

- unos putanje do AI generisane slike
- unos putanje do Blender renderovane slike
- proveru ispravnosti ulaznih fajlova
- proveru PNG formata slike
- proveru veličine slike
- slanje slika OpenAI Vision modelu
- analizu vizuelne sličnosti između slika
- generisanje strukturisanog Markdown izveštaja
- čuvanje izveštaja u poseban fajl sa datumom i vremenom generisanja


## Struktura projekta

```text
projekat/
│
├── main.py
├── analizator.py
├── klijent_slike.py
├── generator_izvestaja.py
├── requirements.txt
├── .env
│
├── izvestaji/
│   └── ...
│
└── README.md
```


## Potrebne biblioteke

Projekat koristi sledeće biblioteke:

```text
openai
langchain-core
langchain-openai
python-dotenv
```

Instalacija svih biblioteka:

```bash
pip install -r requirements.txt
```

---

## Pokretanje aplikacije

### 1. Kloniranje repozitorijuma

```bash
git clone <url-repozitorijuma>
cd naziv-projekta
```

### 2. Kreiranje virtuelnog okruženja

Windows:

```bash
python -m venv .venv
```

Linux/MacOS:

```bash
python3 -m venv .venv
```

### 3. Aktivacija virtuelnog okruženja

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Windows (CMD):

```bash
.venv\Scripts\activate.bat
```

Linux/MacOS:

```bash
source .venv/bin/activate
```

### 4. Instalacija zavisnosti

```bash
pip install -r requirements.txt
```

### 5. Kreiranje .env fajla

U korenskom direktorijumu projekta kreirati fajl:

```text
.env
```

Sadržaj:

```env
OPENAI_API_KEY=vas_api_kljuc
```

### 6. Pokretanje aplikacije

```bash
python main.py
```

---

## Primer korišćenja

Nakon pokretanja programa:

```text
Unesite putanju do AI generisane slike:
C:\Putanja\AI_slika.png

Unesite putanju do Blender renderovane slike:
C:\Putanja\Blender_slika.png
```

Program zatim:

1. proverava slike
2. prikazuje obaveštenje o privatnosti
3. šalje slike OpenAI modelu
4. generiše analizu
5. kreira Markdown izveštaj

Primer izlaza:

```text
Analiza uspešno završena.

Izveštaj sačuvan u fajl:

izvestaj_2026-06-20_14-30-15.md
```


