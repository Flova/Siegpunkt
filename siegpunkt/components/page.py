import justpy as jp

canvas = """
<div class="min-h-screen bg-gradient-to-b from-purple-500 to-indigo-500 flex items-center justify-center">
    <div class="bg-white p-8 rounded-md mt-20 mb-20 w-4/12 shadow-2xl">
        <div name="header" class="flex justify-between mb-8">
            <h1 name="page_title" class="text-black-800 text-3xl"></h1>
        </div>
        <div name="page_canvas"></div>
    </div>
</div>
"""

class PageCanvas(jp.Div):
    def __init__(self, title="", header_btn=jp.Div(), **kwargs):
        super().__init__(**kwargs)
        self.canvas = jp.parse_html(canvas, a=self)
        self.canvas.name_dict["page_title"].text = title
        self.canvas.name_dict["header"].add(header_btn)

    def add(self, content):
        self.canvas.name_dict["page_canvas"].add(content)

