import justpy as jp

class NewButton(jp.Div):
    """
    Button componenet used to create new things on the top of a page of things
    It consits of a new button that transforms into a input field if clicked.
    """
    def __init__(self, text="Neu", **kwargs):
        super().__init__(**kwargs)
        # Style
        self.classes = "flex"
        # Add the first ´New´ button
        first_new_btn = jp.Div(classes = "text-l p-4 rounded-lg bg-indigo-800 text-indigo-100 hover:bg-indigo-00 flex items-center px-4 py-2 leading-5 cursor-pointer", text=text)
        self.add(first_new_btn)

        # Save preference to the parent container for the events
        parent_div = self

        def show_new_game_dialog(self, msg):
            """
            Handles click event for the `New` button which shows the input field
            """
            # Clear `New` button
            parent_div.delete_components()

            def input_cb(self, msg):
                """
                Handles the submission of the naming form
                """
                # Clear the container / delete the form
                parent_div.delete_components()
                # Add the `New` button again
                parent_div.add(first_new_btn)
                first_new_btn.on("click", show_new_game_dialog)

            # Create name form
            input_container = jp.Div(classes="flex justify-between", event_propagation=False)
            name_input_field = jp.Input(a=input_container, classes="w-full mr-4 ml-6 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500", placeholder='Musterspiel')
            add_btn = jp.Div(a=input_container, classes="text-l p-2 rounded-lg bg-indigo-800 text-indigo-100 hover:bg-indigo-600 flex items-center px-4 py-2 leading-5 cursor-pointer", text="Hinzufügen")
            add_btn.input_field = name_input_field
            parent_div.add(input_container)

            add_btn.on("click", input_cb)

        first_new_btn.on("click", show_new_game_dialog)
