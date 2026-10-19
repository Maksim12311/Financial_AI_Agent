AI Financial Analyst Agent



Project Overview



This project is an AI based Financial Analyst Agent created using Python. It can ask questions about the financial market and is able to retrieve financial data and financial indicators from different companies and give financial answers when used in practice, which are queried on a locally installed LLM (Large Language Model).



The agent connects with Yahoo Finance to get financial information and break it down in natural language with the help of Ollama (Qwen 2.5:7B).



Unlike a regular chatbot the agent can select the available tools to the question.



Technologies Used



Main programming language is Python.

Installing and running LLM locally with Ollama.

Qwen 2.5:7B is a financial analysis language model.

yfinance package is a package to download Yahoo Finance Financial data.

The AI agent can call Python functions, it's called Tool Calling.



Main Features



1\. Stock Price Analysis



The agent fetches the past data of the stock exchange market, such as:



The prices of opening and closing periods.



Percentage price change



Highest and lowest prices



Average daily volume (ADV).



There are several periods that can be supported such as 5 days, 1 month, 3 months, 6 months, 1 year.



2\. Fundamental Financial Analysis



The agent can get access to company financial indicators including:



Price-to-Earnings Ratio (P/E)



Earnings per Share (EPS)



Market Capitalization



Total Revenue



Profit Margin



Debt-to-Equity Ratio

Profitability Ratios: ROE



3\. Company Comparison



The number of companies can be displayed with each other using the stock performance, fundamental financial indicators.



For example:



Analyze the P/E ratio, EPS and Market Cap of Apple and Microsoft.



4\. AI Tool Calling



The project adopts two tools:



get\_stock\_data()



Gets stock prices from the past and computes performance metrics.



get\_company\_fundamentals()



Gathers valuation ratios and other financial information.



The AI model learns these functions and can be called on by the user's query.



5\. Interactive Financial Assistant



Financial-related queries can be made directly from the terminal by the user. The agent keeps track of conversations throughout the session.



Installation



1\. Clone the Repository



git clone https://github.com/YOUR\_USERNAME/Financial\_AI\_Agent.git

cd Financial\_AI\_Agent



Change YOUR\_USERNAME with your GitHub user name.



2\. Create a virtual environment, and install required packages into it.



python -m venv venv



To activate on Windows CMD run these commands:



venv\\Scripts\\activate.bat



3\. Install Dependencies



pip install -r requirements.txt



4\. Install Ollama



Download and install Ollama at ollama.com.



Download the model:



ollama pull qwen2.5:7b



Make sure that Ollama is running.



5\. Run the Agent



python agent\_tools.py



Example Questions



Stock performance:



Examine the performance of Apple's stocks in the past month.



Company comparison:



Make comparisons between Apple and Microsoft stock performance in the past month.



Financial ratios:



What is the P/E ratio of Apple; what is its EPS and what is the market capitalisation of the company?



Fundamental comparison:



Make a comparison between apple and microsoft according to their financial fundamentals.



Project Structure



Financial\_AI\_Agent/

|

|-- agent\_tools.py

|-- financial\_agent.py

|-- requirements.txt

|-- README.md

|-- .gitignore



agent\_tools.py — Main AI agent with financial analysis tools.



financial\_agent.py — First draft of financial assistant.



requirements.txt — Required Python packages.



README.md — Project documentation.



.gitignore — List of files and folders that are ignored by Git.



Limitations



The list of financial data depends on Yahoo Finance.

The quality of analysis is based on the local language model.

The agent may misread the information so the result should be confirmed.

The project is not involved in giving investment advice.

Real-time availability and accuracy of data is not guaranteed.



Conclusion



This project shows how to use an AI agent to perform financial analysis, using a local LLM, external financial data sources, and tool calling.



The main objective is to describe an AI system that is able to autonomously choose tools, fetch information, and develop relevant financial explanations.

