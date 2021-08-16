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
    def __init__(self, id=0, **kwargs):
        super().__init__(**kwargs)

        # TODO database
        self.game_title="Skat"
        self.tags=[Tag(text="Karten"), Tag(text="64er Deck")]
        self.num_games=0

        self.add_summary()

        def click_handle(self, msg):
            if len(self) == 3:
                self.delete_components()
                self.add(GameInfos(id=0, on_close=self.add_summary))
                self.classes = ""

        self.on("click", click_handle)

    def add_summary(self, msg=None):
        self.delete_components()
        self.classes = "hover:bg-gray-200 cursor-pointer"
        # Title
        self.add(jp.Td(classes="px-6 py-4 whitespace-nowrap", text=self.game_title))
        # Tags
        cell = jp.Td(classes="px-6 py-4 whitespace-nowrap", a=self)
        for tag in self.tags:
            cell.add(tag)
        # Num Games
        self.add(jp.Td(classes="px-6 py-4 whitespace-nowrap", text=str(self.num_games)))


class GameInfos(jp.Td):
    def __init__(self, id, on_close, **kwargs):
        super().__init__(**kwargs)
        self.game_name = "Doppelkopf"
        self.colspan = "3"
        header = jp.Div(classes="flex justify-between hover:bg-gray-200 cursor-pointer", event_propagation=False)
        header.add(jp.P(classes="px-6 p-4 text-xl whitespace-nowrap", text=self.game_name))
        header.add(jp.parse_html('''<div class="p-4 flex items-center"> <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" class="w-5 h-5 align-right"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg></div>'''))
        header.on("click", on_close)
        self.add(header)
        content = jp.Div(classes="m-6 mt-2", event_propagation=False)
        content.add(jp.P(classes="text-sm", text="Anahl Spiele: 4"))
        content.add(jp.P(classes="text-sm", text="Bester Spieler: Étienne"))
        content.add(jp.P(classes="text-sm", text="Letzter Spieler: Étienne"))
        content.add(jp.H3(classes="mt-4 mb-2 text-xl", text="Spieler"))
        content.add(jp.Hr())

        players_div = jp.Div()

        for person in ["Étienne", "Nick", "Flo"]:
            players_div.add(PersonEntry(0, person))

        content.add(players_div)

        add_player = jp.Div(classes="flex mt-4", event_propagation=False)
        name_inp = jp.Input(a=add_player, classes="w-full mr-4 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500", placeholder='Max Mustermann')
        add_btn = jp.Div(a=add_player, classes="text-l p-2 rounded-lg bg-indigo-800 text-indigo-100 hover:bg-indigo-600 flex items-center px-4 py-2 leading-5 cursor-pointer", text="Hinzufügen")
        add_btn.input_field = name_inp
        add_btn.players_div = players_div

        def add_player_cb(self, msg):
            self.players_div.add(PersonEntry(0, self.input_field.value))

        add_btn.on("click", add_player_cb)
        content.add(add_player)
        self.add(content)


class PersonEntry(jp.Div):
    def __init__(self, game, person, **kwargs):
        super().__init__(**kwargs)

        self.classes="mt-2 mb-2 flex justify-between"

        # Name
        self.add(jp.P(classes="text-md flex items-center", text=person))

        # Counter
        counter_div = jp.Div(classes="flex justify-between font-mono")
        # Score
        score_label = jp.Div(classes="text-l p-0 ml-4 mr-4 flex items-center leading-5", text=0)
        # Plus
        plus_btn = jp.Div(classes="text-l p-2 rounded-lg bg-green-800 text-indigo-100 hover:bg-green-900 flex items-center px-4 py-2 leading-5 cursor-pointer", text="+")
        plus_btn.score_label = score_label
        def inc(self, msg):
            self.score_label.text = int(score_label.text) + 1
        plus_btn.on("click", inc)

        # Minus
        minus_btn = jp.Div(classes="text-l p-2 rounded-lg bg-red-800 text-indigo-100 hover:bg-red-900 flex items-center px-4 py-2 leading-5 cursor-pointer", text="-")
        minus_btn.score_label = score_label
        def dec(self, msg):
            self.score_label.text = int(score_label.text) - 1
        minus_btn.on("click", dec)

        counter_div.add(minus_btn)
        counter_div.add(score_label)
        counter_div.add(plus_btn)
        self.add(counter_div)





class GameList(jp.Div):
    def __init__(self, games=[], **kwargs):
        super().__init__(**kwargs)
        table = jp.parse_html(list_html, a=self)
        games = [Game(i) for i in range(10)]
        for game in games:
            table.name_dict["game_list_body"].add(game)
