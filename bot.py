import discord
import logging
import requests
import re

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = discord.Bot()

# On ready
@bot.event
async def on_ready():
    print("Ready!")

def parseHWIDfromlink(link):
    return link.replace("https://flux.li/windows/start.php?HWID=","")

@bot.slash_command(guild_ids=[1122097621465563187], description="Get the key for you, just pass in your get key link")
async def get_key(ctx, link: str):
    await ctx.response.send_message("Processing...", ephemeral=True)

    if not link.startswith("https://flux.li/windows/start.php?HWID="):
        embed = discord.Embed(title="Failed to fetch the key for you!", description="Please try again later!", color=discord.Color.red())
        embed.add_field(name="Error", value=f"Invalid link!", inline=False)

        await ctx.channel.send_message(content=f"<@{ctx.author.id}>",embeds=[embed])
        return

    linkvertise = "https://linkvertise.com/"

    with ctx.channel.typing():
        hwid = parseHWIDfromlink(link)

        embed = discord.Embed(title="Fetching the key for you...", description="Hold on tight, this process can take serveral seconds!", color=discord.Color.blurple())
        embed.add_field(name="Status", value="Fetching...", inline=False)

        msg = await ctx.channel.send(embeds=[embed])

        key_regex = r'let content = \("([^"]+)"\);'

        endpoints =  [
             # {
                #     "url": f"https://flux.li/windows/start.php?HWID={hwid}",
                #     "referer": ""
                # }, You can skip these links, they are not needed
                {
                    "url": f"https://flux.li/windows/start.php?cf331c115dc1fda3067c0e3d3a8bda76=true&HWID={hwid}",
                    "referer": f"https://flux.li/windows/start.php?HWID={hwid}"
                },
                # {
                #     "url": "https://fluxteam.net/windows/checkpoint/check1.php",
                #     "referer": linkvertise
                # }, You can skip these links, they are not needed
                # {
                #     "url": "https://fluxteam.net/windows/checkpoint/check2.php",
                #     "referer": linkvertise
                # }, You can skip these links, they are not needed
                {
                    "url": "https://fluxteam.net/windows/checkpoint/main.php",
                    "referer": linkvertise
                },
        ]

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x66) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        for i in range (len(endpoints)):
            url = endpoints[i]["url"]
            referer = endpoints[i]["referer"]

            headers["referer"] = referer
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                with open("bypass.html", "w") as f:
                    f.write(response.text)
                print(f"[{i}] Failed to bypass | Status code: {response.status_code}| Response content has been written to bypass.html for debugging purposes.")

                embed = discord.Embed(title="Failed to fetch the key for you!", description="Please try again later!", color=discord.Color.red())
                embed.add_field(name="Status", value=f"Failed to bypass | Status code: {response.status_code}| Response content has been written to bypass.html for debugging purposes.", inline=False)

                await msg.edit(content=f"<@{ctx.author.id}>",embeds=[embed])
                return

            print(f"[{i}] Response: {response.status_code}")

            if i == len(endpoints)-1: # End of the bypass
                match = re.search(key_regex, response.text)
                if match:
                    content = match.group(1)
                    print(f"Bypassed successfully! Code: {content}")

                    embed = discord.Embed(title="Successfully fetched the key for you!", description="Here is your key:", color=discord.Color.green())
                    embed.add_field(name="Status", value="Successfully fetched the key for you!", inline=False)
                    embed.add_field(name="Key", value=content, inline=False)

                    await msg.edit(content=f"<@{ctx.author.id}>",embeds=[embed])

                else:
                    with open("bypass.html", "w") as f:
                        f.write(response.text)

                    embed = discord.Embed(title="Failed to fetch the key for you!", description="Please try again later!", color=discord.Color.red())
                    embed.add_field(name="Status", value="Failed to fetch the key for you!", inline=False)

                    await msg.edit(content=f"<@{ctx.author.id}>",embeds=[embed])
                    
                    print("Bypassed not successfully! Code: None, response content has been written to bypass.html for debugging purposes.")
            else:
                embed = discord.Embed(title="Fetching the key for you... Step: "+ str(i+1), description="Hold on tight, this process can take serveral seconds!", color=discord.Color.blurple())
                embed.add_field(name="Status", value="Fetching...", inline=False)

                await msg.edit(content=f"<@{ctx.author.id}>",embeds=[embed])

bot.run("MTEyMjA5Nzc2MDU1Mjg3ODEyMg.GueGl0.W7UYQvPqfZwc0ERlA4xvf1pZnzpTyGEM5eYM9E")