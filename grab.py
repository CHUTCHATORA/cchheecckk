import asyncio
import re
import requests
import logging
from pyppeteer import launch
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '7363209477:AAG84nYCFSg-EwjkyHtfIPrh5-juaJahsHA'  # Replace with your bot's API token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['grab'])
async def grab_info(message: types.Message):
    url = message.text.split(' ', 1)[1]  # Extract the URL from the command
    try:
        session = await launch()
        pk, urlx = await get_stripe_pk(url)
        email = await get_customer_email(urlx, pk)
        session_id = await get_checkout_session(urlx, pk)
        amount_due = await get_amount_due(urlx, pk)
        currency_chk = await get_checkout_currency(urlx, pk)

        response_message = f'Email: {email}\nSession ID: {session_id}\nAmount Due: {amount_due}\nCurrency: {currency_chk}\nPk: {pk}'
    except Exception as error:
        response_message = f'An error occurred: {error}'
    finally:
        await session.close()

    await message.answer(response_message)

async def get_stripe_pk(url):
    browser = await launch()
    page = await browser.newPage()
    await page.setRequestInterception(True)
    match_found = False
    pk = None
    urlx = None

    def request_handler(request):
        nonlocal match_found, pk, urlx
        post_data = request.postData()
        if not match_found and post_data and 'pk' in post_data:
            regex = r'pk_live_[\w-]+'
            match = re.search(regex, post_data)
            if match:
                pk = match.group(0)
                match_found = True
                urlx = request.url
                page.off('request', request_handler)

        request.continue_()

    page.on('request', request_handler)
    await page.goto(url)
    await browser.close()
    return pk, urlx

async def get_customer_email(url, pk):
    try:
        base_url, _ = url.split("#")
        payload = {'key': pk, 'eid': 'NA', 'browser_locale': 'en-US', 'redirect_type': 'stripe_js'}
        response = await fetch_url(base_url, payload)
        text = await response.text()
        email_regex = r'"email":\s*"([^"]+)"'
        email_match = re.search(email_regex, text)
        email = email_match.group(1) if email_match else None
        return email
    except Exception as error:
        print(error)

async def get_checkout_session(url, pk):
    try:
        base_url, _ = url.split("#")
        payload = {'key': pk, 'eid': 'NA', 'browser_locale': 'en-US', 'redirect_type': 'stripe_js'}
        response = await fetch_url(base_url, payload)
        text = await response.text()
        session_id_regex = r'"session_id":\s*"([^"]+)"'
        session_id_match = re.search(session_id_regex, text)
        session_id = session_id_match.group(1) if session_id_match else None
        return session_id
    except Exception as error:
        print(error)

async def get_checkout_currency(url, pk):
    try:
        base_url, _ = url.split("#")
        payload = {'key': pk, 'eid': 'NA', 'browser_locale': 'en-US', 'redirect_type': 'stripe_js'}
        response = await fetch_url(base_url, payload)
        text = await response.text()
        currency_regex = r'"currency":\s*"([^"]+)"'
        currency_match = re.search(currency_regex, text)
        currency = currency_match.group(1) if currency_match else None
        return currency
    except Exception as error:
        print(error)

async def get_amount_due(url, pk):
    try:
        base_url, _ = url.split("#")
        payload = {'key': pk, 'eid': 'NA', 'browser_locale': 'en-US', 'redirect_type': 'stripe_js'}
        response = await fetch_url(base_url, payload)
        text = await response.text()
        amount_due_regex = r'"unit_amount":\s*(-?\d+)'
        amount_due_match = re.search(amount_due_regex, text)
        amount_due = int(amount_due_match.group(1)) if amount_due_match else None
        return amount_due
    except Exception as error:
        print(error)

async def fetch_url(url, payload):
    return await session.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
