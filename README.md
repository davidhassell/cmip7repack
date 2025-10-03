# cmip7repack

`cmip7repack` is a command-line tool, bespoke to CMIP, which can be used by the modelling groups, prior to dataset publication, to "repack" their files (i.e. to re-organise the file contents to have a different chunk and internal file metadata layout) in such as way as to improve their read-performance over the lifetime of the CMIP7 archive (note that CMIP7 datasets are written only once, but read many times).

## Installation

To install `cmip7repack`, download the shell script in this repository with that name and give it executable permissions. 

## Usage

```
$ cmip7repack -h
cmip7repack(1)             General Commands Manual            cmip7repack(1)

NAME
       cmip7repack - repack CMIP7 netCDF-4 datasets

SYNOPSIS
       cmip7repack [-d size] [-h] [-o] [-v] [-x] [-z n] FILE [FILE ...]

DESCRIPTION
       For each netCDF-4 FILE, cmip7repack will

       — Collate  all of the internal file metadata to a contiguous block at
         the start of the file.

       — Rechunk the time coordinate variable, if it exists, to have a  sin‐
         gle compressed chunk.

       — Rechunk  the  time  bounds variable, if it exists, to have a single
         compressed chunk.

       — OPTIONAL. Rechunk the data variable, if it exists, to have a  given
         uncompressed chunk size.

       All  rechunked variables are de-interlaced with the HDF5 shuffle fil‐
       ter (which significantly  improves  compression)  before  being  com‐
       pressed  with  zlib (see the -z option), and also have the Fletcher32
       HDF5 checksum algorithm activated.

OPTIONS
       -d size
              Rechunk the data variable (the variable  named  by  the  vari‐
              able_id global attribute) to have the given uncompressed chunk
              size  (in  bytes).  The chunk shape will only be changed along
              the leading dimension of the data variable (which  is  usually
              the time axis), and only if A) the original uncompressed chunk
              size is smaller than the new value, and B) the original number
              of  chunk elements along the leading dimension is 1. If either
              of these conditions is not met then the data variable will not
              be rechunked.

       -h     Display this help and exit.

       -o     Overwrite each original file with its repacked version, if the
              repacking was successful. By default, a new file with the suf‐
              fix

       -v     Print version number and exit.

       -x     Do a dry run. Show the repacking command for each file, but do
              not run it.

       -z n   Specify the zlib compression level (between 1 and  9,  default
              4) for rechunked variables.

EXAMPLES
       Repack a file, replacing the original file with its repacked version:

         $ cmip7repack -o file.nc
         cmip7repack: Version 0.2 at /bin/cmip7repack
         cmip7repack: h5repack: Version 1.14.3 at /bin/h5repack

         cmip7repack: date-time: Fri  3 Oct 09:56:03 BST 2025
         cmip7repack: preparing to repack 'file.nc'
         cmip7repack: repack command: h5repack --metadata_block_size=877832 -f /time:SHUF -f /time:GZIP=4 -f /time:FLET -l /time:CHUNK=6000 -f /time_bounds:SHUF -f /time_bounds:GZIP=4 -f /time_bounds:FLET -l /time_bounds:CHUNK=6000x2 file.nc file.nc_cmip7repack
         cmip7repack: running repack command (may take some time ...)
         cmip7repack: successfully created 'file.nc_cmip7repack' in 13 seconds

         cmip7repack: Total of 1 files (297046606 bytes) repacked in 13 seconds (22849738 B/s) to total size 296728324 bytes (0% smaller than input files)
         $

EXIT STATUS
       The  cmip7repack  utility  exits 0 on success, and >0 if an error oc‐
       curs.

AUTHORS
       Written by David Hassell and Ezequiel Cimadevilla.

REPORTING BUGS
       Report any bugs to https://github.com/davidhassell/cmip7repack/issues

COPYRIGHT
       Copyright  2025  License  BSD  3-Clause   <https://opensource.org/li‐
       cense/bsd-3-clause>.  This  is  free software: you are free to change
       and redistribute it. There is NO WARRANTY, to the extent permitted by
       law.

SEE ALSO
       h5repack(1)

2025-10-03                           0.2                      cmip7repack(1)
```
