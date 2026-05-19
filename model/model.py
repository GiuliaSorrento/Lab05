#devo importare il DAO perchè il model si servirà dei metodi del DAO per ottenere le info da utilizzare nella sua logica
from database import corso_DAO, studente_DAO
from model.corso import Corso


class Model:
    def __init__(self):
        self._idMapCorsi={} #creo l'idMap per i corsi
        self._idMapStudenti={}  #idMap per gli studenti

    def getStudentiIscrittiCorso(self, codins_scelto: str): #il dao riceve come parametro una stringa non l'oggetto corso
        #facendo click devi visualizzare tutti gli studenti iscritti al corso
        #il model però deve chiamare il DAO che farà questa query
        #CERCO CODINS NELL'IDMAP
        if codins_scelto in self._idMapCorsi:
            corso_scelto = self._idMapCorsi[codins_scelto]
        else:
            #SE NON E' PRESENTE NELL'IDMAP DEVO RECUPERARLO CON IL METODO DEL DAO CHE MI CREO getCorsoByCodins
            corso_scelto = corso_DAO.DAO.getCorsoByCodins(codins_scelto) #ora che so che mi serve vado a implementarlo nel DAO
            if corso_scelto: #se esiste lo metto nella idMap per la prossima volta
                self._idMapCorsi[codins_scelto] = corso_scelto

        #ORA HO SICURAMENTE L'OGGETTO CORSO DA POTER PASSARE AL DAO
        allStudentiIscritti = studente_DAO.DAO.getAllStudentiIscrittiCorso(corso_scelto)
        return allStudentiIscritti   #lista di dizionari il cui valore è una stringa che descrive lo studente

    def getStudenteByMatricola(self,matricola_scelta):
        #data la matricola restituire nome e cognome dello studente
        if matricola_scelta in self._idMapStudenti:
            studente_scelto = self._idMapStudenti[matricola_scelta]
        else:
            studente_scelto=studente_DAO.DAO.getStudenteByMatricola(matricola_scelta)
            if studente_scelto:
                self._idMapStudenti[matricola_scelta] = studente_scelto
        return studente_scelto

    def getCorsiIscrittoStudente(self,matricola_scelta):
        #deve ritornare tutti i corsi dello studente
        #controllare se lo studente è presente nel db
        if matricola_scelta in self._idMapStudenti:
            studente_scelto = self._idMapStudenti[matricola_scelta]
        else:
            studente_scelto=studente_DAO.DAO.getStudenteByMatricola(matricola_scelta)
            if studente_scelto:
                self._idMapStudenti[matricola_scelta] = studente_scelto
        #lo studente è presente
        corsi = corso_DAO.DAO.getAllCorsiIscritto(matricola_scelta)
        return studente_scelto, corsi

    def getCorsoByCodins(self, codins):
        corso = corso_DAO.DAO.getCorsoByCodins(codins)
        return corso

    def iscriviStudente(self,matricola,codins):  #a volte il model deve solo richiamare i metodi del dao per il controller
        risultato = studente_DAO.DAO.iscriviStudenteACorso(matricola, codins)
        return risultato #booleano
