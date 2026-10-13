
import csv
from operator import attrgetter


class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return (f"{self.codice} - {self.tipo}, {self.marca}, "
                f"anno: {self.anno_acquisto}, valore: {self.valore} euro")


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return (f"{self.id_prestito} - strumento: {self.id_strumento}, "
                f"allievo: {self.cognome_allievo}, data: {self.data}")


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            lettore = csv.reader(file)

            for riga in lettore:
                if len(riga) == 5:
                    codice = riga[0].strip()
                    tipo = riga[1].strip()
                    marca = riga[2].strip()
                    anno = int(riga[3])
                    valore = float(riga[4])

                    strumento = Strumento(
                        codice, tipo, marca, anno, valore
                    )

                    presente = False

                    for s in self.strumenti:
                        if s.codice == codice:
                            presente = True

                    if not presente:
                        self.strumenti.append(strumento)

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: non aggiorna il file"""
        numero = 0

        for strumento in self.strumenti:
            codice = strumento.codice

            if codice.startswith("S"):
                parte_numerica = codice[1:]

                if parte_numerica.isdigit():
                    n = int(parte_numerica)

                    if n > numero:
                        numero = n

        codice = "S" + str(numero + 1)

        strumento = Strumento(
            codice, tipo, marca, anno_acquisto, valore
        )

        self.strumenti.append(strumento)

        return strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=attrgetter("marca"))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        strumento_presente = False

        for strumento in self.strumenti:
            if strumento.codice == id_strumento:
                strumento_presente = True

        if not strumento_presente:
            raise Exception("Lo strumento non è presente nel deposito.")

        for prestito in self.prestiti:
            if prestito.id_strumento == id_strumento:
                raise Exception("Lo strumento è già in prestito.")

        numero = len(self.prestiti) + 1
        id_prestito = "P" + str(numero)

        prestito = Prestito(
            id_prestito, data, id_strumento, cognome_allievo
        )

        self.prestiti.append(prestito)

        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        for prestito in self.prestiti:
            if prestito.id_prestito == id_prestito:
                self.prestiti.remove(prestito)
                return

        raise Exception("Il prestito non esiste.")
