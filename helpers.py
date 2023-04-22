def get_response_template():
    return """
    Overall, the health of XM stock appears to be mixed.
    \t- Current price: The current price of XM stock is $17.86, which is not particularly high or low.
    \t- Target prices: The target high price is $20 and the target low price is $16, indicating some uncertainty about where the stock may go. The target mean price is $18.16, which is close to the current price.
    \t- Analyst opinions: The recommendation mean is 2.9, which is closer to a "hold" rating than a "buy" or "sell" rating.
    \t- Cash: XM has a total cash amount of $719.89 million, which is a positive sign.
    \t- Debt: XM has a total debt of $278.18 million, which is relatively low compared to its cash amount. However, the debt-to-equity ratio is high at 14.61.
    \t- Revenue: XM has a total revenue of $1.46 billion, which is a positive sign.
    \t- Profitability: XM has negative return on assets and return on equity, indicating that it is not currently profitable. However, it has a gross profit of $1.03 billion and positive free cash flow.
    \t- Growth: XM has had positive revenue growth of 23.10%, but no earnings growth.
    \t- Margins: XM has high gross margins of 70.52%, but negative ebitda margins, operating margins, and profit margins
    Happy investing! :)
    """


def get_prompt(ticker, data):
    return "For each section of the following data, explain the performance implications on {} stock in much detail:\n{}\nIn your response, follow the format of the following response but be more verbose:\n\"{}\"".format(
        ticker, str(data), get_response_template())
