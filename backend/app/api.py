from fastapi import FastAPI
import pymongo
import datetime
from bson.json_util import dumps
from bson.timestamp import Timestamp
from bson.objectid import ObjectId
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import json
import os
from rfeed import *

class ArticleItem(BaseModel):
    title: str
    link: str

api_app = FastAPI(title="api-app")
app = FastAPI(title="spa-app")
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

client = pymongo.MongoClient(os.environ["MDBCONNSTR"].strip())
db = client["forgetmelater"]
col = db["articles"]

@api_app.get("/hello")
async def hello():
    return {"message": "Hello World"}
    
@api_app.get("/listAll")
async def listAll():
    cursor = col.find({})
    return json.loads(dumps(cursor))

@api_app.get("/listAllAsRSS")
async def listAll():
    cursor = col.find({})
    items = []
    for a in cursor:
        item = Item(
            title = a["title"],
            link= a["link"],
            guid = Guid(str(a["_id"]))
        )
        items.append(item)

    feed = Feed(
        title = "Grabosky Forget to Read Later",
        link = "http://grabosky.dyndns.org",
        lastBuildDate = datetime.datetime.now(),
        description = "Stuff I'm gonna forget to read later but I want to.",
        items = items
    )
    return feed.rss()

@api_app.put("/save/{id}")
async def save(id:str, ai: ArticleItem):
    # i'm bad at python frameworks
    d = ai.model_dump()
    col.update_one({"_id": ObjectId(id) }, {"$set": d })

@api_app.get("/new")
async def new():
    obj = {"title":"", "link":"" }
    id = col.insert_one(obj).inserted_id
    obj["_id"] = id
    return json.loads(dumps(obj))