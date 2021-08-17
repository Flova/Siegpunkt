import justpy as jp

from datetime import datetime
from sqlalchemy import func, desc

from siegpunkt.components.tag import Tag
from siegpunkt.models import Game, User, Match, Session

s = Session()

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

class GameRow(jp.Tr):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)

        # Set properties
        self.game = game

        if game.tags:
            self.tags = [Tag(text=tag) for tag in game.tags.split(",")]
        else:
            self.tags = [Tag(text="Karten")]

        # Add game infos to table
        self.add_summary()

        def click_handle(self, msg):
            # Handle click if there isn't a GameInfos component inside
            if not isinstance(self.last(), GameInfos):
                # Add GameInfos cell inside
                self.delete_components()
                self.add(GameInfos(game=game, on_close=self.add_summary))
                self.classes = ""

        self.on("click", click_handle)

    def add_summary(self, msg=None):
        # Clear previous content
        self.delete_components()
        # Add style
        self.classes = "hover:bg-gray-200 cursor-pointer"
        # Add game title
        self.add(jp.Td(classes="px-6 py-4 whitespace-nowrap", text=self.game.name))
        # Add game tags
        cell = jp.Td(classes="px-6 py-4 whitespace-nowrap", a=self)
        for tag in self.tags:
            cell.add(tag)
        # Show number of games
        self.add(jp.Td(classes="px-6 py-4 whitespace-nowrap", text=str(s.query(Match).filter(Match.game==self.game).count())))

    def react(self, data):
        # Handle click if there isn't a GameInfos component inside
        if not isinstance(self.last(), GameInfos):
            self.add_summary()


class GameInfos(jp.Td):
    def __init__(self, game, on_close, **kwargs):
        super().__init__(**kwargs)

        self.game = game

        # Set name
        self.game_name = game.name

        # Properties
        self.colspan = "3"
        self.classes = "p-0"

        # Add header which is clicked on close and displays the game name
        header = jp.Div(classes="flex justify-between hover:bg-gray-200 cursor-pointer", event_propagation=False)
        header.add(jp.P(classes="px-6 p-4 whitespace-nowrap", text=self.game_name))
        header.add(jp.parse_html('''<div class="p-4 flex items-center"> <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" class="w-5 h-5 align-right"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg></div>'''))
        header.on("click", on_close)
        self.add(header)

        content = jp.Div(classes="m-6 mt-2", event_propagation=False)

        # Add infos regarding this game
        self.infos = jp.Div()
        content.add(self.infos)

        content.add(jp.H3(classes="mt-4 mb-2 text-xl", text="Spieler"))
        content.add(jp.Hr())

        # Add list of players including their scores
        self.players_div = jp.Div()
        content.add(self.players_div)

        # Add input to add new players
        add_player = jp.Div(classes="flex mt-4", event_propagation=False)
        name_inp = jp.InputChangeOnly(a=add_player, classes="w-full mr-4 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500", placeholder='Max Mustermann')
        add_btn = jp.Div(a=add_player, classes="text-l p-2 rounded-lg bg-indigo-800 text-indigo-100 hover:bg-indigo-600 flex items-center px-4 py-2 leading-5 cursor-pointer", text="Hinzufügen")
        add_btn.input_field = name_inp
        add_btn.players_div = self.players_div

        def add_player_cb(self, msg):
            # Check if user with that name exists
            if s.query(User).filter(User.name==self.input_field.value).count() == 0:
                try:
                    # Create user in db
                    user = User(name=self.input_field.value, creation_date=datetime.now())
                    s.add(user)
                    s.commit()
                except Exception as e:
                    s.rollback()
                    print(e)
                # Add him to the component
                self.players_div.add(PersonEntry(game, user))
                # Clear input field
                self.input_field.value = ""

        add_btn.on("click", add_player_cb)
        content.add(add_player)

        self.add(content)

    def react(self, data):
        # The players which already played sorted by score
        players_db = [x[0] for x in s.query(User, func.sum(Match.score).label('mySum')).filter(Match.game==self.game).join(Match.player).group_by(User).order_by(desc('mySum')).all()]
        players_db.extend(s.query(User).all())
        # Remove duplicates
        players_db = list(dict.fromkeys(players_db))
        # Add players
        self.players_div.delete_components()
        for person in players_db:
            self.players_div.add(PersonEntry(self.game, person))

        self.infos.delete_components()
        self.infos.add(jp.P(classes="text-sm", text=f"Anzahl Spiele: {s.query(Match).filter(Match.game==self.game).count()}"))
        best_player = s.query(User.name, func.sum(Match.score).label('mySum')).filter(Match.game==self.game).join(Match.player).group_by(User).order_by(desc('mySum')).first()
        if best_player:
            self.infos.add(jp.P(classes="text-sm", text=f"Bester Spieler: {best_player[0]}"))

class PersonEntry(jp.Div):
    def __init__(self, game, person, **kwargs):
        super().__init__(**kwargs)

        # Style of the entry container
        self.classes="mt-2 mb-2 flex justify-between"

        # Name of the person
        self.add(jp.P(classes="text-md flex items-center", text=person.name))

        # Counter component
        def write_score_to_db(score):
            # Write it to the db
            try:
                # Create user in db
                user = Match(game=game, player=person, score=score, date=datetime.now())
                s.add(user)
                s.commit()
            except Exception as e:
                s.rollback()
                print(e)

        def inc(self, msg):
            self.score_label.text = int(score_label.text) + 1
            write_score_to_db(1)

        def dec(self, msg):
            self.score_label.text = int(score_label.text) - 1
            write_score_to_db(-1)

        counter_div = jp.Div(classes="flex justify-between font-mono")
        # Score label
        if s.query(Match).filter(Match.game==game, Match.player==person).count():
            score = int(s.query(Match).with_entities(func.sum(Match.score).label("mySum")).filter(Match.game==game, Match.player==person).first().mySum)
        else:
            score = 0
        score_label = jp.Div(
            classes="text-l p-0 ml-4 mr-4 flex items-center leading-5",
            text=score)
        # Plus button
        plus_btn = jp.Div(classes="text-l p-2 rounded-lg bg-green-800 text-indigo-100 hover:bg-green-900 flex items-center px-4 py-2 leading-5 cursor-pointer", text="+")
        plus_btn.score_label = score_label
        plus_btn.on("click", inc)

        # Minus button
        minus_btn = jp.Div(classes="text-l p-2 rounded-lg bg-red-800 text-indigo-100 hover:bg-red-900 flex items-center px-4 py-2 leading-5 cursor-pointer", text="-")
        minus_btn.score_label = score_label
        minus_btn.on("click", dec)

        counter_div.add(minus_btn)
        counter_div.add(score_label)
        counter_div.add(plus_btn)
        self.add(counter_div)


class GameList(jp.Div):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = jp.parse_html(list_html, a=self)

        games = [x[0] for x in s.query(Game, func.count(Match.id).label('mySum')).join(Match.game).group_by(Game).order_by(desc('mySum')).all()]
        games.extend(s.query(Game).all())

        # Remove duplicates
        games = list(dict.fromkeys(games))

        for game in games:
            self.table.name_dict["game_list_body"].add(GameRow(game))

    def add_game(self, game):
        self.table.name_dict["game_list_body"].add(GameRow(game))
