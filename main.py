import discord
import os
import requests
import json

disc_token = os.environ['DISC_TOKEN']
os_api_key = os.environ['OS_API_KEY']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
  
  user_channel = message.channel
  
  if message.author == client.user:
    return

  if message.content.startswith('!'):
    contract_address = str(message.content).split("!")[1]
    headers = {"X-API-KEY": {os_api_key}}
    opensea_api = f"https://api.opensea.io/api/v1/asset_contract/{contract_address}"
    response = requests.get(opensea_api,headers=headers)
    json_data = json.loads(response.text)
    slug = json_data['collection']['slug']
    collection_name = json_data['collection']['name']
    thumbnail_url = json_data['image_url']
    
    website = json_data['collection']['external_url'] if json_data['collection']['external_url'] != "null" else str("Website")
    
    twitter_username = json_data['collection']['twitter_username'] if json_data['collection']['twitter_username'] != "null" else   str("")
    discord_url = json_data['collection']['discord_url'] if json_data['collection']['discord_url'] != "null" else str("")

    embed=discord.Embed(
    title=(f"{collection_name}"),
    color=0x00ff00,
    description=(f"`{contract_address}`\n\n• [Etherscan](https://etherscan.io/address/{contract_address})\n• [NFTNerds](https://nftnerds.ai/collection/{contract_address}/liveview)\n• [Opensea](https://opensea.io/collection/{slug})\n• [x2y2](https://x2y2.io/collection/{contract_address})\n• [Degenmint](https://degenmint.xyz/?address={contract_address})\n• [Website]({website})\n• [Twitter](https://twitter.com/{twitter_username})\n• [Discord]({discord_url})")
  )
    embed.set_thumbnail(url=f"{thumbnail_url}")
    await user_channel.send(embed=embed)
    return

client.run(disc_token)