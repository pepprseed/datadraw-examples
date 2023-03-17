""" Examples set 6.                      http://datadraw.org
    Usage:    python examples6.py .... creates some svg files in cwd
    Or invoked as part of the flask web app.
    Prerequisites: 
     a python3.6+ virtual environment; pip -r requirements.txt
"""

from datadraw import DataDraw,  write_svgfile
from sampledata.variants import variants1


def run_all():
    ex = Examples6()
    svgset = {}
    svgset['bizdays'] = ex.bizdays()
    svgset['chrview'] = ex.chrview()
    return svgset


class Examples6():

    def __init__(self):
        self.dd = DataDraw()


    def bizdays(self):
        """ Business/trading days display can't use ordinary linear datetime 
            space because each day runs from only from 9am - 4pm, and in the
            display e.g.  Monday's 4pm directly abutts to Tuesday's 9am.  
            Instead use this 'multipanel' technique:  First set up X space as 
            categorical, based on the dates found in data set (this keeps days 
            with no activity out of the display, eg. weekends and holidays).  
            Next, use catranges() to capture the category box coordinates.  
            Then iterate over the data.  For each distinct date
            encountered, set up a new X space inside the date's category box,
            scaled 9am - 4pm, and plot there.
              Y space is based on observed share price range across all days 
            and remains in effect thruout.
        """
        shareprice = [
          ('2023-01-12', '09:30:11', 42.29),
          ('2023-01-12', '11:29:27', 42.05),
          ('2023-01-12', '13:45:52', 42.20),
          ('2023-01-12', '14:17:32', 42.21),
          ('2023-01-12', '15:44:06', 42.08),
          ('2023-01-13', '09:30:03', 42.78),
          ('2023-01-13', '10:48:32', 42.92),
          ('2023-01-13', '12:15:48', 43.10),
          ('2023-01-13', '13:49:32', 42.84),
          ('2023-01-13', '13:52:21', 42.62),
          ('2023-01-13', '13:58:52', 42.37),
          ('2023-01-13', '14:01:37', 42.17),
          ('2023-01-13', '14:38:09', 42.20),
          ('2023-01-13', '14:52:34', 42.24),
          ('2023-01-13', '15:58:02', 42.11),
          ('2023-01-17', '09:30:29', 41.96),
          ('2023-01-17', '09:48:32', 41.72),
          ('2023-01-17', '11:15:48', 41.80),
          ('2023-01-17', '13:09:32', 41.61),
          ('2023-01-17', '13:52:21', 41.85),
          ('2023-01-17', '13:58:52', 41.75),
          ('2023-01-17', '15:01:37', 41.58),
          ('2023-01-17', '15:38:09', 41.70),
          ]
        dd = self.dd
        dd.svgbegin(width=650, height=240)
        dd.settext(color='#888')
        dd.setdt('%Y-%m-%d %H:%M:%S')

        # get unique list of days, and use it to set up categorical X space..
        days = dd.catinfo(shareprice, column=0)
        dd.setspace('X', svgrange=(80,640), categorical=days)

        # get share price data range and use it to set up numeric Y space..
        for row in shareprice:
            dd.findrange(row[2])            
        yrange = dd.findrange_result()
        dd.setspace('Y', svgrange=(60,190), datarange=yrange)

        # render categorical X axis and numeric Y axis for entire view
        dd.setline(width=0.5)
        dd.axis('X', grid=True, stubadjust=(0,-15), 
                     dateconvert=('%Y-%m-%d', '%a %b %d'))  # dateconvert use-case
        dd.axis('Y', stubcull=20, stubformat='%.2f', grid=True)
        dd.plotlabels(ylabel='Price', titlepos=+20,
          title='Business / trading days.\n'
                'Weekends and holidays (e.g. Mon Jan 16) are automatically omitted')

        # get category box ranges in native X units
        dayboxes = dd.catranges('X')

        # iterate thru data; plot within one category box at a time.
        # When the day changes, jump to next category box...
        curday = None
        dd.setline(color='#00b', width=1.5, save=True)
        for row in shareprice:
            if row[0] != curday:
                if curday:
                    dd.curvenext(x=dayclose, y=curprice)  # continue to end of day
                curday = row[0]

                # get one day's range and use it to set x space and make the time stubs
                dayopen  = dd.intdt(f'{curday} 09:00:00')
                dayclose = dd.intdt(f'{curday} 16:00:00')
                dd.findrange(dayopen)
                dd.findrange(dayclose)
                xrange = dd.findrange_result(nearest='hour')
                dd.setspace('X', svgrange=dayboxes[curday], datarange=xrange)
                times = dd.datestubs(xrange, dtformat='%I%p', inc='2hour', terse=True)
                dd.setline(color='#777', width=0.5, dash='2,5')
                dd.axis('X', stublist=times[:-1], grid=True)  # omit 5pm
                dd.setline(restore=True)

                # start the day's curve..
                dd.curvebegin(stairs=True)

            utime = dd.intdt(row[0] + ' ' + row[1])
            price = row[2]
            dd.curvenext(x=utime, y=price)
            dd.datapoint(x=utime, y=price, diameter=4)
            curprice = price
        dd.curvenext(x=dayclose, y=curprice)  # continue to end of last day

        return dd.svgresult()


    def chrview(self):
        """ Plotting chromosome basepair coordinates eg. 17:48274798 
            We can't use ordinary linear scaling for these values.  
            We can use a multipanel technique as above, but chromosome
            sizes aren't uniform so chr box coordinates are managed here 
            for best results.
        """
        human38_chr_len = { '1':248956422, '2':242193529, '3':198295559, '4':190214555,
            '5':181538259,  '6':170805979, '7':159345973, '8':145138636, '9':138394717,
            '10':133797422, '11':135086622, '12':133275309, '13':114364328, 
            '14':107043718, '15':101991189, '16':90338345,  '17':83257441,  
            '18':80373285,  '19':58617616,  '20':64444167,  '21':46709983 , 
            '22':50818468,  'X':156040895,  'Y':57227415,   'MT':200000 }

        dd = self.dd
        dd.svgbegin(width=920, height=200)
        dd.settext(color='#888')
        dd.setline(color='#aaa', width=0.5)

        # find Y min and max and set up Y space (remains in effect for all chr)
        for row in variants1:
            dd.findrange(row[3])
        yrange = dd.findrange_result()
        dd.setspace('Y', svgrange=(50,180), datarange=yrange)

        # find sum of all chr sizes and set up a preliminary X space
        sum = 0
        for key in human38_chr_len:
            sum += human38_chr_len[key]
        dd.setspace('X', svgrange=(50,890), datarange=(0,sum)) 
         
        dd.axis('Y')
        dd.plotlabels(xlabel='Human Chromosome', xlabelpos=-40,
                      ylabel='Score', ylabelpos=-30)
        # dd.axis('X', divideby=1000000)  # debug

        # find the native X coords of each chr box
        chrbox = {}
        accum = 0
        for key in human38_chr_len:
            boxleft = dd.nx(accum)
            accum += human38_chr_len[key]
            boxright = dd.nx(accum)
            chrbox[key] = (boxleft, boxright)

        # create a visible box for each chr...
        for key in human38_chr_len:
            dd.setspace('X', svgrange=chrbox[key], datarange=(0,1))  # placeholder
            dd.plotbacking(outline=True)
            if key not in ['21', 'MT']:        # chr label except where too crowded
                dd.plotlabels(xlabel=key, xlabelpos=-20)    
        dd.label(x='max', y=-12, text=' MT')      # slap this on at far right

        # now plot the variants by location and score... (sort not required)
        curchr = None
        for row in variants1:
            coord = row[2]
            chr, bp = coord.split(':')   # parse out chr, bp
            chr = chr.replace('chr','')
            if chr != curchr:
                chrsize = human38_chr_len[chr]
                margin = 500000  # a bit of margin between chr
                # set up an X space within the chr box, and plot therein...
                try:
                    dd.setspace('X', svgrange=chrbox[chr], datarange=(-margin,chrsize+margin))
                except KeyError:
                    print(f'variants1 has unrecognized chr: {chr} ... skipping')
                    continue
                curchr = chr
            try:
                dd.gtag('begin', tooltip=f'{row[0]} {row[1]}  {row[2]}  score={row[3]}')
                dd.datapoint(x=int(bp), y=row[3], diameter=6, color='#7d7')
                dd.gtag('end')
            except:
                print(f'failed to plot: {coord}')
            
        return dd.svgresult()



if __name__ == "__main__":
    svgset = run_all()
    print('writing svg to files...')
    for key in svgset:
        print(f'  {key}.svg ...')
        write_svgfile(svgset[key], f'{key}.svg')
    print('Done.')

