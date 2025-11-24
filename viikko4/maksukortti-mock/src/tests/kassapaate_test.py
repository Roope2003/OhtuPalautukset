import unittest
from unittest.mock import Mock, ANY
from kassapaate import Kassapaate, HINTA
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()

    def test_kortilta_velotetaan_hinta_jos_rahaa_on(self):
        maksukortti_mock = Mock()
        maksukortti_mock.saldo.return_value = 10
        
        self.kassa.osta_lounas(maksukortti_mock)

        maksukortti_mock.osta.assert_called_with(HINTA)

    def test_kortilta_ei_veloteta_jos_raha_ei_riita(self):
        maksukortti_mock = Mock()
        maksukortti_mock.saldo.return_value = 4
        
        self.kassa.osta_lounas(maksukortti_mock)

        maksukortti_mock.osta.assert_not_called()

    def test_lataaminen_veloittaa_korttia_oikein_kun_summa_positiivinen(self):
        kortti = Mock()

        self.kassa.lataa(kortti, 20)

        kortti.lataa.assert_called_with(20)

    def test_lataaminen_ei_tee_mitaan_jos_summa_negatiivinen(self):
        kortti = Mock()

        self.kassa.lataa(kortti, -10)

        kortti.lataa.assert_not_called()