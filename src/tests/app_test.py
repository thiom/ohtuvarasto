import unittest
from app import luo_sovellus
from varastot import Varastot


class TestApp(unittest.TestCase):
    def setUp(self):
        self.varastot = Varastot()
        self.client = luo_sovellus(self.varastot).test_client()

    def post(self, url, **data):
        return self.client.post(url, data=data, follow_redirects=True)

    def test_tyhja_etusivu(self):
        vastaus = self.client.get("/")
        self.assertEqual(vastaus.status_code, 200)
        self.assertIn("ei vielä varastoja", vastaus.text)

    def test_luonti_nakyy_listassa(self):
        vastaus = self.post("/varastot", nimi="mehu", tilavuus="10,5")
        self.assertIn("varasto mehu luotu", vastaus.text)
        self.assertIn("0 / 10.5", vastaus.text)
        self.assertEqual(len(self.varastot.kaikki()), 1)

    def test_luonti_ei_numeerisella_tilavuudella(self):
        vastaus = self.post("/varastot", nimi="mehu", tilavuus="paljon")
        self.assertIn("tilavuuden pitää olla numero", vastaus.text)
        self.assertEqual(self.varastot.kaikki(), [])

    def test_luonti_aarettomalla_tilavuudella(self):
        for arvo in ("inf", "nan"):
            vastaus = self.post("/varastot", nimi="mehu", tilavuus=arvo)
            self.assertIn("tilavuuden pitää olla numero", vastaus.text)

    def test_luonti_virheellisella_nimella(self):
        vastaus = self.post("/varastot", nimi="", tilavuus="5")
        self.assertIn("nimi ei voi olla tyhjä", vastaus.text)

    def test_lisays(self):
        mehu = self.varastot.luo("mehu", 10)
        vastaus = self.post(f"/varastot/{mehu.id}/lisaa", maara="4")
        self.assertIn("mehu: lisättiin 4", vastaus.text)
        self.assertIn("4 / 10", vastaus.text)

    def test_lisays_yli_tilavuuden(self):
        mehu = self.varastot.luo("mehu", 10)
        vastaus = self.post(f"/varastot/{mehu.id}/lisaa", maara="12")
        self.assertIn("lisättiin 10, 2 ei mahtunut", vastaus.text)

    def test_lisays_negatiivisella(self):
        mehu = self.varastot.luo("mehu", 10)
        vastaus = self.post(f"/varastot/{mehu.id}/lisaa", maara="-1")
        self.assertIn("määrän pitää olla positiivinen", vastaus.text)

    def test_otto(self):
        mehu = self.varastot.luo("mehu", 10)
        self.varastot.lisaa(mehu.id, 5)
        vastaus = self.post(f"/varastot/{mehu.id}/ota", maara="7")
        self.assertIn("mehu: saatiin 5", vastaus.text)
        self.assertIn("0 / 10", vastaus.text)

    def test_otto_ei_numeerisella(self):
        mehu = self.varastot.luo("mehu", 10)
        vastaus = self.post(f"/varastot/{mehu.id}/ota", maara="x")
        self.assertIn("määrän pitää olla numero", vastaus.text)

    def test_olematon_varasto_404(self):
        self.assertEqual(
            self.client.post("/varastot/99/lisaa", data={"maara": "1"})
            .status_code, 404)
        self.assertEqual(
            self.client.post("/varastot/99/ota", data={"maara": "1"})
            .status_code, 404)
