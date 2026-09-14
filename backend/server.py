from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from database.data import BUYERS, CROPS, MARKETS, QUALITY_GRADES, RENTALS, apply_quality_price, distances_from, market_rows

ROOT = Path(__file__).resolve().parent.parent


def records(frame):
    return frame.to_dict(orient="records")


def recommendation(payload: dict) -> dict:
    crop = payload.get("crop", "Tomato")
    location = str(payload.get("location", ""))
    quantity = max(1, float(payload.get("quantity", 500)))
    transport = max(0, float(payload.get("transport_cost", 12)))
    grade = payload.get("grade", "Standard grade")
    days = max(1, int(payload.get("days", 3)))
    rows = market_rows(crop)
    rows["Price"] = rows["Price (₹/kg)"].map(lambda price: apply_quality_price(price, grade))
    distances = distances_from(location)
    rows["Your distance"] = rows["Location"].map(distances).fillna(rows["Distance (km)"])
    rows["Net"] = rows.apply(lambda row: row["Price"] * quantity - float(RENTALS.loc[RENTALS["Market"] == row["Market"], "Daily rent"].iloc[0]) * days - transport * row["Your distance"] * 2, axis=1)
    best = rows.loc[rows["Net"].idxmax()]
    rental = RENTALS[RENTALS["Market"] == best["Market"]].iloc[0]
    offers = BUYERS[BUYERS["Crop"] == crop].copy()
    offers["Distance"] = offers["Location"].map(distances).fillna(best["Your distance"])
    offers["Price adjusted"] = offers["Price"].map(lambda price: apply_quality_price(price, grade))
    offers["Net earning"] = offers["Price adjusted"] * quantity - transport * offers["Distance"] * 2
    best_buyer = offers.loc[offers["Net earning"].idxmax()] if not offers.empty else None
    shop_net = int(best["Net"])
    buyer_net = int(best_buyer["Net earning"]) if best_buyer is not None else 0
    return {"best": {"market": best["Market"], "location": best["Location"], "price": float(best["Price"]), "distance": int(best["Your distance"])}, "rental": {"shop": rental["Shop"], "daily_rent": int(rental["Daily rent"]), "security_deposit": int(rental["Security deposit"]), "landmark": rental["Landmark"]}, "shop_net": shop_net, "recommendation": "Rent a shop" if shop_net >= buyer_net else f"Sell to {best_buyer['Buyer']}", "recommendation_value": max(shop_net, buyer_net), "offers": [{"buyer": row["Buyer"], "type": row["Type"], "location": row["Location"], "price": float(row["Price adjusted"]), "net_earning": int(row["Net earning"])} for _, row in offers.sort_values("Net earning", ascending=False).iterrows()]}


class AppHandler(BaseHTTPRequestHandler):
    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/bootstrap":
            self.send_json({"crops": CROPS, "quality_grades": QUALITY_GRADES, "markets": records(MARKETS), "buyers": records(BUYERS)})
            return
        file_path = ROOT / path.lstrip("/") if path.startswith("/frontend/") else ROOT / "frontend" / "index.html"
        if file_path.is_file():
            content_type = "text/css" if file_path.suffix == ".css" else "application/javascript" if file_path.suffix == ".js" else "text/html"
            body = file_path.read_bytes(); self.send_response(200); self.send_header("Content-Type", content_type); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        self.send_error(404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/recommendation": self.send_error(404); return
        length = int(self.headers.get("Content-Length", 0)); payload = json.loads(self.rfile.read(length) or b"{}"); self.send_json(recommendation(payload))

    def log_message(self, *_):
        return


def run(host="127.0.0.1", port=8000):
    print(f"AgriConnect web app: http://{host}:{port}")
    ThreadingHTTPServer((host, port), AppHandler).serve_forever()


if __name__ == "__main__":
    run()
