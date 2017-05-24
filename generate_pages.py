import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.colors as colors

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', serif='New Century Schoolbook')

def getMonths(ra, dec):
    from astropy import units as u
    from astropy.time import Time
    from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun, FK5
    from datetime import datetime
    fk5 = SkyCoord(ra, dec, frame='fk5')
    # fk5c = SkyCoord(ra, dec, frame='fk5')
    # print fk5c
     # same as SkyCoord.from_name('M33'): use the explicit coordinates to allow building doc plots w/o internet
    kpno = EarthLocation.of_site('kpno')
    utcoffset = -7*u.hour  # Mountain Standard Time

    delta_midnight = np.linspace(-5, 5,11)*u.hour

    months = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
    days = np.array([7, 14, 21, 28])
    monthDict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    monthBool = []
    for m in months:
        upMonth = [False, False, False, False]
        for j,day in enumerate(days):
            t = datetime(2017, m, day, 00, 00, 00)
            midnight = Time(t) - utcoffset
            times = midnight + delta_midnight
            # print times
            altazframe = AltAz(obstime=times, location=kpno)
            # sunaltazs = get_sun(times).transform_to(altazframe)
            fk5altazs = fk5.transform_to(altazframe)
            am = fk5altazs.secz
            # print am
            up = np.where((am < 1.5) & (am > 1.0))
            # print len(up[0])
            if len(up[0]) >= 3:
                upMonth[j] = True
        # print upMonth
        if any(upMonth):
            monthBool.append(True)
        else:
            monthBool.append(False)
    monthBool = np.array(monthBool)
    obsmonths = months[monthBool]
    return obsmonths


# d = np.array([0.25, 1.0, 2.0])

name, altname, hi_coords, cz, w50, size, m_hi, a40, other_obs, wiyn_obs, inst, mis, stacked, proc = np.loadtxt('predblist.sort.csv', usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13), dtype=str, delimiter=',', unpack=True)

# get the months the targets are visible
# parse the hi coords into sensible ra and dec strings
mon = []
ra = []
dec = []
seas = []
for i,c in enumerate(hi_coords):
    raStr = c[:8]
    decStr = c[8:]
    r = raStr[:2]+'h'+raStr[2:4]+'m'+raStr[4:]+'s'
    d = decStr[:3]+'d'+decStr[3:5]+'m'+decStr[5:]+'s'
    ra.append(r)
    dec.append(d)
    # print altname[i], ra, dec
    mnth = getMonths(r, d)
    # print mnth
    mon.append(mnth)
    if 9 in mnth or 10 in mnth:
        season = 'Fall'
        seas.append(season)
    elif 3 in mnth or 4 in mnth:
        season = 'Spring'
        seas.append(season)
ra = np.array(ra)
dec = np.array(dec)

sint = {"HVC70.08-46.35-104":1.03,
"HVC97.40-29.92+74":1.74,
"HVC107.25-35.87+49":0.87,
"HVC122.87-47.69+51":1.33,
"HVC128.50-50.26+81":0.96,
"HVC128.40-37.57+83":0.96,
"HVC145.98-43.69+43":1.93,
"HVC141.38-31.05+46":3.58,
"HVC75.1-29.53+48":4.34,
"HVC81.63-51.52+46":7.95,
"HVC99.70-31.72+68":1.14,
"HVC138.78-56.41+53":4.81,
"HVC141.80-30.91+26":1.23}
abar = np.zeros_like(size, dtype=float)
compact = np.where(abar<10)

for i,m in enumerate(m_hi):
    if m == '':
        m_hi[i] = repr(np.log10(sint[name[i]]*236000.0))
    # print  altname[i], hi_coords[i]

for i,s in enumerate(size):
    ab = s.split('x')
    if len(ab) == 1:
        abar[i] = np.sqrt(float(ab[0])*float(ab[0]))
        # print name[i], abar[i]
    else:
        abar[i] =  np.sqrt(float(ab[0])*float(ab[1]))
        # print name[i], abar[i]

s21 = np.power(10,m_hi.astype(float))/236000.0
m_hi = m_hi.astype(float)
# print len(m_hi)
# m_hi_range = 2.0*np.log10(d)
cz = cz.astype(float)
misb = mis=='mis'
mis = np.where(misb)
w50 = w50.astype(float)
n_hi = np.log10(4.4e20*s21/(abar*abar))
m_dyn = np.log10(6.2e3*abar*w50*w50)

odisample = [i for i, n in enumerate(name) if (n_hi[i]>=19 or abar[i] <= 7.5 or misb[i] or '201' in wiyn_obs[i])]
odineed = [i for i, n in enumerate(name) if ((n_hi[i]>=19 or abar[i] <= 7.5 or misb[i]) and not '201' in wiyn_obs[i])]
leftovers = [i for i, n in enumerate(name) if not (n_hi[i]>=19 or abar[i] <= 7.5 or misb[i] or '201' in wiyn_obs[i])]
print len(odisample), len(leftovers), len(odineed)

