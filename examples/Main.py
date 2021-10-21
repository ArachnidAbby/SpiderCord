import sys,json
sys.path.append("src/")
import spidercord
bot = spidercord.Bot()
with open("examples/token.txt") as f:
    TOKEN = f.read()
bot.run(TOKEN)

#bot._post("https://discord.com/api/v9/channels/895854164217827381/messages", {"content":"Gaming"})