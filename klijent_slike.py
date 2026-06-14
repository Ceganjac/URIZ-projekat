import base64  # Koristi se za pretvaranje slike u base64 tekst.
from dataclasses import dataclass  # Koristi se za pravljenje jednostavne klase za podatke o slici.
from pathlib import Path  # Koristi se za jednostavan rad sa putanjama do fajlova.


@dataclass
class Slika:
    # Ova klasa predstavlja jednu učitanu sliku koju šaljemo analizatoru.
    putanja: Path  # Putanja do slike na računaru.
    naziv: str  # Naziv slike, na primer "AI generisana slika".
    mime_tip: str  # Tip fajla, za PNG je "image/png".
    velicina_bajtova: int  # Veličina slike u bajtovima.
    sadrzaj_base64: str  # Sadržaj slike pretvoren u base64 format.


class KlijentSlika:
    # Ova klasa proverava i učitava slike pre slanja analizatoru.

    def _init_(
        self,
        maksimalna_velicina_mb: float = 20.0,
        dozvoljene_ekstenzije: tuple[str, ...] = (".png",),
    ) -> None:
        # Čuvamo maksimalnu veličinu slike u megabajtima.
        self.maksimalna_velicina_mb = maksimalna_velicina_mb

        # Čuvamo maksimalnu veličinu slike pretvorenu u bajtove.
        self.maksimalna_velicina_bajtova = int(maksimalna_velicina_mb * 1024 * 1024)

        # Čuvamo dozvoljene ekstenzije fajlova.
        self.dozvoljene_ekstenzije = dozvoljene_ekstenzije

    def ucitaj_sliku(self, putanja_slike: str | Path, naziv: str) -> Slika:
        # Pretvaramo prosleđenu putanju u Path objekat.
        putanja = Path(putanja_slike)

        # Proveravamo da li fajl postoji.
        self._proveri_da_li_postoji(putanja, naziv)

        # Proveravamo da li je fajl PNG.
        self._proveri_ekstenziju(putanja, naziv)

        # Proveravamo da li slika nije veća od dozvoljene veličine.
        self._proveri_velicinu(putanja, naziv)

        # Čitamo binarni sadržaj slike.
        bajtovi_slike = putanja.read_bytes()

        # Pretvaramo binarni sadržaj slike u base64 tekst.
        sadrzaj_base64 = base64.b64encode(bajtovi_slike).decode("utf-8")

        # Vraćamo objekat Slika sa svim potrebnim podacima.
        return Slika(
            putanja=putanja,
            naziv=naziv,
            mime_tip=self._odredi_mime_tip(putanja),
            velicina_bajtova=len(bajtovi_slike),
            sadrzaj_base64=sadrzaj_base64,
        )

    def _proveri_da_li_postoji(self, putanja: Path, naziv: str) -> None:
        # Ako fajl ne postoji, prekidamo program jasnom porukom.
        if not putanja.exists():
            raise ValueError(f"{naziv} ne postoji: {putanja}")

        # Ako putanja nije fajl, nego folder ili nešto drugo, prijavljujemo grešku.
        if not putanja.is_file():
            raise ValueError(f"{naziv} nije fajl: {putanja}")

    def _proveri_ekstenziju(self, putanja: Path, naziv: str) -> None:
        # Uzimamo ekstenziju fajla i pretvaramo je u mala slova.
        ekstenzija = putanja.suffix.lower()

        # Ako ekstenzija nije dozvoljena, prijavljujemo grešku.
        if ekstenzija not in self.dozvoljene_ekstenzije:
            dozvoljeno = ", ".join(self.dozvoljene_ekstenzije)
            raise ValueError(
                f"{naziv} mora biti u jednom od sledećih formata: {dozvoljeno}. "
                f"Unet je fajl: {putanja}"
            )

    def _proveri_velicinu(self, putanja: Path, naziv: str) -> None:
        # Čitamo veličinu fajla u bajtovima.
        velicina_bajtova = putanja.stat().st_size

        # Ako je fajl veći od dozvoljene veličine, prijavljujemo grešku.
        if velicina_bajtova > self.maksimalna_velicina_bajtova:
            velicina_mb = velicina_bajtova / (1024 * 1024)
            raise ValueError(
                f"{naziv} je prevelika. "
                f"Veličina slike je {velicina_mb:.2f} MB, "
                f"a maksimalno je dozvoljeno {self.maksimalna_velicina_mb:.2f} MB."
            )

    def _odredi_mime_tip(self, putanja: Path) -> str:
        # Za sada podržavamo PNG format, pa vraćamo odgovarajući MIME tip.
        if putanja.suffix.lower() == ".png":
            return "image/png"

        # Ako se kasnije doda podrška za druge formate, ovde se može proširiti logika.
        return "application/octet-stream"