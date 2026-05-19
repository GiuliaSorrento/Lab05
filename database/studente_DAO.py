# Add whatever it is needed to interface with the DB Table studente

from database.DB_connect import get_connection

from database.DB_connect import get_connection
from model.corso import Corso
from model.studente import Studente
#MI SERVE LA TABELLA ISCRIZIONE PER FARE LA QUERY, MA ESSA E UNA TABELLA MOLTI A MOLTI CHE VIENE GESTITA AUTOMATICAMENTE NEL DAO
#IN PYTHON NON MI DEVO PREOCCUPARE DELLA TABELLA ISCRIZIONE
class DAO:
        # SI FA IL METODO DEL DAO NEL DAO CHE RAPPRESENTA L'OGGETTO CHE RESTITUISCE
        @staticmethod
        def getAllStudentiIscrittiCorso(c: Corso):
            #visualizzare tutti gli studenti iscritti al corso
            conn = get_connection()

            result = []

            cursor = conn.cursor(dictionary=True)
            query = """SELECT s.*
                        FROM studente s, iscrizione i
                        WHERE s.matricola = i.matricola 
                        AND i.codins = %s"""

            cursor.execute(query,(c.codins, ))   #anche se il parametro è uno solo ci si aspetta una tupla come parametri

            for row in cursor:
                result.append(Studente(**row))  #lista di dizionari (ogni dizionario è uno studente)

            cursor.close()
            conn.close()
            return result

        @staticmethod
        def getStudenteByMatricola(matricola:int):
            #data una matricola trovare lo studente
            conn = get_connection()



            cursor = conn.cursor(dictionary=True)
            query = """select *
                        from studente s
                        where s.matricola = %s"""

            cursor.execute(query,
                           (matricola,))  # anche se il parametro è uno solo ci si aspetta una tupla come parametri
            #anche qui ci si aspetta una sola riga, quindi non devo restituire una lista ma un oggetto di tipo studente
            row = cursor.fetchone()  #solo una riga da leggere
            if row:
                result = Studente(**row)
            else:
                result = None
            cursor.close()
            conn.close()
            return result

        @staticmethod
        def iscriviStudenteACorso(matricola, codins):
            # data una matricola trovare lo studente
            conn = get_connection()

            cursor = conn.cursor(dictionary=True)
            query = """INSERT INTO iscrizione (matricola, codins) 
                       VALUES (%s, %s)"""

            cursor.execute(query,
                           (matricola,codins))  # anche se il parametro è uno solo ci si aspetta una tupla come parametri

            conn.commit()  # FONDAMENTALE: conferma la modifica nel DB
            cursor.close()
            conn.close()
            return True



