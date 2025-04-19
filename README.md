# 🧪 SATE - Scanner Automation Tool Exploit

> **WordPress Vulnerability Scanner** built for vulnerability detection on plugins & themes.  
> Use responsibly. For authorized testing only.

---

## 🔍 Features

- 🎯 WordPress-specific scanning (Plugins & Themes)
- ⚙️ Support for bulk URL scanning
- 📦 CVE/Vulnerability Database integration from Wordfence API

---

## Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/6f946050-d1eb-4dd8-a5a6-86d2d5bbe700" width="100%" />
  <br><br>
  <img src="https://github.com/user-attachments/assets/d41b3359-77f9-4fae-a45d-36212723a5c7" width="100%" />
</p>

## ⚡ Usage

### 🔸 Basic Scan (Single URL)

```bash
python3 sate.py -u http://target.com --scan-plugins
```

### 🔸 Bulk Mode (Multi-site Scan)

```bash
python3 sate.py --web-list targets.txt --scan-plugins --scan-themes
```

### 🔸 Update Vulnerability DB

```bash
python3 sate.py --update-db
```

---

## 📦 Installation

```bash
git clone https://github.com/gibran-abdillah/sate.git
cd sate
pip install -r requirements.txt
```

---

## 🛑 Legal Disclaimer

> This tool is intended **ONLY** for authorized penetration testing, research, and educational purposes.  
> Misuse of this tool may result in **criminal charges**. The developers do not accept any responsibility for illegal usage.

---
