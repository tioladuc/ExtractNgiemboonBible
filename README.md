Here’s a clean, professional **README.md** draft for your project structure 👇
You can copy-paste this into your `README.md` file.

---

```markdown
# 📖 Bible Extraction and Comparison Tool

This project provides a set of Python scripts for extracting, transforming, and comparing Bible texts between different versions or languages.  
It is designed to process HTML files from various Bible sources, extract verses by chapter, and export them into structured CSV files for further analysis.

---

## 🗂️ Project Structure

│   extractbible_old.py
│   extract_all_bible.py
│   extract_csv_bible.py
│   extract_new_testament_bible_old.py
│   README.md
│
├───core_bible
│   ├───CSB
│   │   │   list_of_urls.txt
│   │   │
│   │   ├───1CH
│   │   │       339_chap_1.html
│   │   │       340_chap_2.html
│   │   │       341_chap_3.html
│   │   │
│   │   ├───1CO
│   │   │       914_chap_1.html
│   │   │       915_chap_2.html
│   │   │
│   │   └───1JN
│   │           1011_chap_1.html
│   │           1012_chap_2.html
│   │
│   └───NNH
│       │   list_of_urls.txt
│       │
│       ├───1CH
│       │       339_chap_1.html
│       │       340_chap_2.html
│       │
│       ├───1CO
│       │       1063_chap_1.html
│       │       1064_chap_2.html
│       │
│       └───1JN
│               1160_chap_1.html
│               1161_chap_2.html
│
└───csv_bible
    │   coherences_verses.txt
    │   incoherences_verses.txt
    │
    ├───1CH
    │       chap_1.csv
    │       chap_2.csv
    │
    ├───1CO
    │       chap_1.csv
    │       chap_2.csv
    │
    └───1JN
            chap_1.csv
            chap_2.csv
---

## 🧩 Folder Description

### `core_bible/`
Contains the **raw HTML files** for each Bible version or language.

- `CSB/` → Example: Christian Standard Bible version (English)
- `NNH/` → Example: Ngiemboon or local language version
- Each book (e.g., `1CH`, `1CO`, `1JN`) has HTML chapters (`*_chap_X.html`)
- `list_of_urls.txt` keeps track of the source web links used for extraction.

---

### `csv_bible/`
Contains the **processed CSV output** generated from the extraction scripts.

- Each book folder (e.g., `1CH/`, `1CO/`, `1JN/`) contains `chap_X.csv`
- `coherences_verses.txt` → lists matching verse pairs between translations
- `incoherences_verses.txt` → lists mismatched or missing verses

---

## ⚙️ Main Python Scripts

| Script | Description |
|--------|--------------|
| `extract_all_bible.py` | Extracts and converts all available Bible chapters to CSV format. |
| `extract_csv_bible.py` | Transforms individual HTML chapter files into structured CSV files. |
| `extractbible_old.py` | Legacy version of the main extraction logic (kept for reference). |
| `extract_new_testament_bible_old.py` | Extracts only the New Testament from HTML sources (older version). |

---

## 🪄 How It Works

1. **Download or prepare** Bible chapter HTML files into `core_bible/<VERSION>/<BOOK>/`.
2. **Run** one of the Python scripts (for example):
   ```bash
   python extract_all_bible.py
````

3. The program will:

   * Parse HTML content
   * Extract verse references and text
   * Generate `.csv` files under `csv_bible/<BOOK>/`
   * Log consistent and inconsistent verse mappings in the `.txt` files

---

## 🧰 Requirements

* Python 3.8+
* Libraries: `os`, `re`, `csv`, `bs4` (BeautifulSoup), `requests` (if downloading)

Install dependencies:

```bash
pip install beautifulsoup4 requests
```

---

## 📊 Output Example

A generated `csv_bible/1CO/chap_1.csv` might look like:

| Verse | CSB_Text                      | NNH_Text            |
| ----- | ----------------------------- | ------------------- |
| 1     | Paul, called as an apostle... | Pɔ́lɔ, ŋwá bɔ́ ... |
| 2     | To the church of God...       | Kɔ̀nɛ́ ɲù mɛ̀ ...  |

---

## 🧠 Notes

* The folder and file naming follows the **book abbreviations** and chapter numbering system.
* Each translation version is isolated to simplify comparisons.
* The project can be extended to support additional versions or automated HTML downloads.

---

## 📜 License

This project is distributed under the **MIT License** — feel free to use, modify, and share.

---

## 👤 Author

**Duclair T L**
*Analyst-Programmer & Bible Digitalization Enthusiast*

---

```

---

Would you like me to add a **“Usage Example” section** showing how to call `extract_csv_bible.py` on one book (e.g. `1JN`) from the command line or inside Python?
```

