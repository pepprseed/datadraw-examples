""" Examples set 2.                http://datadraw.org
    Usage:    python examples2.py .... creates some svg files in cwd
    Or invoked as part of the flask web app.
    Prerequisites: 
     a python3.6+ virtual environment; pip -r requirements.txt
"""

from datadraw import DataDraw, write_svgfile


def run_all():
    """ run examples and return the result svg objects in a dict """
    ex = Examples2()
    svgset = {}
    svgset['bars_v']           = ex.barmodes()
    svgset['bars_v_clustered'] = ex.barmodes(mmode='clustered')
    svgset['bars_v_stacked']   = ex.barmodes(mmode='stacked')
    svgset['bars_h']           = ex.barmodes(horiz=True)
    svgset['bars_h_clustered'] = ex.barmodes(horiz=True, mmode='clustered')
    svgset['bars_h_stacked']   = ex.barmodes(horiz=True, mmode='stacked')

    svgset['curves']           = ex.curvemodes()
    svgset['curves_errbands']  = ex.curvemodes(mode='errbands')
    svgset['curves_fillauc']   = ex.curvemodes(mode='fillauc')

    svgset['scatterplot']      = ex.scatterplot()

    return svgset


class Examples2:

    def __init__(self):
        self.dd = DataDraw()


    def barmodes(self, horiz=False, mmode='single'):
        """ bar graph demo of modes and orientations.  Vertical bars or horizontal.
            mmode is either 'single', 'clustered' or stacked'.  Errorbars are included.
        """
        dd = self.dd
        mydata = [ { 'name':'Group A', 'value':38.4, 'sem':11.8, 'val2':11, 'sem2':4.5 },
                   { 'name':'Group B', 'value':67.4, 'sem':8.5,  'val2':19, 'sem2':7.1 },
                   { 'name':'Group C', 'value':49.2, 'sem':14.3, 'val2':16, 'sem2':7.8 } ]
        if not horiz:  # vertical bars...
            dd.svgbegin(width=250, height=200)
            cat_ax = 'X'; num_ax = 'Y'; csrot = 40
        else:          # horizontal bars...
            dd.svgbegin(width=200, height=250)
            cat_ax = 'Y'; num_ax = 'X'; csrot = 0

        # get a unique list of the categories for the X axis
        cats = dd.catinfo(mydata, 'name')

        dd.settext(ptsize=10, color='#444')
        dd.setline(color='#ccc')

        # set up our categorical axis space located from x=100 to x=400 in the svg
        dd.setspace(cat_ax, svgrange=(60,230), categorical=cats)

        # set up our numeric axis space ocated from y=100 to y=300 in the svg
        dd.setspace(num_ax, svgrange=(60,190), datarange=(0,100))

        # render the axes...
        dd.axis(cat_ax, tics=-8, stubrotate=csrot)
        dd.axis(num_ax, axisline=False, grid=True)

        # render the column bars (clustered or stacked) and error bars....
        dd.setline(color='#777')
        sh = 10 if mmode == 'clustered' else 0
        rnd = True if mmode == 'clustered' else False
        for row in mydata:
            dd.bar(horiz=horiz, x=row['name'], y=row['value'], color='#8a8', width=18, shift=-sh)
            dd.errorbar(horiz=horiz, x=row['name'], y=row['value'], erramt=row['sem'], shift=-sh)
            if mmode != 'single':
                yb   = row['value'] if mmode == 'stacked' else 0
                yval = row['value']+row['val2'] if mmode == 'stacked' else row['val2']
                dd.bar(horiz=horiz, x=row['name'], ybase=yb, y=yval, color='#88a', width=18, shift=sh)
                dd.errorbar(horiz=horiz, x=row['name'], y=yval, erramt=row['sem2'], shift=sh)

        # add a dashed "Goal" line 
        dd.setline(color='#33a', dash='5,2')
        if not horiz:
            dd.plotlabels(ylabel='Score')
            dd.line(x1='min', y1=60.0, x2='max', y2=60.0)
        else:
            dd.plotlabels(xlabel='Score')
            dd.line(y1='min', x1=60.0, y2='max', x2=60.0)

        return dd.svgresult()



    def curvemodes(self, mode='curves'):
        """ curves plot with error bars; irregular X axis stubs; data point tooltips
            mode: curves .. curves only
                  errbands ... show shaded +/- SEM bands also
                  fillauc .... fill the entire Area Under Curve
        """
        # assign some data column names...
        cols=['time','G1','G1sem','G2','G2sem','G3','G3sem']

        # data set with some missing data points (appear as a gap)...
        mydata = [[  0, 33, 2.4, 49, 4.3, 75, 5.8 ],
                  [  3, 35, 3.1, 44, 3.9, 70, 6.1 ],
                  [  6, 30, 2.8, 62, 8.6, 67, 4.0 ],
                  [ 12, 34, 3.7, 58, 3.8, 66, 3.9 ],
                  [ 24, 27, 11.3, 75, 6.2, 63, 8.2 ]]

        dd = self.dd
        dd.svgbegin(width=300, height=250)
        textstyle = 'font-family: sans-serif; font-weight: bold;'  # css
        dd.settext(color='#777', style=textstyle)
        dd.setline(color='#aaa')

        # set up plotting space with fixed ranges, and draw axes...
        dd.setspace('X', svgrange=(50,290), datarange=(0,26))
        dd.setspace('Y', svgrange=(50,240), datarange=(0,100))
        xstubs = [0, 3, 6, 12, 24]   # irregularly spaced
        dd.axis('X', axisline=False, stublist=xstubs, tics=-5)
        dd.axis('Y', axisline=False, grid=True, loc='left-20')
        dd.plotlabels(xlabel='Months of follow-up')

        # render the curves
        for group in ['G1', 'G2', 'G3']:
            # get array index positions for the columns we're working with....
            xcol = cols.index('time')
            ycol = cols.index(group)
            semcol = cols.index(group + 'sem')

            # color...
            if group == 'G1': linecolor = '#8d8'; fillcolor='#cfc'
            elif group == 'G2': linecolor = '#88d'; fillcolor='#ccf'
            elif group == 'G3': linecolor = '#d88'; fillcolor='#fcc'

            if mode in ['errbands', 'fillauc']:
                dd.curvebegin(fill=fillcolor, fillopacity=0.3)
                for row in mydata:
                    try:
                        if mode == 'errbands':
                            yval  = row[ycol]+row[semcol]
                            y2val = row[ycol]-row[semcol] 
                        elif mode == 'fillauc':
                            yval  = row[ycol]
                            y2val = 0.1  # constant
                    except:
                        yval = y2val = None    # render as a gap
                    dd.curvenext(x=row[xcol], y=yval, y2=y2val)

            # set line color, register a legend entry, then draw a curve...
            dd.setline(color=linecolor, width=4)
            if mode == 'fillauc':
                dd.legenditem(label=group, sample='square', color=linecolor)
            else:
                dd.legenditem(label=group, sample='line', ewidth=40)
            dd.setline(width=4)
            dd.curvebegin()
            for row in mydata:
                dd.curvenext(x=row[xcol], y=row[ycol])

        legformat = 'across' if mode != 'fillauc' else 'parkinglot'
        dd.legendrender(location='top', format=legformat)
        return dd.svgresult()



    def scatterplot(self):
        """ a more elaborate scatterplot example """
        dataset1 = [ (-6.3, -5.2), (0.4, 1.8), (8.1, 8.7), (-3.7, -5.1), (8.6, 8.2), (-7.5, -8.3),
             (-8.0, -9.2), (-9.8, -9.1), (-6.7, -5.5), (7.6, 6.9), (-3.0, -2.3), (-4.8, -5.4),
             (-1.1, -0.8), (6.4, 5.7), (-5.2, -5.7), (9.7, 9.9), (5.9, 4.9), (-1.1, -2.5), (-8.3, -8.5),
             (5.8, 5.5), (9.1, 7.6), (-3.8, -3.8), (-7.0, -6.1), (-1.9, -2.7), (-5.9, -6.1), (0.3, -0.1),
             (-3.4, -4.7), (8.9, 8.9), (1.0, 2.1), (-3.5, -4.7), (4.0, 1.6), (2.9, 8.3), (-0.2, 5.6),
             (2.4, -4.1), (1.4, -7.0), (1.6, 7.6), (-1.0, -9.0), (8.8, 0.7), (-5.1, 5.4), (5.7, -4.5) ]
        dataset2 = [ (4.9, 4.2), (-4.9, -3.8), (8.6, 8.7), (0.9, 1.1), (-7.8, -7.9), (-0.1, 0.0),
             (8.6, 8.0), (-3.4, -3.1), (-3.8, -4.5), (6.7, 8.1), (-3.4, -3.0), (8.4, 8.4), (-4.3, -5.1),
             (2.8, 3.4), (5.4, 5.3), (4.0, 4.9), (8.3, 9.6), (7.7, 6.9), (1.7, 2.2), (-6.8, -6.0),
             (6.4, 5.8), (4.4, 3.8), (2.8, 4.3), (-2.0, -0.8), (-5.4, -5.7), (-0.2, 1.2), (-3.3, -2.2),
             (5.7, 5.5), (2.2, 1.9), (-0.2, 0.9), (7.7, -8.1), (-7.6, -8.0), (8.3, 3.7), (-9.9, -0.3),
             (7.2, 6.0), (-8.6, -3.6), (1.4, 1.8), (-5.5, 8.6), (1.1, -2.0), (7.8, -2.3) ]

        dd = self.dd
        dd.svgbegin(width=400, height=400)

        textstyle = 'font-family: sans-serif; font-weight: bold;'
        dd.settext( color='#777', style=textstyle )
        dd.setline( color='#777' )

        # dynamically find the data range in X, then Y, set up spaces, draw axes...
        for tuple in dataset1 + dataset2:
            dd.findrange(tuple[0])
        xrange = dd.findrange_result()
        for tuple in dataset1 + dataset2:
            dd.findrange(tuple[1])
        yrange = dd.findrange_result()
        dd.setspace('X', svgrange=(60,350), datarange=xrange)
        dd.setspace('Y', svgrange=(60,350), datarange=yrange)
        dd.axis('X', tics=8, loc='min-8', axisline=None)
        dd.axis('Y', tics=8, loc='min-8', axisline=None)
        dd.plotbacking(color='#fff', outline=True)

        # do crosshairs at 0, 0
        dd.setline(color='#888', dash='3,3')
        dd.line(x1='min', y1=0.0, x2='max', y2=0.0)
        dd.line(x1=0.0, y1='min', x2=0.0, y2='max')

        # render dataset1 in red data points; dataset2 in blue...
        for tuple in dataset1:
            dd.datapoint(x=tuple[0], y=tuple[1], color='#d88', diameter=10, opacity=0.6)
        for tuple in dataset2:
            dd.datapoint(x=tuple[0], y=tuple[1], color='#88d', diameter=10, opacity=0.6)

        # also a few green using datapoints with text on symbol backing...
        for loc in [(6,-6), (-1,-4), (-8,-2)]:
            dd.datapoint(x=loc[0], y=loc[1], symbol='AE', diameter=7, color='#333',
                      backing={'symbol':'(vcircle)', 'color':'#8d8', 'diameter':14})

        # create a legend... each entry width to 80...
        dd.legenditem(label='Group A', sample='symbol', color='#d88', opacity=0.6,
                        diameter=10, ewidth=80)
        dd.legenditem(label='Group B', sample='symbol', color='#88d', opacity=0.6,
                        diameter=10, ewidth=80)
        dd.legenditem(label='Adverse event',
                        sample='symbol', symbol='AE', diameter=7, color='#333',
                        backing={'symbol':'(vcircle)', 'color':'#8d8', 'diameter':14})
        dd.settext(ptsize=10)
        dd.legendrender(location='top', format='across', adjust=(-15,30))

        return dd.svgresult()



if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')
    for key in svgset:
        print(f'  {key}.svg ...')
        write_svgfile(svgset[key], f'{key}.svg')   
    print('Done.')
