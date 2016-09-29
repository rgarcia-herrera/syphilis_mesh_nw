import svgwrite


class River:
    def __init__(self, filename):
        self.dwg = svgwrite.Drawing(filename=filename)



class Race:
    def __init__(self, color='grey'):
        self.dwg = svgwrite.Drawing()

    def add_recess(self, distance, width):
        pass


class Recess:
    pass


dwg = svgwrite.Drawing('aguas.svg')

p = dwg.path(d="M10,10 Z",
             fill="#00ff00",
             stroke="red",
             stroke_width=6)

p.push("C 30 10")
p.push("30 30")
p.push("0 50")

dwg.add(p)
dwg.save()
