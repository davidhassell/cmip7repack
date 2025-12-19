## Note: _These tools are currently available for testing. Real CMIP7 workflows should use version 1.0 or later._

# `cmip7repack` and `check_cmip7_packing`

`cmip7repack` is a command-line tool for Unix-like platforms, bespoke
to CMIP, which can be used by the modelling groups, prior to dataset
publication, to "repack" their files (i.e. to re-organise the file
contents to have a different chunk and internal file metadata layout)
in such as way as to improve their read-performance over the lifetime
of the CMIP7 archive (note that CMIP7 datasets are written only once,
but read many times).

`check_cmip7_packing` is a command-line tool for Unix-like platforms,
bespoke to CMIP, which can be used to check if datasets have a
sufficiently good internal structure. Any dataset that has been
output by `cmip7repack` is guaranteed to pass the checks.
        
# Citation

Hassell, D., & Cimadevilla Alvarez, E. (2025). cmip7repack: Repack CMIP7 netCDF-4 datasets. Zenodo. https://doi.org/10.5281/zenodo.17550919

# Installation

To install `cmip7repack` and `check_cmip7_packing`, download the scripts
with those names from this repository, give them executable
permissions, and make them available from a location in the `PATH`
environment variable. _These tools will soon be available via `pip` and `conda`._

From conda-forge:

```
conda install -c conda-forge cmip7-repack
```

or from PyPI:

```
pip install cmip7_repack
```

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

### man pages

