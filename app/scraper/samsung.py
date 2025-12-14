from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import re


GALAXY_URLS = {
    "Galaxy S": "https://www.samsung.com/co/smartphones/galaxy-s/",
    "Galaxy A": "https://www.samsung.com/co/smartphones/galaxy-a/",
    "Galaxy Z": "https://www.samsung.com/co/smartphones/galaxy-z/"
}


# --------------------------------------------------
def limpiar_precio_cop(texto):
    if not texto:
        return None

    texto = (
        texto.replace(".", "")
        .replace("$", "")
        .replace("COP", "")
        .replace(",", "")
        .strip()
    )

    numeros = re.findall(r"\d{6,8}", texto)

    for n in numeros:
        valor = int(n)
        if 500_000 <= valor <= 20_000_000:
            return valor

    return None


# --------------------------------------------------
def obtener_precio(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    try:
        precio = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "price-ux__price-current")
            )
        ).text
        return limpiar_precio_cop(precio)
    except:
        pass

    elementos = driver.find_elements(By.XPATH, "//*[contains(text(),'$')]")
    for el in elementos:
        precio = limpiar_precio_cop(el.text)
        if precio:
            return precio

    return None


# --------------------------------------------------
def obtener_nombre_producto(driver, url):
    driver.get(url)
    try:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        ).text.strip()
    except:
        return None


# --------------------------------------------------
def scrape_linea(driver, linea, url):
    print(f"\n🔎 Scraping {linea}...\n")

    driver.get(url)
    time.sleep(5)

    cards = driver.find_elements(By.CLASS_NAME, "pd21-product-card__item")
    print(f"📦 Cards encontradas: {len(cards)}")

    productos_base = []

    for card in cards:
        try:
            producto_url = card.find_element(By.TAG_NAME, "a").get_attribute("href")

            try:
                nombre = card.find_element(
                    By.CLASS_NAME, "pd21-product-card__name"
                ).text.strip()
            except:
                nombre = None

            try:
                imagen = card.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                imagen = None

            productos_base.append({
                "nombre": nombre,
                "url": producto_url,
                "imagen": imagen
            })
        except:
            continue

    productos = []

    for idx, p in enumerate(productos_base, start=1):
        nombre_final = p["nombre"]
        if not nombre_final:
            nombre_final = obtener_nombre_producto(driver, p["url"])

        precio = obtener_precio(driver, p["url"])

        producto = {
            "marca": "Samsung",
            "linea": linea,
            "modelo": nombre_final,
            "precio": precio,
            "tienda": "Samsung",
            "imagen": p["imagen"],
            "url": p["url"],
            "fecha_actualizacion": datetime.now()
        }

        productos.append(producto)

        print(f"✅ {linea} #{idx}")
        print(f"   Modelo : {nombre_final}")
        print(f"   Precio : {precio}")
        print("-" * 50)

    return productos


# --------------------------------------------------
def scrape_samsung():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    todos = []

    for linea, url in GALAXY_URLS.items():
        productos = scrape_linea(driver, linea, url)
        todos.extend(productos)

    driver.quit()

    print(f"\n🎯 TOTAL GENERAL: {len(todos)} productos")
    return todos


# --------------------------------------------------
if __name__ == "__main__":
    productos = scrape_samsung()

    print("\n📊 RESULTADO FINAL")
    for p in productos:
        print(p)
