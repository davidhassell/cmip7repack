# `cmip7repack` and `check_cmip7repack`

`cmip7repack` is a command-line tool for Unix-like platforms, bespoke
to CMIP, which can be used by the modelling groups, prior to dataset
publication, to "repack" their files (i.e. to re-organise the file
contents to have a different chunk and internal file metadata layout)
in such as way as to improve their read-performance over the lifetime
of the CMIP7 archive (note that CMIP7 datasets are written only once,
but read many times).

`check_cmip7repack` is a command-line tool for Unix-like platforms,
bespoke to CMIP, which can be used to check if datasets have a
sufficiently good internal structure. Any dataset that has been
output by `cmip7repack` is guaranteed to pass the checks.
        
# Citations

Hassell, D., & Cimadevilla Alvarez, E. (2025). cmip7repack: Repack CMIP7 netCDF-4 datasets. Zenodo. https://doi.org/10.5281/zenodo.17550919

# Installation

To install `cmip7repack` and `check_cmip7repack`, download the scripts
with those names from this repository, give them executable
permissions, and make them available from a location in the `PATH`
environment variable.

# `cmip7repack` documentation

### Dependencies

`cmip7repack` is a shell script that requires that the HDF5
command-line tools
[`h5stat`](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_t_o_o_l__s_t__u_g.html),
[`h5dump`](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_t_o_o_l__d_p__u_g.html),
and
[`h5repack`](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_t_o_o_l__r_p__u_g.html)
are available from the `PATH` environment variable. These tools are
usually automatically installed as part of a netCDF installation.

### man page


```
cmip7repack(1)              General Commands Manual             cmip7repack(1)

NAME
       cmip7repack - repack CMIP7 datasets

SYNOPSIS
       cmip7repack [-d size] [-h] [-o] [-v] [-x] [-z n] FILE [FILE ...]

DESCRIPTION
       For each CMIP7-compliant netCDF-4 FILE, cmip7repack will

       — Rechunk  the  time  coordinate  variable  (assumed to be the variable
         called "time" in the root group), if it exists, to have a single com‐
         pressed chunk.

       — Rechunk the time bounds variable  (defined  by  the  time  coordinate
         variable's  "bounds"  attribute), if it exists, to have a single com‐
         pressed chunk.

       — Rechunk the data variable (defined by  the  global  attribute  "vari‐
         able_id"),  if  it  exists, to have a given chunk size (of at least 4
         MiB).

       — Collate all of the internal file metadata to a contiguous block  near
         the start of the file, before all of the variables' data chunks.

       All  rechunked variables are de-interlaced with the HDF5 shuffle filter
       (which significantly improves compression) before being compressed with
       zlib (see the -z option), and also have the  Fletcher32  HDF5  checksum
       algorithm activated.

       Files  repacked  with  cmip7repack will pass the CMIP7 ESGF file-layout
       checks.

METHOD
       Each input FILE is analysed using h5stat and h5dump, and then  repacked
       using  h5repack, which changes the layout for objects in the new output
       file. All file attributes and data values are unchanged.

OPTIONS
       -d size
              Rechunk the data variable (the  variable  named  by  the  "vari‐
              able_id"  global attribute) to have the given uncompressed chunk
              size in bytes. If -d is unset, then the size defaults to 4194304
              (i.e. 4 MiB). The size must be at least 4194304. The chunk shape
              will only ever be changed along the leading (i.e.  slowest  mov‐
              ing)  dimension  of  the data, such that resulting chunk size in
              the new file is as large as possible without exceeding the size.

              However, if the original uncompressed chunk size  in  the  input
              file  is  already  larger than size, then the data variable will
              not be rechunked.

       -h     Display this help and exit.

       -o     Overwrite each input file with  its  repacked  version,  if  the
              repacking  was successful. By default, a new file is created for
              each input file, which has the same name with  the  addition  of
              the suffix "_cmip7repack".

       -v     Print version number and exit.

       -x     Do  a dry run. Show the h5repack commands for repacking each in‐
              put file, but do not run them. This allows the  commands  to  be
              edited before being run manually.

       -z n   Specify  the zlib compression level (between 1 and 9, default 4)
              for all rechunked variables.
	      
EXIT STATUS
       0      All input files successfully repacked.

       1      A failure occured during the repacking  of  one  or  more  input
              files. The exit only happens only after it has been attempted to
              repack  all  input  files,  some of which may have been repacked
              successfully. The files which could not be repacked may be found
              by looking for FAILED in the text output log.

       2      An incorrect command-line option.

       3      A missing HDF5 dependency.

EXAMPLES
       1. Repack a file with the default settings (which guarantees  that  the
       repacked  files  will  pass the ESGF file-layout checks), and replacing
       the original file with its repacked version. Note that the  data  vari‐
       able is rechunked to chunks of shape 37 x 144 x 192 elements.

           $ cmip7repack -o file.nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:06:25 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192 file.nc file.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file.nc_cmip7repack'
           cmip7repack: renamed 'file.nc_cmip7repack' -> 'file.nc'
           cmip7repack: time taken: 5 seconds

           cmip7repack: 1/1 files (134892546 bytes) repacked in 5 seconds (26978509 B/s) to total size 94942759 bytes (29% smaller than input files)
           $

       2.  Repack  a  file  using  the non-default data variable chunk size of
       8388608, replacing the original file with its  repacked  version.  Note
       that  the  data variable is rechunked to chunks of shape 75 x 144 x 192
       elements (compare that with the rechunked  data  variable  chunk  shape
       from example 1).

           $ cmip7repack -d 8388608 -o file.nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:07:15 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=75x144x192 file.nc file.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file.nc_cmip7repack'
           cmip7repack: renamed 'file.nc_cmip7repack' -> 'file.nc'
           cmip7repack: time taken: 5 seconds

           cmip7repack: 1/1 files (134892546 bytes) repacked in 5 seconds (26978509 B/s) to total size 94856788 bytes (29% smaller than input files)
           $
       3.  Get the h5repack commands that would be used for repacking each in‐
       put file, but do not run them.

           $ cmip7repack -x file.nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:08:02 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192 file.nc file.nc_cmip7repack
           cmip7repack: dry-run: not repacking
           $

       4. Repack multiple files with one command. This takes the same time  as
       repacking the files with separate commands, but may be more convenient.

           $ cmip7repack -o file[12].nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:09:13 GMT 2025
           cmip7repack: file: 'file1.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192 file1.nc file1.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file1.nc_cmip7repack'
           cmip7repack: renamed 'file1.nc_cmip7repack' -> 'file1.nc'
           cmip7repack: time taken: 5 seconds

           cmip7repack: date-time: Wed  5 Nov 12:09:18 GMT 2025
           cmip7repack: file: 'file2.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=149185  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=708 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=708x2 -f /toz:SHUF -f /toz:GZIP=4 -f /toz:FLET -l /toz:CHUNK=37x144x192 file2.nc file2.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file2.nc_cmip7repack'
           cmip7repack: renamed 'file2.nc_cmip7repack' -> 'file2.nc'
           cmip7repack: time taken: 1 seconds

           cmip7repack: 2/2 files (182714276 bytes) repacked in 6 seconds (30452379 B/s) to total size 140606512 bytes (23% smaller than input files)
           $

AUTHORS
       Written by David Hassell and Ezequiel Cimadevilla.

REPORTING BUGS
       Report any bugs to https://github.com/NCAS-CMS/cmip7repack/issues

COPYRIGHT
       Copyright   2025   License   BSD  3-Clause  <https://opensource.org/li‐
       cense/bsd-3-clause>. This is free software: you are free to change  and
       redistribute it. There is NO WARRANTY, to the extent permitted by law.

SEE ALSO
       h5repack(1), h5stat(1), h5dump(1), ncdump(1)

0.5                               2025-11-12                    cmip7repack(1)
```

