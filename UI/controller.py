import flet as ft

from database import corso_DAO



class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def popolamento_corsi_dd(self):  #faccio questo metodo per popolare il dropdown con le ozpioni di tutti i corsi che trovo su dbeaver
        #prendo tutti i corsi dalla query fatta nel DAO
        # Devi specificare la classe DAO che contiene il metodo statico
        allCorsi = corso_DAO.DAO.getAllCorsi()

        options = [] #le opzioni nel dd si trovano in una lista
        for c in allCorsi:
            options.append(ft.dropdown.Option(
                key=c.codins,  #come detto nel testo del libro
                text=c.__str__()
            ))

        return options



    def handleCercaIscritti(self,e):
        #facendo click devi visualizzare tutti gli studenti iscritti al corso (IL CONTROLLER CHIAMA SOLO IL METODO CHE FA QUESTA AZIONE, METODO DEL MODEL)
        #PER IL RESTO IL CONTROLLER FA SOLO LA GESTIONE DI EVENTUALI ERRORI
        #se nessun corso è selezionato, avvisa utente con messaggio di errore
        #prova a scrivere messaggio di errore usando alertDialog
        codins = self._view._ddSelezioneCorso.value #stringa che mi dice che corso ho selezionato, NB TI RESTITUISCE SOLO IL CODICE DEL CORSO (LA TUA KEY NEL POPOLAMENTO)
        if codins == None or codins=="":
            self._view.txt_result.controls.clear()
            self._view.create_alert("Attenzione, devi selezionare un corso per poter procedere")
            return
        studenti = self._model.getStudentiIscrittiCorso(codins) #lista di tutti gli studenti iscritti
        self._view.txt_result.controls.clear()
        for s in studenti:
            self._view.txt_result.controls.append(ft.Text(s.__str__()))
            self._view.update_page()

    def handleCercaStudente(self,e):
        #se la matricola non è presente visualizza errore con alerdialog
        #se la matricola è presente devi prendere nome e cognome dal metodo del model
        #e scriverli nei due textField appositi
        matricola = self._view._txtInMatricola.value
        if not matricola:
            self._view.create_alert("Attenzione, devi inserire la matricola per poter procedere")
            return
        #se arrivi qua la matricola è presente
        studente= self._model.getStudenteByMatricola(int(matricola))  #ricorda che .value restituisce una stringa e a te serve un intero
        if studente is None:
            self._view.create_alert("Matricola non trovata!")
            self._view._txtInNome.value = ""
            self._view._txtInCognome.value = ""
        else:
            self._view.txt_result.controls.clear()
            self._view._txtInNome.value = studente.nome
            self._view._txtInCognome.value = studente.cognome
        self._view.update_page()

    def handleCercaCorsi(self,e):
        #ricerca corsi a cui è iscritto uno studente
        #data la matricola, controllare se lo studente è presente nel db
        #se si visualizzare tutti i corsi a cui è iscritto
        #se matricola non presente visualizzare mex di errore
        matricola = self._view._txtInMatricola.value
        if not matricola:
            self._view.create_alert("Attenzione, devi inserire la matricola per poter procedere")
            return

        studente, corsi = self._model.getCorsiIscrittoStudente(int(matricola))#ora ho uno studente e la lista dei corsi
        if studente is None:
            self._view.create_alert("Lo studente non è presente in questo database")
        else:
            self._view.txt_result.controls.clear()
            #self._view.txt_result.controls.append(f"Risultano {len(corsi)} corsi:")
            for c in corsi:

                    self._view.txt_result.controls.append(ft.Text(c.__str__()))
                    self._view.update_page()

    def handleIscrivi(self,e):
        #selezionato corso e inserita matricola
        #ti fa iscrivere lo studente
        #puoi inserire solo studenti già iscritti
        codins = self._view._ddSelezioneCorso.value  # stringa con codins, perchè ho messo key=codins nel popolamento del dd
        matricola = self._view._txtInMatricola.value #stringa con matricola
        if codins == None or codins=="":
            self._view.txt_result.controls.clear()
            self._view.create_alert("Attenzione, devi selezionare un corso per poter procedere")
            return
        if not matricola:
            self._view.create_alert("Attenzione, devi inserire la matricola per poter procedere")
            return

        #chiamo la funzione del model che chiama la query del dao per iscrivere
        successo_iscrizione = self._model.iscriviStudente(matricola,codins)
        if successo_iscrizione:
            self._view.create_alert("Studente iscritto con successo!")
            # Magari puliamo i campi o aggiorniamo la lista iscritti
        else:
            self._view.create_alert("Errore nell'iscrizione (forse è già iscritto?)")

        self._view.update_page()