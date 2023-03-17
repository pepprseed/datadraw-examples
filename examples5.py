""" Examples set 5.                      http://datadraw.org
    Usage:    python examples5.py .... creates some svg files in cwd
    Or invoked as part of the flask web app.
    Prerequisites: 
     a python3.6+ virtual environment; pip -r requirements.txt
"""

from datadraw import DataDraw,  write_svgfile
from sampledata.for_distribs import data1, data2, data3, data4
from sampledata.variants import variants1


def run_all():
    ex = Examples5()
    svgset = {}
    svgset['distribs1'] = ex.distribs1(ylog=True)
    svgset['survival1'] = ex.survival1()
    svgset['freqbins'] = ex.freqbins()
    svgset['freqcats'] = ex.freqcats()
    return svgset


class Examples5():

    def __init__(self):
        self.dd = DataDraw()



    def distribs1(self, ylog=False):
        """ distributions with boxplots and beeswarms """
        plotdata = {'1f':data1, '2f':data2, '1m':data3, '2m':data4}
    
        dd = self.dd
        dd.svgbegin(width=550, height=350)
        # textstyle = 'font-family: sans-serif; font-weight: bold;'
        dd.settext(color='#777')
        dd.setline(color='#aaa')
    
        # set up categorical X space..
        dd.setspace('X', svgrange=(100,500), categorical=['1f', '2f', '1m', '2m'])
    
        # find data range in Y (examine all 4 datasets) and set Y space
        for key in plotdata:
            for val in plotdata[key]:
                dd.findrange(val)
        yrange = dd.findrange_result()
        yrange['axmax'] += 50   # tweak to give more room at high end
        dd.setspace('Y', svgrange=(60,340), datarange=yrange, log=ylog)
    
        # render Y axis and plotting area
        if ylog:
            dd.axis('Y', tics=8, loc='min-8', grid=True, inc=50, stubcull=12) 
        else:
            dd.axis('Y', axisline=False, loc='min-8' )
        dd.plotlabels(ylabel='glucose [mg/dL]')
    
        # compute percentiles and other summary info for each 1-D array (column=None)
        info = {}
        for key in plotdata:
            info[key] = dd.numinfo(datarows=plotdata[key], column=None, find_percentiles=True)
            # print(f'For {key} the numinfo is:  {info[key]}\n')
    
        # render beeswarms using left+right clustering .. -8 nat units L of center
        dd.setclustering(mode='left+right', offset=2.0, tolerance=1.0)
        for key in plotdata:
            for val in plotdata[key]:
                color = '#88c' if key in ['1f', '2f'] else '#db8'
                pctiles = info[key]['percentiles']
                if val < pctiles['p5'] or val > pctiles['p95']:
                    dd.gtag('begin', tooltip=f'Outlier: {val}  ID: ____' )
                dd.datapoint(x=key, y=val, diameter=6, color=color, adjust=(-8,0))
                dd.gtag('end')
        dd.setclustering(mode=None)
    
        # render box+whisker plots, and 'N = nnn' ... 8 nat units R of center
        dd.setline(color='#777')
        dd.settext(ptsize=8, color='#777', anchor='middle')
        for key in plotdata:
            color = '#ddf' if key in ['1f', '2f'] else '#fed'
            dd.boxplot(info[key], x=key, color=color, shift=8, n_at_y=2)
    
        return  dd.svgresult()



    def survival1(self):
        """ KM survival curves. 
            In the dataset each tuple is (weeks, %alive control, %alive treated) 
            One missing data point at control 80 wks.
        """
        dataset = [ (0, 100, 100), (15, 100,  99), (30,  91, 95), (40, 84, 91), (50, 80, 89), 
                    (60, 77, 88),  (70, 72, 85), (80, None, 83), (90, 68, 82), (100, 62, 78), 
                    (110, 55, 75), (120, 48, 72), (130, 41, 68), (140, 36, 64)]
        censor_events = [(30, 0), (40, 1), (40, 1), (70, 0), (90, 0), (90, 0), (90,0), 
                         (110, 1), (130, 0), (130, 0)]
        dd = self.dd
        dd.svgbegin(width=550, height=300)
        dd.settext(ptsize=11, color='#777')
        dd.setline(color='#aaa')
        # set up plotting space (fixed X and Y ranges)...
        dd.setspace('X', svgrange=(70,500), datarange=(0,150))
        dd.setspace('Y', svgrange=(80,280), datarange=(0,115))
        dd.axis('X')
        dd.axis('Y', inc=20)
        dd.plotlabels(title='Drug administered: Cisplatin 2mg/kg',
                      xlabel='Weeks after treatment', xlabelpos=-35, 
                      ylabel='Survival %', ylabelpos=-40)
        for studygroup in [1,2]:
            label = 'Control' if studygroup == 1 else 'Treated'
            color = '#008' if studygroup == 1 else '#800'
            dd.setline(color=color)
            dd.legenditem(label=label, sample='line')
            dd.curvebegin(stairs=True, onbadval='gap')
            for tuple in dataset:
                dd.curvenext(x=tuple[0], y=tuple[studygroup])
            dd.curvenext(x=tuple[0]+5, y=tuple[studygroup])  # short segment at end

        dd.legenditem(label='Censor event', sample='circle', color='#aaa')
        dd.setclustering(mode='downward', offset=1.5)
        for event in censor_events:
            color = '#008' if event[1] == 0 else '#800'
            dd.datapoint(x=event[0], y=110, color=color, diameter=6)
            
        dd.settext(ptsize=10)
        dd.legendrender(location='bottom', adjust=(0,35))
        return dd.svgresult()



    def freqbins(self):
        """ compute numeric bins frequency distribution; display histogram """
        dd = self.dd
    
        # get an example array of numbers
        plotdata = data3
    
        dd.svgbegin( width=500, height=200 )
        dd.settext(color='#777')
        dd.setline(color='#aaa')
    
        # find numeric bins frequency distribution....
        info = dd.numinfo(plotdata, column=None, find_distrib=True, binsize='inc/4')
        bins = info['distribution']
    
        # find the data min and max for X axis....
        for val in plotdata:
            dd.findrange(val)
        xrange = dd.findrange_result()
        dd.setspace('X', svgrange=(80,450), datarange=xrange )
    
        # find the histogram min and max for Y axis...
        for row in bins:
            dd.findrange(row['accum'])
        yrange = dd.findrange_result()
        dd.setspace('Y', svgrange=(80,180), datarange=yrange )
    
        # render X and Y axes
        dd.axis('X')
        dd.axis('Y', loc='left-5', inc=yrange['axmax'])  # just 0 and 25
    
        # render histogram
        for bin in bins:
            dd.bar(x=bin['binmid'], y=bin['accum'], width=8, color='pink')
    
        dd.plotlabels(xlabel=f"glucose mg/dL   (bin size = {info['distbinsize']:g})", 
                      ylabel='N instances')
    
        return dd.svgresult()
    


    def freqcats(self):
        """ compute categorical frequency distribution; display histogram.
            input is chromosome occurrences (1 - 22, X, Y, MT)
        """
        dd = self.dd

        dd.svgbegin(width=600, height=200 )
        dd.settext(color='#777')
        dd.setline(color='#aaa')

        # parse out chromosome and score
        vdata = []
        for row in variants1:
            chr = row[2].split(':')[0].replace('chr','')
            try:
                if int(chr) < 10:
                    chr = f'0{chr}'          # to get proper sort order
            except:
                chr = 'mt' if chr == 'MT' else chr  # proper sort order
            vdata.append((chr, row[3]))

        # find categorical freq distribution...
        cats = dd.catinfo(vdata, column=0)  # , accumcol=1)

        # sort cats dict on keys and use result for categorical X space
        tmp1 = sorted(cats.items())
        cats = dict(tmp1)
        dd.setspace('X', svgrange=(80,550), categorical=cats)

        # find min, max for Y axis and histogram bars..
        for key in cats:
            dd.findrange(cats[key])
        yrange = dd.findrange_result()
        yrange['axmin'] = 0
        dd.setspace('Y', svgrange=(80,180), datarange=yrange )

        # render X and Y axes
        dd.axis('X')
        dd.axis('Y', loc='left-5', inc=yrange['axmax'])
        dd.plotlabels(xlabel='Chromosome', ylabel='N instances')

        # render histogram
        for key in cats:
            dd.bar(x=key, y=cats[key], width=12, color='#db8')

        return dd.svgresult()


if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')
    for key in svgset:
        print(f'  {key}.svg ...')
        write_svgfile(svgset[key], f'{key}.svg')
    print('Done.')

