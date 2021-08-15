import justpy as jp

class Tag(jp.Span):
    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.classes="px-2 mr-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800"
        self.text = text
