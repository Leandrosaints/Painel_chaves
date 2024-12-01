from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen, ScreenManager
import cv2
from pyzbar.pyzbar import decode
import numpy as np


class MainScreen(Screen):
    pass


class BarcodeScannerApp(MDApp):
    def build(self):
        self.title = "Leitor de Código de Barras"
        self.camera_active = False
        self.camera_index = 0
        self.capture = None

        # Gerenciador de telas
        self.screen_manager = ScreenManager()

        # Tela principal
        self.main_screen = MainScreen(name="main")
        layout = BoxLayout(orientation="vertical")

        # Barra de ferramentas
        self.toolbar = (MDTopAppBar
                        (title="Scanner"))
        self.toolbar.right_action_items = [
            ["camera", lambda x: self.toggle_camera()],
            ["refresh", lambda x: self.switch_camera()],
            ["exit-to-app", lambda x: self.stop()],
        ]
        layout.add_widget(self.toolbar)

        # Área de exibição da câmera
        self.img = Image()
        layout.add_widget(self.img)

        # Adicionando a tela principal
        self.main_screen.add_widget(layout)
        self.screen_manager.add_widget(self.main_screen)

        return self.screen_manager

    def toggle_camera(self):
        """Liga ou desliga a câmera."""
        if self.camera_active:
            self.camera_active = False
            Clock.unschedule(self.update_frame)
            if self.capture:
                self.capture.release()
                self.capture = None
        else:
            self.camera_active = True
            self.start_camera()

    def start_camera(self):
        """Inicia a câmera."""
        self.capture = cv2.VideoCapture(self.camera_index)
        Clock.schedule_interval(self.update_frame, 1 / 30)

    def switch_camera(self):
        """Alterna entre câmeras, se disponível."""
        if self.capture:
            self.capture.release()
            self.camera_index = 1 - self.camera_index  # Alterna entre 0 e 1
            self.start_camera()

    def update_frame(self, dt):
        """Atualiza os frames da câmera na interface."""
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                # Processa a imagem para identificar códigos de barras
                decoded_objects = decode(frame)
                for obj in decoded_objects:
                    barcode_data = obj.data.decode("utf-8")
                    barcode_type = obj.type
                    print(f"Tipo: {barcode_type}, Dados: {barcode_data}")

                    # Desenha um retângulo ao redor do código
                    points = obj.polygon
                    if len(points) > 0:
                        pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
                        cv2.polylines(
                            frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2
                        )

                # Converte o frame para textura do Kivy
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt="bgr"
                )
                texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
                self.img.texture = texture

    def on_stop(self):
        """Finaliza o aplicativo e libera recursos."""
        if self.capture:
            self.capture.release()


if __name__ == "__main__":
    BarcodeScannerApp().run()
