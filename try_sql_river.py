import svgwrite
import sql_river as plt



nile = plt.Course(label='nile',
              drains=[plt.Drain(offset=1, width=40),
                      plt.Drain(offset=50, width=60),
                      plt.Drain(offset=200, width=80)])

plt.session.add(nile)
plt.session.commit()

volga = plt.Course(label='volga',
                   drains=[plt.Drain(offset=20, width=15),
                           plt.Drain(offset=70, width=20),
                           plt.Drain(offset=100, width=30)])
plt.session.add(volga)
plt.session.commit()

rhin = plt.Course(label='rhin',
                  drains=[plt.Drain(offset=40, width=30),
                          plt.Drain(offset=80, width=20),
                          plt.Drain(offset=130, width=40),
                          plt.Drain(offset=180, width=15)])
plt.session.add(rhin)
plt.session.commit()

river = plt.River()
river.centralize_current()


dwg = svgwrite.Drawing(filename='prueba.svg')
nile.svg_paths(dwg, 'purple')
volga.svg_paths(dwg, 'navy')
rhin.svg_paths(dwg, 'orange')
dwg.save()
