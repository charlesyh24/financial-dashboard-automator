# Financial Dashboard Automator

## Description
It scrapes financial data from [Goodinfo!](https://goodinfo.tw/tw/index.asp) to generate financial ratio statements, pivot tables, and visualizatinos of financial metrics. Then it stores results in an Excel file and send to assigned recipient via email.

## Usage
```
usage: main.py [-h] -i INDUSTRY -c COMPANY [COMPANY ...] -y YEAR -q QUARTER -e EMAIL

  -i INDUSTRY, --industry INDUSTRY
  -c COMPANY [COMPANY ...], --company COMPANY [COMPANY ...]
  -y YEAR, --year YEAR 2017~2021
  -q QUARTER, --quarter QUARTER
  -e EMAIL, --email EMAIL
```

_e.g. `python3 main.py -i "半導體業" -c 2329 2330 2337 2338 -y 2019 -q "Q1" -e recipient@gmail.com`_

_(P.S. To send email successfully, open [emailing script](code/email_handler.py) and revise line 4 and 5 for your email address and app password for the first time.)_

## Output
- [Financial Ratio Statement](pic/statement.png)
- [Pivot Table](pic/pivot.png)
- [Plot](pic/plot.png)

## Procedure
1. Scape company's data from Goodinfo!
    - Name
    - Industry
    - Income Statement
    - Balance sheet
1. Generate statements and visualizations
    - Financial Ratio Statement: Profitability; Liquidity; Efficiency; Leverage
    - Pivot Table: Revenue; Net Income
    - Plot: ROE; ROA
1. Export results as Excel file
1. Send file to recipient via email

## Content
- code
    - [main.py](code/main.py): main script for running code
    - [postman_crawler.py](code/postman_crawler.py): sub script for crawler
    - [finaAnalysis.py](code/finaAnalysis.py): sub script for financial analysis
    - [email_handler.py](code/email_handler.py): sub script for emailing
- pic
    - [statement.png](pic/statement.png): Profitability
    - [pivot.png](pic/pivot.png): Revenue; Net Income
    - [plot.png](pic/plot.png): ROE; ROA