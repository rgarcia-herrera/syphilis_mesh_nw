import svgwrite
import sql_river as plt
import random
import csv

r = csv.DictReader(open('top_kw.csv'))

def random_color():
    return random.choice(['red','green','blue','orange', 'aliceblue',
                          'aqua', 'aquamarine', 'azure', 'bisque',
                          'blanchedalmond', 'blueviolet', 'brown',
                          'burlywood', 'cadetblue', 'chartreuse',
                          'chocolate', 'coral', 'cornflowerblue',
                          'crimson', 'darkblue', 'darkcyan',
                          'darkgoldenrod', 'darkgray', 'darkgreen',
                          'darkgrey', 'darkkhaki', 'darkmagenta',
                          'darkolivegreen', 'darkorange',
                          'darkorchid', 'darkred', 'darksalmon',
                          'darkseagreen', 'darkslateblue',
                          'darkslategray', 'darkslategrey',
                          'darkturquoise', 'darkviolet', 'deeppink',
                          'deepskyblue', 'dimgray', 'dimgrey',
                          'dodgerblue', 'firebrick', 'forestgreen',
                          'gainsboro', 'gold', 'goldenrod', 'hotpink',
                          'indianred', 'indigo', 'khaki', 'lavender',])

for row in r:
    kw = row.pop('kw')
    c = plt.Course(label=kw,
                   fill = random_color())
    plt.session.add(c)
    plt.session.commit()
    y = 1
    for year in sorted(row.keys()):
        width = float(row[year])
        if width > 0:
            d = plt.Drain(offset=y,
                          width=width)
            c.add_drain(d)
        y += 100


dwg = svgwrite.Drawing(filename='syphilis_top_kw.svg')
river = plt.River(dwg)
river.centralize_current()
river.to_svg()
dwg.save()
