# 🔗 Short Link Bypasser

A Python script to automatically bypass short link services (e.g., linkjust.com) and retrieve the final destination URL.  
It simulates real browser requests using **HTTP/2** and **BeautifulSoup** for parsing hidden fields and tokens.

---

## ✨ Features
- Supports **HTTP/2** requests via `httpx`.
- Parses CSRF tokens and hidden form data automatically.
- Custom **delay** and **number of requests** for bypassing link protection.
- CLI-based logs and MySQL-style table output for configuration details.

---

## ⚙️ Requirements
- Python **3.8+**
- Install dependencies:
```bash
pip install httpx[http2] beautifulsoup4
```

---

## 📦 Usage
```bash
python short_link_bypasser.py <short_link_url>
```

### Example:
```bash
python short_link_bypasser.py https://linkjust.com/1KEvtFiwr
```

If no URL is provided, the script displays usage instructions:
```
+------------------------------------------------------------------------+
| Requirements ==> pip install httpx[http2] beautifulsoup4               |
| Usage ==> python short_link_bypasser.py https://linkjust.com/1KEvtFiwr |
+------------------------------------------------------------------------+
```

---

## 📜 Configuration
Supported websites are defined in the `websites` dictionary:
```python
websites = {
    "linkjust.com": {
        "second_url": "https://linkjust.com/links/go",
        "referer": "https://forexrw7.com/",
        "delay": 5,
        "requsts_number": 2,
    }
}
```
You can add more websites by extending this dictionary.

---

## 🔍 Example Output
```
+--------------------------------------------+
|                  CONFIGS                   |
+--------------------+-----------------------+
| Host               | linkjust.com          |
| Number of Requests | 2                     |
| Delay              | 5                     |
| Referer            | https://forexrw7.com/ |
+--------------------+-----------------------+

Logs:
======
[*] First Request ==> 200, done
[*] Sleeping 5 seconds ...
[*] Second Request ==> 200, done

[=] Final URL: https://destination.com/page
```

---

## 🖼 Screenshot
Here’s an example of the script in action:

![Short Link Bypasser Screenshot](./assets/screenshot.png)

> Save a screenshot of your terminal output as `assets/screenshot.png`.


## ⭐ Support
If you find this project helpful, please consider giving it a **star** on GitHub!

[![Star](https://img.shields.io/github/stars/your-username/short-link-bypasser?style=social)](https://github.com/your-username/short-link-bypasser)
