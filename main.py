import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
import requests

from calculator import (
    idr_to_mbg_days,
    days_to_hours_minutes_seconds,
    format_number,
    parse_idr_input,
    format_idr_input,
)
from ui import MBGCalculatorUI
from config import save_config, load_config

config = load_config()
USD_TO_IDR = config.get("USD_TO_IDR", 17734.5)

PREFIXES = {"IDR": "Rp.", "USD": "$"}


class CalcThread(QThread):
    result_ready = pyqtSignal(float, float, float, float)

    def __init__(self, idr_amount):
        super().__init__()
        self.idr_amount = idr_amount

    def run(self):
        days = idr_to_mbg_days(self.idr_amount)
        hours, minutes, seconds = days_to_hours_minutes_seconds(days)
        total_seconds = days * 24 * 60 * 60
        self.result_ready.emit(days, hours, minutes, total_seconds)


class MBGCalculator(MBGCalculatorUI):
    def __init__(self):
        super().__init__()
        self.calc_thread = None
        self.set_input_changed_handler(self.on_input_changed)
        self.set_fetch_button_handler(self.fetch_data)
        self.set_currency_changed_handler(self.on_currency_changed)
        self.update_info_label()
        prefix = self.get_prefix()
        self.set_idr_input(prefix)

    def get_prefix(self):
        return PREFIXES[self.get_currency()]

    def strip_prefix(self, text: str) -> str:
        for prefix in PREFIXES.values():
            if text.startswith(prefix):
                return text[len(prefix):]
        return text

    def update_info_label(self):
        currency = self.get_currency()
        self.set_info_text(f"1,2T Rupiah = 1 Hari MBG\n1 USD = {format_number(USD_TO_IDR)} IDR")
        self.idr_input.setPlaceholderText(f"Masukkan jumlah {currency}...")

    def on_input_changed(self, text: str):
        prefix = self.get_prefix()

        if not text.startswith(prefix):
            self.block_signals(True)
            self.set_idr_input(prefix)
            self.block_signals(False)
            self.set_cursor_position(len(prefix))
            return

        number_part = text[len(prefix):]
        has_content = any(ch.isdigit() for ch in number_part)
        self.set_input_alignment(has_content)

        clean = ""
        for ch in number_part:
            if ch.isdigit() or ch in ".,":
                clean += ch

        formatted = format_idr_input(clean)
        if formatted != clean:
            self.block_signals(True)
            self.set_idr_input(prefix + formatted)
            self.block_signals(False)
            self.set_cursor_position(len(prefix) + len(formatted))

        self.calculate()

    def on_currency_changed(self, currency: str):
        prefix = self.get_prefix()
        text = self.strip_prefix(self.get_idr_input())
        self.block_signals(True)
        self.set_idr_input(prefix + text)
        self.block_signals(False)
        self.set_cursor_position(len(prefix) + len(text))
        self.update_info_label()
        self.calculate()

    def fetch_data(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            new_usd_to_idr = data["rates"]["IDR"]

            config = load_config()
            config["USD_TO_IDR"] = new_usd_to_idr
            save_config(config)

            global USD_TO_IDR
            USD_TO_IDR = new_usd_to_idr

            self.update_info_label()
            self.calculate()
            self.show_error(f"Kurs USD ke IDR diperbarui menjadi: {format_number(USD_TO_IDR, 0)}")
        except Exception as e:
            self.show_error(f"Gagal memperbarui kurs: {e}")

    def calculate(self):
        try:
            text = self.strip_prefix(self.get_idr_input())
            if not text:
                self.reset_results()
                return

            currency = self.get_currency()
            idr_amount = parse_idr_input(text)
            if currency == "USD":
                idr_amount *= USD_TO_IDR

            if self.calc_thread is not None:
                self.calc_thread.result_ready.disconnect(self.display_results)
                self.calc_thread.quit()
                self.calc_thread.wait()

            self.calc_thread = CalcThread(idr_amount)
            self.calc_thread.result_ready.connect(self.display_results)
            self.calc_thread.start()

        except ValueError:
            pass

    def display_results(self, days, hours, minutes, total_seconds):
        days_formatted = format_number(days)
        self.set_result_hari(f"Hasil\n{days_formatted}\nHari MBG")

        _, _, seconds = days_to_hours_minutes_seconds(days)

        if total_seconds < 1:
            self.set_result_detail(f"Setara dengan\n{int(hours)} Jam\n{int(minutes)} Menit\n{seconds:.2f} Detik")
        else:
            self.set_result_detail(f"Setara dengan\n{int(hours)} Jam\n{int(minutes)} Menit\n{int(seconds)} Detik")
        self.set_result_detail_style("font-size: 14px; color: #666;")

        if total_seconds < 1:
            self.set_result_precise(f"Atau tepatnya\n{total_seconds:.8f} detik MBG")
        else:
            self.set_result_precise(f"Atau tepatnya\n{int(total_seconds)} detik MBG")
        self.set_result_precise_style("font-size: 14px; color: #FFD700;")

    def reset_results(self):
        self.set_result_hari("Hasil\n0\nHari MBG")
        self.set_result_detail("Setara dengan\n0 Jam\n0 Menit\n0 Detik")
        self.set_result_precise("Atau tepatnya\n0 detik MBG")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    from PyQt6.QtGui import QIcon
    icon_path = os.path.join(os.path.dirname(__file__), "res", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = MBGCalculator()
    window.show()
    sys.exit(app.exec())