month = np.array(mon)[odineed]
obs = wiyn_obs[odineed]
ra_new = ra[odineed]
dec_new = dec[odineed]
nhi_new = n_hi[odineed]
abar_new = abar[odineed]
mhi_new = m_hi[odineed]
with open('need_these.list', 'w+') as f:
    for i,n in enumerate(altname[odineed]):
        if 9 in month[i] or 10 in month[i]:
            season = 'Fall'
        elif 3 in month[i] or 4 in month[i]:
            season = 'Spring'

        print >> f, '{0:9s} {1:6s} {2:s} {3:s} {4:6.3f} {5:5.2f} {6:6.2f} {7:s}'.format(n, season, ra_new[i], dec_new[i], nhi_new[i], mhi_new[i], abar_new[i], obs[i])

with open('props.csv', 'w+') as f:
    for i,n in enumerate(altname):
        if 'Sep' in mon[i] or 'Oct' in mon[i]:
            season = 'Fall'
            seas.append(season)
        elif 'Mar' in mon[i] or 'Apr' in mon[i]:
            season = 'Spring'
            seas.append(season)

        print >> f, '{0:9s}, {1:6s}, {2:s}, {3:s}, {4:6.3f}, {5:5.2f}, {6:6.2f}, {7:s}'.format(n, season, ra[i], dec[i], n_hi[i], m_hi[i], abar[i], wiyn_obs[i])    

n_mhi, bins_mhi = np.histogram(m_hi, bins=16, range=[4.8,6.4])
n_mdyn, bins_mdyn = np.histogram(m_dyn, bins=16, range=[6.5,8.5])
n_cz, bins_cz = np.histogram(cz, bins=13)
n_nhi, bins_nhi = np.histogram(n_hi, bins=13, range=[18.3,19.6])
n_abar, bins_abar = np.histogram(abar, bins=13)
n_w50, bins_w50 = np.histogram(w50, bins=13)

cmap=colors.ListedColormap(['black','gold','red'])
# cmap.set_under('black')
colors = np.empty_like(name, dtype=int)
have = [i for i,obs in enumerate(wiyn_obs) if ('201' in obs)]
ps = [i for i,obs in enumerate(wiyn_obs) if ('poor' in obs)]

colors[:] = 0
colors[have] = 2
colors[ps] = 1

# Two subplots sharing both x/y axes
f, (ax1) = plt.subplots(nrows=1, ncols=1,  sharex='col', sharey='row')

# make a line for compact/most compact
nhi_x = np.linspace(18.3, 19.6)
mhi_mc = 2.0*np.log10(6.0)+nhi_x-15.74+0.614
mhi_c = 2.0*np.log10(10.0)+nhi_x-15.74+0.46
# print nhi_x, mhi_mc, mhi_c

# ax1.hlines(bins_mhi,bins_nhi[0],bins_nhi[-1], linestyles='dotted')
ax1.vlines([19.0,19.2],4.5,6.5, linestyles=['-.','--'])
# ax1.arrow(18.4,6.4,0.0,m_hi_range[0], lw=1, color='black')
# ax1.arrow(19.4,4.8,0.0,m_hi_range[2], lw=1, color='black')
pts = ax1.scatter(n_hi,m_hi, s=abar, c=colors, cmap=cmap, edgecolors='none', label='UCHVCs (size $\propto \\bar{a}$)')
samp = ax1.scatter(n_hi[odisample],m_hi[odisample], s=30, lw=0.5, c='none', edgecolors='black', label='ODI sample')
leop = ax1.scatter([19.5], [np.log10(8.1e5)], s=50, marker="*", facecolor='limegreen', edgecolors='none', label='Leo P')
leot = ax1.scatter([19.59],[np.log10(2.8e5)], marker='>', s=50, facecolor='limegreen', edgecolors='none', label='Leo T')
ax1.plot(nhi_x, mhi_mc, c='black', linestyle='--')
ax1.text(nhi_x[3], mhi_mc[6], "$\\bar{a} \simeq 6'$", fontsize=10, rotation=33)
ax1.plot(nhi_x, mhi_c, c='black', linestyle='-.')
ax1.text(nhi_x[1], mhi_c[4]+0.01, "$\\bar{a} \simeq 10'$", fontsize=10, rotation=33)
red = patches.Patch(color='red', label='observed, good')
gold = patches.Patch(color='gold', label='observed, poor seeing')
black = patches.Patch(color='black', label='not yet observed')


ax1.set_ylim(4.8,6.4)
ax1.set_xlim(18.3, 19.6)
ax1.set_xlabel('log $\\bar{N}_{HI}$')
ax1.set_ylabel('log $M_{HI}$')
ax1.legend(handles=[pts, samp, red, gold, black, leop, leot], loc=2, fontsize='x-small', scatterpoints=1)

