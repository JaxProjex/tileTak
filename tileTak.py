import asyncio
import socket
import time
from datetime import datetime, timedelta
from aiohttp import ClientSession
from pytile import async_login

#ATAK server/multicast
transport_protocol = "UDP"
server_ip = "239.2.3.1"
server_port = 6969
interval = 600 #how frequent to ping Tile location to TAK in seconds

#Tile Account Credentials
email = "johndoe@hotmail.com"
password = "secretpassword"


current_time = datetime.now()
date = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
stale = (current_time + timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

while True:
   async def main() -> None:
       """Run!"""
       async with ClientSession() as session:
           api = await async_login(email, password, session)

           tiles = await api.async_get_tiles()
           print(tiles)

           for tile_uuid, tile in tiles.items():
               color = "-16711936"
               name = tile.name
               lat = tile.latitude
               lon = tile.longitude
               isDead = tile.dead
               kind = tile.kind
               lastPing = tile.last_timestamp
               lostPing = tile.last_timestamp
               isLost = tile.lost
               isVisible = tile.visible
               if isVisible == True and isLost == False:
                  color = "-16711936" #green
               elif isLost == True:
                  color = "-65536" #red
               elif isDead == True:
                  color = "-256" #yellow
               elif isVisible == False:
                  color = "-8947849" #grey
               else:
                  color = "-8947849" #grey

               cot_message = """<?xml version="1.0" encoding="UTF-8"?>
               <event version="2.0" uid="{0}" type="a-u-G" how="m-g" time="{3}" start="{3}" stale="{4}">
               <point lat="{1}" lon="{2}" hae="0.0" ce="9999999.0" le="9999999.0"/>
               <detail>
               <status readiness="true"/>
               <archive/>
               <usericon iconsetpath="COT_MAPPING_SPOTMAP/b-m-p-s-m/{11}"/>
               <remarks>TILE DETAILS: kind: {6}, visible: {10}, lost: {9}, dead: {5}, lastPing: {7}, lostPing: {8},  </remarks>
               <contact callsign="Tile: {0}"/>
               <archive/>
               <color argb="{11}"/>
               </detail>
               </event>""".format(
               name,
               lat,
               lon,
               date,
               stale,
               isDead,
               kind,
               lastPing,
               lostPing,
               isLost,
               isVisible,
               color
               )
               print(cot_message)

               if transport_protocol == "TCP":
                  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  sock.connect((server_ip, server_port))
                  sock.sendall(cot_message.encode())
                  sock.close()
               elif transport_protocol == "UDP":
                  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                  sock.sendto(cot_message.encode(), (server_ip, server_port))
                  sock.close()
               else:
                  print("Invalid transport protocol specified. Please choose TCP or UDP.")

   asyncio.run(main())
   time.sleep(interval)
