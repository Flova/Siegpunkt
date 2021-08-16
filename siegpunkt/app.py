import justpy as jp
import asyncio

from siegpunkt.components.gamelist import GameList
from siegpunkt.components.page import PageCanvas
from siegpunkt.components.new_button import NewButton


@jp.SetRoute('/games')
def gamepage(request):
    wp = jp.WebPage(
        # Add html header for responsive webdesign
        head_html='''
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
        html {
            width: 100vw;
        }
        </style>
        ''')

    # Page properties
    wp.title = "Siegpunkt"
    wp.favicon = None
    wp.display_url = 'games'

    # Add main component
    can = PageCanvas(a=wp, title="Spiele", header_btn=NewButton())
    can.add(GameList())
    return wp

jp.justpy()
