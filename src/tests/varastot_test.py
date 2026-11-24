import unittest
from varastot import Varastot


class TestVarastot(unittest.TestCase):
    def setUp(self):
        self.varastot = Varastot()
        self.mehu = self.varastot.luo("mehu", 10)

    def test_luo_lisaa_listaan(self):
        self.varastot.luo("olut", 5)
        nimet = [v.nimi for v in self.varastot.kaikki()]
        self.assertEqual(nimet, ["mehu", "olut"])

    def test_luodulla_varastolla_oikea_tilavuus_ja_tyhja_saldo(self):
        self.assertAlmostEqual(self.mehu.tilavuus, 10)
        self.assertAlmostEqual(self.mehu.saldo, 0)

    def test_idt_ovat_yksilollisia(self):
        olut = self.varastot.luo("olut", 5)
        self.assertNotEqual(self.mehu.id, olut.id)

    def test_nimi_trimmataan(self):
        self.assertEqual(self.varastot.luo("  olut ", 5).nimi, "olut")

    def test_tyhja_nimi_hylataan(self):
        with self.assertRaises(ValueError):
            self.varastot.luo("   ", 5)

    def test_sama_nimi_hylataan(self):
        with self.assertRaises(ValueError):
            self.varastot.luo("mehu", 5)

    def test_epapositiivinen_tilavuus_hylataan(self):
        with self.assertRaises(ValueError):
            self.varastot.luo("olut", 0)

    def test_hae_palauttaa_varaston(self):
        self.assertIs(self.varastot.hae(self.mehu.id), self.mehu)

    def test_hae_olematon_palauttaa_none(self):
        self.assertIsNone(self.varastot.hae(999))

    def test_lisaa_kasvattaa_saldoa(self):
        self.assertAlmostEqual(self.varastot.lisaa(self.mehu.id, 4), 4)
        self.assertAlmostEqual(self.mehu.saldo, 4)

    def test_lisaa_yli_tilavuuden_palauttaa_mahtuneen(self):
        self.assertAlmostEqual(self.varastot.lisaa(self.mehu.id, 15), 10)
        self.assertAlmostEqual(self.mehu.saldo, 10)

    def test_lisaa_epapositiivinen_hylataan(self):
        with self.assertRaises(ValueError):
            self.varastot.lisaa(self.mehu.id, -1)

    def test_ota_pienentaa_saldoa(self):
        self.varastot.lisaa(self.mehu.id, 8)
        self.assertAlmostEqual(self.varastot.ota(self.mehu.id, 3), 3)
        self.assertAlmostEqual(self.mehu.saldo, 5)

    def test_ota_yli_saldon_palauttaa_saldon(self):
        self.varastot.lisaa(self.mehu.id, 2)
        self.assertAlmostEqual(self.varastot.ota(self.mehu.id, 5), 2)
        self.assertAlmostEqual(self.mehu.saldo, 0)

    def test_ota_epapositiivinen_hylataan(self):
        with self.assertRaises(ValueError):
            self.varastot.ota(self.mehu.id, 0)

    def test_taytto_prosentti(self):
        self.varastot.lisaa(self.mehu.id, 2.5)
        self.assertEqual(self.mehu.taytto_prosentti, 25)
