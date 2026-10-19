
import json
import yfinance as yf
from ollama import chat

MODEL = "qwen2.5:7b"


def get_stock_data(ticker: str, period: str = "1mo") -> str:
    """Get stock market performance for a company ticker."""
    ticker = ticker.strip().upper()

    allowed_periods = ["5d", "1mo", "3mo", "6mo", "1y"]
    if period not in allowed_periods:
        return "Error: Unsupported period."

    try:
        data = yf.Ticker(ticker).history(period=period)

        if data.empty:
            return f"No stock data found for {ticker}."

        first = float(data["Close"].iloc[0])
        last = float(data["Close"].iloc[-1])

        result = {
            "ticker": ticker,
            "period": period,
            "first_date": str(data.index[0].date()),
            "last_date": str(data.index[-1].date()),
            "first_close": round(first, 2),
            "last_close": round(last, 2),
            "change_percent": round((last / first - 1) * 100, 2),
            "highest_price": round(float(data["High"].max()), 2),
            "lowest_price": round(float(data["Low"].min()), 2),
            "average_volume": round(float(data["Volume"].mean()))
        }

        return json.dumps(result)

    except Exception as e:
        return f"Error retrieving data: {e}"


tools = {
    "get_stock_data": get_stock_data
}

messages = [
    {
        "role": "system",
        "content": (
            "You are a financial analysis AI agent. "
            "Use get_stock_data when the user requests stock "
            "prices, performance or comparisons. "
            "Never invent financial figures or market news. "
            "Use the dates returned by tools and distinguish "
            "observed performance from predictions. "
            "Explain your findings in simple English. "
            "Do not give personalized investment advice."
        )
    }
]

print("=== AI FINANCIAL ANALYST AGENT ===")
print("Ask about stocks or compare companies.")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    messages.append({"role": "user", "content": question})

    try:
        for _ in range(5):
            response = chat(
                model=MODEL,
                messages=messages,
                tools=[get_stock_data]
            )

            messages.append(response.message)

            if not response.message.tool_calls:
                print("\nAI Analyst:\n")
                print(response.message.content)
                print()
                break

            for call in response.message.tool_calls:
                name = call.function.name
                arguments = call.function.arguments

                if name not in tools:
                    result = f"Unknown tool: {name}"
                else:
                    print(f"\n[Tool] {name}: {arguments}")
                    result = tools[name](**arguments)

                messages.append({
                    "role": "tool",
                    "tool_name": name,
                    "content": str(result)
                })
        else:
            print("Agent reached the tool-call limit.")

    except Exception as e:
        print("Error:", e)
