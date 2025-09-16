# cmip7repack

`cmip7repack` is a command line tool, bespoke to CMIP, which can be used by the modelling groups, prior to dataset publication, to "repack" their files (i.e. to re-organise the file contents to have a different chunk and B-tree layout) in such as way as to improve their read-performance over the lifetime of the CMIP7 archive (note that CMIP7 datasets are written only once, but read many times).

The full list of command line options for `cmip7repack` is:

```
$ Usage: cmip7repack [-d size] [-h] [-o] [-v] [-x] [-z n] FILE [FILE ...]
    -d|--data size  Also rechunk the data variable to have the given
                    chunk size (in bytes), but only if the original
                    chunk size is smaller than the new value.w
                    Only chunks along the leading axis may be 
                    changed (which is usually the time axis). By 
                    default the data variable is not rechunked.
    -h|--help       Display this help and exit.
    -o|--overwrite  Overwrite each original file with its repacked
                    version, if the repacking was successful.
                    By default, a new file with the suffix
                    '_cmip7repack' is created for each input file.
    -v|--version    Print version number and exit.
    -x|--dry-run    Do a dry run: Show the repacking command for
                    each file, but do not run it.
    -z|--gzip n     Specify the deflate compression level (between 1
                    and 9, default 4) for rechunked data variables.
    FILE [FILE ...] One or more netCDF-4 files to be repacked.
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