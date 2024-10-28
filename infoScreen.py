from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

kv = """
<InfoScreen>:
    name: 'info_screen'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.8, 0.6

        MDLabel:
            id: info_title
            text: "Sala/Local"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Primary"

        MDLabel:
            id: info_details
            text: "Número da Sala"
            font_style: "H6"
            halign: "center"
            theme_text_color: "Secondary"
        Image:
            source: "src/digital_red.png"  # Coloque o caminho correto para a imagem da logo
            size_hint_y: None
            height: dp(100)
            allow_stretch: True
            keep_ratio: True
        MDRaisedButton:
            text: "Voltar"
            pos_hint: {"center_x": 0.5}
            on_release: app.go_back_to_main_screen()
"""

Builder.load_string(kv)

class InfoScreen(MDScreen):
    pass
