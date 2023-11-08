# dpdprops

A python package for mapping parameters between:
* DPD and fluid properties.
* parameters of coarsed grained models for elastic membranes and macroscopic membrane parameters.

## Installation

	python -m pip install dpdprops


## DPD <-> fluid properties

The mapping is computed as explained in the appendix of

	Groot, Robert D., and Patrick B. Warren.
	"Dissipative particle dynamics: Bridging the gap between atomistic and mesoscopic simulation."
	The Journal of chemical physics 107.11 (1997): 4423-4435.

The integrals are adapted to match the modified kernel of the dissipative forces, with the general enveloppe coeficient `s`.
See also:

	Amoudruz, L., 2022. 
	Simulations and Control of Artificial Microswimmers in Blood 
	(Doctoral dissertation, ETH Zurich).


## Membranes

Wrapper classes to hold red blood cell membrane parameters.
The classes provide a helper to convert from physical quantities to simulation quantities.
Holds default values obtained from the following studies:

	Economides, A., Arampatzis, G., Alexeev, D., Litvinov, S., Amoudruz, L., 
	Kulakova, L., Papadimitriou, C. and Koumoutsakos, P., 2021. 
	Hierarchical Bayesian uncertainty quantification for a model of the red blood cell. 
	Physical Review Applied, 15(3), p.034062.


	Amoudruz, L., Economides, A., Arampatzis, G. and Koumoutsakos, P., 2023. 
	The stress-free state of human erythrocytes: Data-driven inference of a transferable RBC model. 
	Biophysical Journal, 122(8), pp.1517-1525.
