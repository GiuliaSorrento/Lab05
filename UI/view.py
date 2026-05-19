import flet as ft
from flet_core import MainAxisAlignment


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab O5 - segreteria studenti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddSelezioneCorso = None #inizializzo tutti gli elementi nel costruttore
        self._btnCercaIscritti = None
        self._txtInMatricola = None
        self._txtInNome = None
        self._txtInCognome = None
        self._btnCercaStudente = None
        self._btnCercaCorsi = None
        self._btnIscrivi = None
        self.txt_result = None


    def load_interface(self):
        """Function that loads the graphical elements of the view"""
        # title
        self._title = ft.Text("App Gestione Studenti", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW1
        self._ddSelezioneCorso = ft.Dropdown(label="Selezionare un corso",options=self._controller.popolamento_corsi_dd()) #metto solo la label perchè dovrà essere popolata con il DAO
        self._btnCercaIscritti = ft.ElevatedButton(text="Cerca Iscritti", on_click=self._controller.handleCercaIscritti)
        row1 = ft.Row([ft.Container(self._ddSelezioneCorso, width=500), ft.Container(self._btnCercaIscritti, width=250)],
                      alignment=MainAxisAlignment.CENTER)
        #ROW2
        self._txtInMatricola = ft.TextField(label="matricola")
        self._txtInNome = ft.TextField(label="nome", read_only = True) #il testo diceva di inserire che non sono editabili
        self._txtInCognome = ft.TextField(label="cognome", read_only=True) #il testo diceva di inserire che non sono editabili
        row2 = ft.Row(
            [ft.Container(self._txtInMatricola, width=250), ft.Container(self._txtInNome, width=250), ft.Container(self._txtInCognome, width=250)],
        alignment=MainAxisAlignment.CENTER)
        #ROW3
        self._btnCercaStudente = ft.ElevatedButton(text="Cerca Studente", on_click=self._controller.handleCercaStudente)
        self._btnCercaCorsi = ft.ElevatedButton(text="Cerca Corsi", on_click=self._controller.handleCercaCorsi)
        self._btnIscrivi = ft.ElevatedButton(text="Iscrivi", on_click=self._controller.handleIscrivi)
        row3 = ft.Row(
            [ft.Container(self._btnCercaStudente, width=250), ft.Container(self._btnCercaCorsi, width=250),
             ft.Container(self._btnIscrivi, width=250)], alignment=MainAxisAlignment.CENTER)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.add(row1,row2, row3, self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        """Function that opens a popup alert window, displaying a message
        :param message: the message to be displayed"""
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
