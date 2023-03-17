""" First set of some simple examples.        http://datadraw.org
    Usage:    python examples1.py .... creates some svg files in cwd
    Or invoked as part of the flask web app.
    Prerequisites: 
     a python3.6+ virtual environment; pip -r requirements.txt
"""

from datadraw import DataDraw, write_svgfile

from sampledata.webhits_3weeks import webhits_3weeks


def run_all():
    """ run examples and return the result svg objects in a dict """
    ex = Examples1()
    svgset = {}
    svgset['hello_world']  = ex.hello_world()
    svgset['bargraph1']    = ex.bargraph1()
    svgset['curves1']      = ex.curves1()
    svgset['scatterplot1'] = ex.scatterplot1()
    svgset['webhits1']     = ex.webhits1()
    svgset['heatmap1']     = ex.heatmap1()
    svgset['pie1']         = ex.pie1()
    return svgset



class Examples1:

    def __init__(self):
        self.dd = DataDraw()



    def hello_world(self):
        """ invoke the built-in test pattern """
        dd = self.dd
        dd.svgbegin(500, 200, testpat=True)
        return dd.svgresult()



    def bargraph1(self):
        mydata = [('Group A', 38.4, 11.8), ('Group B', 67.4, 8.5), ('Group C', 49.2, 6.2)]
        dd = self.dd
        dd.svgbegin(width=300, height=220)
        dd.settext(ptsize=11, color='#777')
        dd.setline(color='#aaa', save=True)

        # set up a plotting space with fixed X and Y ranges and draw axes...
        dd.setspace('X', svgrange=(60,290), categorical=['Group A', 'Group B', 'Group C'])
        dd.setspace('Y', svgrange=(60,190), datarange=(0,100))
        dd.axis('X')
        dd.axis('Y', grid=True)
        dd.plotlabels(ylabel='Score', ylabelpos=-30)

        # draw the column bars and error bars...
        for tuple in mydata:
            dd.bar(x=tuple[0], y=tuple[1], color='#8a8', width=18)
            dd.errorbar(x=tuple[0], y=tuple[1], erramt=tuple[2])

        return dd.svgresult()



    def curves1(self):
        mydata = [[(0, 33, 8.4), (3, 35, 11.1), (6, 30, 5.8), (12, 34, 9.7), (24, 27, 11.3)],
                  [(0, 49, 10.3), (3, 44, 13.9), (6, 67, 7.3), (12, 58, 13.8), (24, 75, 11.2) ]]
        names  = ['Treated', 'Control']
        colors = ['#8d8', '#88d']
        dd = self.dd
        dd.svgbegin(width=550, height=300)
        dd.settext(ptsize=11, color='#777')
        dd.setline(color='#aaa', save=True)

        # set up a plotting space with fixed X and Y ranges and draw axes...
        dd.setspace('X', svgrange=(100,530), datarange=(0,26))
        dd.setspace('Y', svgrange=(60,280), datarange=(0,100))
        xstubs = [0, 3, 6, 12, 24]   # irregularly spaced X stubs so supply as list
        dd.axis('X', stublist=xstubs)
        dd.axis('Y', grid=True, axisline=None, loc='left-20')
        dd.plotlabels(xlabel='Months after treatment', xlabelpos=-40,
                    ylabel='O<sub>2</sub> exchange ratio %', ylabelpos=-60)

        # draw the two curves, error bars and data points w/ tooltips
        for group in [0, 1]:
            points = mydata[group]
            dd.setline(color=colors[group], width=3, )
            dd.legenditem(label=names[group], sample='line')  # register current color
            dd.curvebegin()
            for tuple in points:
                dd.curvenext(x=tuple[0], y=tuple[1]) 
            dd.setline(restore=True)  # restore to most recent 'save'
            for tuple in points:
                dd.errorbar(x=tuple[0], y=tuple[1], erramt=tuple[2])  
            for tuple in points:
                dd.gtag('begin', tooltip=f'{tuple[0]} mos, ratio = {tuple[1]} %')
                dd.datapoint(x=tuple[0], y=tuple[1], color='#fff', 
                                symbol='(vcircle-o)', diameter=12, opacity=1.0)
                dd.gtag('end')

        dd.legendrender(location='top', format='across')
        return dd.svgresult()



    def scatterplot1(self):
        mydata = [('Jean', 77, 85), ('Bill', 93, 88), ('Sarah', 78, 81), ('Ken', 62, 73),
                  ('Gladys', 78, 86), ('Frank', 54, 62), ('Dianne', 90, 72)]
        dd = self.dd
        dd.svgbegin(width=300, height=300)
        dd.setline(color='#aaa')
        dd.settext(color='#888')

        # set up X and Y space with fixed dataranges and render axes...
        dd.setspace('X', svgrange=(80,280), datarange=(40,100))
        dd.setspace('Y', svgrange=(80,280), datarange=(40,100))
        dd.axis('X', tics=8, loc='min-8', axisline=None)
        dd.axis('Y', tics=8, loc='min-8', axisline=None)
        dd.plotbacking(color='#fff', outline=True)
        dd.plotlabels(title='Scores', ylabel='Exam 1', xlabel='Exam 2', ylabelpos=-35)
        
        for tuple in mydata:
            dd.gtag('begin', tooltip=f'{tuple[0]} scored {tuple[1]} and {tuple[2]}')
            dd.datapoint(x=tuple[2], y=tuple[1], symbol='(vcircle-o)', 
                          color='#a44', diameter=15, opacity=0.4)
            dd.gtag('end', tooltip=tuple[0])

        return dd.svgresult()



    def webhits1(self):
        """ In a 3 week datetime X space display web hit data.  For datetime formats see:
            https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-behavior
        """
        dd = self.dd
        dd.svgbegin(width=620, height=150)
        dd.setline(color='#aaa')
        dd.settext(color='#888')
        dd.setdt('%Y-%m-%d %H:%M:%S.%f', weekday0=6)   # beginning of week = Sunday (6)

        # dynamically find datetime min and max and use it to set up X space..
        for timestamp in webhits_3weeks:
            dd.findrange(dd.intdt(timestamp))
        xrange = dd.findrange_result(nearest='day') 
        dd.setspace('X', svgrange=(20,600), datarange=xrange)

        dd.setspace('Y', svgrange=(60,140), datarange=(0,10)) # datarange is arbitrary

        # create 2 lists of datetime stubs... 1) weekday and day; 2) month 'year
        daystubs = dd.datestubs(xrange, inc='day', dtformat='%a\n%d', terse=True)
        dd.axis('X', stublist=daystubs, tics=-5)
        crossings = dd.datestubs(xrange, inc='month', crossings=True, dtformat="%b'%y")
        dd.axis('X', stublist=crossings, loc=f'bottom-32', axisline=None, stubanchor='start')
        
        # histogram of occurrances using upward clustering technique..
        dd.setclustering(mode='upward', tolerance=2, offset=0.2)   
        for timestamp in sorted(webhits_3weeks):
            dd.datapoint(x=dd.intdt(timestamp), y=0.1, symbol='(vrect)', diameter=4, color='#7a7')

        return dd.svgresult()


    def heatmap1(self):
        """ display a 10 x 10 heatmap of magnitude values """
        mydata = [ [ 0, 0, 1, 3, 0, 0, 4, 3, 8, 10  ],
                   [ 0, 1, 0, 0, 0, 4, 3, 8, 7, 3   ],
                   [ 1, 0, 0, 0, 4, 3, 12, 7, 3, 0  ],
                   [ 0, 0, 0, 2, 3, 9, 11, 3, 1, 0  ],
                   [ 0, 3, 0, 4, 7, 5, 2, 0, 1, 0   ],
                   [ 0, 0, 4, 3, 12, 16, 3, 0, 1, 0 ],
                   [ 0, 3, 7, 11, 14, 3, 2, 0, 0, 0 ],
                   [ 2, 4, 10, 7, 3, 0, 0, 0, 2, 0  ],
                   [ 7, 9, 6, 2, 0, 2, 0, 1, 0, 0   ],
                   [ 10, 8, 3, 4, 0, 0, 2, 4, 0, 0 ] ]

        def cellcolor(val):
            if val == 0:   return '#000'
            elif val == 1: return '#303'
            elif val == 2: return '#606'
            elif val <= 4: return '#909'
            elif val <= 8: return '#b0b'
            elif val < 12: return '#d0d'
            return '#f0f'

        dd = self.dd
        dd.svgbegin(width=400, height=380)
        textstyle = 'font-family: sans-serif; font-weight: bold;'  # css style
        dd.settext(color='#777', ptsize=12, style=textstyle)
        dd.setline(color='#777')

        # set up X and Y space with fixed ranges, and draw axes..
        dd.setspace('X', svgrange=(100,350), datarange=(0,10))
        dd.setspace('Y', svgrange=(100,350), datarange=(0,10))
        dd.axis('X', tics=8, loc='min-8')
        dd.axis('Y', tics=8, loc='min-8')
        dd.plotbacking(color='#eee', outline=True) 
        dd.plotlabels(ylabel='&#916; density  g/cm<sup>2</sup>', ylabelpos=-40,
                      xlabel='&#916; weight  g', xlabelpos=-45)   # 916 = &Delta;

        # render heatmap as a matrix of colored rectangles...
        for iy in reversed(range(10)):   # top to bottom
            for ix in range(10):
                val = mydata[ix][iy]
                if val == None: 
                    continue
                dd.gtag('begin', tooltip=f'({ix},{iy}) magnitude is {val}')
                dd.rectangle(cx=ix+0.5, cy=iy+0.5, width=1.0, height=1.0, color=cellcolor(val))
                dd.gtag('end')

        return dd.svgresult()


    
    def pie1(self):
        mydata = [ 0.33, 0.25, 0.2, 0.15, 0.07 ]
        dd = self.dd
        dd.svgbegin(width=500, height=300)
        textstyle = 'font-family: sans-serif; font-weight: bold;'  # css style
        dd.settext(color='#333', style=textstyle)
    
        # set up X space and Y space for centering of pie...
        dd.setspace('X', svgrange=(50,400))
        dd.setspace('Y', svgrange=(50,280))
    
        dd.setline(color='#aaa', width=0.5);
        dd.plotbacking(outline=True, rounded=True)
    
        colors = [ '#f00', '#0f0', '#aaf', '#0ff', '#ff0', '#f0f' ]
        labels = [ 'Delaware', 'Vermont', 'Alabama', 'Utah', 'Arkansas' ]
    
        # render pie slices, with a legend and tooltip for each...
        dd.setline( color='#fff', width=4 )   # outline the slices w/ a fat white line
        accum = 0.4;     # rotate entire pie 0.4 radians for pleasing appearance
        islice = 0
        for val in mydata:
            dd.gtag('begin', tooltip=labels[islice])
            dd.pieslice(pctval=val, startval=accum, color=colors[islice],
                 outline=True, showpct=True, opacity=0.5 )
            dd.gtag('end')
            dd.legenditem(sample='square', label=labels[islice], color=colors[islice])
            accum += val
            islice += 1
    
        # render the legend
        dd.settext( color='#888' )
        dd.legendrender(title='Incidence by U.S. state')

        return dd.svgresult()


if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')
    for key in svgset:
        print(f'  {key}.svg ...')
        write_svgfile(svgset[key], f'{key}.svg')   
    print('Done.')
