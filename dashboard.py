import concurrent.futures
from bs4 import BeautifulSoup
import FinanceDataReader as fdr
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="계좌별 실시간 포트폴리오 대시보드",
    page_icon="📊",
    layout="wide",
)

# 60초(1분)마다 화면 자동 새로고침
st_autorefresh(interval=60000, key="portfolio_autorefresh")

# --- 2. 나의 포트폴리오 데이터 설정 ---
isa_portfolio = [
    {
        "ticker": "005389",
        "name": "현대차3우B",
        "avg_price": 223985,
        "quantity": 28,
        "category": "국내주식",
    },
    {
        "ticker": "071055",
        "name": "한국금융지주우",
        "avg_price": 164185,
        "quantity": 85,
        "category": "국내주식",
    },
    {
        "ticker": "003475",
        "name": "유안타증권우",
        "avg_price": 4282,
        "quantity": 450,
        "category": "국내주식",
    },
    {
        "ticker": "0098N0",
        "name": "PLUS자사주매입고배당주",
        "avg_price": 13362,
        "quantity": 920,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "329200",
        "name": "TIGER리츠부동산인프라",
        "avg_price": 4246,
        "quantity": 310,
        "category": "리츠",
    },
    {
        "ticker": "069500",
        "name": "KODEX200(7900)",
        "avg_price": 125217,
        "quantity": 17,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "152100",
        "name": "PLUS200(7880)",
        "avg_price": 126865,
        "quantity": 16,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "105190",
        "name": "ACE200(7810)",
        "avg_price": 123823,
        "quantity": 17,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "102110",
        "name": "TIGER200(7800)",
        "avg_price": 123962,
        "quantity": 17,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "122090",
        "name": "PLUS코스피50(7350)",
        "avg_price": 87776,
        "quantity": 9,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "237350",
        "name": "KODEX코스피100(7300)",
        "avg_price": 92649,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "277640",
        "name": "TIGER코스피대형주(7270)",
        "avg_price": 39822,
        "quantity": 13,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "337140",
        "name": "KODEX코스피대형주(7240)",
        "avg_price": 38421,
        "quantity": 14,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "302450",
        "name": "RISE코스피(7230)",
        "avg_price": 75063,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "305050",
        "name": "ACE코스피(7150)",
        "avg_price": 74304,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "277630",
        "name": "TIGER코스피(6965)",
        "avg_price": 72739,
        "quantity": 7,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "226490",
        "name": "KODEX코스피(6960)",
        "avg_price": 71678,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "153270",
        "name": "KIWOOM코스피100(6230)",
        "avg_price": 76743,
        "quantity": 3,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "360200",
        "name": "ACE미국S&P500",
        "avg_price": 27247,
        "quantity": 16,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "360750",
        "name": "TIGER미국S&P500",
        "avg_price": 26533,
        "quantity": 14,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "379780",
        "name": "RISE미국S&P500",
        "avg_price": 22864,
        "quantity": 10,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "449180",
        "name": "KODEX미국S&P500(H)",
        "avg_price": 17230,
        "quantity": 12,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "368590",
        "name": "RISE미국나스닥100",
        "avg_price": 30806,
        "quantity": 17,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "367380",
        "name": "ACE미국나스닥100",
        "avg_price": 31497,
        "quantity": 13,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "379810",
        "name": "KODEX미국나스닥100",
        "avg_price": 26607,
        "quantity": 10,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "449190",
        "name": "KODEX미국나스닥100(H)",
        "avg_price": 22180,
        "quantity": 11,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "458730",
        "name": "TIGER미국배당다우존스",
        "avg_price": 15042,
        "quantity": 31,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "475350",
        "name": "RISE버크셔포트폴리오TOP10",
        "avg_price": 14721,
        "quantity": 48,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "455030",
        "name": "KODEX미국달러SOFR금리액티브(합성)",
        "avg_price": 11906,
        "quantity": 13,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "455960",
        "name": "RISE미국달러SOFR금리액티브(합성)",
        "avg_price": 12161,
        "quantity": 12,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "456880",
        "name": "ACE미국달러SOFR금리(합성)",
        "avg_price": 12564,
        "quantity": 31,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "411060",
        "name": "ACEKRX 금현물",
        "avg_price": 26496,
        "quantity": 4,
        "category": "원자재",
    },
    {
        "ticker": "468380",
        "name": "KODEXiShares미국하이일드액티브",
        "avg_price": 11037,
        "quantity": 15,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "484790",
        "name": "KODEX미국30년국채액티브(H)",
        "avg_price": 8200,
        "quantity": 12,
        "category": "채권/파킹 ETF",
    },
]

