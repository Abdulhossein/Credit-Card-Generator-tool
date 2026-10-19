# 💳 Card & Address Tools

A mobile-friendly PySide6 desktop application for generating **test credit card numbers**, **bulk card data**, and **fake addresses** for multiple countries. Built with a touch-optimized, dark-themed interface.

> ⚠️ **Disclaimer:** This tool is intended **strictly for development, QA testing, and educational purposes**. Generated card numbers are mathematically valid (pass the Luhn algorithm) but are **not real**. Do not use them for fraud or any illegal activity.

---

## ✨ Features

### 💳 Card Simulator
- Generates **Luhn-valid** card numbers
- Supports **Visa**, **Mastercard**, and **American Express**
- Auto-generated **expiry date**, **CVV**, and **cardholder name**
- One-tap copy for each field or the entire card

### ⚙️ Batch Generator
- Generate **1–50 cards** at once
- Custom **BIN prefix** (e.g. `4` for Visa, `51` for Mastercard)
- Auto-detects card length (15 digits for Amex, 16 for others)
- Scrollable touch-friendly result list
- Individual copy button per card

### 📍 Address Generator
- Fake addresses for **8 countries**:
  - 🇺🇸 United States
  - 🇬🇧 United Kingdom
  - 🇨🇦 Canada
  - 🇦🇺 Australia
  - 🇩🇪 Germany
  - 🇫🇷 France
  - 🇯🇵 Japan
  - 🇧🇷 Brazil
- Fields: Full name, street, city, state/province, postal code, phone
- Copy individual fields or the full formatted address

---

## 🖼️ UI Highlights

- **Dark theme** with a modern blue accent palette
- **Custom tab bar** designed for mobile/tablet layouts
- **Touch-friendly** buttons (50px+ tap targets)
- **Custom spin box** with large +/− buttons
- **Smooth scrolling** with `QScroller` touch gestures
- Responsive layout that adapts to resizing

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language  | Python 3.9+ |
| GUI       | [PySide6](https://pypi.org/project/PySide6/) |
| Algorithm | Luhn checksum |
| Platform  | Windows / Linux / macOS |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/card-address-tools.git
cd card-address-tools