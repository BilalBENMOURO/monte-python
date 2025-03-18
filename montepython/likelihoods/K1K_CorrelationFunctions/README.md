This repository contains the likelihood modules for the KiDS-1000 (in short: K1K) 2PCFs measurements from [Asgari et al. 2020 (arXiv:2007.15633)](https://ui.adsabs.harvard.edu/abs/2020arXiv200715633A).
The module will be working 'out-of-the-box' within a [KCAP setup](https://github.com/KiDS-WL/kcap). The required KiDS-1000 data files are included in the `data` folder and the parameter file for reproducing the fiducial run of [Asgari et al. 2020](https://ui.adsabs.harvard.edu/abs/2020arXiv200715633A) is supplied in the `input` folder.

Assuming that KCAP and MontePython (with CLASS version >= 2.8 including the HMcode module) are set up (we recommend to use nested sampling), please proceed as follows:

1) Set the path to the KCAP folder in `K1K_CorrelationFunctions.data` and modify parameters as you please (note that everything is set up to reproduce the fiducial run).

2) Start your runs using e.g. the `K1K.param` supplied in the subfolder `input` (make sure to set `data.experiments=['K1K_CorrelationFunctions']`).

3) If you publish your results based on using this likelihood, please cite [Asgari et al. 2020 (arXiv:2007.15633)](https://ui.adsabs.harvard.edu/abs/2020arXiv200715633A) and all further references for the KiDS-1000 data release (as listed on the [KiDS science data webpage](http://kids.strw.leidenuniv.nl/sciencedata.php)) and also all relevant references for KCAP, Monte Python and CLASS.

As of version 3.5.0 of MontePython, S_8 is not implemented as a sampling parameter. To reproduce the fiducial run of [Asgari et al. 2020](https://ui.adsabs.harvard.edu/abs/2020arXiv200715633A) you need to enable S_8 sampling by adding the following lines to the for loop starting in line 789 of `/your/path/to/montepython_public/montepython/data.py`:
```python
if elem == 'S_8':
    h = self.cosmo_arguments['h']
    # infer sigma8 from S_8, h, omega_b, omega_cdm, and omega_nu (assuming one standard massive neutrino and omega_nu=m_nu/93.14)
    omega_b = self.cosmo_arguments['omega_b']
    omega_cdm = self.cosmo_arguments['omega_cdm']
    #
    try:
        omega_nu = self.cosmo_arguments['m_ncdm'] / 93.14
    except:
        omega_nu = 0.
    self.cosmo_arguments['sigma8'] = self.cosmo_arguments['S_8'] * math.sqrt((0.3*h**2) / (omega_b+omega_cdm+omega_nu))
    del self.cosmo_arguments[elem]
```

This likelihood is equivalent to the one in [https://github.com/BStoelzner/KiDS-1000_MontePython_likelihood](https://github.com/BStoelzner/KiDS-1000_MontePython_likelihood). Additionally, this repository conbtains the '_2cosmos' likelihood modules that were used in Section B.2 of [Asgari et al. 2020](https://ui.adsabs.harvard.edu/abs/2020arXiv200715633A) for a consistency analysis following the methodology developed in [Köhlinger et al. 2019 (MNRAS, 484, 3126)](http://adsabs.harvard.edu/abs/2019MNRAS.484.3126K) with the modified 'Monte Python 2cosmos' version of Monte Python, i.e. [montepython_2cosmos_public](https://github.com/fkoehlin/montepython_2cosmos_public)

WARNING: This likelihood only produces valid results for `\Omega_k = 0`, i.e. flat cosmologies!
