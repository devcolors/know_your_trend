from datetime import datetime


def is_a_new_day():
    date = datetime.now().date()
    prev_date_file = open("prev_date.txt", "r")
    prev_date_string = prev_date_file.readline().strip()
    prev_date = datetime.strptime(prev_date_string, "%d/%m/%Y").date()
    prev_date_file.close()

    if date > prev_date:
        prev_date_file = open("prev_date.txt", "w")
        prev_date_file.write(date.strftime("%d/%m/%Y"))
        return True

    return False


def get_num_requests():
    num_requests_file = open("num_requests.txt", "r")
    num_requests = int(num_requests_file.read())

    if is_a_new_day():
        num_requests = 0

    num_requests += 1
    num_requests_file.close()

    num_requests_file = open("num_requests.txt", "w")
    num_requests_file.write(str(num_requests))


def get_response_template():
    return """
    Overall, the health of XM stock appears to be mixed.
    - Current price: The current price of XM stock is $17.86, which is not particularly high or low.
    - Target prices: The target high price is $20 and the target low price is $16, indicating some uncertainty about where the stock may go. The target mean price is $18.16, which is close to the current price.
    - Analyst opinions: The recommendation mean is 2.9, which is closer to a "hold" rating than a "buy" or "sell" rating.
    - Cash: XM has a total cash amount of $719.89 million, which is a positive sign.
    - Debt: XM has a total debt of $278.18 million, which is relatively low compared to its cash amount. However, the debt-to-equity ratio is high at 14.61.
    - Revenue: XM has a total revenue of $1.46 billion, which is a positive sign.
    - Profitability: XM has negative return on assets and return on equity, indicating that it is not currently profitable. However, it has a gross profit of $1.03 billion and positive free cash flow.
    - Growth: XM has had positive revenue growth of 23.10%, but no earnings growth.
    - Margins: XM has high gross margins of 70.52%, but negative ebitda margins, operating margins, and profit margins
    """
