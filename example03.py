import grates as gt 
import numpy as np
import cartopy as ctp 
import matplotlib.pyplot as plt


# import the potential field data (this assumes you have run example01 or example02 before)
monthly_coeffs = gt.io.loadgfc('ITSG-Grace2018_n96_2008-05.gfc')
static_coeffs = gt.io.loadgfc('data/GOCO06s_aodReduced_static_2010-01-01.gfc')

# reduce the static compoment to reveal time variations
monthly_coeffs -= static_coeffs
monthly_coeffs.truncate(96)

# filter the GRACE solution with a reasonable filter
shc_filter = gt.filter.DDK(3)
coeffs_filtered = shc_filter.filter(monthly_coeffs)

# visualize the filtered grid
grid = coeffs_filtered.to_grid()
f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})

im = ax.imshow(grid.value_array * 100, cmap='RdBu', vmin=-25, vmax=25, transform=ctp.crs.PlateCarree())
ax.coastlines()
gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
plt.savefig('grid_grace_filtered.png', bbox_inches='tight', transparent=True, dpi=600)

# Load the model data. Our goal is to reduce hydrological signal on the continents using a model.
# The model has a vastly higher resolution than the GRACE data. 
model_coeffs = gt.io.loadgfc('data/model_hydrology_2008-05.gfc')

# visualize the hydrological model
shc_filter = gt.filter.Gaussian(100)
grid = shc_filter.filter(model_coeffs).to_grid()
f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})

im = ax.imshow(grid.value_array * 100, cmap='RdBu', vmin=-25, vmax=25, transform=ctp.crs.PlateCarree())
ax.coastlines()
gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
plt.savefig('grid_model.png', bbox_inches='tight', transparent=True, dpi=600)

# Form and visualize the difference between the GRACE water storage estimate and the model values.
# Due to the difference in spatial resolution, there will be a lot of small-scale featerus visible,
# which are not visible in the original GRACE solution. 
grid = (coeffs_filtered - shc_filter.filter(model_coeffs)).to_grid()

f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})

im = ax.imshow(grid.value_array * 100, cmap='RdBu', vmin=-25, vmax=25, transform=ctp.crs.PlateCarree())
ax.coastlines()
gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
plt.savefig('grid_diff.png', bbox_inches='tight', transparent=True, dpi=600)

# But: if we filter the model values with the same filter as the GRACE data,
# the picture looks much more consistent.
shc_filter = gt.filter.DDK(3)
model_coeffs.truncate(96)
grid = (coeffs_filtered - shc_filter.filter(model_coeffs)).to_grid()
f, ax = plt.subplots(subplot_kw={'projection': ctp.crs.Robinson()})

im = ax.imshow(grid.value_array * 100, cmap='RdBu', vmin=-25, vmax=25, transform=ctp.crs.PlateCarree())
ax.coastlines()
gt.plot.colorbar(im, ax, label='water storage [cm]', extend='both')
plt.savefig('grid_diff_filtered.png', bbox_inches='tight', transparent=True, dpi=600)