```
$ cmip7repack -h
cmip7repack(1)              General Commands Manual             cmip7repack(1)

NAME
       cmip7repack - repack CMIP7 datasets

SYNOPSIS
       cmip7repack [-d size] [-h] [-o] [-V] [-x] [-z n] FILE [FILE ...]

DESCRIPTION
       For each CMIP7-compliant netCDF-4 FILE, cmip7repack will

       — Rechunk  the  time  coordinate  variable  (assumed to be the variable
         called "time" in the root group), if it exists, to have a single com‐
         pressed chunk.

       — Rechunk  the  time  bounds  variable  (defined by the time coordinate
         variable's "bounds" attribute), if it exists, to have a  single  com‐
         pressed chunk.

       — Rechunk  the  data  variable  (defined by the global attribute "vari‐
         able_id"), if it exists, to have a given chunk size (of  at  least  4
         MiB).

       — Collate  all of the internal file metadata to a contiguous block near
         the start of the file, before all of the variables' data chunks.

       Any of these variables that already has an appropriate chunk size  will
       not be rechunked. If no variables need rechunking then cmip7repack will
       only collate the internal file metadata, which is very fast in compari‐
       son to also having to rechunk one or more variables.

       A  rechunked  variable  is  de-interlaced  with the HDF5 shuffle filter
       (which significantly improves compression) before being compressed with
       zlib (see the -z option), and also has the Fletcher32 HDF5 checksum al‐
       gorithm activated.

       Files repacked with cmip7repack are guaranteed to pass the CMIP7  file-
       layout checks tested by cmip7_check_packing.

DEPENDENCIES
       Requires  that  the command-line tools h5stat, h5dump, and h5repack are
       available from a location given by the PATH environment variable.

METHOD
       Each  input FILE is analysed using h5stat and h5dump, and then repacked
       using h5repack, which changes the layout for objects in the new  output
       file. All file attributes and data values are unchanged.

OPTIONS
       -d size
              Rechunk  the  data  variable  (the  variable named by the "vari‐
              able_id" global attribute) to have the given uncompressed  chunk
              size in bytes. If -d is unset, then the size defaults to 4194304
              (i.e. 4 MiB). The size must be at least 4194304.

              The chunk shape will only ever  be  changed  along  the  leading
              (i.e. slowest moving) dimension of the data, such that resulting
              chunk size in the new file is as large as possible  without  ex‐
              ceeding  size  (note  that  the  resulting  chunk  size could be
              smaller than size).

              However, if the original uncompressed chunk size  in  the  input
              file  is already larger than size, or the data in the input file
              only has one chunk, then the data variable will not  be  rechun‐
              ked.

       -h     Display this help and exit.

       -o     Overwrite  each  input  file  with  its repacked version, if the
              repacking was successful. By default, a new file is created  for
              each  input  file,  which has the same name with the addition of
              the suffix "_cmip7repack".

       -V     Print version number and exit.

       -x     Do a dry run. Show the h5repack commands for repacking each  in‐
              put  file,  but  do not run them. This allows the commands to be
              edited before being run manually.

       -z n   Specify the zlib compression level (between 1 and 9, default  4)
              for all rechunked variables.

EXIT STATUS
       0      All input files successfully repacked.

       1      A  failure  occurred  during  the repacking of one or more input
              files. The exit only happens only after it has been attempted to
              repack  all  input  files,  some of which may have been repacked
              successfully. The files which could not be repacked may be found
              by looking for FAILED in the text output log.

       2      An incorrect command-line option.

       3      A missing HDF5 dependency.

EXAMPLES
       1.  Repack  a file with the default settings (which guarantees that the
       repacked files will pass the ESGF file-layout  checks),  and  replacing
       the  original  file with its repacked version. Note that the data vari‐
       able is rechunked to chunks of shape 37 x 144 x 192 elements.

           $ cmip7repack -o file.nc
           cmip7repack: Version 0.6 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:06:25 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: rechunking variable /time with shape (1800) and original chunk shape (512)
           cmip7repack: rechunking variable time_bnds with shape (1800, 2) and original chunk shape (1, 2)
           cmip7repack: rechunking variable /pr with shape (1800, 144, 192) and original chunk shape (1, 144, 192) = 110592 B
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192 'file.nc' 'file.nc_cmip7repack'
           cmip7repack: running repack command ...
           cmip7repack: successfully created 'file.nc_cmip7repack'
           cmip7repack: renamed 'file.nc_cmip7repack' -> 'file.nc'
           cmip7repack: time taken: 5 seconds

           cmip7repack: 1/1 files (134892546 B) repacked in 5 seconds (26978509 B/s) to total size 94942759 B (29% smaller than input files)

       2. Repack a file using the non-default  data  variable  chunk  size  of
       8388608,  replacing  the  original file with its repacked version. Note
       that the data variable is rechunked to chunks of shape 75 x 144  x  192
       elements  (compare  that  with  the rechunked data variable chunk shape
       from example 1).

           $ cmip7repack -d 8388608 file.nc
           cmip7repack: Version 0.6 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:07:15 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: rechunking variable /time with shape (1800) and original chunk shape (512)
           cmip7repack: rechunking variable time_bnds with shape (1800, 2) and original chunk shape (1, 2)
           cmip7repack: rechunking variable /pr with shape (1800, 144, 192) and original chunk shape (1, 144, 192) = 110592 B
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=75x144x192 'file.nc' 'file.nc_cmip7repack'
           cmip7repack: running repack command ...
           cmip7repack: successfully created 'file.nc_cmip7repack'
           cmip7repack: time taken: 5 seconds

           cmip7repack: 1/1 files (134892546 B) repacked in 5 seconds (26978509 B/s) to total size 94856788 B (29% smaller than input files)

       If the repacked file file.nc_cmip7repack is itself repacked, then since
       none  of  the variables now need rechunking, only the internal metadata
       is collated, which is very fast:

           $ cmip7repack -o file.nc_cmip7repack
           cmip7repack: Version 0.6 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:07:43 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: not rechunking variable /time with shape (1800) and original chunk shape (1800)
           cmip7repack: not rechunking variable time_bnds with shape (1800, 2) and original chunk shape (1800, 2)
           cmip7repack: not rechunking variable /pr with shape (1800, 144, 192) and original chunk shape (75, 144, 192) = 8294400 B
           cmip7repack: repack command: h5repack --metadata_block_size=43360 'file.nc_cmip7repack' 'file.nc_cmip7repack_cmip7repack'
           cmip7repack: running repack command ...
           cmip7repack: successfully created 'file.nc_cmip7repack_cmip7repack'
           cmip7repack: renamed 'file.nc_cmip7repack_cmip7repack' -> 'file.nc_cmip7repack'
           cmip7repack: time taken: 0 seconds

           cmip7repack: 1/1 files (94856788 B) repacked in 0 seconds (94856788 B/s) to total size 94856788 B (<1% smaller than input files)

       3. Get the h5repack commands that would be used for repacking each  in‐
       put file, but do not run them.

           $ cmip7repack -x file.nc
           cmip7repack: Version 0.6 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:08:02 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: rechunking variable /time with shape (1800) and original chunk shape (512)
           cmip7repack: rechunking variable time_bnds with shape (1800, 2) and original chunk shape (1, 2)
           cmip7repack: rechunking variable /pr with shape (1800, 144, 192) and original chunk shape (1, 144, 192) = 110592 B
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192 'file.nc' 'file.nc_cmip7repack'
           cmip7repack: dry-run: not repacking

       4.  Repack multiple files with one command. This takes the same time as
       repacking the files with separate commands, but may be more convenient.

           $ cmip7repack -o file[12].nc
           cmip7repack: Version 0.6 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:09:13 GMT 2025
           cmip7repack: file: 'file1.nc'
           cmip7repack: rechunking variable /time with shape (1800) and original chunk shape (512)
           cmip7repack: rechunking variable time_bnds with shape (1800, 2) and original chunk shape (1, 2)
           cmip7repack: rechunking variable /pr with shape (1800, 144, 192) and original chunk shape (1, 144, 192) = 110592 B
           cmip7repack: repack command: h5repack --metadata_block_size=236570  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192 'file1.nc' 'file1.nc_cmip7repack'
           cmip7repack: running repack command ...
           cmip7repack: successfully created 'file1.nc_cmip7repack'
           cmip7repack: renamed 'file1.nc_cmip7repack' -> 'file1.nc'
           cmip7repack: time taken: 5 seconds

           cmip7repack: date-time: Wed  5 Nov 12:09:18 GMT 2025
           cmip7repack: file: 'file2.nc'
           cmip7repack: rechunking variable /time with shape (708) and original chunk shape (1)
           cmip7repack: rechunking variable time_bnds with shape (708, 2) and original chunk shape (1, 2)
           cmip7repack: rechunking variable /pr with shape (708, 144, 192) and original chunk shape (1, 144, 192) = 110592 B
           cmip7repack: repack command: h5repack --metadata_block_size=149185  -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=708 -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET -l /time_bnds:CHUNK=708x2 -f /toz:SHUF -f /toz:GZIP=4 -f /toz:FLET -l /toz:CHUNK=37x144x192 'file2.nc' 'file2.nc_cmip7repack'
           cmip7repack: running repack command ...
           cmip7repack: successfully created 'file2.nc_cmip7repack'
           cmip7repack: renamed 'file2.nc_cmip7repack' -> 'file2.nc'
           cmip7repack: time taken: 1 seconds

           cmip7repack: 2/2 files (182714276 B) repacked in 6 seconds (30452379 B/s) to total size 140606512 B (23% smaller than input files)

AUTHORS
       Written by David Hassell and Ezequiel Cimadevilla.

REPORTING BUGS
       Report any bugs to https://github.com/NCAS-CMS/cmip7repack/issues

COPYRIGHT
       Copyright  2025   License   BSD   3-Clause   https://opensource.org/li‐
       cense/bsd-3-clause.  This  is free software: you are free to change and
       redistribute it. There is NO WARRANTY, to the extent permitted by law.

SEE ALSO
       cmip7_check_packing(1), h5repack(1), h5stat(1), h5dump(1), ncdump(1)

0.6                               2025-12-19                    cmip7repack(1)
```

