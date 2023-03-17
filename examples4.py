""" Examples set 4.                      http://datadraw.org
    Usage:    python examples4.py .... creates some svg files in cwd
    Or invoked as part of the flask web app.
    Prerequisites: 
     a python3.6+ virtual environment; pip -r requirements.txt
"""

from datadraw import DataDraw, write_svgfile
from sampledata.wind_12hours import wind_12hours
from sampledata.wind_3days import wind_3days
from sampledata.incidents_12years import incidents_12years
from sampledata.webhits_3weeks import webhits_3weeks


def run_all():
    ex = Examples4()
    svgset = {}
    svgset['axisdemo']     = ex.axisdemo()
    svgset['axis_3days']   = ex.axis_3days()
    svgset['axis_2days']   = ex.axis_2days()
    svgset['axis_12years'] = ex.axis_12years()
    svgset['axis_3years']  = ex.axis_3years(mode='showyears')
    svgset['axis_3years_fy']  = ex.axis_3years(mode='showfy')
    svgset['axis_3weeks']  = ex.axis_3weeks(mode='weekdays')
    svgset['axis_3weeks_mon']  = ex.axis_3weeks(mode='monthdays')
    svgset['axis_3weeks_webhits'] = ex.axis_3weeks(mode='webhits')
    svgset['axis_48hours']   = ex.axis_48hours(mode='full')
    svgset['axis_48hours_partial'] = ex.axis_48hours(mode='partial')
    svgset['webhits']      = ex.axis_3weeks(mode='webhits')
    return svgset


