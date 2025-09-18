"""
Get the time coordinate values from an original CMIP6 file and its
repacked version, using both HDF5-C and pure-Python pyfive backends.

Note that the access to the original file may take a very long time.
"""
import time
import fsspec, pyfive, h5netcdf

fs = fsspec.filesystem("https")

# Repacked file
repacked = fs.open("https://gws-access.jasmin.ac.uk/public/canari/uas_3hr_IPSL-CM6A-LR_piControl_r1i1p1f1_gr_187001010300-197001010000.nc_cmip7repack", "rb")

# Original file
original = fs.open("https://gws-access.jasmin.ac.uk/public/canari/uas_3hr_IPSL-CM6A-LR_piControl_r1i1p1f1_gr_187001010300-197001010000.nc", "rb")

#---------------------------------------------------------------------
# Repacked file
#---------------------------------------------------------------------

# Using the HDF5-C backend
h1 = h5netcdf.File(repacked)

start = time.time()
t = h1["time"][...]
print(f"Time taken (repacked, h5netcdf): {time.time() - start}")

# Using the pure Python pyfive backend
p1 = pyfive.File(repacked)

start = time.time()
t = p1["time"][...]
print(f"Time taken (repacked, pyfive): {time.time() - start}")

#---------------------------------------------------------------------
# Original file
#---------------------------------------------------------------------

# Using the HDF5-C backend
h0 = h5netcdf.File(original)

start=time.time()
t = h0["time"][...]
print(f"Time taken (original, h5netcdf): {time.time() - start}")

# Using the pure Python pyfive backend
p0 = pyfive.File(original)

start = time.time()
t = p0["time"][...]
print(f"Time taken (original, pyfive): {time.time() - start}")