# `check_cmip7_packing` documentation

### Dependencies

`check_cmip7_packing` is a Python script that requires Python 3.10 or
later, and that the Python libraries
[pyfive](https://pyfive.readthedocs.io), [numpy](https://numpy.org),
and [packaging](https://packaging.pypa.io) are available from a
location in the `PYTHONPATH` environment variable.

### man page

```
$ check_cmip7_packing -h
check_cmip7_packing(1)      General Commands Manual     check_cmip7_packing(1)

NAME
       check_cmip7_packing - check that datasets meet the CMIP7 internal pack‐
       ing requirements.

SYNOPSIS
       check_cmip7_packing [-h] [-v] [-V] FILE [FILE ...]

DESCRIPTION
       For each input FILE, check_cmip7_packing will

       — Check that the time coordinate variable (assumed to be  the  variable
         called "time" in the root group), if it exists, has a single chunk or
         is contiguous.

       — Check that the time bounds variable (identified by the  time  coordi‐
         nate variable's "bounds" attribute), if it exists, has a single chunk
         or is contiguous.

       — Check that data variable (identified by the global "variable_id"  at‐
         tribute),  if it exists, has a single chunk, is contiguous, or has an
         uncompressed chunk size of at least 41943044 bytes (i.e. 4 MiB). How‐
         ever,  the check will still pass for smaller chunks if increasing the
         chunk's shape by one element along the leading (i.e. slowest  moving)
         dimension of the data would result in a chunk size of at least 4 MiB.

       — Check  that  all  of the internal file metadata is collated to a con‐
         tiguous block near the start of the file, before  all  of  the  vari‐
         ables' data chunks.

       Any  input  FILE  that  has been output by cmip7repack is guaranteed to
       pass these checks.

DEPENDENCIES
       Requires Python 3.10 or later, and that  the  Python  libraries  pyfive
       (https://pyfive.readthedocs.io), numpy (https://numpy.org), and packag‐
       ing (https://packaging.pypa.io) are available from a location given  by
       the PYTHONPATH environment variable.

METHOD
       Each input FILE is analysed using the Python pyfive package.

OPTIONS
       -h     Display this help and exit.

       -v     Verbose mode. Print extra information.

       -V     Print version number and exit.

EXIT STATUS
       0      All  input  files  meet the CMIP7 internal file packing require‐
              ments.

       1      At least one input file does not meet the  CMIP7  internal  file
              packing requirements. All files were checked.

       2      An incorrect command-line option. No input files are checked.

       3      An input file does not exist. No input files are checked.

       4      An input file can not be opened. No input files are checked.

       5      An  input file can be opened, but not parsed as an HDF5 file. No
              input files are checked.

EXAMPLES
       1. Testing two files that both pass the checks. The exit code is 0  be‐
       cause all files passed.

           $ check_cmip7_packing file1.nc file2.nc
           PASS: File 'file1.nc'
           PASS: File 'file2.nc'
           $ echo $?
           0

       2. Repeating the test of example 1. with verbose mode enabled.

           $ check_cmip7_packing -v file1.nc file2.nc
           check_cmip7_packing: Version 0.6 at /usr/bin/check_cmip7_packing
           check_cmip7_packing: pyfive: Version 1.0.0 at /usr/bin/pyfive/__init__.py
           check_cmip7_packing: date-time: 2025-11-13 09:31:57.232149

           PASS: File 'file1.nc'
           PASS: File 'file2.nc'

           check_cmip7_packing: time taken: 0.0622 seconds
           check_cmip7_packing: 2/2 files passed, 0/2 files failed

       3.  Testing  five files, one of which (file5.nc) passes the checks, and
       the other four fail at least one check each. The exit code is 1 because
       not all files passed.

           $ check_cmip7_packing file[3-7].nc
           PASS: File 'file5.nc'
           FAIL: File 'file3.nc' does not have consolidated internal metadata
           FAIL: File 'file4.nc' time coordinates variable 'time' has 6000 chunks (expected 1 chunk or contiguous)
           FAIL: File 'file6.nc' time bounds variable 'time_bnds' has 1800 chunks (expected 1 chunk or contiguous)
           FAIL: File 'file7.nc' data variable 'ps' has uncompressed chunk size 411840 B (expected at least 4111936 B or 1 chunk or contiguous)
           $ echo $?
           1

AUTHORS
       Written by David Hassell and Ezequiel Cimadevilla.

REPORTING BUGS
       Report any bugs to https://github.com/NCAS-CMS/cmip7_repack/issues

COPYRIGHT
       Copyright   2025   License   BSD  3-Clause  (https://opensource.org/li‐
       cense/bsd-3-clause). This is free software: you are free to change  and
       redistribute it. There is NO WARRANTY, to the extent permitted by law.

SEE ALSO
       cmip7repack(1), h5stat(1), h5dump(1), ncdump(1)

0.6                               2025-12-19            check_cmip7_packing(1)
```

# Linting

`cmip7repack` passes
[ShellCheck](https://github.com/koalaman/shellcheck) analysis.

`check_cmip7_packing` is linted with [black](https://black.readthedocs.io).