pension_portfolio = [
    {
        "ticker": "0098N0",
        "name": "PLUS자사주매입고배당주",
        "avg_price": 13078,
        "quantity": 675,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "329200",
        "name": "TIGER리츠부동산인프라",
        "avg_price": 4249,
        "quantity": 301,
        "category": "리츠",
    },
    {
        "ticker": "069500",
        "name": "KODEX200(7260)",
        "avg_price": 115070,
        "quantity": 3,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "152100",
        "name": "PLUS200(7085)",
        "avg_price": 114095,
        "quantity": 1,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "105190",
        "name": "ACE200(7285)",
        "avg_price": 115513,
        "quantity": 3,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "102110",
        "name": "TIGER200(7260)",
        "avg_price": 115183,
        "quantity": 3,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "360200",
        "name": "ACE미국S&P500",
        "avg_price": 26518,
        "quantity": 9,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "449180",
        "name": "KODEX미국S&P500(H)",
        "avg_price": 17145,
        "quantity": 3,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "368590",
        "name": "RISE미국나스닥100",
        "avg_price": 30183,
        "quantity": 7,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "449190",
        "name": "KODEX미국나스닥100(H)",
        "avg_price": 22359,
        "quantity": 4,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "475350",
        "name": "RISE버크셔포트폴리오TOP10",
        "avg_price": 14684,
        "quantity": 24,
        "category": "해외지수 ETF",
    },
    {
        "ticker": "455030",
        "name": "KODEX미국달러SOFR금리액티브(합성)",
        "avg_price": 12005,
        "quantity": 5,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "455960",
        "name": "RISE미국달러SOFR금리액티브(합성)",
        "avg_price": 12276,
        "quantity": 12,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "456880",
        "name": "ACE미국달러SOFR금리(합성)",
        "avg_price": 12713,
        "quantity": 31,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "455660",
        "name": "ACE미국하이일드액티브(H)",
        "avg_price": 9708,
        "quantity": 26,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "484790",
        "name": "KODEX미국30년국채액티브(H)",
        "avg_price": 8178,
        "quantity": 6,
        "category": "채권/파킹 ETF",
    },
]

comprehensive_brokerage_portfolio = [
    {
        "ticker": "005389",
        "name": "현대차3우B",
        "avg_price": 205867,
        "quantity": 9,
        "category": "국내주식",
    },
    {
        "ticker": "0098N0",
        "name": "PLUS자사주매입고배당주",
        "avg_price": 13303,
        "quantity": 820,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "329200",
        "name": "TIGER리츠부동산인프라",
        "avg_price": 4238,
        "quantity": 310,
        "category": "리츠",
    },
    {
        "ticker": "069500",
        "name": "KODEX200(7900)",
        "avg_price": 124859,
        "quantity": 17,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "152100",
        "name": "PLUS200(7880)",
        "avg_price": 127220,
        "quantity": 16,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "105190",
        "name": "ACE200(7810)",
        "avg_price": 123788,
        "quantity": 17,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "102110",
        "name": "TIGER200(7800)",
        "avg_price": 123639,
        "quantity": 17,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "122090",
        "name": "PLUS코스피50(7350)",
        "avg_price": 87788,
        "quantity": 9,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "237350",
        "name": "KODEX코스피100(7300)",
        "avg_price": 92634,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "277640",
        "name": "TIGER코스피대형주(7270)",
        "avg_price": 39341,
        "quantity": 14,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "337140",
        "name": "KODEX코스피대형주(7240)",
        "avg_price": 38412,
        "quantity": 14,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "302450",
        "name": "RISE코스피(7230)",
        "avg_price": 75063,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "305050",
        "name": "ACE코스피(7150)",
        "avg_price": 74304,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "277630",
        "name": "TIGER코스피(6965)",
        "avg_price": 72749,
        "quantity": 7,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "226490",
        "name": "KODEX코스피(6960)",
        "avg_price": 71678,
        "quantity": 8,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "153270",
        "name": "KIWOOM코스피100(6230)",
        "avg_price": 76754,
        "quantity": 5,
        "category": "국내지수 ETF",
    },
    {
        "ticker": "455960",
        "name": "RISE미국달러SOFR금리액티브(합성)",
        "avg_price": 12343,
        "quantity": 12,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "456880",
        "name": "ACE미국달러SOFR금리(합성)",
        "avg_price": 12689,
        "quantity": 33,
        "category": "채권/파킹 ETF",
    },
    {
        "ticker": "455660",
        "name": "ACE미국하이일드액티브(H)",
        "avg_price": 9685,
        "quantity": 23,
        "category": "채권/파킹 ETF",
    },
]

# --- 3. 계좌 상태 유지 로직 (Query Parameters & Session State) ---
accounts = ("ISA 계좌", "연금 계좌", "위탁종합계좌")

# URL 쿼리 파라미터에서 현재 저장된 계좌 확인
query_account = st.query_params.get("account", None)

if "selected_account" not in st.session_state:
    if query_account in accounts:
        st.session_state["selected_account"] = query_account
    else:
        st.session_state["selected_account"] = accounts[0]


# 라디오 버튼 변경 시 URL 및 Session State 동기화하는 콜백 함수
def on_account_change():
    st.query_params["account"] = st.session_state["selected_account"]


st.sidebar.title("📌 계좌 선택")
selected_account = st.sidebar.radio(
    "조회할 계좌를 선택하세요:",
    accounts,
    key="selected_account",
    on_change=on_account_change,
)

