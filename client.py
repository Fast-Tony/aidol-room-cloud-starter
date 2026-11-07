"""Aidol Room Cloud sample client. Python standard library only."""
import json, os, time, uuid, urllib.request, urllib.error

DEFAULT_BASE="https://genaidol.com/cloud-api/developer/v1"
class AidolClient:
 def __init__(self,api_key="",session_id="",base_url=DEFAULT_BASE):
  self.base=base_url.rstrip("/");self.key=api_key;self.session=session_id
 def request(self,method,path,data=None,retry=False):
  for attempt in range(3 if retry else 1):
   headers={"Content-Type":"application/json"}
   if self.key:headers["Authorization"]="Bearer "+self.key
   req=urllib.request.Request(self.base+path,data=json.dumps(data).encode() if data is not None else None,headers=headers,method=method)
   try:
    with urllib.request.urlopen(req,timeout=35) as r:return json.load(r)
   except urllib.error.HTTPError as e:
    try:detail=json.loads(e.read()).get("error",{})
    except ValueError:detail={}
    finally:e.close()
    if not retry or attempt==2 or e.code not in (502,503,504):raise RuntimeError(str(detail.get("code",e.code))+": "+detail.get("message","Request failed")) from None
   except (OSError,TimeoutError):
    if not retry or attempt==2:raise RuntimeError("Delivery unconfirmed. Retry with the SAME event id.") from None
   time.sleep(2**attempt)
 def connect(self,code):
  result=self.request("POST","/connect",{"code":code});self.key=result["api_key"];self.session=result["session_id"];return result
 def get_config(self):
  return self.request("GET","/rooms/"+self.session+"/config")
 def update_config(self,expected_revision,**changes):
  return self.request("PUT","/rooms/"+self.session+"/config",{"expected_revision":expected_revision,**changes})
 def voices(self):
  return self.request("GET","/rooms/"+self.session+"/catalog/voices")
 def send(self,kind,name,text="",platform="custom",event_id=None,reply=False):
  event={"id":event_id or uuid.uuid4().hex,"type":kind,"platform":platform,"user":{"name":name},"text":text}
  return self.request("POST","/rooms/"+self.session+"/events",{"events":[event],"auto_reply_interactions":reply},retry=True)

if __name__=="__main__":
 import argparse
 p=argparse.ArgumentParser();p.add_argument("--code");p.add_argument("--text",default="Hello");p.add_argument("--name",default="Demo");p.add_argument("--type",choices=["comment","join","follow","share","like","gift"],default="comment");p.add_argument("--event-id");p.add_argument("--reply-interactions",action="store_true");p.add_argument("--connect-only",action="store_true");a=p.parse_args()
 c=AidolClient(os.getenv("AIDOL_API_KEY",""),os.getenv("AIDOL_SESSION_ID",""),os.getenv("AIDOL_API_BASE",DEFAULT_BASE))
 if a.code:
  c.connect(a.code);print("Connected:",c.session,"(key kept in memory for this process only)")
 if not a.connect_only:print(json.dumps(c.send(a.type,a.name,a.text,event_id=a.event_id,reply=a.reply_interactions),ensure_ascii=False,indent=2))
