from datetime import datetime
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, "kod", "pipeline.txt"), "a", encoding="utf-8") as plik:
    plik.write(f"Uruchomiono: {datetime.now()}\n")