plt.savefig('uchvc-db/props.png')

# make a front page with a list of all the objects
with open('uchvc-db.md', 'w+') as f:
    print >> f, "---"
    print >> f, "layout: page"
    print >> f, "title: uchvc-db"
    print >> f, "--- "
    # print >> f, "![props](props.png)"
    print >> f, '<table>'
    print >> f, "<tr><td>Name</td><td>Season</td><td>Observed</td><td>Inst</td><td>Stacked</td><td>Processed</td><td>RA</td><td>Dec</td><td>cz</td><td>abar</td><td>log MHI</td><td>log NHI</td></tr>"
    # print >> f, "|---:|------|---|---|"
    for i in range(len(name)):
        if '201' in wiyn_obs[i]:
            print >> f, '<tr class="yesobs"><td><a href="/uchvc-db/'+altname[i].lower()+'">'+altname[i]+'</a></td><td>'+seas[i]+'</td><td>'+wiyn_obs[i]+'</td><td>'+inst[i]+'</td><td>'+stacked[i]+'</td><td>'+proc[i]+'</td><td>'+ra[i]+'</td><td>'+dec[i]+'</td><td>'+'{0:5.0f}'.format(cz[i])+'</td><td>'+'{0:5.2f}'.format(abar[i])+'</td><td>'+'{0:5.2f}'.format(m_hi[i])+'</td><td>'+'{0:6.2f}'.format(n_hi[i])+'</td></tr>'
        elif wiyn_obs[i]=='no':
            print >> f, '<tr class="notobs"><td><a href="/uchvc-db/'+altname[i].lower()+'">'+altname[i]+'</a></td><td>'+seas[i]+'</td><td>'+wiyn_obs[i]+'</td><td>'+inst[i]+'</td><td>'+stacked[i]+'</td><td>'+proc[i]+'</td><td>'+ra[i]+'</td><td>'+dec[i]+'</td><td>'+'{0:5.0f}'.format(cz[i])+'</td><td>'+'{0:5.2f}'.format(abar[i])+'</td><td>'+'{0:5.2f}'.format(m_hi[i])+'</td><td>'+'{0:6.2f}'.format(n_hi[i])+'</td></tr>'
        elif wiyn_obs[i]=='planned':
            print >> f, '<tr class="planobs"><td><a href="/uchvc-db/'+altname[i].lower()+'">'+altname[i]+'</a></td><td>'+seas[i]+'</td><td>'+wiyn_obs[i]+'</td><td>'+inst[i]+'</td><td>'+stacked[i]+'</td><td>'+proc[i]+'</td><td>'+ra[i]+'</td><td>'+dec[i]+'</td><td>'+'{0:5.0f}'.format(cz[i])+'</td><td>'+'{0:5.2f}'.format(abar[i])+'</td><td>'+'{0:5.2f}'.format(m_hi[i])+'</td><td>'+'{0:6.2f}'.format(n_hi[i])+'</td></tr>'
        elif 'poor' in wiyn_obs[i]:
            print >> f, '<tr class="poorobs"><td><a href="/uchvc-db/'+altname[i].lower()+'">'+altname[i]+'</a></td><td>'+seas[i]+'</td><td>'+wiyn_obs[i]+'</td><td>'+inst[i]+'</td><td>'+stacked[i]+'</td><td>'+proc[i]+'</td><td>'+ra[i]+'</td><td>'+dec[i]+'</td><td>'+'{0:5.0f}'.format(cz[i])+'</td><td>'+'{0:5.2f}'.format(abar[i])+'</td><td>'+'{0:5.2f}'.format(m_hi[i])+'</td><td>'+'{0:6.2f}'.format(n_hi[i])+'</td></tr>' 
        with open('uchvc-db/'+altname[i].lower()+'.md','w+') as md:
            print >> md, "---"
            print >> md, "layout: page"
            print >> md, "title: ", altname[i]
            print >> md, "--- "
            print >> md, "|alt id|"+name[i]+'|'
            print >> md, "|ra|"+ra [i]+'|'
            print >> md, "|dec|"+dec[i]+'|'
            print >> md, "|cz|"+repr(cz[i])+'|'
            print >> md, "|w50|"+repr(w50[i])+'|'
            print >> md, "|abar|"+repr(abar[i])+'|'
            print >> md, "|m_hi|"+repr(m_hi[i])+'|'
            print >> md, "|n_hi|"+repr(n_hi[i])+'|'
            # print >> md, "|months observable|"+mon[i]+'|'
    print >> f, "</table>"   

# print n_mhi
# print n_cz
# print n_w50
# print len(cz[have]),len(cz[taken]),len(cz[ps]),len(cz[have])+len(cz[taken])+len(cz[ps])
