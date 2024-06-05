import requests
from datetime import datetime
from cdps.plugin.events import onServerStartEvent
from cdps.plugin.manager import Listener, event_listener  

url_eew = "https://api-1.exptech.dev/api/v1/eq/eew?type=cwa"
url_report = "https://api-1.exptech.dev/api/v2/eq/report"

@event_listener(onServerStartEvent)
class onServerStartListener(Listener):
    def on_event(self, event):
        print("CDPS EEW 已啟動!")   

max_list = {
  1: "1 級",
  2: "2 級",
  3: "3 級",
  4: "4 級",
  5: "5 弱",
  6: "5 強",
  7: "6 弱",
  8: "6 強",
  9: "7 級"
}
           
last_earthquake_id = None
@new_thread
def get_eew():
    global last_earthquake_id
    response = requests.get(url_eew)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            latest_report = data[0]
            if latest_report['id'] != last_earthquake_id:
                last_earthquake_id = latest_report['id']
                eq_data = latest_report['eq']
                timestamp = int(eq_data['time'] / 1000)
                max_intensity = eq_data['max']
                max = max_list.get(max_intensity, 'Unknown')
                print(f'{timestamp} 於 {eq_data.get("loc")} 發生有感地震，慎防強烈搖晃\n預估規模 `{eq_data.get("mag")}` ，震源深度 `{eq_data.get("depth")}` 公里，最大震度 {max}\由 ExpTech Studio 提供 僅供參考，請以中央氣象署資料為準\n若感受到晃動請立即**【趴下、掩護、穩住】**')

get_eew()