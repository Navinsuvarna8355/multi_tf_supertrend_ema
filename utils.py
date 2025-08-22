import requests
import json
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def fetch_option_chain(symbol="NIFTY"):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": f"https://www.nseindia.com/option-chain"
    }
    session = requests.Session()
    try:
        # Warm-up request to get cookies
        session.get("https://www.nseindia.com/option-chain", headers=headers, timeout=5)
        response = session.get(url, headers=headers, timeout=5)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"⚠️ NSE scrape failed: {e}")
        return None

def parse_option_metrics(data):
    if not data:
        return {"PCR": None, "IV": None, "Delta": None, "Gamma": None, "Vega": None}

    expiry_dates = data["records"]["expiryDates"]
    current_expiry = expiry_dates[0]
    total_ce_oi = 0
    total_pe_oi = 0
    atm_iv = None
    atm_delta = None
    atm_gamma = None
    atm_vega = None

    underlying = data["records"]["underlyingValue"]
    strikes = sorted({item["strikePrice"] for item in data["records"]["data"]})
    atm_strike = min(strikes, key=lambda x: abs(x - underlying))

    for item in data["records"]["data"]:
        if item["expiryDate"] != current_expiry:
            continue
        strike = item["strikePrice"]
        ce = item.get("CE", {})
        pe = item.get("PE", {})
        total_ce_oi += ce.get("openInterest", 0)
        total_pe_oi += pe.get("openInterest", 0)

        if strike == atm_strike:
            atm_iv = (ce.get("impliedVolatility", 0) + pe.get("impliedVolatility", 0)) / 2
            atm_delta = ce.get("delta", None)
            atm_gamma = ce.get("gamma", None)
            atm_vega = ce.get("vega", None)

    pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi else None
    return {
        "PCR": pcr,
        "IV": atm_iv,
        "Delta": atm_delta,
        "Gamma": atm_gamma,
        "Vega": atm_vega
    }

def fetch_option_metrics(symbol="NIFTY"):
    data = fetch_option_chain(symbol)
    return parse_option_metrics(data)

def fetch_index_data(symbol="NIFTY"):
    try:
        data = fetch_option_chain(symbol)
        if not data:
            return {"last_price": None, "change": None, "percent_change": None}
        last_price = data["records"]["underlyingValue"]
        return {
            "last_price": last_price,
            "change": None,
            "percent_change": None
        }
    except Exception as e:
        print(f"⚠️ Index fetch failed: {e}")
        return {"last_price": None, "change": None, "percent_change": None}
