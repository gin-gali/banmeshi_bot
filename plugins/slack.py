from re import A
import sys
sys.path.append("/~/slackbot_banmeshi")

from slackbot.bot import listen_to, respond_to
from menus import menu_list
from gif.gif_container import gif_list
from random import choice
import requests
from slackbot_settings import API_TOKEN
import json

@listen_to("こんにちは")
@listen_to("こんばんは")
@listen_to("Hello")
@listen_to("hello")
@respond_to("こんにちは")
@respond_to("こんばんは")
@respond_to("Hello")
@respond_to("hello")
def hello(message):
    message.reply("こんばんは！今日の晩ご飯はお決まりですか？")


@listen_to("ありがとう")
@respond_to("ありがとう")
def thankyou(message):
    message.reply("どういたしまして！")


@listen_to("メニュー")
@listen_to("menu")
@respond_to("メニュー")
@respond_to("menu")
def menu(message):
    message.reply(choice(menu_list))


@listen_to("わかってないな")
@respond_to("わかってないな")
def try_menu(message):
    message.reply("ご自分で決めたらどうですか？ https://cookpad.com/")


with open("config.json", "r") as f:
    id = json.load(f)

url = f'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId={id.get("rakuten_app_id")}&categoryId=30'
api_data = requests.get(url).json()
recipe_list = []

@listen_to("recipe")
@listen_to("レシピ")
@respond_to("recipe")
@respond_to("レシピ")
def recipe(message):
    for recipe in api_data["result"]:
        recipe_list.append(recipe)

    pick_up = choice(recipe_list)
    recipe_title = pick_up["recipeTitle"]
    recipe_url = pick_up["recipeUrl"]
    recipe_material = ", ".join(pick_up["recipeMaterial"])
    
    suggestion = f"""
【 {recipe_title} 】
URL: {recipe_url}
材料: {recipe_material}"""
    
    message.reply(suggestion)

@respond_to("gif")
def gif_upload(message):
    _gif_uploader()

    message.reply("gifを送信しました")

channel = "C02JM25TNV7"

def _gif_uploader():
    gif_file = choice(gif_list)

    files = {'file': open(gif_file, 'rb')}
    param = {'token':API_TOKEN, 'channels':channel}
    requests.post(url="https://slack.com/api/files.upload", params=param, files=files)
