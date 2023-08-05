#include "KernelFunctions.h"
#include "RMSDCalculationData.h"
#include "RMSDTools.h"

#include <iostream>
using namespace std;

/**
 * Given a set of calculation coordinates which have already been superposed, the function
 * rewrites the RMSD calculation to be the minimum RMSD of all the possible symmetric
 * structures.
 *
 * \param reference_conformation_number Is the index of the reference conformation in the
 *
 * \param rmsd The array storing the rmsds
 *
 * \param data The RMSD data object containing all the details of the calculation.
 *
 */
void KernelFunctions::handleSymmetriesWithCalcCoords(
				int reference_conformation_number,
				double* rmsd,
				RMSDCalculationData* data){

	double* calc_reference = data->getCalculationConformationAt(reference_conformation_number);

	for (int i = reference_conformation_number + 1; i < data->numberOfConformations; ++i) {

		double* calc_conformation_coords = data->getCalculationConformationAt(i);

		rmsd[i - (reference_conformation_number + 1)] = RMSDTools::calcMinRMSDOfAllSymmetryGroups(
				calc_reference,
				calc_conformation_coords,
				data->atomsPerCalculationConformation,
				data->symmetryGroups);
	}
}
