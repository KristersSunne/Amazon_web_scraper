# Amazon.de Cena Meklētājs

## Projekta dalībnieki
- **Kristers Sunne**
- **Jorens Jānis Trēgers**

---

## Projekta uzdevums

Šis projekts paredzēts, lai automatizēti meklētu produktu cenas **Amazon.de** vietnē, pamatojoties uz lietotāja ievadi.

Programmas galvenie uzdevumi:
- Lietotājs ievada meklējamo produktu un minimālo cenu.
- Tiek atvērta Amazon.de lapa un meklēta attiecīgā prece.
- Ja preces cena pārsniedz norādīto minimumu, tās nosaukums un cena tiek saglabāta `filtered_results.json` failā.
- Katram produktam tiek pievienots arī **laiks un datums**, kad cena tika atrasta.
- Ja produkts jau eksistē ar citu cenu, vecā informācija netiek pārrakstīta — tā vietā tiek saglabāta cenu **vēsture**.

---

##  Izmantotās Python bibliotēkas

| Bibliotēka | Lietojums |
|------------|-----------|
| `selenium` | Lai atvērtu mājaslapu no kuras tiek nolasīti header faili, kuru nosaukums sakrīt ar meklēto preci |
| `json`     | Json faila atveršanai, modifikācijai, lasīšanai vai izveidošanai, lai saglabātu meklētās preces cenu, laiku un datumu vienā vietā |
| `os`       | Lai vienkārši pārbaudītu faila ceļa eksistēšanu |
| `re`       | Regulāro izteiksmju izmantošana produktu nosaukumu attīrīšanai |
| `datetime` | Precīzai laika un datuma uzskaitei cenu vēsturē |

---

## Pašu definētas datu struktūras

Projektā izmantojām iebūvētas Python library un Python lists - kā pielāgotas struktūras, lai uzglabātu un pārvaldītu produktu informāciju.

---

###  1. Produkta ieraksts (`new_entry`)

**Fails:** `main.py`  
 **Rinda:** `104 - 107`

```python
save_to_json("filtered_results.json", {
    "title": cleaned_title,
    "price": price_text
})
```
Šī vārdnīca pārstāv vienu produktu ar tā pašreizējo cenu. Tā tiek padota uz save_to_json() funkciju tālākai apstrādei un saglabāšanai.

### 2. Cena ar laika zīmogu (`price_history`)

**Fails:** `main.py`  
**Rinda:** `39-52`

```python

# Ja cena mainās:

    for item in data:
        if item["title"] == new_entry["title"]:
            if item["price"] != new_entry["price"]:
                item["price"] = new_entry["price"]
                item.setdefault("price_history", []).append({
                    "price": new_entry["price"],
                    "timestamp": timestamp
                })
            return

# Ja jauns produkts:

    new_entry["price_history"] = [{
        "price": new_entry["price"],
        "timestamp": timestamp
    }]
```