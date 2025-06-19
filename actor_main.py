import asyncio
import Apify
from src.get_g2_products import get_g2_products     # ← eigentliche Scraper-Funktion

async def main() -> None:
    # Eingabe vom Actor holen (JSON aus dem Input-Tab)
    inp = await Apify.get_input() or {}

    # Defaults setzen (sonst kracht die Botasaurus-Funktion bei leerem Input)
    inp.setdefault("search_queries", [])
    inp.setdefault("max_reviews", 1000)

    # --- SCRAPEN ----------------------------------------------------------
    # Achtung: get_g2_products ist synchron → daher in Thread ausführen
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, get_g2_products, inp)
    # ----------------------------------------------------------------------

    # Datensätze ins default-Dataset schreiben
    await Apify.push_data(result)

    # Kleines Status-Objekt als Key-Value-Store-Eintrag „OUTPUT“
    await Apify.set_value("OUTPUT", {
        "items_scraped": len(result),
        "ok": True,
    })

Apify.run(main)        # <- Pflicht für jeden Apify-Actor
