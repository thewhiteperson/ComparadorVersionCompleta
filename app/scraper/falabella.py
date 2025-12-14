from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import re

URL = "https://www.falabella.com.co/falabella-co/search?Ntt=samsung&facetSelected=true&f.product.L1_category_paths=cat50868%7C%7CTecnolog%C3%ADa%2Fcat910963%7C%7CTelefon%C3%ADa&f.product.attribute.Sistema_operativo=android&f.product.brandName=samsung"


def detectar_linea(nombre):
    if not nombre:
        return "Desconocida"
    nombre = nombre.upper()
    if "GALAXY S" in nombre:
        return "Galaxy S"
    if "GALAXY Z" in nombre:
        return "Galaxy Z"
    if "GALAXY A" in nombre:
        return "Galaxy A"
    return "Otra"


def limpiar_precio(texto):
    if not texto:
        return None
    numeros = re.sub(r"[^\d]", "", texto)
    return int(numeros) if numeros else None


def scrape_falabella():
    print("🔎 Iniciando scraping Falabella Samsung...\n")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)
    time.sleep(6)

    productos = []

    cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="ssr-pod"]')
    print(f"📦 Productos encontrados: {len(cards)}\n")

    for idx, card in enumerate(cards, start=1):
        try:
            # Marca
            try:
                marca = card.find_element(By.CLASS_NAME, "pod-title").text
            except:
                marca = "Samsung"

            # Nombre / Modelo
            try:
                nombre = card.find_element(By.CLASS_NAME, "pod-subTitle").text
            except:
                nombre = None

            # Precio
            try:
                precio_texto = card.find_element(By.CLASS_NAME, "line-height-22").text
                precio = limpiar_precio(precio_texto)
            except:
                precio = None

            # URL
            try:
                url = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                url = None

            linea = detectar_linea(nombre)

            producto = {
                "marca": marca,
                "linea": linea,
                "modelo": nombre,
                "precio": precio,
                "tienda": "Falabella",
                "url": url,
                "fecha_actualizacion": datetime.now()
            }

            productos.append(producto)

            print(f"✅ Producto #{idx}")
            print(f"   Modelo : {nombre}")
            print(f"   Línea  : {linea}")
            print(f"   Precio : {precio}")
            print("-" * 60)

        except Exception as e:
            print(f"❌ Error producto #{idx}: {e}")

    driver.quit()

    print(f"\n🎯 Total productos guardados: {len(productos)}")
    return productos


# 🚀 ESTE BLOQUE ES OBLIGATORIO
if __name__ == "__main__":
    productos = scrape_falabella()

    print("\n📊 RESULTADO FINAL")
    for p in productos:
        print(p)
