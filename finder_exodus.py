import requests
import json
from playsound import playsound
import time
from rich.console import Console
from rich.table import Table

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Referer': '',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br'}

while True:
    r = requests.get("https://api.prod.projectexodus.us/get-locations/v2/55432?radius=10",
                    headers=headers)
    if r.status_code != 200:
        print(f"Got bad response from API: {r.status_code} {r.text}")
    else:
        # updatedTime = r.json()['responsePayloadData']['currentTime']
        # updatedTimeCDT = updatedTime[11:19].replace(updatedTime[11:13], str(int(updatedTime[11:13])+2))
        # print(f"\nTime: {updatedTimeCDT}")
        
        console = Console()

        table = Table(footer_style="dim", show_header=True, header_style="bold magenta")
        table.add_column("Location", footer=f"")
        table.add_column("Address")
        table.add_column("City")
        table.add_column("Apts Updated")
        table.add_column("Appointments")

        available = False
        for s in r.json()['results']:
            if s['appointments'] is not None:
                available = True
            table.add_row(
                s['locationName'], s['address1'], s['city'], s['appointmentsUpdated'], str(s['appointments'])
            )
        if available:
            playsound('meow.mp3')
        
        console.print(table)
    
    time.sleep(600) # Wait 10 minutes