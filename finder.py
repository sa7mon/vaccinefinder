import requests
import json
from playsound import playsound
import time
from rich.console import Console
from rich.table import Table

cvsHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Referer': 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br'}

while True:
    r = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.MN.json?vaccineinfo=",
                    headers=cvsHeaders)
    if r.status_code != 200:
        print(f"Got bad response from CVS: {r.status_code} {r.text}")
    else:
        updatedTime = r.json()['responsePayloadData']['currentTime']
        updatedTimeCDT = updatedTime[11:19].replace(updatedTime[11:13], str(int(updatedTime[11:13])+2))
        # print(f"\nTime: {updatedTimeCDT}")
        
        console = Console()

        table = Table(show_footer=True, footer_style="dim", show_header=True, header_style="bold magenta")
        table.add_column("Location", footer=f"Updated: {updatedTimeCDT}")
        table.add_column("Availability")

        mnData = r.json()['responsePayloadData']['data']['MN']
        available = False
        for location in mnData:
            statusColor = "red"
            if location['status'] == 'Available':
                available = True
                statusColor = "green"
            table.add_row(location['city'], f"[{statusColor}]{location['status']}[/{statusColor}]")
        if available:
            playsound('meow.mp3')
        
        console.print(table)
    
    time.sleep(600) # Wait 10 minutes