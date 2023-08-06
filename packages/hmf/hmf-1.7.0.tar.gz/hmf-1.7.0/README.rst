===
hmf
===

**The halo mass function calculator**

.. image:: https://travis-ci.org/steven-murray/hmf.png?branch=master   
		:target: https://travis-ci.org/steven-murray/hmf
.. image:: https://pypip.in/d/hmf/badge.png
        :target: https://pypi.python.org/pypi/hmf/
.. image:: https://pypip.in/v/hmf/badge.png
        :target: https://pypi.python.org/pypi/hmf/
        
`hmf` is a python application that provides a flexible and simple way to calculate the 
Halo Mass Function for any input cosmology, redshift, dark matter model, virial
overdensity or several other variables. Addition of further variables should be simple. 

It is also the backend to `HMFcalc`, the online HMF calculator at http://hmf.icrar.org.

Documentation
-------------
You can find the documentation at http://hmf.readthedocs.org

Attribution
-----------
Please cite `Murray, Power and Robotham (2013)
<http://http://arxiv.org/abs/1306.6721>`_ if you find this code useful in your
research.

License
-------
Copyright (c) 2014, Steven Murray. 

See LICENSE.txt for details.


HISTORY
-------
1.7.0 - October 28, 2014
		Modified get_hmf to be more general
		Moved get_hmf and related functions to "functional.py"
		Very much updated fitting routines, in class structure
		Made fitting_functions more flexible and model-like.
		
1.6.2 - September 16, 2014
		Fixed bug in Behroozi fit which caused an infinite recursion
		Better Singleton labelling in get_hmf
		New HALOFIT option for original co-oefficients from Smith+03
		Much cleaning of mass function integrations. New separate module for it.
		IMPORTANT: Removal of nltm routine altogether, as it is inconsistent.
		IMPORTANT: mltm now called rho_ltm, and mgtm called rho_gtm
		IMPORTANT: Definition of rho_ltm now assumes all mass is in halos.
		Tests fixed for new cumulants.
		Behroozi-specific modifications moved to Behroozi class
		New property _fit which is the actual class for mf_fit
		
1.6.1 - September 8, 2014
		Fixed "transfer" property
		Updates fixed for transfer_fit
		Updates fixed for nu
		Better get_hmf function
		Fixed cache bug where unexecuted branches caused some properties to be misinterpreted
		Fixed bug in CAMB transfer options, where defaults would overwrite user-given values (introduced in 1.6.0)
		Fixed dependence on transfer_options
		Fixed typo in Tinker10 fit at z = 0
		
		 
1.6.0 - August 19, 2014
        Completely re-worked caching module to be easier to code and faster.
        New Tinker10 fit (Tinker renamed Tinker08, but Tinker still available)
        Fixed all tests. 
        Better Cosmology class -- more input combinations available.
        
1.5.0 - May 08, 2014
		Introduced _cache module
		Extracts all caching logic to a separate module which defines 
		decorators -- much simpler coding!
		
1.4.5 - January 24, 2014
		Fixed a bug on updating delta_c
		Added Behroozi alias to fits
		Added get_hmf function to tools.py -- easy iteration over models!
		Added hmf script which provides cmd-line access to most functionality.
		Changed kmax and k_per_logint back to have transfer__ prefix.
		Changed default kmax and k_per_logint values a little higher for accuracy.
		
1.4.4 - January 23, 2014
		Fixed a bug in the Tinker function (log was meant to be log10)
			-- thanks to Sebastian Bocquet for pointing this out!
		Updated this README
		Made updating Cosmology simpler.
		Added ability to change the default cosmology parameters
		Fixed a bug in updating n and sigma_8 on their own (introduced in 1.4.0)
		Fixed a bug when using a file for the transfer function.
		
1.4.3 - January 10, 2014
		Changed license in setup
		
1.4.2 - January 10, 2014
		Mocked imports of cosmolopy for setup
		Cleaner imports of cosmolopy
		
1.4.1 - January 10,2014
		Updated setup requirements and fixed a few tests
		
1.4.0 - January 10, 2014
		Upgraded API once more. 
		Now Perturbations --> MassFunction
		Added transfer.py which handles all k-based quantities
		Upgraded docs significantly.
		
1.3.1 - January 06, 2014
		Fixed bug in transfer read-in introduced in 1.3.0
		
1.3.0 - January 03, 2014
		A few more documentation updates (especially tools.py)
		Removed new_k_bounds function from tools.py
		Added `w` parameter to cosmolopy dictionary in `cosmo.py`
		Changed cosmography significantly to use cosmolopy in general
		Fixed a pretty bad bug where updating h/H0 would crash the program if
		only one of omegab/omegac was updated alongside it
		Generally tidied up some of the update mechanisms.
		API CHANGE: cosmography.py no longer exists -- I've chosen to utilise
		cosmolopy more heavily here.
		Added Travis CI usage
		Fixed a compatibility issue with older versions of numpy in cumulative
		functions
		
