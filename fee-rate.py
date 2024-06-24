import discord
import requests
import asyncio
from datetime import datetime
import time
# Replace 'TOKEN' with your actual bot token
TOKEN = ""

API_1 = 'https://mempool.space/api/v1/mining/blocks/timestamp/'
API_2 = 'https://mempool.space/api/v1/blocks/'




intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def update_activity():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            uni = time.time()
            uni = time.time()
            unisecs = int(uni)
            stringuni = str(unisecs)

            URL = API_1+stringuni
            response = requests.get(URL)
            data = response.json()
            height = data.get('height')


            URL2 = API_2+str(height)
            response2 = requests.get(URL2)
            data2 = response2.json()
            median = data2[0]['extras']['medianFee']
            feerate = data2[0]['extras']['feeRange']

            
            finalmedian = round(median)

            
            first = feerate[0]
            last = feerate[6]
            finalfirst = round(first)
            finallast = round(last)




            now = datetime.now()
            print(f"{now} [{height}] -{finalmedian} | {finalfirst} - {finallast} ")

            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{finalmedian} sat | {finalfirst} - {finallast} sat"
            )
            await client.change_presence(activity=activity)
        except Exception as e:
            now = datetime.now()
            print(f"{now} - Error fetching data: {e}")
        
        # Update every 3 seconds
        await asyncio.sleep(3)

@client.event
async def on_ready():

    print(f'Bot is ready as {client.user}')

client.loop.create_task(update_activity())
client.run(TOKEN)
