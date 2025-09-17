# cmip7repack

`cmip7repack` is a command-line tool, bespoke to CMIP, which can be used by the modelling groups, prior to dataset publication, to "repack" their files (i.e. to re-organise the file contents to have a different chunk and B-tree layout) in such as way as to improve their read-performance over the lifetime of the CMIP7 archive (note that CMIP7 datasets are written only once, but read many times).

## Installation

To install `cmip7repack`, download the shell script in this repository with that name and give it executable permissions. 

## Usage

The full help page for `cmip7repack` is:

```
$ cmip7repack -h
NAME
    cmip7repack - repack CMIP7 netCDF-4 datasets

SYNOPSIS
    cmip7repack [-d size] [-h] [-o] [-v] [-x] [-z n] FILE [FILE ...]

DESCRIPTION
    For each netCDF-4 FILE, cmip7repack will

    1) Collate all of the B-trees to a contiguous block at the start
       of the file.

    2) Rechunk the time coordinate variable, if it exists, to have a
       single compressed chunk.

    3) Rechunk the time_bounds coordinate variable, if it exists, to
       have a single compressed chunk.

    4) Optionally rechunk the leading axis of the data variable to a
       given chunk size, but only if the original chunk size is
       smaller than the new value.

    -d size  Also rechunk the data variable to have the given
             uncompressed chunk size (in bytes), but only if the
             original uncompressed chunk size is smaller than the new
             value. The chunk shape will only be changed along the
             leading dimension of the data (which is usually the time
             axis). By default the data variable is not rechunked.

    -h       Display this help and exit.

    -o       Overwrite each original file with its repacked version,
             if the repacking was successful. By default, a new file
             with the suffix '_cmip7repack' is created for each input
             file.

    -v       Print version number and exit.

    -x       Do a dry run. Show the repacking command for each
             file, but do not run it.

    -z n     Specify the deflate compression level (between 1 and 9,
             default 4) for rechunked variables.

EXAMPLES
    Repack a file, replacing the original file with its repacked
    version:

    $ cmip7repack -o file.nc
    cmip7repack: Version 0.1 at /bin/cmip7repack
    cmip7repack: h5repack: Version 1.14.3 at /bin/h5repack
    
    cmip7repack: date-time: Wed 17 Sep 08:37:14 BST 2025
    cmip7repack: preparing to repack 'file.nc'
    cmip7repack: repack command: kh5repack --metadata_block_size=877832 -l /time:CHUNK=6000 -f /time:GZIP=4 -l /time_bounds:CHUNK=6000x2 -f /time_bounds:GZIP=4 file.nc file.nc_cmip7repack
    cmip7repack: running repack command (may take some time ...)
    cmip7repack: successfully created 'file.nc_cmip7repack' in 13 seconds
    cmip7repack: renamed 'file.nc_cmip7repack' -> 'file.nc'
    
    cmip7repack: Total of 1 files repacked in 13 seconds
    $

AUTHOR
    Written by David Hassell and Ezequiel Cimadevilla.

REPORTING BUGS
    Report any bugs to
    <https://github.com/davidhassell/cmip7repack/issues>

COPYRIGHT
    Copyright © 2025 License BSD 3-Clause
    <https://opensource.org/license/bsd-3-clause>. This is free
    software: you are free to change and redistribute it. There is NO
    WARRANTY, to the extent permitted by law.

SEE ALSO
    h5repack(1)
```

In practice it is expected that, after initial testing, running with only the `-o|--overwrite` option will be always be acceptable:

```
$ cmip7repack -o *.nc
```

A different deflate compression level for any rechunked variables may be set with the `-z|--gzip` option:

```
$ cmip7repack -z 5 -o *.nc
```

To also rechunk the data variable, a data variable chunk size must be provided with the `-d|--data` option:

```
$ cmip7repack -d 4194304 -o *.nc
```

For those who want full control, running with he `-x|--dry-run` option (which may be used in conjunction with any other options) provides the `h5repack` command used by internally `cmip7repack`, but does not run it, thereby allowing it to be be altered in any way before being run manually:

```
$ cmip7repack -x file.nc
cmip7repack: Version 0.1 at /bin/cmip7repack
cmip7repack: h5repack: Version 1.14.3 at /bin/h5repack

cmip7repack: start time: Mon 15 Sep 16:13:46 BST 2025
cmip7repack: preparing to repack file.nc
cmip7repack: repack command: h5repack --metadata_block_size=40988486 -l /time:CHUNK=292192 -f /time:GZIP=4 -l /time_bounds:CHUNK=292192x2 -f /time_bounds:GZIP=4 file.nc file.nc_cmip7repack
cmip7repack: dry-run: not repacking
```