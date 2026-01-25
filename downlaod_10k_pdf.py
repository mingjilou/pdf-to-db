import requests
from pathlib import Path

HEADERS = {
    "User-Agent": "Mingji your@email.com"  # REQUIRED by SEC
}

def cik_from_ticker(ticker: str) -> str:
    url = "https://www.sec.gov/files/company_tickers.json"
    data = requests.get(url, headers=HEADERS).json()
    for v in data.values():
        if v["ticker"].lower() == ticker.lower():
            return str(v["cik_str"]).zfill(10)
    raise ValueError("Ticker not found")

def download_latest_10k_pdf(ticker: str, out_dir="pdf_reports"):
    cik = cik_from_ticker(ticker)
    submissions = requests.get(
        f"https://data.sec.gov/submissions/CIK{cik}.json",
        headers=HEADERS
    ).json()

    filings = submissions["filings"]["recent"]
    for form, accession, doc in zip(
        filings["form"],
        filings["accessionNumber"],
        filings["primaryDocument"]
    ):
        if form == "10-K":
            accession_nodash = accession.replace("-", "")
            base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_nodash}"
            pdf_url = f"{base}/{doc}"

            Path(out_dir).mkdir(exist_ok=True)
            pdf_path = Path(out_dir) / f"{ticker}_10K.pdf"

            r = requests.get(pdf_url, headers=HEADERS)
            pdf_path.write_bytes(r.content)

            return pdf_path

    raise RuntimeError("No 10-K found")

# Example
download_latest_10k_pdf("AAPL")
