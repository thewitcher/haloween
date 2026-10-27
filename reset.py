#!/usr/bin/env python3
"""Reset gry uruchomionej lokalnie."""
import json, os, urllib.request
url="http://127.0.0.1:"+os.environ.get("SWIATY_PORT","8000")+"/api/admin/reset"
password=os.environ.get("SWIATY_HASLO","morthar-2026")
request=urllib.request.Request(url,data=json.dumps({"password":password}).encode(),headers={"Content-Type":"application/json"},method="POST")
try:
    with urllib.request.urlopen(request,timeout=5) as response: print(response.read().decode())
except Exception as exc: print("Nie udało się zresetować:",exc)
