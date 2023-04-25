from fastapi import FastAPI
import openai
import requests
import helpers
import os
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request
from fastapi.responses import JSONResponse

# Set up rate limiter & FastAPI app object
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Fetch API keys
openai.api_key = os.environ.get("OPENAI_API_KEY")
RAPIDAPI_API_KEY = os.environ.get("RAPIDAPI_API_KEY")


# Health check endpoint
@app.get("/")
async def root(request: Request):
    content = {"message": "HELLO"}
    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(content=content, headers=headers)


# Request a ticker, get a quick financial breakdown on stock performance
@app.get("/{ticker}")
@limiter.limit("125/day")
async def get_info(request: Request, ticker):
    print("Requested ticker:", ticker)

    url = "https://mboum-finance.p.rapidapi.com/qu/quote/financial-data"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_API_KEY,
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }
    query_string = {"symbol": ticker}
    response = requests.request(
        "GET", url, headers=headers, params=query_string)

    print("mboum finance response:\n" + str(response.json()))

    prompt = "For each section of the following data, explain the performance implications on {} stock in much detail:\n{}\nIn your response, follow the format of the following response but be more verbose:\n\"{}\"".format(
        ticker, str(response.json()), helpers.get_response_template())

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1000
    )

    print("gpt_response:\n", gpt_response)

    content = {"message": gpt_response["choices"][0]["message"]["content"]}
    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(content=content, headers=headers)