1.2.2 - December 10, 2013
		Bug in "EH" transfer function call
		
1.2.1 - December 6, 2013
		Small bugfixes to update() method
		
1.2.0 - December 5, 2013
		Major documentation overhaul -- most docstrings are now in Sphinx/numpydoc format
		Addition of cosmo module, which deals with the cosmological parameters in a cleaner way
		Some tidying up of several functions.
		
1.1.10- October 29, 2013
		Fixed bug in mltm property
		Better updating -- checks if update value is actually different.
		Now performs a check to see if mass range is inside fit range.
		
1.1.9 - October 4, 2013
		Fixed some issues with n(<m) and M(<m) causing them to give NaN's
		
1.1.85- October 2, 2013
		The normalization of the power spectrum now saved as an attribute (mostly
		for use with the hod package... coming soon ;)
		
1.1.8 - September 19, 2013
		Fixed small bug in SMT function which made it crash
		
1.1.7 - September 19, 2013
		Updated "ST" fit to "SMT" fit to avoid confusion. "ST" is still available for now.
		Now uses trapezoid rule for integration as it is faster.
		
1.1.6 - September 05, 2013
		Modified comments to reflect parameters
		Couple of bugfixes for fitting_functions.py
		Included an option to use delta_halo as compared to critical rather than mean density (thanks to A. Vikhlinin and anonymous referree)
		Fixed mass range of Tinker (thanks to J. Tinker and anonymous referee for this)
		
1.1.5 - September 03, 2013
		Fixed bug in mgtm (thanks to J. Mirocha)
		Fixed an embarrassing error in Reed07 fitting function
		Fixed a bug in which dndlnm and its dependents (ngtm, etc..) were calculated wrong
		if dndlog10m was called first.
		Added a whole suite of tests against genmf that actually work
		Fixed error in which for some choices of M, the whole extension in ngtm would be NAN and give error
		
1.1.4 - August 27, 2013
		Added ability to change resolution in CAMB from hmf interface
		(This requires a re-install of pycamb to the newest version on the fork)
		
1.1.3 - August 7, 2013
		Added Behroozi Fit (thanks to P. Behroozi)
		
1.1.2 - July 02, 2013
		Ability to calculate fitting functions to whatever mass you want (BEWARE!!)
		Small bugfix
		
1.1.1 - July 02, 2013
		Corrections to Watson fitting function from latest update on arXiv (thanks to W. Watson)
		** Fixed units for k and transfer function ** (Thanks to A. Knebe)
		Improved docstring for Perturbations class
		Added Eisenstein-Hu fit to the transfer function
		
1.1.0 - June 27, 2013
		Massive overhaul of structure
		Now dependencies are tracked throughout the program, making updates even faster
		
1.0.10- June 24, 2013
		Added dependence on Delta_vir to Tinker
		
1.0.9 - June 19, 2013
		Fixed an error with an extra ln(10) in the mass function (quoted as dn/dlnM but actually outputting dn/dlog10M)
		
1.0.8 - June 19, 2013
		Took out log10 from cumulative mass functions
		Better cumulative mass function logic
		
1.0.6 - June 19, 2013
		Fixed cumulative mass functions (extra factor of M was in there)
		
1.0.4 - June 6, 2013
		Added Bhattacharya fitting function
		Fixed concatenation of list and dict issue
		
1.0.2 - May 21, 2013
		Fixed some warnings for non-updated variables passed to update()
		
1.0.1 - May 20, 2013
		Added better warnings for non-updated variables passed to update()
		Made default cosmology WMAP7
		
0.9.99- May 10, 2013
		Added warning for k*R limits
		Couple of minor bugfixes
		**Important** Angulo fitting function corrected (arXiv version had a typo).
		
0.9.97- April 15, 2013
		Urgent Bugfix for updating cosmology (for transfer functions)
		
0.9.96- April 11, 2013
		Few bugfixes
		
0.9.95- April 09, 2013
		Added cascading variable changes for optimization
		Added this README
		Added update() function to simply change parameters using cascading approach
		
0.9.9 - April 08, 2013
        First version in its own package
        Added pycamb integration
        Removed fitting function from being a class variable
        Removed overdensity form being a class variable
        
0.9.7 - March 18, 2013
        Modified set_z() so it only does calculations necessary when z changes
        Made calculation of dlnsdlnM in init since it is same for all z
        Removed mean density redshift dependence
        
0.9.5 - March 10, 2013
        The class has been in the works for almost a year now, but it currently
        will calculate a mass function based on any of several fitting functions.
