from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 이 부분을 추가

@app.route("/stocks", methods=["GET"])

def get_stocks():
    URL = "https://www.kokstock.com/stock/amount.asp?search_base=0&page=1&pagesize=20&view_quant=0&search_tp=KOSDAQ&search_quant=0&search_sort=5"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table tr")
    stocks = []

    for row in rows[1:6]:
        columns = row.select("td")
        stock_code_element = columns[1].select_one("span.copySelection")
        stock_code = stock_code_element.text.strip() if stock_code_element else None

        stock_url = (
            f"https://m.finance.daum.net/quotes/A{stock_code}/home"
            if stock_code
            else None
        )
        stock_img_src_d = (
            f"https://t1.daumcdn.net/finance/chart/kr/candle/d/A{stock_code}.png"
            if stock_code
            else None
        )
        stock_img_src_w = (
            f"https://t1.daumcdn.net/finance/chart/kr/candle/w/A{stock_code}.png"
            if stock_code
            else None
        )
        stock_img_src_m = (
            f"https://t1.daumcdn.net/finance/chart/kr/candle/m/A{stock_code}.png"
            if stock_code
            else None
        )

        stock_name_element = columns[2].select_one("a.StockItem")
        if stock_name_element:
            stock_name = stock_name_element.text.strip()
        else:
            stock_name = columns[2].text.strip()

        closing_price = columns[3].text.strip() + "원"
        rate_of_change_element = columns[4]
        rate_of_change = rate_of_change_element.text.strip()
        if rate_of_change_element.select_one("span.fBlue.text-rate"):
            rate_of_change = "-" + rate_of_change
        transaction_amount = columns[5].text.strip() + "억"
        market_cap_value = int(columns[7].text.strip().replace(",", ""))
        chos = market_cap_value // 10000
        oks = market_cap_value % 10000
        market_cap = f"{chos}조 {oks}억" if chos > 0 else f"{oks}억"

        stocks.append(
            {
                "code": stock_code,
                "name": stock_name,
                "closing_price": closing_price,
                "rate_of_change": rate_of_change,
                "transaction_amount": transaction_amount,
                "market_cap": market_cap,
                "stock_url": stock_url,
                "stock_img_src_d": stock_img_src_d,
                "stock_img_src_w": stock_img_src_w,
                "stock_img_src_m": stock_img_src_m,
            }
        )

    return jsonify(stocks)

if __name__ == "__main__":
    app.run(debug=True)

