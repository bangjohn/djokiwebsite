# import library for matematika
import math


class hitungkomisi():
    def __init__(self, nilaitransaksi, komisi):
        self.nilaitransaksi = nilaitransaksi
        self.komisi = komisi
        self.pendapatan = 0
    def hitungkomisi(self):
        self.pendapatan = self.komisi * self.nilaitransaksi / 100
        return (self.pendapatan)