import aiohttp
import asyncio
import json
import brotli
import gzip
import re
import time

# API Endpoints
BALANCE_URL = "https://zero-api.kaisar.io/user/balances?symbol=point"
SPIN_URL = "https://zero-api.kaisar.io/lucky/spin"
CONVERT_URL = "https://zero-api.kaisar.io/lucky/convert"

# Request User for Auth Token
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2N2Y0YTFhNDRjMTMwMmNiMjljODU2ODIiLCJpZCI6IjY3ZjRhMWE0NGMxMzAyY2IyOWM4NTY4MiIsInJvbGUiOiJ1c2VyIiwic3RhdHVzIjoxLCJpYXQiOjE3NDQwODU3NjIsImV4cCI6MTc3NTY0MzM2Mn0.mmUgsQ5W0N_C08HtQPQGiYcKzyw-NDvbKPQu5XdIeTk"
HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8",
    "authorization": f"Bearer {auth_token}",
    "content-type": "application/json",
    "origin": "https://zero.kaisar.io",
    "referer": "https://zero.kaisar.io/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "Android",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
}

timeout = aiohttp.ClientTimeout(total=5)

async def check_balance():
    """Fetches the user's point balance."""
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(BALANCE_URL, headers=HEADERS) as response:
                raw_data = await response.read()
                encoding = response.headers.get("content-encoding", "")
                
                # Handle decompression
                if "br" in encoding:
                    raw_data = brotli.decompress(raw_data)
                elif "gzip" in encoding:
                    raw_data = gzip.decompress(raw_data)
                
                decoded_data = raw_data.decode("utf-8", errors="ignore")
                print(f"Raw Response: {decoded_data[:400]}")
                
                balance_match = re.search(r'"balance":"?(\d+)"?', decoded_data)
                if balance_match:
                    balance = int(balance_match.group(1))
                    print(f"Extracted Balance: {balance}")
                    return balance
                else:
                    print("Error: Balance not found in response. Buying 1 ticket and spinning.")
                    return -1  # Special flag indicating balance not found
        except Exception as e:
            print(f"Error checking balance: {e}")
            return 0

async def send_request(session):
    """Sends a single request to the API."""
    try:
        async with session.post(SPIN_URL, headers=HEADERS, json={}) as response:
            return response.status
    except:
        return None

async def buy_tickets(session, tickets=1):
    """Buys the specified number of tickets."""
    for _ in range(tickets):
        await session.post(CONVERT_URL, headers=HEADERS, json={})
    print(f"Bought {tickets} tickets.")

async def main():
    """Handles the balance check, ticket buying, and execution loop."""
    target_points = int(2000000)
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        while True:
            balance = await check_balance()
            
            if balance == -1:
                await buy_tickets(session, 1)
                balance = 300  # Assume minimum required balance for spin
            
            print(f"Current Balance: {balance}")
            
            if balance >= 300:
                tickets_to_buy = min(balance // 300, 1)
                await buy_tickets(session, tickets_to_buy)
                balance = await check_balance()
                print(f"Updated Balance after buying tickets: {balance}")
            
            if balance >= target_points:
                print("Target points achieved. Exiting script.")
                break
            
            tasks = [send_request(session) for _ in range(500)]  # Batch processing of 500 requests
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            success = sum(1 for status in responses if status == 200)
            print(f"Successful spins: {success}")
            
            # 1-second delay after each loop iteration
            await asyncio.sleep(1)
            
asyncio.run(main())
