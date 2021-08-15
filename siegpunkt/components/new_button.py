import justpy as jp

class NewButton(jp.Div):
    def __init__(self, text="Neu", **kwargs):
        super().__init__(**kwargs)
        self.classes = "text-l p-4 rounded-lg bg-indigo-800 text-indigo-100 hover:bg-indigo-600 flex items-center px-4 py-2 leading-5 cursor-pointer"
        self.text = text
