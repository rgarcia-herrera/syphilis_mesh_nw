import svgwrite
import sql_river as plt
import random

for n in range(7):
    c = plt.Course(label=str(n), fill =
                   random.choice(['red','green','blue','orange',
                                  'aliceblue', 'aqua', 'aquamarine', 'azure',
                                  'bisque', 'blanchedalmond', 'blueviolet', 'brown',
                                  'burlywood', 'cadetblue', 'chartreuse',
                                  'chocolate', 'coral', 'cornflowerblue', 'crimson',
                                  'darkblue', 'darkcyan', 'darkgoldenrod',
                                  'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
                                  'darkmagenta', 'darkolivegreen', 'darkorange',
                                  'darkorchid', 'darkred', 'darksalmon',
                                  'darkseagreen', 'darkslateblue', 'darkslategray',
                                  'darkslategrey', 'darkturquoise', 'darkviolet',
                                  'deeppink', 'deepskyblue', 'dimgray', 'dimgrey',
                                  'dodgerblue', 'firebrick', 'forestgreen',
                                  'gainsboro', 'gold', 'goldenrod', 'hotpink',
                                  'indianred', 'indigo', 'khaki', 'lavender', ]))
    plt.session.add(c)
    plt.session.commit()
    o = 1
    for m in range(random.randint(8,35)):
        o += random.randint(80,100)
        d = plt.Drain(offset=o,
                      width=random.randint(25,60))
        c.add_drain(d)


dwg = svgwrite.Drawing(filename='prueba.svg')

river = plt.River(dwg)
river.centralize_current()
river.to_svg()
dwg.save()
