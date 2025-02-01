import re
import asyncio
import os
import io
import httpx

from telethon import events, types, errors
from telethon.tl.functions.messages import GetHistoryRequest
from ..func import http
from bs4 import BeautifulSoup as bs
from ubb import Ubot, DUMP_ID
from datetime import datetime


d = datetime.now()
m = d.strftime("%m")
y = d.strftime("%Y")


@Ubot.on(events.NewMessage(pattern=r'\.xcrap'))
async def xcrapper(event):
    target = event.message.message[len('.xcrap '):]
    CCS = []
    LIST = []
    if str(target).startswith('-1'):
        target = int(target)
    me = await Ubot.get_me()
    if not event.sender_id == me.id:
        return await event.reply("Not Allowed!!")
    async for message in Ubot.iter_messages(target):
        try:
            msgs = message.text
            CCS.append(msgs)
        except:
            pass
    for CC in set(CCS):
        try:
            i = re.findall('[0-9]+', CC)
            cc = i[0]
            mm = i[1]
            yy = i[2]
            cvv = i[3]
            if len(mm) >= 3: 
                mm, yy, cvv = yy, cvv, mm
            if str(mm).startswith('2'):
                mm, yy = yy, mm
            if len(mm) == 1:
                mm = f'0{mm}'
            if len(yy) == 2:
                yy = f'20{yy}'
            if mm+yy <= m+y:
                continue
            values = f'{cc}|{mm}|{yy}|{cvv}\n'
            regex = re.compile(r'((?:(^(4|5|6)[0-9]{15,15})|(^3[0-9]{14,14}))\|[0-9]{1,2}\|[0-9]{2,4}\|[0-9]{3,4})')
            if regex.match(values):
                LIST.append(values)
        except:
            pass

    for parsed in LIST:
        with io.open(f'{target}.txt', 'a') as f:
            f.write(parsed)
    await Ubot.send_file(event.peer_id,
                         f'{target}.txt', 
                         caption=f'**CC Scrapper\nTarget: {target}\nNo. of cards after cleanup: {len(LIST)}\nUserBotBy-» @Xbinner2**',
                         force_document=True)
    os.remove(f'{target}.txt')


@Ubot.on(events.NewMessage(pattern=r'\.scrape'))
async def scrapper(event):
    # use .scrape [channel_id or username] 100
    # default limit 100 u can scrape below 100 at a time
    target, limit = event.message.message[len('.scrape '):].split()
    if str(target).startswith('-1'):
        target = int(target)
    me = await Ubot.get_me()
    if not event.sender_id == me.id:
        return await event.reply("Not Allowed!!")
    posts = await Ubot(
        GetHistoryRequest(
            peer=target, 
            limit=int(limit), 
            offset_date=None, 
            offset_id=0, 
            max_id=0, 
            min_id=0,
            add_offset=0,
            hash=0)
    )
    cards = re.findall(r"message='([^']+)", posts.stringify())
    RAWCC = []
    for cc in cards:
        try:
            x = re.findall('[0-9]+', cc)
            cn = x[0]
            mm = x[1]
            yy = x[2]
            cvv = x[3]
            if str(mm).startswith('2'):
                mm, yy = yy, mm
            if len(mm) >= 3: 
                mm, yy, cvv = yy, cvv, mm
            if len(mm) == 1:
                mm = f'0{mm}'
            if len(yy) == 2:
                yy = f'20{yy}'
            if mm+yy <= m+y:
                continue
            value = f'{cn}|{mm}|{yy}|{cvv}\n'
            regex = re.compile(r'((?:(^(4|5|6)[0-9]{15,15})|(^3[0-9]{14,14}))\|[0-9]{1,2}\|[0-9]{2,4}\|[0-9]{3,4})')
            if regex.match(value):
                RAWCC.append(value)  # append valid format ccs!
        except:
            pass
        
    CLEAN = set(RAWCC) # rm duplicates from list
    for CC in CLEAN:
        with io.open(f'{target}.txt', 'a') as f:
            f.write(CC)
    await Ubot.send_file(event.peer_id,
                         f'{target}.txt', 
                         caption=f'**CC Scrapper\nNo. of cards from {target}: {len(CLEAN)}\nUserBotBy-» @Xbinner2**',
                         force_document=True)
    os.remove(f'{target}.txt') # rm old file to prevent duplicates


   
@Ubot.on(events.NewMessage())  # pylint:disable=E0602
async def check_incoming_messages(event):
    me = await Ubot.get_me()
    if event.sender_id == me.id:
        return
    prefixes = ['?', '/', '.', '!']
    # Get both formatted and raw text
    message = event.message
    m = None
    
    # Check if message has monospace formatting
    if message.entities:
        for entity in message.entities:
            if isinstance(entity, types.MessageEntityCode):
                # Get the monospace text
                m = message.raw_text[entity.offset:entity.offset + entity.length]
                break
    
    # If no monospace text found, use regular text
    if not m:
        m = message.text or message.raw_text
        
    if not m:  # If still no text, return
        return
    
    if m.startswith(tuple(prefixes)) or len(m) < 25 or event.is_private or len(m) > 600:
        return
    if "already" in m:
        return
    # Updated regex to catch both formats including piped format
    card_pattern = r'\b\d{15,16}(?:\b|(?:\|[^|]+)+)'
    if re.search(card_pattern, str(m)):
        try:
            x = re.findall(r'\d+', m)
            if len(x) > 10:
                return
            card_number = re.search(r'\b\d{15,16}\b', str(m))[0]
            BIN = card_number[:6]

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://bins.su',
                'referer': 'https://bins.su/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
            }

            data = {
                'action': 'searchbins',
                'bins': BIN,
                'bank': '',
                'country': ''
            }

            async with httpx.AsyncClient() as client:
                r = await client.post(
                    'https://bins.su/',
                    headers=headers,
                    data=data
                )
                r = r.text

            # Parse the response to extract bin info
            bin_info = "No BIN information found"
            soup = bs(r, features='html.parser')
            result_div = soup.find('div', {'id': 'result'})
            if result_div:
                table = result_div.find('table')
                if table:
                    rows = table.find_all('tr')
                    if len(rows) > 1:  # Has header and at least one data row
                        # Get the first result (most relevant)
                        data_cells = rows[1].find_all('td')
                        if len(data_cells) >= 6:
                            bin_info = f"""
{data_cells[0].text}
{data_cells[3].text}
{data_cells[4].text}
{data_cells[2].text}
{data_cells[5].text}
{data_cells[1].text}"""
            
            MSG = f"""
{m}
{bin_info}"""
            await asyncio.sleep(1)
            await Ubot.send_message(DUMP_ID, MSG)
                
        except errors.FloodWaitError as e:
            print(f'flood wait: {e.seconds}')
            await asyncio.sleep(e.seconds)
            await Ubot.send_message(DUMP_ID, MSG)
