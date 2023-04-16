from fastapi import FastAPI
import openai
import requests
import helpers
import os

app = FastAPI()
openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.get("/")
async def root():
    return "hello"


@app.get("/{ticker}")
async def get_info(ticker):
    if helpers.get_num_requests() > 125:
        return "Maximum number of requests reached for the day, come back tomorrow :)"

    print("Requested ticker:", ticker)

    url = "https://mboum-finance.p.rapidapi.com/qu/quote/financial-data"

    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_API_KEY"),
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }

    query_string = {"symbol": ticker}

    response = requests.request(
        "GET", url, headers=headers, params=query_string)

    print("mboum finance response:\n" + str(response.json()))

    responseTemplate = helpers.get_response_template()

    prompt = "For each section of the following data, explain the performance implications on {} stock in much detail:\n{}\nIn your response, follow the format of the following response but be more verbose:\n\"{}\"".format(
        ticker, str(response.json()), responseTemplate)

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1000
    )

    return gpt_response["choices"][0]["message"]["content"]
