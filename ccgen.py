import sys
import random
import string
from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMessageBox,
    QScrollArea, QSizePolicy, QScroller, QComboBox, QStackedWidget
)
from PySide6.QtGui import QGuiApplication, QFont
from PySide6.QtCore import Qt, Signal


# ============ HELPERS (CARDS) ============

def luhn_checksum(card_number: str) -> int:
    digits = [int(d) for d in card_number]
    odd = digits[-1::-2]
    even = digits[-2::-2]
    total = sum(odd)
    for d in even:
        total += sum(divmod(d * 2, 10))
    return total % 10

def generate_card_number(prefix="4", length=16):
    body = prefix + "".join(random.choices(string.digits, k=length - len(prefix) - 1))
    check = (10 - luhn_checksum(body + "0")) % 10
    return body + str(check)

def generate_expiry():
    return (datetime.today() + timedelta(days=random.randint(30, 365 * 4))).strftime("%m/%y")

def generate_cvv():
    return f"{random.randint(100, 999)}"

def generate_holder_name():
    first = ["ALEX", "SAM", "JORDAN", "TAYLOR", "CASEY", "MORGAN", "RILEY", "JAMIE"]
    last = ["SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "GARCIA", "MILLER", "DAVIS"]
    return f"{random.choice(first)} {random.choice(last)}"


# ============ HELPERS (MULTI-COUNTRY ADDRESS) ============

COUNTRIES_DATA = {
    "United States": {
        "first": ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda"],
        "last": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"],
        "streets": ["Main St", "Oak Ave", "Park Blvd", "Maple Dr", "Cedar Ln", "Elm St", "Washington Ave"],
        "cities": [("New York", "NY", "10001"), ("Los Angeles", "CA", "90001"), ("Chicago", "IL", "60601"), 
                   ("Houston", "TX", "77001"), ("Miami", "FL", "33101"), ("Seattle", "WA", "98101")],
        "phone": lambda: f"+1 ({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    },
    "United Kingdom": {
        "first": ["Oliver", "Amelia", "Harry", "Olivia", "Jack", "Emily", "George", "Ava"],
        "last": ["Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson", "Davies"],
        "streets": ["High St", "Station Rd", "London Rd", "Church St", "Victoria Rd", "Green Ln"],
        "cities": [("London", "Greater London", "SW1A 1AA"), ("Manchester", "Greater Manchester", "M1 1AE"), 
                   ("Birmingham", "West Midlands", "B1 1AA"), ("Leeds", "West Yorkshire", "LS1 1UR")],
        "phone": lambda: f"+44 {random.randint(10, 99)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"
    },
    "Canada": {
        "first": ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "Benjamin", "Sophia"],
        "last": ["Smith", "Brown", "Tremblay", "Martin", "Roy", "Wilson", "MacDonald", "Gagnon"],
        "streets": ["Maple Ave", "Main St", "Oak St", "King St", "Queen St", "Yonge St"],
        "cities": [("Toronto", "ON", "M5V 2H1"), ("Vancouver", "BC", "V6B 1A1"), 
                   ("Montreal", "QC", "H2Y 1C6"), ("Calgary", "AB", "T2P 2M5")],
        "phone": lambda: f"+1 ({random.randint(200, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    },
    "Australia": {
        "first": ["Oliver", "Charlotte", "Jack", "Olivia", "William", "Amelia", "Thomas", "Isla"],
        "last": ["Smith", "Jones", "Williams", "Brown", "Wilson", "Taylor", "Johnson", "White"],
        "streets": ["George St", "Collins St", "Elizabeth St", "Bourke St", "Macquarie St"],
        "cities": [("Sydney", "NSW", "2000"), ("Melbourne", "VIC", "3000"), 
                   ("Brisbane", "QLD", "4000"), ("Perth", "WA", "6000")],
        "phone": lambda: f"+61 4{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)}"
    },
    "Germany": {
        "first": ["Lukas", "Marie", "Leon", "Sophie", "Finn", "Anna", "Paul", "Emma"],
        "last": ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker"],
        "streets": ["Hauptstraße", "Schulstraße", "Gartenstraße", "Bahnhofstraße", "Dorfstraße"],
        "cities": [("Berlin", "Berlin", "10115"), ("Munich", "Bavaria", "80331"), 
                   ("Hamburg", "Hamburg", "20095"), ("Frankfurt", "Hesse", "60311")],
        "phone": lambda: f"+49 {random.randint(150, 179)} {random.randint(1000000, 9999999)}"
    },
    "France": {
        "first": ["Gabriel", "Emma", "Louis", "Jade", "Raphaël", "Louise", "Jules", "Alice"],
        "last": ["Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois"],
        "streets": ["Rue de Rivoli", "Avenue des Champs-Élysées", "Boulevard Saint-Germain", "Rue de la Paix"],
        "cities": [("Paris", "Île-de-France", "75001"), ("Marseille", "PACA", "13001"), 
                   ("Lyon", "Auvergne-Rhône-Alpes", "69001"), ("Toulouse", "Occitanie", "31000")],
        "phone": lambda: f"+33 {random.randint(1, 9)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"
    },
    "Japan": {
        "first": ["Haruto", "Yui", "Sota", "Aoi", "Yuto", "Rin", "Sota", "Hina"],
        "last": ["Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura"],
        "streets": ["Chome-1-1", "Chome-2-5", "Chome-3-10", "Chome-4-2"],
        "cities": [("Tokyo", "Tokyo", "150-0002"), ("Osaka", "Osaka", "530-0001"), 
                   ("Kyoto", "Kyoto", "600-8001"), ("Yokohama", "Kanagawa", "220-0012")],
        "phone": lambda: f"+81 90-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    },
    "Brazil": {
        "first": ["Miguel", "Alice", "Arthur", "Laura", "Davi", "Isabella", "Gabriel", "Manuela"],
        "last": ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira"],
        "streets": ["Avenida Paulista", "Rua das Flores", "Avenida Atlântica", "Rua XV de Novembro"],
        "cities": [("São Paulo", "SP", "01310-100"), ("Rio de Janeiro", "RJ", "22021-001"), 
                   ("Brasília", "DF", "70040-010"), ("Salvador", "BA", "40020-000")],
        "phone": lambda: f"+55 ({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    }
}

def generate_fake_address(country_name):
    data = COUNTRIES_DATA[country_name]
    first = random.choice(data["first"])
    last = random.choice(data["last"])
    city, state, zip_code = random.choice(data["cities"])
    street = f"{random.randint(1, 9999)} {random.choice(data['streets'])}"
    
    return {
        "Full Name": f"{first} {last}",
        "Street": street,
        "City": city,
        "State/Province": state,
        "Postal Code": zip_code,
        "Country": country_name,
        "Phone": data["phone"]()
    }


# ============ SHARED STYLES ============

BG_MAIN = "#0f1722"
BG_PANEL = "#1e2a38"
BG_FIELD = "#0f3460"
BORDER_FIELD = "#1a5f9e"
TEXT_LABEL = "#8899aa"

FIELD_QSS = f"""
    QLineEdit {{
        background-color: {BG_FIELD};
        color: #ffffff;
        border: 2px solid {BORDER_FIELD};
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 14px;
        min-height: 32px;
    }}
    QLineEdit:focus {{ border-color: #3498db; }}
"""

COPY_BTN_QSS = """
    QPushButton {
        background-color: #00b894;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        padding-bottom: 2px;
    }
    QPushButton:pressed { background-color: #009874; }
"""


# ============ TOUCH-FRIENDLY SPINBOX ============

class TouchSpinBox(QWidget):
    valueChanged = Signal(int)

    def __init__(self, min_val=1, max_val=100, value=1):
        super().__init__()
        self._min, self._max, self._value = min_val, max_val, value

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.btn_minus = QPushButton("−")
        self.btn_minus.setFixedSize(50, 50)
        self.btn_minus.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white;
                border: none; border-radius: 10px;
                font-size: 24px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #c0392b; }
        """)
        self.btn_minus.clicked.connect(self._decrement)

        self.value_label = QLabel(str(value))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setMinimumHeight(50)
        self.value_label.setStyleSheet("""
            QLabel {
                background-color: #2c3e50; color: white;
                border-radius: 10px;
                font-size: 20px; font-weight: bold;
            }
        """)
        self.value_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedSize(50, 50)
        self.btn_plus.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                border: none; border-radius: 10px;
                font-size: 24px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #229954; }
        """)
        self.btn_plus.clicked.connect(self._increment)

        layout.addWidget(self.btn_minus)
        layout.addWidget(self.value_label, 1)
        layout.addWidget(self.btn_plus)

    def value(self): return self._value

    def setValue(self, v):
        v = max(self._min, min(self._max, v))
        self._value = v
        self.value_label.setText(str(v))
        self.valueChanged.emit(v)

    def _increment(self):
        if self._value < self._max: self.setValue(self._value + 1)

    def _decrement(self):
        if self._value > self._min: self.setValue(self._value - 1)


# ============ TAB 1: CARD SIMULATOR ============

class CardSimulatorTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build()
        self.generate_new_card()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("💳 Credit Card Simulator")
        title.setStyleSheet("color: #ecf0f1; font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border-radius: 18px;
                border: 1px solid #0f3460;
            }
        """)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(14)

        cl.addWidget(self._label("Card Number"))
        self.number_edit = QLineEdit()
        self.number_edit.setReadOnly(True)
        self.number_edit.setFont(QFont("Courier", 17, QFont.Bold))
        self.number_edit.setStyleSheet(FIELD_QSS)
        cl.addLayout(self._row_with_copy(self.number_edit, is_number=True))

        row = QHBoxLayout()
        row.setSpacing(14)

        v1 = QVBoxLayout()
        v1.addWidget(self._label("Expiry"))
        self.expiry_edit = QLineEdit()
        self.expiry_edit.setReadOnly(True)
        self.expiry_edit.setStyleSheet(FIELD_QSS)
        v1.addLayout(self._row_with_copy(self.expiry_edit))

        v2 = QVBoxLayout()
        v2.addWidget(self._label("CVV"))
        self.cvv_edit = QLineEdit()
        self.cvv_edit.setReadOnly(True)
        self.cvv_edit.setStyleSheet(FIELD_QSS)
        v2.addLayout(self._row_with_copy(self.cvv_edit))

        row.addLayout(v1)
        row.addLayout(v2)
        cl.addLayout(row)

        cl.addWidget(self._label("Card Holder"))
        self.holder_edit = QLineEdit()
        self.holder_edit.setReadOnly(True)
        self.holder_edit.setStyleSheet(FIELD_QSS)
        cl.addLayout(self._row_with_copy(self.holder_edit))

        self.type_label = QLabel()
        self.type_label.setStyleSheet("color: #00d2ff; font-size: 14px; font-style: italic;")
        cl.addWidget(self.type_label)

        layout.addWidget(card)

        btn_new = QPushButton("🔄 Generate New Card")
        btn_new.setMinimumHeight(50)
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                border: none; border-radius: 10px;
                font-size: 16px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #2980b9; }
        """)
        btn_new.clicked.connect(self.generate_new_card)
        layout.addWidget(btn_new)

        btn_all = QPushButton("Copy Entire Card Details")
        btn_all.setMinimumHeight(45)
        btn_all.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; color: white;
                border: none; border-radius: 10px;
                font-size: 15px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #ca6f1e; }
        """)
        btn_all.clicked.connect(self._copy_entire)
        layout.addWidget(btn_all)

        layout.addStretch()

    def _label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(f"color: {TEXT_LABEL}; font-size: 12px; font-weight: bold;")
        return lbl

    def _row_with_copy(self, edit, is_number=False):
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(edit, 1)
        btn = QPushButton("⧉")
        btn.setFixedSize(45, 45)
        btn.setStyleSheet(COPY_BTN_QSS)
        
        if is_number:
            btn.clicked.connect(lambda: QGuiApplication.clipboard().setText(edit.text().replace(" ", "")))
        else:
            btn.clicked.connect(lambda: QGuiApplication.clipboard().setText(edit.text()))
            
        row.addWidget(btn)
        return row

    def _copy_entire(self):
        raw_num = self.number_edit.text().replace(" ", "")
        text = (f"Card Number: {raw_num}\n"
                f"Expiry: {self.expiry_edit.text()}\n"
                f"CVV: {self.cvv_edit.text()}\n"
                f"Card Holder: {self.holder_edit.text()}")
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied", "Full card details copied to clipboard.")

    def generate_new_card(self):
        types = {"4": "Visa", "51": "Mastercard", "52": "Mastercard",
                 "53": "Mastercard", "54": "Mastercard", "55": "Mastercard",
                 "34": "Amex", "37": "Amex"}
        prefix = random.choice(list(types.keys()))
        length = 15 if prefix in ("34", "37") else 16
        num = generate_card_number(prefix, length)
        formatted = " ".join(num[i:i+4] for i in range(0, len(num), 4))
        self.number_edit.setText(formatted)
        self.expiry_edit.setText(generate_expiry())
        self.cvv_edit.setText(generate_cvv())
        self.holder_edit.setText(generate_holder_name())
        self.type_label.setText(f"Card Type: {types[prefix]}")


# ============ TAB 2: BATCH GENERATOR ============

class BatchGeneratorTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("⚙️ Batch Generator")
        title.setStyleSheet("color: #ecf0f1; font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        count_row = QHBoxLayout()
        lbl = QLabel("How many cards?")
        lbl.setStyleSheet("color: #ecf0f1; font-size: 15px; font-weight: bold;")
        self.count_spin = TouchSpinBox(1, 50, 10)
        count_row.addWidget(lbl)
        count_row.addWidget(self.count_spin, 1)
        layout.addLayout(count_row)

        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("BIN Prefix (e.g., 4 for Visa)")
        self.prefix_edit.setStyleSheet(FIELD_QSS)
        layout.addWidget(self.prefix_edit)

        btn_gen = QPushButton("⚡ Generate Cards")
        btn_gen.setMinimumHeight(50)
        btn_gen.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; color: white;
                border: none; border-radius: 10px;
                font-size: 16px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #8e44ad; }
        """)
        btn_gen.clicked.connect(self.generate_batch)
        layout.addWidget(btn_gen)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: #1e2a38; width: 6px; border-radius: 3px; }
            QScrollBar::handle:vertical { background: #3498db; min-height: 20px; border-radius: 3px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self.container = QWidget()
        self.container.setStyleSheet("background-color: transparent;")
        self.results_layout = QVBoxLayout(self.container)
        self.results_layout.setSpacing(6)
        self.results_layout.addStretch()
        self.scroll.setWidget(self.container)
        
        QScroller.grabGesture(self.scroll.viewport(), QScroller.ScrollerGestureType.TouchGesture)
        layout.addWidget(self.scroll, 1)

    def generate_batch(self):
        while self.results_layout.count() > 1:
            item = self.results_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        count = self.count_spin.value()
        prefix = self.prefix_edit.text().strip()

        for _ in range(count):
            p = prefix if prefix else random.choice(["4", "51", "52", "53", "54", "55", "34", "37"])
            length = 15 if p in ("34", "37") else 16
            num = generate_card_number(p, length)
            formatted = " ".join(num[i:i+4] for i in range(0, len(num), 4))
            exp = generate_expiry()
            cvv = generate_cvv()

            row_frame = QFrame()
            row_frame.setStyleSheet("""
                QFrame {
                    background-color: #2c3e50;
                    border-radius: 8px;
                }
            """)
            rl = QHBoxLayout(row_frame)
            rl.setContentsMargins(10, 8, 10, 8)
            rl.setSpacing(8)

            num_lbl = QLabel(formatted)
            num_lbl.setStyleSheet("color: #ffffff; font-family: Courier; font-size: 14px; font-weight: bold;")
            rl.addWidget(num_lbl, 1)

            detail = QLabel(f"{exp} · {cvv}")
            detail.setStyleSheet("color: #8899aa; font-family: Courier; font-size: 12px;")
            rl.addWidget(detail)

            btn = QPushButton("⧉")
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(COPY_BTN_QSS)
            btn.clicked.connect(lambda checked=False, t=num: QGuiApplication.clipboard().setText(t))
            rl.addWidget(btn)

            self.results_layout.insertWidget(self.results_layout.count() - 1, row_frame)


# ============ TAB 3: ADDRESS GENERATOR ============

class AddressGeneratorTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build()
        self.generate_address()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("📍 Address Generator")
        title.setStyleSheet("color: #ecf0f1; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.country_combo = QComboBox()
        self.country_combo.addItems(list(COUNTRIES_DATA.keys()))
        self.country_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {BG_PANEL};
                color: white;
                border: 2px solid #3498db;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 14px;
                min-height: 32px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {BG_PANEL};
                color: white;
                selection-background-color: #3498db;
                selection-color: white;
                border: 1px solid #3498db;
                outline: none;
                padding: 4px;
            }}
            QComboBox QAbstractItemView::item {{
                min-height: 40px;
            }}
        """)
        self.country_combo.currentTextChanged.connect(self.generate_address)
        layout.addWidget(self.country_combo)

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_PANEL};
                border-radius: 12px;
                border: 1px solid #2c3e50;
            }}
        """)
        fl = QVBoxLayout(frame)
        fl.setSpacing(2)
        fl.setContentsMargins(10, 10, 10, 10)

        self.fields = {}
        field_names = ["Full Name", "Street", "City", "State/Province", "Postal Code", "Country", "Phone"]
        
        for key in field_names:
            row = QHBoxLayout()
            row.setSpacing(6)
            
            lbl = QLabel(key)
            lbl.setFixedWidth(100)
            lbl.setStyleSheet(f"color: {TEXT_LABEL}; font-size: 11px; font-weight: bold;")
            row.addWidget(lbl)

            edit = QLineEdit()
            edit.setReadOnly(True)
            edit.setStyleSheet(FIELD_QSS)
            edit.setFixedHeight(36)
            self.fields[key] = edit
            row.addWidget(edit, 1)
            
            btn = QPushButton("⧉")
            btn.setFixedSize(36, 36)
            btn.setStyleSheet(COPY_BTN_QSS)
            btn.clicked.connect(lambda checked=False, e=edit: QGuiApplication.clipboard().setText(e.text()))
            row.addWidget(btn)
            
            fl.addLayout(row)

        layout.addWidget(frame)
        layout.addStretch()

        btn_new = QPushButton("🔄 Generate New Address")
        btn_new.setMinimumHeight(45)
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                border: none; border-radius: 10px;
                font-size: 15px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #2980b9; }
        """)
        btn_new.clicked.connect(self.generate_address)
        layout.addWidget(btn_new)

        btn_all = QPushButton("Copy Full Address")
        btn_all.setMinimumHeight(45)
        btn_all.setStyleSheet("""
            QPushButton {
                background-color: #e67e22; color: white;
                border: none; border-radius: 10px;
                font-size: 15px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #ca6f1e; }
        """)
        btn_all.clicked.connect(self._copy_full)
        layout.addWidget(btn_all)

    def _copy_full(self):
        f = self.fields
        text = (f"{f['Full Name'].text()}\n"
                f"{f['Street'].text()}\n"
                f"{f['City'].text()}, {f['State/Province'].text()} {f['Postal Code'].text()}\n"
                f"{f['Country'].text()}\n"
                f"Phone: {f['Phone'].text()}")
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied", "Full address copied to clipboard.")

    def generate_address(self):
        country = self.country_combo.currentText()
        if not country: return
        data = generate_fake_address(country)
        for key, val in data.items():
            self.fields[key].setText(val)


# ============ MAIN WINDOW ============

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Card & Address Tools")
        self.setStyleSheet(f"QMainWindow {{ background-color: {BG_MAIN}; }}")

        # Main Container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Custom Tab Bar (Using Buttons for perfect mobile layout)
        tab_bar_layout = QHBoxLayout()
        tab_bar_layout.setContentsMargins(0, 0, 0, 0)
        tab_bar_layout.setSpacing(2)

        self.btn_card = QPushButton("💳 Card")
        self.btn_batch = QPushButton("⚙️ Batch")
        self.btn_address = QPushButton("📍 Address")
        
        self.tab_buttons = [self.btn_card, self.btn_batch, self.btn_address]
        
        for i, btn in enumerate(self.tab_buttons):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, index=i: self.switch_tab(index))
            tab_bar_layout.addWidget(btn)

        main_layout.addLayout(tab_bar_layout)

        # Stacked Widget for content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(CardSimulatorTab())
        self.stacked_widget.addWidget(BatchGeneratorTab())
        self.stacked_widget.addWidget(AddressGeneratorTab())
        main_layout.addWidget(self.stacked_widget)

        # Initialize first tab
        self.switch_tab(0)

    def switch_tab(self, index):
        self.stacked_widget.setCurrentIndex(index)
        for i, btn in enumerate(self.tab_buttons):
            if i == index:
                # Active Tab Style
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        font-size: 14px;
                        font-weight: bold;
                        border: none;
                        border-top-left-radius: 8px;
                        border-top-right-radius: 8px;
                        padding: 12px 5px;
                    }
                """)
            else:
                # Inactive Tab Style
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #1e2a38;
                        color: #8899aa;
                        font-size: 14px;
                        font-weight: bold;
                        border: none;
                        border-top-left-radius: 8px;
                        border-top-right-radius: 8px;
                        padding: 12px 5px;
                        margin-top: 4px;
                    }
                """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(420, 780)
    win.show()
    sys.exit(app.exec())