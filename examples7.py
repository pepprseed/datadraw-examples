""" Examples set 7.                      http://datadraw.org
    Usage:    python examples7.py .... creates some svg files in cwd
    Or invoked as part of the flask web app.
    Prerequisites: 
     a python3.6+ virtual environment; pip -r requirements.txt
"""

from datadraw import DataDraw, write_svgfile

from sampledata.wind_12hours import wind_12hours


def run_all():
    ex = Examples7()
    svgset = {}
    svgset['secchi1'] = ex.secchi1()
    svgset['windbarbs1'] = ex.windbarbs1()
    return svgset


class Examples7():

    def __init__(self):
        self.dd = DataDraw()


    def secchi1(self):
        """ Secchi lake depth transparency readings plot with reversed Y axis """
        depthdata = [
          ('09/21/2016', 6.60), ('09/19/2016', 6.20), ('09/08/2016', 4.85), ('09/01/2016', 6.00),
          ('08/18/2016', 7.00), ('08/09/2016', 7.60), ('08/03/2016', 7.10), ('07/28/2016', 7.25),
          ('07/22/2016', 8.10), ('07/14/2016', 8.65), ('07/08/2016', 9.95), ('06/29/2016', 9.60),
          ('06/22/2016', 9.40), ('06/16/2016', 8.60), ('06/9/2016',  8.40), ('06/02/2016', 8.30),
          ('05/26/2016', 8.40), ('05/19/2016', 7.85), ('05/11/2016', 7.95), ('05/05/2016', 7.70),
          ('04/28/2016', 7.85), ('04/19/2016', 7.15), ('03/30/2016', 7.20)   ]

        dd = self.dd
        dd.svgbegin(width=800, height=220)
        dd.setdt('%m/%d/%Y')
        dd.settext(color='#777', style='font-family: sans-serif; font-weight: bold;')
        dd.setline(color='#777')
    
        # find date range for X...
        for tuple in depthdata:
            dd.findrange(dd.intdt(tuple[0]))
        xrange = dd.findrange_result(nearest='month')
        dd.setspace('X', svgrange=(60,750), datarange=xrange)

        # find Y max and set up reversed Y space (0 at top)
        for tuple in depthdata:
            dd.findrange(tuple[1])
        yrange = dd.findrange_result()
        yrange['axmin'] = 0    # tweak yrange to fix min at 0 and add margin on max
        yrange['axmax'] += 3
        # datarange = (0, yrange['axmax']+3)  # fix a zero min; add +3 margin on max
        dd.setspace('Y', svgrange=(60,180), datarange=yrange, reverse=True)

        monthstubs = dd.datestubs(xrange, inc='month', dtformat='%b') 
        yearstubs = dd.datestubs(xrange, inc='year', crossings=True, dtformat='%Y')
        dd.axis('X', stublist=monthstubs)
        dd.axis('X', stublist=yearstubs, loc='bottom-18', axisline=False) # show year(s)
        dd.setline(color='#777', width=0.5, dash='4,6')
        dd.axis('Y', tics=8, grid=True)
        dd.setline(color='#777', dash=None)
        dd.plotlabels(title='Secchi lake depth transparency readings',
                        ylabel='Depth (m)', ylabelpos=-30)
        dd.setline(width=1.0)
        dd.plotbacking(outline=True)
    
        # render the blue depth lines...
        dd.setline(color='#99f', width=1)
        for tuple in depthdata:
             xloc = dd.intdt(tuple[0])
             dd.line(x1=xloc, y1=0.0, x2=xloc, y2=tuple[1])
             dd.gtag('begin', tooltip=f'{tuple[0]} reading of {tuple[1]} m')
             dd.datapoint(x=xloc, y=tuple[1], diameter=8, color='#99f')
             dd.gtag('end')
    
        return dd.svgresult()
    


    def windbarbs1(self):
        """ full example - meteorology wind barbs display, 12 hours """
        dd = self.dd

        dd.svgbegin(width=800, height=500)

        dataset = wind_12hours
        # name the 4 columns..
        timestamp = 0
        elevation = 1
        speed     = 2
        direction = 3

        # see https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        dd.setdt('%Y-%m-%d %H:%M:%S')

        # find date/time range and set up X space..
        for row in dataset:
            dd.findrange( dd.intdt(row[timestamp]) )
        xrange = dd.findrange_result(nearest='hour')
        dd.setspace('X', svgrange=(100,750), datarange=xrange)

        # find Y range...
        for row in dataset:
            dd.findrange(row[elevation])
        yrange = dd.findrange_result()
        dd.setspace('Y', svgrange=(100,480), datarange=yrange)

        dd.setline(color='#777');
        dd.settext(color='#555', style='font-family: sans-serif; font-weight: bold;')
        dd.plotlabels(title='Wind speed indicated by size of barb tip.',
                    xlabel='Measurements\ntaken on 7 May 2022', xlabelpos=-60,
                    ylabel='Air Elevation Level (m)')
        # dd.plotbacking(outline=True)

        # render axes...
        stubs = dd.datestubs(xrange, inc='3hour', dtformat='%l%P')
        dd.axis('X', stublist=stubs, tics=8, loc='bottom-20')
        dd.axis('Y', tics=8, loc='left-20')

        # render windbarbs and data points
        dd.setline(color='#83a')
        for row in dataset:
            xloc = dd.intdt(row[timestamp])     # convert 'timestamp' to utime int
            dd.arrow(x1=xloc, y1=row[elevation], direction=row[direction], magnitude=40, tiptype='barb', headlen=row[speed])
            dd.datapoint(xloc, row[elevation], diameter=5, color='#888')

        return dd.svgresult()



if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')
    for key in svgset:
        print(f'  {key}.svg ...')
        write_svgfile(svgset[key], f'{key}.svg')
    print('Done.')

