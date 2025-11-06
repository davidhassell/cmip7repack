# cmip7repack

`cmip7repack` is a command-line tool, bespoke to CMIP, which can be used by the modelling groups, prior to dataset publication, to "repack" their files (i.e. to re-organise the file contents to have a different chunk and internal file metadata layout) in such as way as to improve their read-performance over the lifetime of the CMIP7 archive (note that CMIP7 datasets are written only once, but read many times).

## Installation

To install `cmip7repack`, download the shell script in this repository with that name and give it executable permissions. 

## Dependencies

`cmip7repack` is a shell script that requires that the HDF5 tools
[`h5stat`](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_t_o_o_l__s_t__u_g.html),
[`h5dump`](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_t_o_o_l__d_p__u_g.html),
and
[`h5repack`](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_t_o_o_l__r_p__u_g.html)
are available from the `$PATH` environment variable. These tools are
usually automatically installed as part of a netCDF installation.

## Usage

```
cmip7repack(1)            General Commands Manual            cmip7repack(1)

NAME
       cmip7repack - repack CMIP7 datasets

SYNOPSIS
       cmip7repack [-d size] [-h] [-o] [-v] [-x] [-z n] FILE [FILE ...]

DESCRIPTION
       For each CMIP7-compliant netCDF-4 FILE, cmip7repack will

       — Rechunk  the  time coordinate variable (assumed to be the variable
         called "time" in the root group), if it exists, to have  a  single
         compressed chunk.

       — Rechunk  the  time bounds variable (defined by the time coordinate
         variable's "bounds" attribute), if it exists,  to  have  a  single
         compressed chunk.

       — Rechunk  the data variable (defined by the global attribute "vari‐
         able_id"), if it exists, to have a given chunk size (of at least 4
         MiB).

       — Collate  all  of  the internal file metadata to a contiguous block
         near the start of the file, before  all  of  the  variables'  data
         chunks.

       All rechunked variables are de-interlaced with the HDF5 shuffle fil‐
       ter (which significantly improves  compression)  before  being  com‐
       pressed  with zlib (see the -z option), and also have the Fletcher32
       HDF5 checksum algorithm activated.

       Files repacked with cmip7repack will pass the CMIP7 ESGF file-layout
       checks.

METHOD
       Each  input  FILE  is  analysed  using  h5stat  and h5dump, and then
       repacked using h5repack, which changes the layout for objects in new
       output file. All file attributes and data values are unchanged.

OPTIONS
       -d size
              Rechunk  the  data variable (the variable named by the "vari‐
              able_id" global attribute) to  have  the  given  uncompressed
              chunk  size  in bytes. If -d is unset, then the size defaults
              to 4194304 (i.e. 4 MiB). The size must be at  least  4194304.
              The  chunk  shape will only ever be changed along the leading
              (i.e. slowest moving) dimension of the data,  such  that  re‐
              sulting  chunk  size  in the new file is as large as possible
              without exceeding the size.

              However, if the original uncompressed chunk size in the input
              file is already larger than size, then the data variable will
              not be rechunked.

       -h     Display this help and exit.

       -o     Overwrite each input file with its repacked version,  if  the
              repacking  was  successful. By default, a new file is created
              for each input file, which has the same name with  the  addi‐
              tion of the suffix "_cmip7repack".

       -v     Print version number and exit.

       -x     Do  a  dry run. Show the h5repack commands for repacking each
              input file, but do not run them. This allows the commands  to
              be edited before being run manually.

       -z n   Specify  the zlib compression level (between 1 and 9, default
              4) for all rechunked variables.

EXIT STATUS
       0      All input files successfully repacked.

       1      An incorrect command-line option.

       2      A missing HDF5 dependency.

       3      A failure occured during the repacking of one or  more  input
              files. The exit only happens only after it has been attempted
              to repack all input  files,  some  of  which  may  have  been
              repacked  successfully. The files which could not be repacked
              may be found by looking for FAILED in the text output log.

EXAMPLES
       1.  Repack  a  file with the default settings (which guarantees that
       the repacked files will pass the ESGF file-layout checks),  and  re‐
       placing  the  original file with its repacked version. Note that the
       data variable is rechunked to chunks of shape 37 x 144  x  192  ele‐
       ments.

           $ cmip7repack -o file.nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:06:25 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570
               -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800
               -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET
               -l /time_bnds:CHUNK=1800x2 -f /pr:SHUF -f /pr:GZIP=4
               -f /pr:FLET -l /pr:CHUNK=37x144x192
               file.nc file.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file.nc_cmip7repack' in 5 seconds
           cmip7repack: renamed 'file.nc_cmip7repack' -> 'file.nc'

           cmip7repack: 1/1 files (134892546 bytes) repacked in 5 seconds (26978509 B/s) to total size 94942759 bytes (29% smaller than input files)
           $

       2.  Repack  a file using the non-default data variable chunk size of
       8388608, replacing the original file with its repacked version. Note
       that  the  data  variable is rechunked to chunks of shape 75 x 144 x
       192 elements (compare that with the rechunked  data  variable  chunk
       shape from example 1).

           $ cmip7repack -d 8388608 -o file.nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:07:15 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570
               -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800
               -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET
               -l /time_bnds:CHUNK=1800x2
               -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=75x144x192
               file.nc file.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file.nc_cmip7repack' in 5 seconds
           cmip7repack: renamed 'file.nc_cmip7repack' -> 'file.nc'

           cmip7repack: 1/1 files (134892546 bytes) repacked in 5 seconds (26978509 B/s) to total size 94856788 bytes (29% smaller than input files)
           $

       3.  Get  the h5repack commands that would be used for repacking each
       input file, but do not run them.

           $ cmip7repack -x file.nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:08:02 GMT 2025
           cmip7repack: file: 'file.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570
               -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800
               -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET
               -l /time_bnds:CHUNK=1800x2
               -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192
               file.nc file.nc_cmip7repack
           cmip7repack: dry-run: not repacking
           $

       4. Repack multiple files with one command. This takes the same  time
       as  repacking the files with separate commands, but may be more con‐
       venient.

           $ cmip7repack -o file[12].nc
           cmip7repack: Version 0.3 at /usr/bin/cmip7repack
           cmip7repack: h5repack: Version 1.14.6 at /usr/bin/h5repack

           cmip7repack: date-time: Wed  5 Nov 12:09:13 GMT 2025
           cmip7repack: file: 'file1.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=236570
	       -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=1800
	       -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET
	       -l /time_bnds:CHUNK=1800x2
	       -f /pr:SHUF -f /pr:GZIP=4 -f /pr:FLET -l /pr:CHUNK=37x144x192
	       file1.nc file1.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file1.nc_cmip7repack' in 5 seconds
           cmip7repack: renamed 'file1.nc_cmip7repack' -> 'file1.nc'

           cmip7repack: date-time: Wed  5 Nov 12:09:18 GMT 2025
           cmip7repack: file: 'file2.nc'
           cmip7repack: repack command: h5repack --metadata_block_size=149185
               -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=708
               -f /time_bnds:SHUF -f /time_bnds:GZIP=4 -f /time_bnds:FLET
               -l /time_bnds:CHUNK=708x2
               -f /toz:SHUF -f /toz:GZIP=4 -f /toz:FLET -l /toz:CHUNK=37x144x192
               file2.nc file2.nc_cmip7repack
           cmip7repack: running repack command (may take some time ...)
           cmip7repack: successfully created 'file2.nc_cmip7repack' in 1 seconds
           cmip7repack: renamed 'file2.nc_cmip7repack' -> 'file2.nc'

           cmip7repack: 2/2 files (182714276 bytes) repacked in 6 seconds (30452379 B/s) to total size 140606512 bytes (23% smaller than input files)
           $

AUTHORS
       Written by David Hassell and Ezequiel Cimadevilla.

REPORTING BUGS
       Report any bugs to https://github.com/NCAS-CMS/cmip7repack/issues

COPYRIGHT
       Copyright  2025  License  BSD  3-Clause  <https://opensource.org/li‐
       cense/bsd-3-clause>.  This  is free software: you are free to change
       and redistribute it. There is NO WARRANTY, to the  extent  permitted
       by law.

SEE ALSO
       h5repack(1), h5stat(1), h5dump(1), ncdump(1)

0.4                              2025-11-05                  cmip7repack(1)
```

## Linting

`cmip7repack` passes
[ShellCheck](https://github.com/koalaman/shellcheck) analysis.