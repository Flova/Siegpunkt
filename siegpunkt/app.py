import justpy as jp
import asyncio

from siegpunkt.components.gamelist import GameList
from siegpunkt.components.page import PageCanvas
from siegpunkt.components.new_button import NewButton


@jp.SetRoute('/games')
def testpage(request):
    wp = jp.WebPage()
    wp.title = "Siegpunkt"
    wp.favicon = None
    wp.display_url = 'games'
    can = PageCanvas(a=wp, title="Spiele", header_btn=NewButton())
    can.add(GameList())
    return wp

jp.justpy()
