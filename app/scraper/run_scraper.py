from app.scraper.samsung import scrape_samsung
from app.scraper.falabella import scrape_falabella
from app.scraper.productos_repo import guardar_productos


def ejecutar_scrapers():
    print("\n🚀 Iniciando proceso de scraping...\n")

    productos_totales = []

    # 🔹 Samsung
    print("🔵 Ejecutando scraper Samsung...\n")
    productos_samsung = scrape_samsung()
    print(f"🧾 Samsung: {len(productos_samsung)} productos\n")
    productos_totales.extend(productos_samsung)

    # 🔹 Falabella
    print("🟠 Ejecutando scraper Falabella...\n")
    productos_falabella = scrape_falabella()
    print(f"🧾 Falabella: {len(productos_falabella)} productos\n")
    productos_totales.extend(productos_falabella)

    print(f"📦 Total productos recolectados: {len(productos_totales)}\n")

    # 🔹 Guardar en MongoDB
    guardar_productos(productos_totales)

    print("✅ Productos guardados / actualizados en MongoDB")


if __name__ == "__main__":
    ejecutar_scrapers()
