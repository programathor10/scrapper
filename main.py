import re
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. Definimos la URL de la portada
url = "https://www.promiedos.com.ar/"

# 2. Hacemos la petición HTTP para traer el HTML
response = requests.get(url, headers=headers)

# 3. Parseamos el HTML con BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# 4. Buscamos todas las ligas del menú lateral
ligas = soup.find_all("li", class_=re.compile("aside_selectItem"))

if not ligas:
    ligas = soup.select("div[class*='aside'] li")

# 5. Recorremos los resultados y extraemos el nombre y la URL
ligas_destacadas = []

for li in ligas:
    nombre_liga = li.text.strip()
    link_tag = li.find("a")
    link_url = link_tag["href"] if link_tag else None
    
    if nombre_liga:
        ligas_destacadas.append({
            "liga": nombre_liga,
            "url": link_url
        })

# 6. Elegimos la primera liga encontrada (Liga Profesional)
primera_liga = ligas_destacadas[0]
print(f"\n⚽ Scrapeando datos de: {primera_liga['liga']}...")

url_liga = primera_liga["url"]
if not url_liga.startswith("http"):
    url_liga = f"https://www.promiedos.com.ar{url_liga}"

print(f"URL de destino: {url_liga}")
res_liga = requests.get(url_liga, headers=headers)
soup_liga = BeautifulSoup(res_liga.text, "html.parser")

# 7. Buscamos las filas <tr> usando el patrón parcial de las clases inspeccionadas
filas = soup_liga.find_all("tr", class_=re.compile("table-row|row_row"))
print(f"Total de filas encontradas en la tabla: {len(filas)}")

# 8. Extraemos los datos de cada celda
tabla_posiciones = []

for fila in filas:
    celdas = fila.find_all(["td", "th"])
    datos_fila = [col.text.strip() for col in celdas if col.text.strip()]
    
    if datos_fila:
        tabla_posiciones.append(datos_fila)

# 9. Mostramos las primeras 10 filas extraídas
print("\n--- Primeros 10 equipos de la tabla ---")
for f in tabla_posiciones[:10]:
    print(f)


import json

# 7. Buscamos el tag script donde Next.js guarda la data cruda
next_data_script = soup_liga.find("script", id="__NEXT_DATA__")

if next_data_script:
    # Convertimos el texto del script a un diccionario de Python
    data = json.loads(next_data_script.string)
    
    print("✅ ¡JSON de Next.js encontrado e interpretado!")
    
    # 8. Guardamos el JSON completo para analizar la estructura exacta
    with open("liga_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("💾 Se guardó 'liga_data.json'. Ahora tenemos todos los datos estructurados.")
else:
    print("❌ No se encontró el tag __NEXT_DATA__")