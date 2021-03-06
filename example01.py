import grates as gt
import matplotlib.pyplot as plt
from ftplib import FTP
import cartopy as ctp
import urllib.request


# Download a GRACE L2 Solution from TU Graz FTP server
ftp_url = 'ftp.tugraz.at'
data_directory = 'outgoing/ITSG/GRACE/ITSG-Grace2018/monthly/monthly_n96'
file_name = 'ITSG-Grace2018_n96_2008-05.gfc'

with FTP(ftp_url) as ftp:
    ftp.login()
    ftp.cwd(data_directory)
    with open(f'{file_name}', 'wb') as fp:
        ftp.retrbinary(f'RETR {file_name}', fp.write)

# import the downloaded file and a static field as PotentialCoefficients instance
monthly_l2_field = gt.io.loadgfc('ITSG-Grace2018_n96_2008-05.gfc')
static_field = gt.io.loadgfc('data/GOCO06s_aodReduced_static_2010-01-01.gfc')

monthly_l2_field -= static_field  # reduce the static field to reveal the time-variable signal 
monthly_l2_field.truncate(96)  # truncate the reduced field to the original maximum spherical harmonic degree

shc_filter = gt.filter.Gaussian(350)  # Create a Gaussian filter object with 300 km filter radius
monthly_l2_filtered = shc_filter.filter(monthly_l2_field)  # apply the filter to the L2 solution 

mass_change_grid = monthly_l2_filtered.to_grid(kernel='ewh')  # propagate the potential coefficients to gridded equivalent water height

# visualize the grid with cartopy
f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})
im = ax.imshow(mass_change_grid.value_array * 100, cmap='RdBu', vmin=-25, vmax=25, transform=ctp.crs.PlateCarree())
ax.coastlines()
gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
plt.savefig('l2_solution.png', bbox_inches='tight', transparent=True, dpi=300)

# Download the GSFC GRACE/GRACE-FO mascons from their website
urllib.request.urlretrieve('https://earth.gsfc.nasa.gov/sites/default/files/2022-05/gsfc.glb_.200204_202112_rl06v2.0_obp-ice6gd.h5', 'gsfc.glb_.200204_202112_rl06v2.0_obp-ice6gd.h5')

# create a mascon TimeSeries object from the data file
gfsc_time_series = gt.io.loadgsfc06mascons('gsfc.glb_.200204_202112_rl06v2.0_obp-ice6gd.h5')
gsfc_grid = gfsc_time_series[0]

# visualize the mascon solution as colored surface tiles
f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})
ax.set_global()
gsfc_grid.values *= 100
im = gt.plot.surface_tiles(gsfc_grid, vmin=-25, vmax=25, cmap='RdBu')
ax.coastlines()
gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
plt.savefig('mascon_solution.png', bbox_inches='tight', transparent=True, dpi=300)
