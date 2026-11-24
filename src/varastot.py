from dataclasses import dataclass

from varasto import Varasto


@dataclass
class NimettyVarasto:
    id: int
    nimi: str
    varasto: Varasto

    @property
    def saldo(self):
        return self.varasto.saldo

    @property
    def tilavuus(self):
        return self.varasto.tilavuus

    @property
    def taytto_prosentti(self):
        return round(100 * self.saldo / self.tilavuus)


def _tarkista_maara(maara):
    if maara <= 0:
        raise ValueError("määrän pitää olla positiivinen")


class Varastot:
    """Pitää kirjaa nimetyistä varastoista muistissa"""

    def __init__(self):
        self._varastot = {}
        self._seuraava_id = 1

    def _tarkista_uusi(self, nimi, tilavuus):
        if not nimi:
            raise ValueError("nimi ei voi olla tyhjä")
        if any(v.nimi == nimi for v in self._varastot.values()):
            raise ValueError(f"varasto nimeltä {nimi} on jo olemassa")
        if tilavuus <= 0:
            raise ValueError("tilavuuden pitää olla positiivinen")

    def luo(self, nimi, tilavuus):
        nimi = nimi.strip()
        self._tarkista_uusi(nimi, tilavuus)
        uusi = NimettyVarasto(self._seuraava_id, nimi, Varasto(tilavuus))
        self._varastot[uusi.id] = uusi
        self._seuraava_id += 1
        return uusi

    def kaikki(self):
        return list(self._varastot.values())

    def hae(self, varasto_id):
        """Palauttaa varaston tai None, jos sitä ei ole"""
        return self._varastot.get(varasto_id)

    def lisaa(self, varasto_id, maara):
        """Palauttaa varastoon oikeasti mahtuneen määrän"""
        _tarkista_maara(maara)
        varasto = self._varastot[varasto_id].varasto
        mahtui = min(maara, varasto.paljonko_mahtuu())
        varasto.lisaa_varastoon(maara)
        return mahtui

    def ota(self, varasto_id, maara):
        """Palauttaa varastosta oikeasti saadun määrän"""
        _tarkista_maara(maara)
        return self._varastot[varasto_id].varasto.ota_varastosta(maara)