# `check_cmip7repack` documentation

### Dependencies

`check_cmip7repack` is a Python script that requires Python 3.10 or
later, and that the Python libraries
[pyfive](<https://pyfive.readthedocs.io>, [numpy](https://numpy.org),
and [packaging](https://packaging.pypa.io) are available from a
location in the `PYTHONPATH` environment variable.

### man page

```
check_cmip7repack(1)        General Commands Manual       check_cmip7repack(1)

NAME
       check_cmip7repack  -  check  that datasets meet the CMIP7 repacking re‐
       quirements.

SYNOPSIS
       check_cmip7repack  [-h] [-v] FILE [FILE ...]

DESCRIPTION
       For each input FILE, check_cmip7repack will

       — Check that time coordinate  variable  (assumed  to  be  the  variable
         called "time" in the root group), if it exists, has a chunk.

       — Check  that  the time bounds variable (defined by the time coordinate
         variable's "bounds" attribute), if it exists, has a single chunk.

       — Check that data variable (defined  by  the  global  attribute  "vari‐
         able_id"),  if  it  exists, has a single chunk or has an uncompressed
         chunk size of at least 41943044 bytes  (i.e.  4  MiB).  However,  the
         check  will  still  pass for smaller chunks if increasing the chunk's
         shape by one element along the leading (i.e. slowest  moving)  dimen‐
         sion of the data would result in a chunk size of at least 4 MiB.

       — Check  that  all  of the internal file metadata is collated to a con‐
         tiguous block near the start of the file, before  all  of  the  vari‐
         ables' data chunks.

       Any    input    FILE    that    has    been   output   by   cmip7repack
       <https://github.com/NCAS-CMS/cmip7repack> is guaranteed to  pass  these
       checks.

DEPENDENCIES
       Requires  Python  3.10  or  later, and that the Python libraries pyfive
       <https://pyfive.readthedocs.io>, numpy <https://numpy.org>, and packag‐
       ing <https://packaging.pypa.io> are available from a  location  in  the
       PYTHONPATH environment variable.

METHOD
       Each input FILE is analysed using the Python pyfive package.

OPTIONS
       -h     Display this help and exit.

       -v     Print version number and exit.

EXIT STATUS
       0      All input files meet the CMIP7 repacking requirements

       1      At  least  one  input file does not meet the CMIP7 repacking re‐
              quirements. All files were checked.

       2      An incorrect command-line option.

       3      An input file does not exist. No input files are checked.

       4      An input file can not be opened. No input files are checked.

       5      An input file can be opened put not parsed as an HDF5  file.  No
              input files are checked.

AUTHORS
       Written by David Hassell and Ezequiel Cimadevilla.

REPORTING BUGS
       Report any bugs to https://github.com/NCAS-CMS/cmip7repack/issues

COPYRIGHT
       Copyright   2025   License   BSD  3-Clause  <https://opensource.org/li‐
       cense/bsd-3-clause>. This is free software: you are free to change  and
       redistribute it. There is NO WARRANTY, to the extent permitted by law.

SEE ALSO
       cmip7repack(1)

0.5                               2025-11-12              check_cmip7repack(1)
```

# Linting

`cmip7repack` passes
[ShellCheck](https://github.com/koalaman/shellcheck) analysis.

`check_cmip7repack` is linted with [black](https://black.readthedocs.io).
