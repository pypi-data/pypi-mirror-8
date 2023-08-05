from numpy import *
from datetime import *
from matplotlib.dates import * # only for date2num?
from ncdfextract import ncgettypecode

# # should be the same as ncgettypecode
# def ncgetformat(fmt):    
#     if fmt == float64: #double
#         return 'd'
#     elif fmt == float32:
#         return 'f'
#     elif fmt == int:
#         return 'i'
#     elif fmt == long:
#         return 'l'
#     elif fmt == datetime:
#         return 'd' 
#     else:
#         print (' WARNING: format '+fmt+' could not be discovered! Assuming that it is double.')
#         return 'd'

def csv2netcdf(infile,outfile,sep=None,nalist = [''],formatlist=[],refdat = datetime(2000,1,1), \
        tunits = 'hours',readcolnames=True, customnames=[], timestep=None):
    '''
    purpose: convert a csv-file to a netcdf timeseries. 

    infile: reference to a filestream containing csv data (example: open('file.csv'))
    outfile: reference to a writable netcdf-file NetCDF.NetCDFFile('file.nc')
    nalist: list with characters that should be skipped. It will be assigned as nan
    formatlist: a list of pairs, in which one specifies the format for each csv-column. The first element
    of a pair is the data type, the second element is the data format (e.g. like '%Y/%m/%d for a date)?.
        Example: ((datetime,'%Y/%m/%d'),(double,nan))
                 (('daytime','dayssince'),(double,nan))
    tunits: the unit for the output 'time' coordinate (default: 'hours')
    refdat: reference date. (will be used to make the time dimension e.g. 'hours' since refdat)
    ''' 

    # todo: 
    tell = infile.tell()

    # we read the column names from the first line
    if readcolnames:
        lenout = len(infile.readlines()) - 1
        infile.seek(tell)
        colnames = infile.readline().replace('\n','').split(sep)

    # otherwise, we set dummy columnnames
    else:
        lenout = len(infile.readlines()) 
        infile.seek(tell)
        line = infile.readline().replace('\n','').split(sep)
        colnames = [nan]*len(line)
        infile.seek(tell)

    for icustomname,customname in enumerate(customnames):
        if icustomname >= len(colnames):
            colnames.append(customname)
        else:
            # we just keep the original colname if np.nan is specified
            if customname != nan:
                colnames[icustomname] = customname

    # we give dummy names for the variables that were not identified
    ivar = 0
    for icolname,colname in enumerate(colnames):
    #    print(colname)
        if type(colname) != str:
            while ('var'+str(ivar)) in colnames:
                ivar += 1
            colnames[icolname] = 'var'+str(ivar)
        
    #print(colnames)


    # # workaround ncview crash for underscores
    # for colname in colnames:
    #     colname.replace('_','')
    #formatlist.extend(repeat((nan,nan),len(colnames) - len(formatlist)))

    # add missing
    for i in range(len(colnames) - len(formatlist)):
        formatlist.append((double,nan))

    outfile.createDimension('time',lenout)
    outfile.createVariable('time','d',('time',))

    # a standard timestepping. This will be overriden
    outfile.variables['time'][:] = arange(lenout)

    # if (tunits not in nalist):
    setattr(outfile.variables['time'],\
            'units', \
            tunits +' since '+ datetime.strftime(refdat,'%Y-%m-%d %H:%M:%S'))

    excludeformattypes = (datetime,'daytime')

    for icn,ecnorig in enumerate(colnames):
        # print (icn,ecnorig)
        ecn = ''.join(e for e in ecnorig if e.isalnum())
        # if formatlist[icn][0].__name__ != 'datetime':
        if formatlist[icn][0] not in excludeformattypes:
            # print ('ecn',ecn)
            # print(icn,formatlist[icn])
            outfile.createVariable(ecn,ncgettypecode(formatlist[icn][0]),('time',))
    dt = refdat
    for iline,eline in enumerate(infile):
        currline = eline.replace('\n','').split(sep)
        colnum = min(len(currline),len(colnames))
        # print('currline',currline)
        for icn in range(colnum):
            ecn = ''.join(e for e in colnames[icn] if e.isalnum())
            # print('icn ecn',icn,ecn)
            # print('currline[icn]',currline[icn])
            if currline[icn] not in nalist:
                # if formatlist[icn][0] == datetime:
                #     outfile.variables[ecn][iline] = date2num(datetime.strptime(currline[icn],formatlist[icn][1]))
		if formatlist[icn][0] not in excludeformattypes:
                    # print (formatlist[icn][0], currline[icn], )
                    # print (formatlist[icn][0](currline[icn]))
                    try:
                        outfile.variables[ecn][iline] = formatlist[icn][0](currline[icn])
                    except:
                        outfile.variables[ecn][iline] = nan
            else:
                outfile.variables[ecn][iline] = nan

        lfirst = True

        uzformatlist = zip(*formatlist)
        # print(uzformatlist[1])
        # get date of string
        dtype = datetime
        if dtype in uzformatlist[0]:
            icn = uzformatlist[0].index(dtype)
            if currline[icn] not in nalist:
                dt = datetime.strptime(currline[icn],uzformatlist[1][icn])
                lfirst = False
        dtype = date
        if dtype in uzformatlist[0]:
            icn = uzformatlist[0].index(dtype)
            if currline[icn] not in nalist:
                dt = datetime.strptime(currline[icn],uzformatlist[1][icn])
                lfirst = False

        # tbi loop over every 'daytime' type and add them together
        dtype = 'timesince'
        if dtype in uzformatlist[0]:
            icn = uzformatlist[0].index(dtype)
            if currline[icn] not in nalist:
                currval = double(currline[icn])
                sec = 0.
                if uzformatlist[1][icn] == 'HMint':
                    sec = (int(currval/100.)*60. + (currval - int(currval/100.)*100.))*60.
                elif uzformatlist[1][icn] == 'days':
                    sec = currval*24.*60.*60.

                if lfirst:
                    # override automatic timestepping
                    dt = refdat + timedelta(seconds = sec)
                else:
                    dt = dt + timedelta(seconds = sec)


        # output to netcdf
        # outfile.variables['datetime'][iline] = date2num(dt)

        if tunits == 'hours':
            outfile.variables['time'][iline] = \
                    (dt-refdat).total_seconds()/3600.
            if timestep == None:
                dt = dt + timedelta(hours=1)
        if tunits == 'days':
            outfile.variables['time'][iline] = \
                    (dt-refdat).total_seconds()/3600./24.
            # automatic timestepping
            if timestep == None:
                dt = dt + timedelta(days=1)
        if tunits == 'seconds':
            outfile.variables['time'][iline] = \
                    (dt-refdat).total_seconds()
            # automatic timestepping
            if timestep == None:
                dt = dt + timedelta(seconds=1)
        if tunits == 'minutes':
            outfile.variables['time'][iline] = \
                    (dt-refdat).total_seconds()/60.
            # automatic timestepping
            if timestep == None:
                dt = dt + timedelta(minutes=1)
        if timestep != None:
            dt = dt + timestep

