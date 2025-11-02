# 🦊 My Animal Repository

A simple Python project that reads animal data from a JSON file, allows filtering by `skin_type`, and generates a responsive HTML page with neatly formatted animal cards.

---

## 📖 Overview

This project demonstrates how to:
- Load and process structured JSON data in Python.
- Prompt the user for a filtering option (`skin_type`).
- Dynamically generate an HTML page using a template.
- Safely embed text into HTML with proper escaping.
- Style data with CSS for a clean, readable layout.

It’s designed as an educational exercise for practicing file handling, string manipulation, and templating basics — with attention to accessibility and PEP 8 conventions.

---

## 🗂️ Project Structure

```
My-Zootopia/
│
├── animals_data.json          # Source data with animal details
├── animals_template.html      # HTML template with placeholders
├── animals.html               # Generated output file (after running the script)
├── main.py                    # Python script (contains logic)
└── README.md                  # This file
```

---

## ⚙️ How It Works

1. The script loads animal data from `animals_data.json`.
2. It scans available `skin_type` values (e.g. “Hair”, “Fur”, “Scales”).
3. The user chooses a `skin_type` (or `Unknown` if missing).
4. The script filters animals with that type.
5. It replaces a placeholder (`__REPLACE_ANIMALS_INFO__`) in the HTML template with generated content.
6. The finished page is saved as `animals.html` and ready to open in a browser.

---

## 💻 Usage

### 1. Run the script

```bash
python main.py
```

### 2. Choose a skin type
The program will show available options:

```
Available skin types:
 - Hair
 - Fur
 - Scales
 - Unknown
```

Then prompt you to enter one.

### 3. View the result
After completion, open the generated file:

```
animals.html
```

in your browser — it will display all matching animals in a nicely formatted list of cards.

---

## 🎨 HTML & CSS

The generated HTML uses semantic tags and a simple, responsive design.

- **Template file:** `animals_template.html`
- **Placeholder:** `__REPLACE_ANIMALS_INFO__`  
  is replaced dynamically by Python.
- **Main styles:** defined directly in the `<style>` block inside the template.

---

## 🧩 Key Python Functions

| Function | Purpose |
|-----------|----------|
| `load_data()` | Loads and parses the JSON file. |
| `collect_skin_types()` | Collects unique `skin_type` values. |
| `filter_by_skin_type()` | Filters animals by user-selected type. |
| `serialize_animal()` | Converts one animal record into an HTML block. |
| `create_new_html()` | Generates and writes the final `animals.html` file. |

---

## ✅ Features

- Follows **PEP 8** naming and formatting standards.
- UTF-8 safe file reading and HTML escaping.
- Handles animals missing `skin_type` (listed as “Unknown”).
- Clean, readable, mobile-friendly design.
- Minimal dependencies — uses only the Python standard library.

---

## 📋 Requirements

- Python 3.10+
- No third-party libraries required.

---

## 📄 License

This project is released for educational purposes and may be freely modified or shared.

---

## 💡 Author

Created by **[margarita-bykadorova](https://github.com/margarita-bykadorova)**  
