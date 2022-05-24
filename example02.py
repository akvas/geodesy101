import grates as gt
import matplotlib.pyplot as plt
from ftplib import FTP
import cartopy as ctp


ftp_url = 'ftp.tugraz.at'
data_directory = 'outgoing/ITSG/GRACE/ITSG-Grace2018/monthly/monthly_n96'
file_name = 'ITSG-Grace2018_n96_2008-05.gfc'

with FTP(ftp_url) as ftp:
    ftp.login()
    ftp.cwd(data_directory)
    with open(f'{file_name}', 'wb') as fp:
        ftp.retrbinary(f'RETR {file_name}', fp.write)

monthly_l2_field = gt.io.loadgfc('ITSG-Grace2018_n96_2008-05.gfc')
static_field = gt.io.loadgfc('data/GOCO06s_aodReduced_static_2010-01-01.gfc')

monthly_l2_field -= static_field
monthly_l2_field.truncate(96)

mass_change_grid = monthly_l2_field.to_grid(kernel='ewh')

f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})
im = ax.imshow(mass_change_grid.value_array * 100, cmap='RdBu', vmin=-25, vmax=25, transform=ctp.crs.PlateCarree())
ax.coastlines()
gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
plt.savefig('l2_solution_unfiltered.png', bbox_inches='tight', transparent=True, dpi=300)


shc_filters = {'Gauss_300km': gt.filter.Gaussian(300), 'DDK3': gt.filter.DDK(3)}

for filter_name, shc_filter in shc_filters.items():
    filtered_coefficients = shc_filter.filter(monthly_l2_field)

    mass_change_grid = filtered_coefficients.to_grid(kernel='ewh')

    f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})
    im = ax.imshow(mass_change_grid.value_array * 100, cmap='RdBu', vmin=-25, vmax=25, transform=ctp.crs.PlateCarree())
    ax.coastlines()
    gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
    plt.savefig(f'l2_solution_{filter_name}.png', bbox_inches='tight', transparent=True, dpi=300)