# 현재 선택된 계좌 URL 파라미터 보장
st.query_params["account"] = selected_account

if selected_account == "ISA 계좌":
    current_portfolio = isa_portfolio
    page_title = "🏢 ISA 계좌 실시간 포트폴리오 맵"
elif selected_account == "연금 계좌":
    current_portfolio = pension_portfolio
    page_title = "🏦 연금 계좌 실시간 포트폴리오 맵"
else:
    current_portfolio = comprehensive_brokerage_portfolio
    page_title = "💼 위탁종합계좌 실시간 포트폴리오 맵"

st.title(page_title)


# --- 4. 병렬 처리로 모든 종목 실시간 가격 수집 ---
@st.cache_data(ttl=60)
def get_all_prices_parallel(tickers):
    def fetch(ticker):
        try:
            df_stock = fdr.DataReader(ticker)
            if not df_stock.empty:
                return ticker, float(df_stock["Close"].iloc[-1])
        except Exception:
            pass

        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            url = f"https://finance.naver.com/item/main.naver?code={ticker}"
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            price_elem = soup.select_one("p.no_today .blind")
            if price_elem:
                return ticker, float(price_elem.text.replace(",", ""))
        except Exception:
            pass

        return ticker, None

    prices = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ticker = {executor.submit(fetch, t): t for t in set(tickers)}
        for future in concurrent.futures.as_completed(future_to_ticker):
            t, p = future.result()
            prices[t] = p
    return prices


# --- 5. 계좌별 데이터 계산 ---
portfolio_data = []
tickers_to_fetch = [item["ticker"] for item in current_portfolio]

with st.spinner(
    "🚀 포트폴리오 주가 데이터를 고속(병렬)으로 불러오는 중입니다..."
):
    prices_dict = get_all_prices_parallel(tickers_to_fetch)

for item in current_portfolio:
    ticker = item["ticker"]
    current_price = prices_dict.get(ticker)

    if current_price is None or pd.isna(current_price):
        current_price = item["avg_price"]

    avg_price = item["avg_price"]
    quantity = item["quantity"]

    invested = avg_price * quantity
    current_value = current_price * quantity
    profit_loss = current_value - invested

    return_rate = (profit_loss / invested) * 100 if invested > 0 else 0.0

    portfolio_data.append(
        {
            "종목명": item["name"],
            "카테고리": item["category"],
            "티커": ticker,
            "보유수량": quantity,
            "평단가": avg_price,
            "현재가": current_price,
            "매수금액": invested,
            "평가금액": current_value,
            "수익금": profit_loss,
            "수익률": return_rate,
        }
    )

df = pd.DataFrame(portfolio_data)


# --- 6. Finviz 스타일 트리맵 ---
if not df.empty:
    finviz_colors = [
        [0.0, "#8B0000"],  # 더 또렷하고 깊은 레드
        [0.2, "#C62828"],
        [0.35, "#E53935"],
        [0.48, "#2A2A2A"],
        [0.5, "#1A1A1A"],  # 선명한 다크 그레이
        [0.52, "#2A2A2A"],
        [0.65, "#2E7D32"],
        [0.8, "#388E3C"],
        [1.0, "#1B5E20"],  # 더 또렷하고 깊은 그린
    ]

    df["return_str"] = df["수익률"].map(lambda x: f"{x:+.2f}%")

    fig = px.treemap(
        df,
        path=[px.Constant(selected_account), "카테고리", "종목명"],
        values="평가금액",
        color="수익률",
        color_continuous_scale=finviz_colors,
        range_color=[-3.0, 3.0],
        color_continuous_midpoint=0,
        custom_data=[
            "return_str",
            "평가금액",
            "수익금",
            "평단가",
            "현재가",
            "보유수량",
        ],
    )

    fig.update_traces(
        texttemplate=(
            "<b>%{label}</b><br>"
            "<span style='font-size: 13px;'>%{customdata[5]:,.0f}주 · 평단: %{customdata[3]:,.0f}원</span><br>"
            "<span style='font-size: 16px; font-weight: 900;'>%{customdata[0]}</span>"
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "보유수량: %{customdata[5]:,.0f}주<br>"
            "평단가: %{customdata[3]:,.0f}원<br>"
            "현재가: %{customdata[4]:,.0f}원<br>"
            "평가금액: %{customdata[1]:,.0f}원<br>"
            "수익금: %{customdata[2]:+,.0f}원<br>"
            "수익률: %{customdata[0]}"
        ),
        textfont=dict(
            size=15,
            family="Pretendard, Malgun Gothic, Apple SD Gothic Neo, sans-serif",
            color="#FFFFFF",
        ),
        marker=dict(
            line=dict(width=1.5, color="#121212"),
            pad=dict(t=25, l=4, r=4, b=4),
        ),
        tiling=dict(packing="squarify"),
    )

    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        height=700,
        coloraxis_showscale=False,
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("포트폴리오 데이터가 존재하지 않습니다.")
