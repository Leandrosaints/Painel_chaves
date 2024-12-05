from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

KV = """
<HistoryScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)

        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": 0.5}
            on_release: app.try_go_back_to_main()

        ScrollView:
            MDBoxLayout:
                id: history_layout
                orientation: "vertical"
                spacing: dp(10)
                adaptive_height: True
                padding: dp(10)
"""
Builder.load_string(KV)
class HistoryScreen(MDScreen):

    def add_historico(self, historicos):
        """Adiciona uma lista de históricos ao layout."""
        history_layout = self.ids.history_layout