class Examples4:

    def __init__(self):
        self.dd = DataDraw()


    def axisdemo(self):
        """ several plotting areas, w/ various numeric, categorical axis options """
        dd = self.dd
        dd.svgbegin(width=800, height=600)
        dd.settext(color='#777', save=True)

        # left column ... X categorical space...
        cats = ['Ohio', 'Kansas', 'Michigan', 'Oklahoma', 'Mississippi', 'New Mexico',
                'Wisconsin', 'South Dakota', 'New Hampshire', 'Georgia']
        dd.setspace('X', svgrange=(50,350), categorical=cats)      # stays in effect for all

        dd.setspace('Y', svgrange=(500,550), datarange=(0,10))
        dd.axis('X', tics=-8, stubrotate=40)
        dd.axis('Y', tics=-10, inc=5)
        dd.settext(color='#77a')
        dd.plotlabels(title='Categorical X (stubs rotated 40)')
        dd.settext(restore=True)

        dd.setspace('Y', svgrange=(300,350), datarange=(0,10))
        dd.axis('X', tics=5, stubrotate=-45)
        dd.axis('Y', inc=5)
        dd.axis('Y', loc='right', inc=5)
        dd.settext(color='#77a')
        dd.plotlabels(title='Y axis on left and right.\nCategorical X (stubs rotated -45)')
        dd.settext(restore=True)

        dd.setspace('Y', svgrange=(60,180), datarange=(0,410), log=True)
        dd.setline(width=0.5, dash='4,1')
        dd.axis('Y', tics=8, grid=True, inc=10, stubcull=12)
        dd.settext(color='#77a')
        dd.plotlabels(title='Y log space with stubcull')
        dd.setline(restore=True)
        dd.settext(restore=True)
        dd.plotbacking(outline=True)

        ### right column ... X numeric space....
        dd.setspace('X', svgrange=(450,750), datarange=(0,10000))  # stays in effect for all
        catlist=['Group A', 'Group B', 'Group C']

        dd.setspace('Y', svgrange=(500,550), categorical=catlist)
        dd.axis('X', tics=-4, comma000=True )
        dd.axis('Y', tics=5)
        dd.settext(color='#77a')
        dd.plotlabels(title='Categorical Y, numeric X (stubs with commas)')
        dd.settext(restore=True)

        dd.setspace('Y', svgrange=(300,350), categorical=catlist)
        dd.axis('X', loc='top', tics=4, stubrange=(2000,8000), comma000=True, stubrotate=-55)
        dd.axis('Y', stubrotate=20)
        dd.settext(color='#77a', anchor='middle', adjust=(10,-30))
        dd.plotlabels(title='Y stubs rotated 20.\nNumeric X axis at top w/ limited stubrange')
        dd.settext(restore=True)

        return dd.svgresult()


    """ datetime axis examples begin here """

    def axis_3days(self):
        """ axis demo: 3 days with date shown on midnight crossing """
        dd = self.dd
    
        dd.svgbegin(width=620, height=80)
        dd.setdt('%Y-%m-%d %H:%M:%S')

        for row in wind_3days:
            dd.findrange(dd.intdt(row[0]))

        xrange = dd.findrange_result(nearest='6hour')  
        dd.setspace('X', svgrange=(20,600), datarange=xrange)
        dd.setspace('Y', svgrange=(60,80), datarange=(0,10)) # arbitrary

        # do 1st X axis scale on 6hour intervals
        hourstubs = dd.datestubs(xrange, inc='6hour', dtformat='%H:%M', terse=True)
        dd.axis('X', stublist=hourstubs, tics=-5)

        # 2nd X axis scale to show date at day boundary / midnite crossings
        daystubs = dd.datestubs(xrange, inc='day', crossings=True, dtformat='%b %d')
        dd.axis('X', stublist=daystubs, loc='bottom-20', axisline=None)

        return dd.svgresult()


    def axis_2days(self):
        """ axis demo: 8 hours with date shown on midnight crossing """
        dd = self.dd
    
        dd.svgbegin(width=620, height=80)
        dd.setdt( '%Y-%m-%d %H:%M:%S' )

        istart = dd.intdt('2022-11-17 20:00:00')  # select data from this range
        istop  = dd.intdt('2022-11-18 05:00:00')

        for row in wind_3days:
            idt = dd.intdt(row[0])
            if idt >= istart and idt <= istop:
                dd.findrange(idt)      # use inrange data only

        xrange = dd.findrange_result(nearest='hour')
                                       
        dd.setspace('X', svgrange=(20,600), datarange=xrange)
        dd.setspace('Y', svgrange=(60,80), datarange=(0,10)) # arbitrary

        # do 1st X axis scale on hours..
        hourstubs = dd.datestubs(xrange, inc='hour', dtformat='%H:%M', terse=True)
        dd.axis('X', stublist=hourstubs, tics=-5)

        # 2nd X axis scale to show date at day boundary / midnite crossings
        daystubs = dd.datestubs(xrange, inc='day', crossings=True, dtformat='%b %d')
        dd.axis('X', stublist=daystubs, loc='bottom-20', axisline=None)

        return dd.svgresult()


    def axis_12years(self):
        """ axis demo: 12+ years with year-boundary crossing labelled """
        dd = self.dd
    
        dd.svgbegin(width=620, height=150)
        dd.setdt('%Y-%m-%d')

        for date in incidents_12years:
            dd.findrange(dd.intdt(date))

        xrange = dd.findrange_result(nearest='year')
        dd.setspace('X', svgrange=(20,600), datarange=xrange)
        dd.setspace('Y', svgrange=(60,140), datarange=(0,10)) # arbitrary

        # X axis scale using years..
        yearstubs = dd.datestubs(xrange, inc='year', dtformat='%Y')
        dd.axis('X', stublist=yearstubs, tics=-8)

        # do a 2nd x axis scale to get tic marks every 3 months... 
        minortics = dd.datestubs(xrange, inc='3month', dtformat='')
        dd.axis('X', stublist=minortics, tics=-5, axisline=None)  

        # quick histogram of occurrances using upward-clustered data points
        # adjust offset to bring max in range; tolerance adjusts 'bin size'
        dd.setclustering(mode='upward', tolerance=2, offset=0.5)  
        for date in sorted(incidents_12years):
            dd.datapoint(x=dd.intdt(date), y=0.1, symbol='(vrect)', 
                         diameter=4, color='#77a')

        return dd.svgresult()


    def axis_3years(self, mode):
        """ axis demo: 3+ years with months labeled.  mode is either 
           'showyears' to show year crossings, or 'showfy' to show fiscal year crossings.
        """
        dd = self.dd
    
        dd.svgbegin(width=620, height=80)
        dd.setdt('%Y-%m-%d', fymonth1=7)  # set fiscal year starting July

        for date in incidents_12years:
            if date[:3] == '202' or date[:7] == '2019-12':    # use only late 2019 onward
                dd.findrange(dd.intdt(date))

        xrange = dd.findrange_result(nearest='3month') 
        dd.setspace('X', svgrange=(20,600), datarange=xrange)
        dd.setspace('Y', svgrange=(60,100), datarange=(0,10)) # arbitrary

        monthstubs = dd.datestubs(xrange, inc='month', dtformat='%b', terse=True)
        dd.settext(ptsize=8)
        dd.axis('X', stublist=monthstubs, tics=-5)
        dd.settext(restore=True)

        quarters = dd.datestubs(xrange, inc='3month', crossings=True, dtformat='')  # show tics only
        dd.axis('X', stublist=quarters, axisline=None, tics=10) 

        if mode == 'showyears':
            inc = 'year'
        elif mode == 'showfy':
            inc = 'fy'
            dd.setdt(fymonth1=7)   # set fiscal year starting July

        years = dd.datestubs(xrange, inc=inc, crossings=True, dtformat='%Y')  # format ignored for FY
        dd.axis('X', stublist=years, axisline=None, loc='bottom-20', 
                    stubcull=40, stubanchor='start') # stubcull avoids colliding; left-aligned

        return dd.svgresult()


    def axis_3weeks(self, mode):
        """ axis demo: 3 weeks.  mode is either 'weekdays', 'monthdays', or 'webhits'.
            'webhits' does both weekdays and monthdays and plots some data in green.
        """
        dd = self.dd
    
        ht = 150 if mode == 'webhits' else 80
        dd.svgbegin(width=620, height=ht)
        dd.setdt('%Y-%m-%d %H:%M:%S.%f', weekday0=6)   # (seconds component includes milliseconds)
                                                       # set beginning of week to Sunday (6)
        for timestamp in webhits_3weeks:
            dd.findrange(dd.intdt(timestamp))

        xrange = dd.findrange_result(nearest='day')    # or, nearest='week'
        dd.setspace('X', svgrange=(20,600), datarange=xrange)
        if mode == 'webhits':
            dd.setspace('Y', svgrange=(60,140), datarange=(0,10)) # arbitrary
        else:
            dd.setspace('Y', svgrange=(60,100), datarange=(0,10)) # arbitrary
        sanc = None
        x2drop = 20

        if mode == 'weekdays':
            # x stubs are weekdays, with MMdd on each week boundary 
            daystubs = dd.datestubs(xrange, inc='day', dtformat='%a', terse=True)
            crossings = dd.datestubs(xrange, inc='week', crossings=True, dtformat='%b%d')
        elif mode == 'monthdays':
            daystubs = dd.datestubs(xrange, inc='day', dtformat='%d', terse=True)
            crossings = dd.datestubs(xrange, inc='month', crossings=True, dtformat='%b')
            # sanc = 'start'  # stubs left-aligned
        elif mode in ['both', 'webhits']:
            daystubs = dd.datestubs(xrange, inc='day', dtformat='%a\n%d', terse=True)
            crossings = dd.datestubs(xrange, inc='month', crossings=True, dtformat="%b'%y")
            x2drop = 32
            sanc = 'start'  # stubs left-aligned

        # 2 X axis passes....
        dd.axis('X', stublist=daystubs, tics=-5)
        dd.axis('X', stublist=crossings, loc=f'bottom-{x2drop}', axisline=None, stubanchor=sanc)

        if mode == 'webhits':
            # quick histogram of occurrances using upward-clustered data points
            dd.setclustering(mode='upward', tolerance=2, offset=0.2) 
            for timestamp in sorted(webhits_3weeks):
                dd.datapoint(x=dd.intdt(timestamp), y=0.1, symbol='(vrect)', diameter=4, color='#7a7')

        return dd.svgresult()


    def axis_48hours(self, mode):
        """ axis demo: times.  mode is either 'full' or 'partial'   """
        dd = self.dd
    
        dd.svgbegin(width=620, height=80)
        dd.setdt('%Y-%m-%d %H:%M:%S.%f', weekday0=6)   # (seconds component includes milliseconds)
                                                       # set beginning of week to Sunday (6)
        for timestamp in webhits_3weeks:
            # use only a portion of the data (2 days, or a chunk of hours w/ midnite crossing)
            if (mode == 'full' and timestamp[:10] in ['2023-02-07', '2023-02-08']) or \
               (mode == 'partial' and timestamp[:12] in ['2023-02-07 1', '2023-02-08 0']):
                dd.findrange(dd.intdt(timestamp))

        xrange = dd.findrange_result(nearest='3hour')    
        dd.setspace('X', svgrange=(20,585), datarange=xrange)
        dd.setspace('Y', svgrange=(60,100), datarange=(0,10)) # arbitrary
        sanc = None

        if mode == 'full':
            inc = '6hour' 
            fmt = '%I%p'
        elif mode == 'partial':
            inc = '3hour'
            fmt = '%H:00'
            sanc = 'start'  # stubs left-aligned
        hourstubs = dd.datestubs(xrange, inc=inc, dtformat=fmt, terse=True)  
        crossings = dd.datestubs(xrange, inc='day', crossings=True, dtformat='%b%d')

        dd.axis('X', stublist=hourstubs, tics=-5)
        dd.axis('X', stublist=crossings, loc=f'bottom-20', axisline=None, stubanchor=sanc)
  
        return dd.svgresult()


if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')
    for key in svgset:
        print(f'  {key}.svg ...')
        write_svgfile(svgset[key], f'{key}.svg')
    print('Done.')

