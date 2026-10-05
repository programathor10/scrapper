import json
import pandas as pd

# 1. Cargar el JSON
with open("liga_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

page_props = data.get("props", {}).get("pageProps", {})
datos_liga = page_props.get("data", {})
tablas = datos_liga.get("tables_groups", [])

# 2. Recorremos torneos, grupos y filas
for torneo in tablas:
    nombre_torneo = torneo.get("name", "Torneo")
    print(f"\n🏆 ================= {nombre_torneo} =================")
    
    zonas = torneo.get("tables", [])
    
    for zona in zonas:
        nombre_zona = zona.get("name", "Zona")
        
        # 'rows' está dentro de 'table' de la zona
        config_tabla = zona.get("table", {})
        filas = config_tabla.get("rows", [])
        
        equipos_procesados = []
        for fila in filas:
            num_pos = fila.get("num", "-")
            
            # Nombre del equipo
            entity = fila.get("entity", {}).get("object", {})
            equipo_nombre = entity.get("short_name") or entity.get("name", "Desconocido")
            
            # Mapeamos los valores estadísticos (Points, GamePlayed, Goals, etc.)
            valores_lista = fila.get("values", [])
            stats = {item.get("key"): item.get("value") for item in valores_lista if isinstance(item, dict)}
            
            datos_equipo = {
                "Pos": num_pos,
                "Equipo": equipo_nombre,
                "PTS": stats.get("Points", "-"),
                "PJ": stats.get("GamePlayed", "-"),
                "G": stats.get("GamesWon", "-"),
                "E": stats.get("GamesEven", "-"),
                "P": stats.get("GamesLost", "-"),
                "DG": stats.get("Ratio", "-"),
                "Goles": stats.get("Goals", "-"),
            }
            equipos_procesados.append(datos_equipo)
            
        if equipos_procesados:
            print(f"\n📊 --- {nombre_zona} ---")
            df = pd.DataFrame(equipos_procesados)
            print(df.to_string(index=False))