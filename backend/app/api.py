from fastapi import FastAPI, Response
import pymongo
import datetime
from bson.json_util import dumps
from bson.timestamp import Timestamp
from bson.objectid import ObjectId
from fastapi.staticfiles import StaticFiles
import json
import os
from rfeed import *
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware

api_app = FastAPI(title="api-app")
app = FastAPI(title="spa-app")
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

client = pymongo.MongoClient(os.environ["MDBCONNSTR"].strip())
db = client["forgetmelater"]
col = db["articles"]

@api_app.get("/hello")
async def hello():
    return {"message": "Hello World"}
    
@api_app.get("/listAll")
async def listAll():
    cursor = col.find({}).sort("_id", pymongo.DESCENDING)
    return json.loads(dumps(cursor))

@api_app.get("/listAllAsRSS")
async def listAll():
    cursor = col.find({}).sort("_id", pymongo.DESCENDING)
    items = []
    for a in cursor:
        item = Item(
            title = a["title"],
            link= a["link"],
            guid = Guid(str(a["_id"])),
            description = a['description']
        )
        items.append(item)

    feed = Feed(
        title = "Grabosky Forget to Read Later",
        link = "http://grabosky.dyndns.org",
        lastBuildDate = datetime.datetime.now(),
        description = "Stuff I'm gonna forget to read later but I want to.",
        items = items
    )
    return Response(content=feed.rss(), media_type="text/xml")

@api_app.put("/save/{id}")
async def save(id:str, d: Dict[Any, Any]):
    page = requests.get(d["link"])
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text
    paras = soup.select('p')
    if (len(paras) > 0):
        firstPara = soup.select('p')[0].text
    else:
        firstPara = title
    d["title"] = title
    d["description"] = firstPara 
    col.update_one({"_id": ObjectId(id) }, {"$set": d })

@api_app.get("/new")
async def new():
    obj = {"title":"", "link":"" }
    id = col.insert_one(obj).inserted_id
    obj["_id"] = id
    return json.loads(dumps(obj))

@api_app.post("/newItem")
async def newItem(d: Dict[Any, Any]):
    print(d)
    page = requests.get(d["link"])
    soup = BeautifulSoup(page.content, 'html.parser')
    paras = soup.select('p')
    if (len(paras) > 0):
        firstPara = soup.select('p')[0].text
    else:
        firstPara = title
    d["description"] = firstPara 
    col.insert_one(d)

@api_app.get("/delete/{id}")
async def delete(id:str):
    col.delete_one({"_id": ObjectId(id) })