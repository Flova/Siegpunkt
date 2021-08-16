import justpy as jp

class NewButton(jp.Div):
    def __init__(self, text="Neu", **kwargs):
        super().__init__(**kwargs)
        self.classes = "flex"
        first_new_btn = jp.Div(classes = "text-l p-4 rounded-lg bg-indigo-800 text-indigo-100 hover:bg-indigo-00 flex items-center px-4 py-2 leading-5 cursor-pointer", text=text)
        self.add(first_new_btn)

        parent_div = self

        def show_new_game_dialog(self, msg):
            parent_div.delete_components()

            add_game = jp.Div(classes="flex justify-between", event_propagation=False)
            name_inp = jp.Input(a=add_game, classes="w-full mr-4 ml-6 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500", placeholder='Max Mustermann')
            add_btn = jp.Div(a=add_game, classes="text-l p-2 rounded-lg bg-indigo-800 text-indigo-100 hover:bg-indigo-600 flex items-center px-4 py-2 leading-5 cursor-pointer", text="Hinzufügen")
            add_btn.input_field = name_inp

            parent_div.add(add_game)

            def add_game_input_cb(self, msg):
                parent_div.delete_components()
                parent_div.add(first_new_btn)
                first_new_btn.on("click", show_new_game_dialog)

            add_btn.on("click", add_game_input_cb)

        first_new_btn.on("click", show_new_game_dialog)
