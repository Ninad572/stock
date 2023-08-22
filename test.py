import streamlit as st
import requests as req
import yfinance as yf
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as BS
from textblob import TextBlob
#newsorg api key-e71b4643f603432896b0924579d00cc4

api_key = 'DDKIS5YWO963MRYT'
st.title('Stock Analysis')


st.sidebar.title('Popular Stock Tickers')
ts = ['Apple : AAPL', 'Amazon : AMZN', 'Google : GOOGL', 'Microsoft : MSFT', 'Tesla : TSLA','Netflix : NFLX']
for i in ts:
    st.sidebar.write(i)


symbol = st.text_input("",placeholder="Enter Stock Ticker")
if symbol:
    symbol=symbol.upper()

ss=[symbol]

dt=yf.download(ss,start='2010-01-01',end=date.today())
df = pd.DataFrame(dt)

st.markdown(
    """
    <style>
    .stButton button {
        display: inline-block;
        background-color: green;
        color: white;
        size:18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


b1=st.button("Get Stock Information")
b2=st.button("Get Financial Ratios")
b3=st.button("Get Income Statement")
b4=st.button("Get Balance Sheet")
b5=st.button("Get CashFlow Statement")



st_name=""

if b1:
    response = req.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}')
    data = response.json()
    
    for i,j in data.items():
        if(i=="Description" or i=="Name" or i=="Industry" or i=="MarketCapitalization"):
            if(i=="MarketCapitalization"):
                st.write(i,":",str(int(j)/1000000000)," Billion USD")
            elif(i=="Name"):
                st_name=j
                st.write(i,":",j)
            else:
                st.write(i,":",j)

    fig = plt.figure(figsize=(14, 10), facecolor='#f5f5f5')

    plt.plot(df['Close'], color='blue', linestyle='-', linewidth=2)

    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.title('Market Price', fontsize=16)

    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.legend(['Close'], loc='upper left', fontsize=12)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_linewidth(0.5)
    plt.gca().spines['left'].set_linewidth(0.5)
    
    st.pyplot(fig)
    st.write(st_name)
    api_key = 'YOUR_API_KEY'
    endpoint = 'https://newsapi.org/v2/everything'

# Parameters for the API request
    parameters = {

        
            'q':st_name,
            'apiKey': 'e71b4643f603432896b0924579d00cc4',
            'language':'en'
                }

# Send the request to the NewsAPI
    response = req.get(endpoint, params=parameters)

    st.subheader('Latest News Related To Stock')

# Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        c=0
        senti=0
    # Extract and print the news articles
        articles = data['articles']
        for article in articles:
            title = article['title']
            description = article['description']
            blob=TextBlob(description)
            st.write('Sentiment:',str(blob.sentiment.polarity))
            senti+=blob.sentiment.polarity
            url = article['url']
        
            st.write('Title:', title)
            st.write('Description:', description)
            st.write('URL:', url)
            st.write('---')
            c+=1
            if(c==20):
                break
            
    else:
        st.write('Error:', response.status_code)
    z=senti/c
    st.sidebar.subheader('Market Sentiment For Stock-',str(z))
    if z>0.1:
        st.sidebar.write("<p style='color: green;font-size:20px;'>POSITIVE</p>", unsafe_allow_html=True)
    elif (-0.1<z<0.1):
        st.sidebar.write('Neutral')
    else:
        st.sidebar.write("<p style='color: red;font-size:20px;'>NEGATIVE</p>", unsafe_allow_html=True)



elif b2:
    response = req.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}')
    data = response.json()
    
    l=['EBITDA','PERatio','PEGRatio','BookValue','DividendPerShare','DividendYeild','EPS','RevenuePerShareTTM','PriceToBookRatio','ProfitMargin','PriceToSalesRatioTTM','QuarterlyEarningsGrowthYOY','QuarterlyRevenueGrowthYOY']
    for i,j in data.items():
        if i in l:
            st.write(i,":",j)
    st.sidebar.subheader('Terms & What They Mean')
    st.sidebar.write("EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization): EBITDA is a measure of a company's operating profitability, indicating its earnings from core operations before accounting for interest, taxes, depreciation, and amortization expenses. It helps assess the company's ability to generate cash flow.")
    st.sidebar.write("PERatio (Price-to-Earnings Ratio): PERatio is a valuation metric that compares a company's current stock price to its earnings per share (EPS). It shows how much investors are willing to pay for each dollar of earnings. A higher PERatio may indicate a higher valuation and expectations of future growth.")
    st.sidebar.write("PEGRatio (Price/Earnings to Growth Ratio): PEGRatio is a valuation ratio that considers a company's PERatio in relation to its earnings growth rate. It provides insights into whether the stock is overvalued or undervalued based on expected earnings growth. A PEGRatio above 1 suggests a stock may be overvalued relative to its growth prospects.")
    st.sidebar.write("BookValue: BookValue represents the total value of a company's assets minus its liabilities. It indicates the net worth of the company on its balance sheet and provides an insight into the company's underlying value. ")   
    st.sidebar.write("DividendPerShare: DividendPerShare is the total dividends paid by the company divided by the number of outstanding shares. It shows the amount of cash returned to shareholders per share. ")   
    st.sidebar.write("DividendYield: DividendYield is the dividend per share divided by the stock's current market price. It shows the percentage return a shareholder receives from dividends relative to the stock's price. ")   
    st.sidebar.write("EPS (Earnings Per Share): EPS measures a company's profitability by dividing its net earnings by the number of outstanding shares. It indicates how much profit is attributable to each share. ")   
    st.sidebar.write("RevenuePerShareTTM (Revenue Per Share Trailing Twelve Months): This metric divides the total revenue generated by the company over the past twelve months by the number of outstanding shares. It provides insights into the company's revenue-generating capability per share. ") 
    st.sidebar.write("ProfitMargin: ProfitMargin represents the company's net income as a percentage of its total revenue. It shows the proportion of revenue that turns into profit after covering all expenses. ") 
    st.sidebar.write("PriceToSalesRatioTTM: PriceToSalesRatioTTM compares the company's market capitalization to its total revenue over the trailing twelve months. It helps assess the company's valuation relative to its sales performance. ")   
    st.sidebar.write("PriceToBookRatio: PriceToBookRatio compares the company's stock price to its book value per share. A high ratio may indicate that the stock is overvalued relative to its book value. ")   
    st.sidebar.write("QuarterlyEarningsGrowthYOY: This measures the percentage change in a company's earnings from one quarter to the same quarter in the previous year. A positive value indicates earnings growth, while a negative value suggests a decline. ")
    st.sidebar.write("QuarterlyRevenueGrowthYOY: This measures the percentage change in a company's revenue from one quarter to the same quarter in the previous year. A positive value indicates revenue growth, while a negative value suggests a decline. ")
  
elif b3:
    response = req.get(f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}')
    data = response.json()
 
    for i,j in data['annualReports'][0].items():
        st.write(i,":",j)   
    st.sidebar.subheader('Terms & What They Mean')
    st.sidebar.write("Fiscal Date Ending (2023-01-29): The end date of the fiscal reporting period for which the financial data is presented. ")
    st.sidebar.write("Reported Currency (USD): The currency in which the financial figures are reported, in this case, United States Dollars (USD). ")
    st.sidebar.write("Gross Profit: The profit earned from core business operations, calculated by subtracting the cost of goods sold (COGS) from total revenue. ")
    st.sidebar.write("Total Revenue: The overall income generated by a company from all its revenue streams, including sales of goods and services. ")
    st.sidebar.write("Cost of Revenue: The direct costs associated with producing the goods or services sold, including raw materials and direct labor. ")
    st.sidebar.write("Cost of Goods and Services Sold: Specific costs related to producing goods or providing services, a subset of the total Cost of Revenue. ")
    st.sidebar.write("Operating Income: Also known as operating profit, it is the income earned from core business operations after deducting operating expenses but before interest and taxes. ")
    st.sidebar.write("Selling, General, and Administrative (SG&A) Expenses: The combined expenses related to selling products, managing the company, and general administrative functions. ")
    st.sidebar.write("Research and Development (R&D) Expenses: The expenses incurred in developing new products, processes, or services. ")
    st.sidebar.write("Operating Expenses: The total expenses incurred to run the core business operations, including SG&A and R&D expenses. ")
    st.sidebar.write("Investment Income Net: The net income generated from investments, such as interest, dividends, and capital gains. ")
    st.sidebar.write("Net Interest Income: The difference between interest earned and interest paid by the company. ")
    st.sidebar.write("Interest Income: The income earned by the company from interest on investments or loans. ")
    st.sidebar.write("Interest Expense: The cost of borrowing money, paid as interest on loans or debt. ")
    st.sidebar.write("Non-Interest Income: Income generated from sources other than interest, such as fees, commissions, or gains on assets. ")
    st.sidebar.write("Other Non-Operating Income: Income from non-core business activities or one-time gains or losses. ")
    st.sidebar.write("Depreciation: The systematic allocation of the cost of tangible assets over their useful lives to reflect their wear and tear. ")
    st.sidebar.write("Depreciation and Amortization: The sum of depreciation and amortization expenses, which is the allocation of the cost of tangible and intangible assets, respectively. ")
    st.sidebar.write("Income Before Tax: The company's income before accounting for taxes. ")
    st.sidebar.write("Income Tax Expense: The amount of taxes owed by the company. ")
    st.sidebar.write("Interest and Debt Expense: The total cost of interest and debt-related expenses. ")
    st.sidebar.write("Net Income from Continuing Operations: The income from core business operations after taxes and other expenses. ")
    st.sidebar.write("Comprehensive Income Net of Tax: The overall income of the company, including all gains and losses, after adjusting for tax implications. ")
    st.sidebar.write("EBIT (Earnings Before Interest and Taxes): A measure of a company's profitability that shows earnings before accounting for interest and taxes. ")
    st.sidebar.write("EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization): A measure of a company's operating performance, excluding non-operational expenses like interest, taxes, depreciation, and amortization. ")
    st.sidebar.write("Net Income: The total profit earned by the company after all expenses, including taxes and interest. It is also known as the bottom line or the company's earnings. ")

elif b4:
    response = req.get(f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}')
    data = response.json()
 
    for i,j in data['annualReports'][0].items():
        st.write(i,":",j)   
    st.sidebar.subheader('Terms & What They Mean')

    st.sidebar.write("Fiscal Date Ending: The end date of the fiscal reporting period for which the financial data is presented.")
    st.sidebar.write("Reported Currency: The currency in which the financial figures are reported, in this case, United States Dollars (USD).")
    st.sidebar.write("Gross Profit: The profit earned from core business operations, calculated by subtracting the cost of goods sold (COGS) from total revenue.")
    st.sidebar.write("Total Revenue: The overall income generated by a company from all its revenue streams, including sales of goods and services.")
    st.sidebar.write("Cost of Revenue: The direct expenses associated with producing the goods or services sold, including raw materials and direct labor.")
    st.sidebar.write("Cost of Goods and Services Sold: Specific costs related to producing goods or providing services, a subset of the total Cost of Revenue.")
    st.sidebar.write("Operating Income: Also known as operating profit, it is the income earned from core business operations after deducting operating expenses, but before interest and taxes.")
    st.sidebar.write("Selling, General, and Administrative (SG&A) Expenses: The combined expenses related to selling products, managing the company, and general administrative functions.")
    st.sidebar.write("Research and Development (R&D) Expenses: The expenses incurred in developing new products, processes, or services.")
    st.sidebar.write("Operating Expenses: The total expenses incurred to run the core business operations, including SG&A and R&D expenses.")
    st.sidebar.write("Investment Income Net: The net income generated from investments, such as interest, dividends, and capital gains.")
    st.sidebar.write("Net Interest Income: The difference between interest earned and interest paid by the company.")
    st.sidebar.write("Interest Income: The income earned by the company from interest on investments or loans.")
    st.sidebar.write("Interest Expense: The cost of borrowing money, paid as interest on loans or debt.")
    st.sidebar.write("Non-Interest Income: Income generated from sources other than interest, such as fees, commissions, or gains on assets.")
    st.sidebar.write("Other Non-Operating Income: Income from non-core business activities or one-time gains or losses.")
    st.sidebar.write("Depreciation: The systematic allocation of the cost of tangible assets over their useful lives to reflect their wear and tear.")
    st.sidebar.write("Depreciation and Amortization: The sum of depreciation and amortization expenses, which is the allocation of the cost of tangible and intangible assets, respectively.")
    st.sidebar.write("Income Before Tax: The company's income before accounting for taxes.")
    st.sidebar.write("Income Tax Expense: The amount of taxes owed by the company.")
    st.sidebar.write("Interest and Debt Expense: The total cost of interest and debt-related expenses.")
    st.sidebar.write("Net Income from Continuing Operations: The income from core business operations after taxes and other expenses.")
    st.sidebar.write("Comprehensive Income Net of Tax: The overall income of the company, including all gains and losses, after adjusting for tax implications.")
    st.sidebar.write("EBIT (Earnings Before Interest and Taxes): A measure of a company's profitability that shows earnings before accounting for interest and taxes.")
    st.sidebar.write("EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization): A measure of a company's operating performance, excluding non-operational expenses like interest, taxes, depreciation, and amortization.")
    st.sidebar.write("Net Income: The total profit earned by the company after all expenses, including taxes and interest. It is also known as the bottom line or the company's earnings.")
    st.sidebar.write("Total Current Liabilities: The total value of debts and obligations that are due within one year.")
    st.sidebar.write("Current Accounts Payable: The short-term debts owed by the company to its suppliers for goods or services received.")
    st.sidebar.write("Deferred Revenue: The income received in advance for goods or services that the company has not yet delivered.")
    st.sidebar.write("Current Debt: The portion of the long-term debt that is due within one year.")
    st.sidebar.write("Short-Term Debt: Short-term borrowings or debts due within one year.")
    st.sidebar.write("Total Non-Current Liabilities: The sum of all long-term debts and obligations that are not due within one year.")
    st.sidebar.write("Capital Lease Obligations: The value of lease obligations that are treated as a capital lease.")
    st.sidebar.write("Long-Term Debt: The value of debts and borrowings that are due after one year.")
    st.sidebar.write("Current Long-Term Debt: The portion of long-term debt that is due within one year.")
    st.sidebar.write("Long-Term Debt Noncurrent: The portion of long-term debt that is not due within one year.")
    st.sidebar.write("Total Shareholder Equity: The residual interest in the company's assets after deducting liabilities. It represents the ownership interest of shareholders.")
    st.sidebar.write("Common Stock Shares Outstanding: The total number of common shares held by shareholders as of the reporting date.")


elif b5:
    response = req.get(f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}')
    data = response.json()
 
    for i,j in data['annualReports'][0].items():
        st.write(i,":",j)   
    st.sidebar.subheader('Terms & What They Mean')    

    st.sidebar.write("Fiscal Date Ending: The fiscal year-end date, which marks the conclusion of the financial reporting period for the company's financial statements.")
    st.sidebar.write("Reported Currency: The currency in which the company reports its financial figures, indicating the denomination used in financial statements.")
    st.sidebar.write("Operating Cashflow: The net cash generated or used by the company from its core business operations, excluding financing and investing activities.")
    st.sidebar.write("Payments for Operating Activities: The total cash outflows resulting from day-to-day business operations, including payments for expenses, supplies, and salaries.")
    st.sidebar.write("Proceeds from Operating Activities: The total cash inflows generated from day-to-day business operations, including receipts from sales and services.")
    st.sidebar.write("Change in Operating Liabilities: The net change in the company's short-term obligations and payables, reflecting the increase or decrease in amounts owed to suppliers or creditors.")
    st.sidebar.write("Change in Operating Assets: The net change in the company's short-term assets, indicating the increase or decrease in cash, inventory, and accounts receivable during the reporting period.")
    st.sidebar.write("Depreciation, Depletion, and Amortization: The total non-cash expenses incurred due to the gradual reduction in the value of tangible assets (depreciation) and intangible assets (amortization).")
    st.sidebar.write("Capital Expenditures: The total cash expenditures made to acquire or enhance long-term assets, such as machinery, equipment, and property, which are expected to benefit the company beyond the current fiscal period.")
    st.sidebar.write("Change in Receivables: The net change in the company's accounts receivable, representing the increase or decrease in amounts owed to the company by its customers or clients.")
    st.sidebar.write("Change in Inventory: The net change in the company's inventory levels, showing the increase or decrease in goods or materials held for production or resale.")
    st.sidebar.write("Profit/Loss: The net income or loss earned by the company during the fiscal period after accounting for all revenues, expenses, taxes, and extraordinary items.")
    st.sidebar.write("Cashflow from Investment: The net cash flow resulting from investment activities, including purchases and sales of long-term assets, investments, and acquisitions.")
    st.sidebar.write("Cashflow from Financing: The net cash flow resulting from financing activities, including issuing or repurchasing stock, borrowing or repaying debt, and paying dividends.")
    st.sidebar.write("Proceeds from Repayments of Short-Term Debt: The cash proceeds received by the company from repaying short-term debts or loans.")
    st.sidebar.write("Payments for Repurchase of Common Stock: The cash payments made by the company to repurchase its own common stock from the open market or shareholders.")
    st.sidebar.write("Payments for Repurchase of Equity: The cash payments made by the company to repurchase its own equity, including common and preferred stock.")
    st.sidebar.write("Payments for Repurchase of Preferred Stock: The cash payments made by the company to repurchase its own preferred stock from shareholders.")
    st.sidebar.write("Dividend Payout: The total cash paid out as dividends to shareholders, representing the distribution of profits to investors.")
    st.sidebar.write("Dividend Payout Common Stock: The cash paid out as dividends specifically to common stockholders as a share of the company's profits.")
    st.sidebar.write("Dividend Payout Preferred Stock: The cash paid out as dividends specifically to preferred stockholders as a share of the company's profits.")
    st.sidebar.write("Proceeds from Issuance of Common Stock: The cash proceeds received by the company from issuing new common stock to investors.")
    st.sidebar.write("Proceeds from Issuance of Long-Term Debt and Capital Securities Net: The net cash proceeds received by the company from issuing long-term debt and capital securities, after deducting any costs or discounts associated with the issuance.")
    st.sidebar.write("Proceeds from Issuance of Preferred Stock: The cash proceeds received by the company from issuing new preferred stock to investors.")
    st.sidebar.write("Proceeds from Repurchase of Equity: The cash proceeds received by the company from repurchasing its own equity, including common and preferred stock, from the open market or shareholders.")
    st.sidebar.write("Proceeds from Sale of Treasury Stock: The cash proceeds received by the company from selling its own previously repurchased stock (treasury stock) back to the open market or investors.")
    st.sidebar.write("Change in Cash and Cash Equivalents: The net change in the company's cash and cash equivalents, indicating the increase or decrease in readily available funds for business operations.")
    st.sidebar.write("Change in Exchange Rate: The net change in the company's cash and cash equivalents due to fluctuations in exchange rates when dealing with foreign currencies.")
    st.sidebar.write("Net Income: The company's total profit or loss earned during the fiscal period after accounting for all revenues, expenses, taxes, and extraordinary items.")


