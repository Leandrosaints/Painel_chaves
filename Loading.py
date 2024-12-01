from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivymd.uix.spinner import MDSpinner
from kivy.metrics import dp

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(20)
    spacing: dp(20)

    MDLabel:
        text: "Tela Principal"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]

    MDRaisedButton:
        text: "Mostrar Carregando"
        size_hint: None, None
        size: dp(200), dp(50)
        pos_hint: {'center_x': .5}
        on_release: app.show_loading()
'''

class LoadingOverlay(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = [0, 0, 0, 0.5]  # Fundo semitransparente
        self.auto_dismiss = False  # Não fechar ao clicar fora

        # Layout para centralizar os elementos
        layout = BoxLayout(orientation="vertical", spacing=20, padding=50)
        layout.add_widget(Label(text="Carregando...", font_size=18, color=[1, 1, 1, 1]))  # Texto de carregamento

        # Adiciona o MDSpinner ao layout
        loading_spinner = MDSpinner(size_hint=(None, None), size=(dp(46), dp(46)), active=True)
        layout.add_widget(loading_spinner)

        # Adicionar o layout ao ModalView
        self.add_widget(layout)
'''
class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_loading(self):
        # Exibe o overlay de carregamento
        loading_overlay = LoadingOverlay()
        loading_overlay.open()

        # Simula um processo de carregamento que dura 3 segundos
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.close_loading(loading_overlay), 3)

    def close_loading(self, loading_overlay):
        # Fecha o overlay de carregamento
        loading_overlay.dismiss()

if __name__ == '__main__':
    TestApp().run()
'''