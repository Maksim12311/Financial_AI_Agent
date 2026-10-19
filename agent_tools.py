
import json
import yfinance as yf
from ollama import chat

MODEL = "qwen2.5:7b"


# Tool 1: Stock market analysis
def get_stock_data(ticker: str, period: str = "1mo") -> str:
    """Get stock prices and performance. Period: 5d, 1mo, 3mo, 6mo, 1y."""

    ticker = ticker.strip().upper()
    period = str(period).strip().lower()

    period_mapping = {
        "30d": "1mo",
        "1m": "1mo",
        "1month": "1mo",
        "90d": "3mo",
        "180d": "6mo",
        "365d": "1y",
        "12mo": "1y",
        "1d": "5d"
    }

    period = period_mapping.get(period, period)

    allowed_periods = ["5d", "1mo", "3mo", "6mo", "1y"]

    if period not in allowed_periods:
        return json.dumps({
            "error": f"Unsupported period: {period}",
            "allowed_periods": allowed_periods
        })

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)

        if data.empty:
            return json.dumps({
                "error": f"No stock data found for {ticker}"
            })

        first = float(data["Close"].iloc[0])
        last = float(data["Close"].iloc[-1])

        result = {
            "ticker": ticker,
            "period": period,
            "start_date": str(data.index[0].date()),
            "end_date": str(data.index[-1].date()),
            "first_close": round(first, 2),
            "last_close": round(last, 2),
            "price_change_percent": round(
                (last / first - 1) * 100, 2
            ),
            "period_high": round(float(data["High"].max()), 2),
            "period_low": round(float(data["Low"].min()), 2),
            "average_daily_volume": round(
                float(data["Volume"].mean())
            )
        }

        return json.dumps(result)

    except Exception as e:
        return json.dumps({"error": str(e)})


# Tool 2: Fundamental financial analysis
def get_company_fundamentals(ticker: str) -> str:
    """Get P/E ratio, EPS, market cap, revenue and financial ratios."""

    ticker = ticker.strip().upper()

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or not info.get("symbol"):
            return json.dumps({
                "error": f"No company information found for {ticker}"
            })

        result = {
            "ticker": ticker,
            "company_name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "currency": info.get("currency"),
            "market_cap": info.get("marketCap"),
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "trailing_eps": info.get("trailingEps"),
            "total_revenue": info.get("totalRevenue"),
            "profit_margin": info.get("profitMargins"),
            "debt_to_equity": info.get("debtToEquity"),
            "return_on_equity": info.get("returnOnEquity")
        }

        return json.dumps(result)

    except Exception as e:
        return json.dumps({"error": str(e)})


# Available agent tools
available_tools = {
    "get_stock_data": get_stock_data,
    "get_company_fundamentals": get_company_fundamentals
}


# AI agent instructions
messages = [
    {
        "role": "system",
        "content": (
            "You are a professional AI Financial Analyst Agent. "
            "You have access to two financial analysis tools. "
            "Use get_stock_data for stock prices, historical "
            "performance and comparisons. "
            "Use get_company_fundamentals for P/E ratios, "
            "EPS, market capitalization, revenue, "
            "profitability and valuation comparisons. "
            "Always call the appropriate tools when financial "
            "data is needed. "
            "For company comparisons, retrieve data for "
            "every company involved. "
            "Use only figures returned by your tools. "
            "Never invent stock prices, financial ratios, "
            "company earnings or market news. "
            "If data is missing, clearly explain it. "
            "Do not confuse daily and monthly statistics. "
            "Explain your analysis in clear, simple English. "
            "Do not provide personalized investment advice."
        )
    }
]


print("===================================")
print("      AI FINANCIAL ANALYST AGENT")
print("===================================")
print("Powered by Ollama + Yahoo Finance")
print("Model:", MODEL)
print()
print("Capabilities:")
print("- Stock price analysis")
print("- Company financial fundamentals")
print("- Stock and company comparisons")
print("- AI-powered financial explanations")
print()
print("Type 'exit' to quit.")
print()


# Main agent loop
while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    messages.append({
        "role": "user",
        "content": question
    })

    try:
        for step in range(6):
            response = chat(
                model=MODEL,
                messages=messages,
                tools=[
                    get_stock_data,
                    get_company_fundamentals
                ]
            )

            messages.append(response.message)

            if not response.message.tool_calls:
                print("\nAI Financial Analyst:\n")
                print(response.message.content)
                print()
                break

            for call in response.message.tool_calls:
                name = call.function.name
                arguments = call.function.arguments

                print(f"\n[Tool Call] {name}")
                print("Arguments:", arguments)

                if name in available_tools:
                    try:
                        result = available_tools[name](**arguments)
                    except Exception as e:
                        result = json.dumps({
                            "error": str(e)
                        })
                else:
                    result = json.dumps({
                        "error": f"Unknown tool: {name}"
                    })

                print("[Tool Result]", result)

                messages.append({
                    "role": "tool",
                    "tool_name": name,
                    "content": str(result)
                })

        else:
            print("Agent reached the tool-call limit.")

    except Exception as e:
        print("Error:", e)
