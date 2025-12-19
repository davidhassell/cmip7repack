Version 0.6
-----------

**2025-12-19**

* `cmip7repack`: Detect when rechunking is not necessary and don't
  rechunk those variables, which can greatly increase performance
  (https://github.com/NCAS-CMS/cmip7_repack/issues/22)
* Changed dependency: ``pyfive>=1.0.1``
  (https://github.com/NCAS-CMS/cmip7_repack/issues/21)

Version 0.5
-----------

**2025-11-12**

* New script: `check_cmip7_packing`
* Upated exit return codes from `cmip7repack`
