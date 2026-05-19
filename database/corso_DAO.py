# Add whatever it is needed to interface with the DB Table corso

from database.DB_connect import get_connection
from model.corso import Corso
from model.studente import Studente

class DAO:

        @staticmethod
        def getAllCorsi():
            conn = get_connection()

            result = []

            cursor = conn.cursor(dictionary=True)
            query = """select *
                        from  corso c """

            cursor.execute(query)

            for row in cursor:
                result.append(Corso(**row))  #lista di dizionari

            cursor.close()
            conn.close()
            return result

        @staticmethod
        def getCorsoByCodins(codins_scelto):
            conn = get_connection()



            cursor = conn.cursor(dictionary=True)
            query = """select *
                        from corso c
                        where c.codins=%s"""

            cursor.execute(query, (codins_scelto,))
            #non devi restituire una lista, perchè il risultato è un unico corso
            row=cursor.fetchone() #hai solo una riga da leggere

            if row:
                result = Corso(**row)
            else:
                result=None

            cursor.close()
            conn.close()
            return result  #result in questo caso non è una lista ma un oggetto corso

        @staticmethod
        def getAllCorsiIscritto(matricola_scelta):
            ##ricerca tutti i corsi a cui è iscritto uno studente
            conn = get_connection()

            cursor = conn.cursor(dictionary=True)
            query = """select c.*
                    from corso c, iscrizione i
                    where c.codins = i.codins 
                    and i.matricola = %s"""
            result = []
            cursor.execute(query, (matricola_scelta,))
            #qua invece ricevo una lista di corsi come risultato
            for row in cursor:
                result.append(Corso(**row))
            cursor.close()
            conn.close()
            return result  # result in questo caso è una lista di corsi


