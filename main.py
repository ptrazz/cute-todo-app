import datetime
import json
import os

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ILeftBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

# -------------------------------------------------------------
# DESAIN DESAIN VISUAL (TEMA PASTEL CERIA)
# -------------------------------------------------------------
KV = """
MDScreen:
    md_bg_color: 1, 0.97, 0.91, 1  # Kuning Krim Pastel (#FFF8E7)

    MDBoxLayout:
        orientation: 'vertical'
        padding: "16dp"
        spacing: "12dp"

        # 1. HEADER CERIA
        MDCard:
            size_hint_y: None
            height: "90dp"
            md_bg_color: 0.63, 0.91, 0.86, 1  # Biru Toska Pastel (#A2E8DD)
            radius: [20,]
            padding: "12dp"
            elevation: 0

            MDBoxLayout:
                orientation: 'vertical'
                MDLabel:
                    text: "✨ Task Harian Ceria ✨"
                    font_style: "H6"
                    halign: "center"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.25, 0.25, 0.25, 1

                MDLabel:
                    text: "Dicetak = Hilang, Besok Muncul Lagi~ 🌸"
                    font_style: "Caption"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.4, 0.4, 0.4, 1

        # 2. INPUT TUGAS BARU
        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            spacing: "8dp"

            MDTextField:
                id: task_input
                hint_text: "Ketik tugas harian baru..."
                mode: "round"
                line_color_focus: 1, 0.72, 0.7, 1  # Pink Pastel
                fill_color_normal: 1, 1, 1, 1

            MDRaisedButton:
                text: "➕ Tambah"
                md_bg_color: 1, 0.85, 0.75, 1  # Koral Pastel
                text_color: 0.2, 0.2, 0.2, 1
                elevation: 0
                radius: [15,]
                on_release: app.add_task(task_input.text)

        # 3. DAFTAR TUGAS (SCROLLABLE)
        ScrollView:
            MDList:
                id: task_list_container
                spacing: "8dp"
"""


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    """Komponen baris tugas kustom"""

    pass


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Checkbox kustom di sisi kiri"""

    pass


# -------------------------------------------------------------
# LOGIKA APLIKASI UTAMA
# -------------------------------------------------------------
class CuteToDoKivyApp(MDApp):

    def build(self):
        self.title = "To-Do List Pastel Harian"
        self.data_file = "tasks.json"
        self.tasks = self.load_tasks()

        # Terapkan Tema Warna KivyMD
        self.theme_cls.primary_palette = "Pink"

        return Builder.load_string(KV)

    def on_start(self):
        """Dijalankan saat aplikasi pertama kali terbuka"""
        self.check_daily_reset()
        self.refresh_list()

    def load_tasks(self):
        """Membaca data tugas dari file JSON lokal"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass

        # Data Bawaan Pertama Kali Buka Aplikasi
        return {
            "last_login": str(datetime.date.today()),
            "tasks": [
                {"title": "🎨 Menggambar", "completed_today": False},
                {"title": "💧 Minum Air 2 Liter", "completed_today": False},
            ],
        }

    def save_tasks(self):
        """Menyimpan data tugas ke file JSON"""
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def check_daily_reset(self):
        """Mereset centang jika tanggal telah berganti ke hari berikutnya"""
        today = str(datetime.date.today())
        if self.tasks.get("last_login") != today:
            self.tasks["last_login"] = today
            # Reset semua tugas agar muncul kembali hari ini
            for t in self.tasks.get("tasks", []):
                t["completed_today"] = False
            self.save_tasks()

    def refresh_list(self):
        """Memperbarui tampilan daftar tugas"""
        container = self.root.ids.task_list_container
        container.clear_widgets()

        active_tasks = [
            t for t in self.tasks["tasks"] if not t["completed_today"]
        ]

        for idx, task in enumerate(self.tasks["tasks"]):
            # Lewati tugas yang sudah dicentang hari ini
            if task["completed_today"]:
                continue

            # Buat Item List Baru
            item = ListItemWithCheckbox(
                text=task["title"],
                bg_color=(1, 1, 1, 1),  # Warna background kartu putih
                radius=[15, 15, 15, 15],
            )

            # Buat Checkbox
            checkbox = LeftCheckbox(
                selected_color=(0.78, 0.8, 0.91, 1),
                unselected_color=(1, 0.72, 0.7, 1),
            )

            # Event ketika dicentang
            checkbox.bind(
                on_release=lambda chk, i=idx: self.complete_task(i)
            )

            item.add_widget(checkbox)
            container.add_widget(item)

    def complete_task(self, index):
        """Logika saat tugas dicentang (hilang & diset ulang untuk besok)"""
        self.tasks["tasks"][index]["completed_today"] = True
        self.save_tasks()
        self.refresh_list()

    def add_task(self, text):
        """Menambah tugas harian baru"""
        if text.strip():
            self.tasks["tasks"].append(
                {"title": text.strip(), "completed_today": False}
            )
            self.save_tasks()
            self.root.ids.task_input.text = ""  # Reset field input
            self.refresh_list()


# -------------------------------------------------------------
# JALANKAN APLIKASI
# -------------------------------------------------------------
if __name__ == "__main__":
    CuteToDoKivyApp().run()