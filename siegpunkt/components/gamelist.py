import justpy as jp
from siegpunkt.components.tag import Tag

list_html = """
<div class="flex flex-col">
<div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
    <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
    <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
        <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Spiel
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Tags
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Anzahl
            </th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200" name="game_list_body">

        </tbody>
        </table>
    </div>
    </div>
</div>
</div>
"""

class Game(jp.Tr):
    def __init__(self, id=0, title="", tags=[Tag(text="Karten"), Tag(text="64er Deck")], num_games=0, **kwargs):
        super().__init__(**kwargs)
        self.classes = "hover:bg-gray-200 cursor-pointer"

        # Title
        self.add(jp.Td(classes="px-6 py-4 whitespace-nowrap", text=title))

        # Tags
        cell = jp.Td(classes="px-6 py-4 whitespace-nowrap", a=self)
        for tag in tags:
            cell.add(tag)

        # Num Games
        self.add(jp.Td(classes="px-6 py-4 whitespace-nowrap", text=str(num_games)))
        self.on("click", lambda x,y: print(id))


class GameList(jp.Div):
    def __init__(self, games=[Game(i, "Skat") for i in range(10)], **kwargs):
        super().__init__(**kwargs)
        table = jp.parse_html(list_html, a=self)
        for game in games:
            table.name_dict["game_list_body"].add(game)




