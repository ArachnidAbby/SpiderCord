import aiohttp, asyncio
import json, random

class Bot:
    def __init__(self, prefix="!"):
        self.prefix = prefix
        self._token = ""
        self._session = None
        self.loop = asyncio.get_event_loop()

    def run(self, token):
        self._token = token
        self._session = aiohttp.ClientSession()
        self.loop.run_until_complete(self._main())
    
    async def _main(self):
        async with self._session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json") as ws:
            data = {
                "op": 2,
                "d": {
                    "token": self._token,
                    "intents": 513,
                    "properties": {
                        "$os": "linux",
                        "$browser": "SpiderCord V0.1.0a",
                        "$device": "SpiderCord"
                    },
                "s":None,
                "t": None
                }
            }
            heartbeat = 0
            msg = await ws.receive()
            j = json.loads(msg.data)
            if j["op"]==10:
                heartbeat = j['d']['heartbeat_interval']
            await ws.send_str(json.dumps(data))

            self.sequence = None
            print("BOT STARTED")
            self.c=0
            asyncio.ensure_future(self._sustain_heartbeat(ws,heartbeat))
            while True:
                msg = await ws.receive()
                self.c+=1
                #print("")
                if msg.data!=None:
                    if type(msg.data)==int:print( msg.data)
                    data = json.loads(msg.data)
                    if data['op']!=11:
                        self.sequence = data['s']
                        if data['t'] == "MESSAGE_CREATE":
                            member = await self._get(f"https://discord.com/api/v9/users/{data['d']['author']['id']}")
                            print(member)
                            print(data['d']['content'])
                            if not "bot" in member.keys(): await self._post("https://discord.com/api/v9/channels/895854164217827381/messages", {"content":"RECIEVED"})
                        if data['t'] == "READY":
                            print("BOT READY")
                # await asyncio.sleep()
            await self._session.close()
    
    async def _sustain_heartbeat(self,ws,heartbeat):
        while True:
            await ws.send_str(json.dumps({'op':1, 'd':self.sequence}))
            await asyncio.sleep(max((heartbeat*random.random())/10000,0.5))

    
    async def _get(self, url):
        r = await self._session.get(url, headers={"Authorization":f"Bot {self._token}"})
        #print(await r.read())
        return json.loads(await r.read())
    
    
    async def _post(self, url, data):
        r = await self._session.post(url, data=data, headers={"Authorization":f"Bot {self._token}"})
    
    def _prepare_packet(self, packet, sequence):
        output = packet
        output["d"] = sequence
        return output

    def __del__(self):
        print(self.c)
