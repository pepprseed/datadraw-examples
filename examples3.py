""" Examples set 3.                      http://datadraw.org
    Usage:    python examples3.py .... creates some svg files in cwd
    Or invoked as part of the flask web app.
    Prerequisites: 
     a python3.6+ virtual environment; pip -r requirements.txt
"""

from datadraw import DataDraw, write_svgfile



def run_all():
    """ run examples and return the result svg objects in a dict """
    ex = Examples3()
    svgset = {}
    svgset['elements1']    = ex.elements1()
    svgset['datapoints1']  = ex.datapoints1()
    svgset['image_annot1'] = ex.image_annot1()
    return svgset



class Examples3:

    def __init__(self):
        self.dd = DataDraw()


    def elements1(self):
        """ various shapes, elements, and legend demo """
        dd = self.dd
        dd.svgbegin(width=550, height=400)
        dd.setspace('X', svgrange=(50,530), datarange=(0,100))
        dd.setspace('y', svgrange=(50,380), datarange=(0,100))
        dd.setline(width=0.5, color='#88c')
        dd.axis('X', grid=True)
        dd.axis('Y', grid=True)
        dd.setline(width=1, color='#777')

        # blue ellipse, placed at native equiv of (50,80) in data units
        x, y = dd.natpair(50, 80)
        dd.ellipse(x, y, width=100, height=60, color='#aff', opacity=0.7)
        dd.legenditem(color='#aff', sample='circle', label='Ellipse')

        # green rectangle, placed at native coordinates
        x, y = dd.natpair(50, 60)
        x2 = x + dd.natdist('X', 40)
        y2 = y + dd.natdist('Y', 20)
        dd.rect(x, y, x2, y2, color='#afa', opacity=0.7)
        dd.legenditem(color='#afa', sample='square', label='Rectangle')

        # magenta circle, placed at native equiv of (80,40) in data units
        x, y = dd.natpair(80, 40)
        diam = dd.natdist('X', 20)
        dd.circle(x, y, diameter=diam, color='#faf', opacity=0.7, outline=True)
        dd.legenditem(color='#faf', sample='circle', label='Circle (outlined)')

        # salmon rectangle, rounded corners centered at (60,20) in data units
        dd.rectangle(60, 20, width=40, height=17, color='#faa', opacity=0.7,
                         outline=True, rounded=True)
        dd.legenditem(color='#faa', label='Rectangle (rounded corners)')

        # an arrow
        dd.arrow(50, 17, 75, 10)
        dd.legenditem(sample='line', label='Arrow')

        # display a png image
        dd.image(href="https://www.python.org/static/community_logos/python-powered-w-100x40.png",
                           x=dd.nx(78), y=dd.ny(16), width=100, opacity=0.8)

        # demo multi-line legend entries and various-sized datapoints ...
        dd.legenditem(sample='symbol', symbol='(vcircle-o)', diameter=10,
                         color='#fed', label='Circular (vector)\n data point')
        dd.legenditem(sample='symbol', symbol='(vcircle-o)', diameter=18,
                         color='#fed', label='Larger\n')
        dd.legenditem(sample='symbol', symbol='(vcircle-o)', diameter=25,
                         color='#fed', label='Even larger\n')

        dd.legenditem(sample='symbol', symbol='(diamond-o)', diameter=12,
                         color='#3a3', label='Diamond (html char)\n data point')
        dd.legenditem(sample='symbol', symbol='(diamond-o)', diameter=20,
                         color='#3a3', label='Larger\n')
        dd.legenditem(sample='symbol', symbol='(diamond-o)', diameter=27,
                         color='#3a3', label='Even larger\n')

        # demo image in legend
        dd.legenditem(sample='symbol', symbol='(img)/static/img/cherries.png', 
                          diameter=14, label='Image (png)\n data point')

        # demo symbol with backing in legend
        dd.legenditem(sample='symbol', symbol='B', diameter=8, color='#000', 
                       label='Char data point\n w/ pink diamond backing',
                       backing={'symbol':'(diamond)', 'diameter':15, 'color':'#fbb'})

        dd.settext(color='#777')
        dd.legendrender(format='down')

        return dd.svgresult()


    def datapoints1(self):
        dd = self.dd
        dd.svgbegin(width=600, height=160)
        dd.setspace('X', svgrange=(20,580), datarange=(0,18))
        dd.setspace('Y', svgrange=(20,115), datarange=(0,4))
        dd.setline(color='#ddd')
        dd.axis('X', inc=1, stubs=False, grid=True)
        dd.axis('Y', inc=1, stubs=False, grid=True)
    
        # do first row of symbols... pre-defined vector and glyph-based
        symbolnames = ['(vcircle)', '(vcircle-o)', '(vrect)', '(vrect-o)',
             '(circle)', '(circle-o)', '(triangle)', '(triangle-o)', '(dtriangle)',
             '(square)', '(square-o)', '(diamond)', '(diamond-o)',
             '(star4)', '(spokes5)', '(spokes8)']
        dd.settext(ptsize=10, color='#777', rotate=-40, anchor='start')
        dd.setline(color='#faa', width=2)
        xpos = 1
        for sym in symbolnames:
            dd.datapoint(x=xpos, y=3, symbol=sym, color='#373', diameter=15)
            dd.label(x=xpos, y=3, text=sym, adjust=(4,10))
            xpos += 1
        dd.setline(restore=True)
    
        # 2nd row... other possible constructs 
        dd.settext(ptsize=10, color='#333')
        dd.setline(width=0.5, color='#333')
    
        dd.datapoint(x=1, y=1, symbol='&Sigma;', diameter=12, color='#333')         # HTML char
        dd.datapoint(x=2, y=1, symbol='W',   diameter=10, color='#333')             # ordinary char
        dd.datapoint(x=3, y=1, symbol='CBS', diameter=10, color='#333')             # word or acronym
    
        # stretch can be used to vrect or vcircle...
        dd.datapoint(x=4, y=1, symbol='(vrect)', diameter=15, stretch=(1.4,0.6), color='#373')
        dd.datapoint(x=5, y=1, symbol='(vrect-o)', diameter=15, stretch=(0.6,1.4), color='#a88')
        dd.datapoint(x=6, y=1, symbol='(vcircle)', diameter=15, stretch=(1.4,0.6), color='#373')
    
        # text with backing symbol
        dd.datapoint(x=7, y=1, symbol='P', diameter=7, color='#000',
                       backing={'symbol':'(square-o)', 'diameter':12, 'color':'#000'})
        dd.datapoint(x=8, y=1, symbol='G', diameter=8, color='#000',
                       backing={'symbol':'(circle)', 'diameter':15, 'color':'#bff'})
        dd.datapoint(x=9, y=1, symbol='B', diameter=8, color='#000',
                       backing={'symbol':'(diamond)', 'diameter':15, 'color':'#fbb'})
        dd.datapoint(x=10, y=1, symbol='(circle)', diameter=10, color='#77b',
                       backing={'symbol':'(circle-o)', 'diameter':14, 'color':'#000'})
    
        # png images
        dd.datapoint(x=10, y=1, symbol='(img)/static/img/cherries.png', diameter=15)
        dd.datapoint(x=11, y=1, symbol='(img)/static/img/pretzel.png', diameter=17)
        dd.datapoint(x=12, y=1, symbol='(img)/static/img/checkmark.png', diameter=13)
    
        return dd.svgresult()



    def image_annot1(self):
        """ annotating a jpg image with arbitrary vector drawing """
        dd = self.dd
        dd.svgbegin(width=550, height=400)
        dd.setspace('X', svgrange=(50,530), datarange=(0,100))
        dd.setspace('y', svgrange=(50,380), datarange=(0,100))
        dd.plotbacking(image="static/img/examp_ctscan_img.jpg")
        dd.setline(width=0.5, color='#88c')
        dd.axis('X', grid=True, stubs=False)
        dd.axis('Y', grid=True, stubs=False)
        dd.setline(width=2, color='#33f')
        dd.rectangle(75, 25, width=18, height=20, color='#aaf',
                         opacity=0.2, outline=True, rounded=True)
        dd.settext(ptsize=12, color='#99f')
        dd.label(78, 5, 'AF27955-02')
        return dd.svgresult()





if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')
    for key in svgset:
        print(f'  {key}.svg ...')
        write_svgfile(svgset[key], f'{key}.svg')   
    print('Done.')
