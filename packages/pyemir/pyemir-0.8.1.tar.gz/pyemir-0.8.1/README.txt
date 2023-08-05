
This is PyEmir, the data reduction pipeline for EMIR. 

PyEmir is distributed under GNU GPL, either version 3 of the License, 
or (at your option) any later version. See the file COPYING for details.

PyEmir requires the following packages installed in order to
be able to be installed and work properly:

 - setuptools (http://peak.telecommunity.com/DevCenter/setuptools)
 - numpy (http://numpy.scipy.org/) 
 - scipy (http://www.scipy.org)
 - astropy (http://www.astropy.org/)
 - numina (http://guaix.fis.ucm.es/hg/numina)
 - photutils (https://github.com/sergiopasra/photutils/tree/numpy18) [1]

EMIR is a wide-field, near-infrared, multi-object spectrograph proposed 
for the Nasmyth focus of GTC. It will allow observers to obtain from tens to 
hundreds of intermediate resolution spectra simultaneously, in the 
nIR bands Z, J, H and K. A multi-slit mask unit will be used for target acquisition. 
EMIR is designed to address the science goals of the proposing team and 
of the Spanish community at large. 

Webpage: https://guaix.fis.ucm.es/projects/emir
Maintainer: sergiopr@fis.ucm.es            
      
[1] This particular branch of photutils is required due a bug in the main package
