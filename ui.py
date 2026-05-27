from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt


class MBGCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kalkulator MBG - IDR ke Hari MBG")
        self.setMinimumSize(450, 550)

        layout = QVBoxLayout()

        title = QLabel("Kalkulator MBG")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.info = QLabel("1,2T Rupiah = 1 Hari MBG\n1 USD = 17.400 IDR")
        self.info.setStyleSheet("font-size: 12px; color: #666;")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info)

        layout.addSpacing(20)

        input_layout = QHBoxLayout()

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["IDR", "USD"])

        self.idr_input = QLineEdit()
        self.idr_input.setPlaceholderText("0")
        self.idr_input.setStyleSheet("font-size: 16px; padding: 8px;")

        self.fetch_button = QPushButton("Perbarui Kurs")
        self.fetch_button.setStyleSheet("padding: 8px; font-size: 12px;")

        input_layout.addWidget(self.currency_combo)
        input_layout.addWidget(self.idr_input)
        input_layout.addWidget(self.fetch_button)
        layout.addLayout(input_layout)

        layout.addSpacing(20)

        self.result_hari = QLabel("Hasil\n0\nHari MBG")
        self.result_hari.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        self.result_hari.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_hari)

        self.result_detail = QLabel("Setara dengan\n0 Jam\n0 Menit\n0 Detik")
        self.result_detail.setStyleSheet("font-size: 14px; color: #666;")
        self.result_detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_detail)

        self.result_precise = QLabel("Atau tepatnya\n0 detik MBG")
        self.result_precise.setStyleSheet("font-size: 14px; color: #FFD700;")
        self.result_precise.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_precise)

        layout.addStretch()

        self.setLayout(layout)

    def set_input_changed_handler(self, handler):
        self.idr_input.textChanged.connect(handler)

    def set_fetch_button_handler(self, handler):
        self.fetch_button.clicked.connect(handler)

    def set_currency_changed_handler(self, handler):
        self.currency_combo.currentTextChanged.connect(handler)

    def get_currency(self) -> str:
        return self.currency_combo.currentText()

    def set_info_text(self, text: str):
        self.info.setText(text)

    def get_idr_input(self) -> str:
        return self.idr_input.text()

    def set_idr_input(self, text: str):
        self.idr_input.setText(text)

    def set_cursor_position(self, pos: int):
        self.idr_input.setCursorPosition(pos)

    def block_signals(self, block: bool):
        self.idr_input.blockSignals(block)

    def show_error(self, message: str):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Error", message)

    def set_result_hari(self, text: str):
        self.result_hari.setText(text)

    def set_result_hari_style(self, style: str):
        self.result_hari.setStyleSheet(style)

    def set_result_detail(self, text: str):
        self.result_detail.setText(text)

    def set_result_detail_style(self, style: str):
        self.result_detail.setStyleSheet(style)

    def set_result_precise(self, text: str):
        self.result_precise.setText(text)

    def set_result_precise_style(self, style: str):
        self.result_precise.setStyleSheet(style)

    def set_input_alignment(self, center: bool):
        if center:
            self.idr_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.idr_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
