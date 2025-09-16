# cmip7repack

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