import sys
sys.path.append("/~/slackbot_banmeshi")

from slackbot.bot import listen_to, respond_to
from menus import menu_list
from random import choice
import requests
from pprint import pprint

@listen_to("こんにちは")
@listen_to("Hello")
@listen_to("hello")
def hello(message):
    message.reply("こんにちは！")


@listen_to("ありがとう")
def thankyou(message):
    message.reply("どういたしまして！")


@listen_to("メニュー")
@listen_to("menu")
def menu(message):
    message.reply(choice(menu_list))


@listen_to("わかってないな")
def try_menu(message):
    message.reply("ご自分で決めたらどうですか？ https://cookpad.com/")


url = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1034865116788635147&categoryId=30"
api_data = requests.get(url).json()
recipe_list = []

@listen_to("recipe")
@listen_to("レシピ")
def recipe(message):
    for recipe in api_data["result"]:
        recipe_list.append(recipe)

    pick_up = choice(recipe_list)
    recipe_title = pick_up["recipeTitle"]
    recipe_url = pick_up["recipeUrl"]
    recipe_material = pick_up["recipeMaterial"]
    
    suggestion = f"""【 {recipe_title} 】
    URL: {recipe_url}
    材料: {recipe_material}
    """
    
    
    message.reply(suggestion)