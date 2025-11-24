import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from tuote import Tuote

class TestKauppa(unittest.TestCase):

    def setUp(self):
        self.pankki_mock = Mock()

        self.viite_mock = Mock()
        self.viite_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viite_mock)


    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):

        self.varasto_mock.saldo.return_value = 10
        self.varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called()


    def test_yksi_tuote_oikea_tilisiirto(self):

        self.varasto_mock.saldo.return_value = 10
        self.varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            "matti", 42, "11111", "33333-44455", 5
        )


    def test_kaksi_eri_tuotetta(self):

        self.varasto_mock.saldo.side_effect = [10, 10]
        self.varasto_mock.hae_tuote.side_effect = [
            Tuote(1, "maito", 5),
            Tuote(2, "leipä", 3)
        ]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)   # 5€
        self.kauppa.lisaa_koriin(2)   # 3€
        self.kauppa.tilimaksu("teppo", "22222")

        self.pankki_mock.tilisiirto.assert_called_with(
            "teppo", 42, "22222", "33333-44455", 8
        )


    def test_kaksi_samaa_tuotetta(self):

        self.varasto_mock.saldo.return_value = 10
        self.varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("simo", "33333")

        self.pankki_mock.tilisiirto.assert_called_with(
            "simo", 42, "33333", "33333-44455", 10
        )


    def test_toinen_tuote_loppu(self):

        def saldo(id):
            return {1: 10, 2: 0}[id]

        self.varasto_mock.saldo.side_effect = saldo
        self.varasto_mock.hae_tuote.side_effect = [
            Tuote(1, "maito", 5),
            Tuote(2, "banaani", 7)
        ]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)   # loppu -> ei lisätä
        self.kauppa.tilimaksu("kalle", "44444")

        self.pankki_mock.tilisiirto.assert_called_with(
            "kalle", 42, "44444", "33333-44455", 5
        )


    def test_aloita_asiointi_nollaa_ostokset(self):

        self.varasto_mock.saldo.return_value = 10
        self.varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)

        self.kauppa.aloita_asiointi()
        self.kauppa.tilimaksu("arto", "55555")

        self.pankki_mock.tilisiirto.assert_called_with(
            "arto", 42, "55555", "33333-44455", 0
        )


    def test_uusi_viite_joka_maksulla(self):

        self.viite_mock.uusi.side_effect = [10, 20]

        self.varasto_mock.saldo.return_value = 10
        self.varasto_mock.hae_tuote.return_value = Tuote(1, "maito", 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "11111")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("teppo", "22222")

        self.assertEqual(self.viite_mock.uusi.call_count, 2)

        self.pankki_mock.tilisiirto.assert_any_call(
            "matti", 10, "11111", "33333-44455", 5
        )

        self.pankki_mock.tilisiirto.assert_any_call(
            "teppo", 20, "22222", "33333-44455", 5
        )


    def test_poista_korista_palauttaa_varastoon(self):

        tuote = Tuote(1, "maito", 5)
        self.varasto_mock.hae_tuote.return_value = tuote
        self.varasto_mock.saldo.return_value = 10

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)

        self.kauppa.poista_korista(1)

        self.varasto_mock.palauta_varastoon.assert_called_with(tuote)

        self.kauppa.tilimaksu("ville", "99999")

        self.pankki_mock.tilisiirto.assert_called_with(
            "ville", 42, "99999", "33333-44455", 0
        )