def ncwritedatetime(ncfile,dt,tunits = None, refdat = None):
    ''' purpose: write given time coordinate to ncdf file
    dt: array of datetimes
    tunits: time unit (can be either 'hour', 'days', 'minutes' or 'seconds')
    refdat: reference date from which the timesteps are represented
    '''

    if refdat == None: refdat = dt[0]
    if 'time' not in ncfile.dimensions:
        ncfile.createDimension('time',len(dt))
    if 'time' not in ncfile.variables:
        ncfile.createVariable('time','d',('time',))

    if tunits == None:
        try:
            if (dt[1] - dt[0]) == timedelta(years=1): tunits = 'years'
            elif (dt[1] - dt[0]) == timedelta(days=1): tunits = 'days'
            elif (dt[1] - dt[0]) == timedelta(hours=1): tunits = 'hours'
            elif (dt[1] - dt[0]) == timedelta(minutes=1): tunits = 'minutes'
            elif (dt[1] - dt[0]) == timedelta(hours=1): tunits = 'seconds'
            else: tunits = 'hours'
        except:
            tunits = 'hours'

    setattr(ncfile.variables['time'],\
            'units', \
             tunits +' since '+ datetime.strftime(refdat,'%Y-%m-%d %H:%M:%S'))

    for idt,edt in enumerate(dt):
        if tunits == 'hours':
            ncfile.variables['time'][idt] = \
                    (edt-refdat).total_seconds()/3600.
        if tunits == 'days':
            ncfile.variables['time'][idt] = \
                    (edt-refdat).total_seconds()/3600./24.
        if tunits == 'seconds':
            ncfile.variables['time'][idt] = \
                    (edt-refdat).total_seconds()
        if tunits == 'minutes':
            ncfile.variables['time'][idt] = \
                    (edt-refdat).total_seconds()/60.

