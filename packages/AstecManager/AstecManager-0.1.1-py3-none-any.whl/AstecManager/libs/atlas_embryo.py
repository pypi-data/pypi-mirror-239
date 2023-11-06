import copy
import os
import sys
import statistics

from operator import itemgetter

import numpy as np
import sklearn.linear_model as sklm

import astec.utils.common as common
import astec.utils.properties as properties
import astec.utils.diagnosis as udiagnosis
import astec.utils.ioproperties as ioproperties

import ascidian.core.symmetry as symmetry

monitoring = common.Monitoring()


############################################################
#
#
#
############################################################

def get_division_time_by_cell_atlas(atlases):
    """

    Parameters
    ----------
    atlases

    Returns
    -------
    A dictionary indexed by cell names. Each entry is a also a dictionary indexed by atlas names,
    whose value is the time of division.
    """
    proc = "get_division_time_by_cell_atlas"
    timepoints = {}
    ref_atlases = atlases.get_atlases()
    for a in ref_atlases:
        div = 10 ** ref_atlases[a].time_digits_for_cell_id
        cell_name = ref_atlases[a].cell_name
        if cell_name is None or len(cell_name) == 0:
            continue
        cell_lineage = ref_atlases[a].cell_lineage
        temporal_coefficients = ref_atlases[a].temporal_alignment
        divisions = [c for c in cell_lineage if len(cell_lineage[c]) == 2]
        for d in divisions:
            if d not in cell_name:
                continue
            #
            # pool together '_' and '*'
            #
            cname = cell_name[d]
            aname = a
            if cname not in timepoints:
                timepoints[cname] = {}
            if aname in timepoints[cname]:
                msg = "weird, '" + str(aname) + "' is already in division of cell '" + str(cname) + "'"
                monitoring.to_log_and_console("    " + proc + ": " + msg)
            else:
                acq_time = int(d) // div
                t = temporal_coefficients[0] * acq_time + temporal_coefficients[1]
                timepoints[cname][aname] = [t]
    return timepoints


def _diagnosis_division_timepoint(atlases, parameters):
    #
    # timepoints is a dictionary indexed by cell names (without '_' or '*'). Each entry is a list of tuples
    # (time of division, atlas name + [_ or *]) sorted by increasing time
    # timepoints is a dictionary indexed by cell names (with '_' or '*'). Each entry is a dictionary
    # indexed by atlas name, and values is a list of times of division
    #
    timepoints = get_division_time_by_cell_atlas(atlases)
    #
    # intra-embryo largest (normalized) time interval
    #
    intra_timepoints = {}
    for d in timepoints:
        # d left and right
        dlr = d[:-1]
        if dlr not in intra_timepoints:
            intra_timepoints[dlr] = {}
        for a in timepoints[d]:
            for t in timepoints[d][a]:
                intra_timepoints[dlr][a] = intra_timepoints[dlr].get(a, []) + [t]

    #
    # intra_timepoints[dlr][a] : dictionary (cell name without * or _) of dictionary (atlas names) of time divisions
    #
    intra_division_time_interval = []
    for d in intra_timepoints:
        for a in intra_timepoints[d]:
            if len(intra_timepoints[d][a]) != 2:
                continue
            intra_division_time_interval += [(d, a, abs(intra_timepoints[d][a][0] - intra_timepoints[d][a][1]))]
    intra_division_time_interval = sorted(intra_division_time_interval, key=itemgetter(2), reverse=True)

    #
    # inter-embryo largest (normalized) time interval
    #
    inter_timepoints = {}
    for d in timepoints:
        dlr = d[:-1]
        if dlr not in inter_timepoints:
            inter_timepoints[dlr] = []
        for a in timepoints[d]:
            for t in timepoints[d][a]:
                inter_timepoints[dlr] += [t]

    inter_division_time_interval = []
    for d in inter_timepoints:
        inter_division_time_interval += [(d, max(inter_timepoints[d]) - min(inter_timepoints[d]))]
    inter_division_time_interval = sorted(inter_division_time_interval, key=itemgetter(1), reverse=True)

    monitoring.to_log_and_console("")
    monitoring.to_log_and_console("  === division (normalized) time interval diagnosis === ")

    monitoring.to_log_and_console("  - intra-embryo largest (normalized) time interval")
    n = parameters.items
    if n > len(intra_division_time_interval):
        n = len(intra_division_time_interval)
    for i in range(n):
        msg = "    cell " + str(intra_division_time_interval[i][0])
        msg += " '" + str(intra_division_time_interval[i][1]) + "'"
        msg += " time interval = {:.2f}".format(intra_division_time_interval[i][2])
        monitoring.to_log_and_console(msg)
        msg = "       "
        msg += str(intra_division_time_interval[i][1]) + ": "
        for j, e in enumerate(['_', '*']):
            d = str(intra_division_time_interval[i][0]) + e
            msg += str(d) + ": {:.2f}".format(timepoints[d][intra_division_time_interval[i][1]][0])
            if j == 0:
                msg += ", "

        monitoring.to_log_and_console(msg)

    monitoring.to_log_and_console("  - inter-embryo largest (normalized) time interval")
    n = parameters.items
    if n > len(inter_division_time_interval):
        n = len(inter_division_time_interval)
    for i in range(n):
        msg = "    cell " + str(inter_division_time_interval[i][0])
        msg += " time interval = {:.2f}".format(inter_division_time_interval[i][1])
        monitoring.to_log_and_console(msg)
        msg = "       "
        j = 0
        lj = 0
        for e in ['_', '*']:
            d = str(inter_division_time_interval[i][0]) + e
            if d in timepoints:
                lj += len(timepoints[d])
        for e in ['_', '*']:
            d = str(inter_division_time_interval[i][0]) + e
            if d in timepoints:
                for a in timepoints[d]:
                    msg += str(a) + "(" + str(e) + ") at " + "{:.2f}".format(timepoints[d][a][0])
                    if j < lj-1:
                        msg += ", "
                        if j > 0 and (j+1) % 3 == 0:
                            msg += "\n"
                            msg += "       "
                    j += 1
        monitoring.to_log_and_console(msg)
    monitoring.to_log_and_console("  === end of diagnosis === ")
    monitoring.to_log_and_console("")


############################################################
#
#
#
############################################################

class AtlasParameters(udiagnosis.DiagnosisParameters, symmetry.EmbryoSymmetryParameters):

    ############################################################
    #
    # initialisation
    #
    ############################################################

    def __init__(self, prefix=None):

        if "doc" not in self.__dict__:
            self.doc = {}

        udiagnosis.DiagnosisParameters.__init__(self, prefix=prefix)
        symmetry.EmbryoSymmetryParameters.__init__(self, prefix=prefix)

        #
        # atlas general parameters
        #

        doc = "\t List of atlas files. An atlas file is a property file that contains lineage,\n"
        doc += "\t names, and contact surfaces for an embryo."
        self.doc['atlasFiles'] = doc
        self.atlasFiles = []

        doc = "\t Reference atlas. Use for time alignment. If not provide, the first atlas of\n"
        doc += "\t 'atlasFiles' is used as reference. Warning, the reference atlas has to be in\n"
        doc += "\t 'atlasFiles' list also."
        self.doc['referenceAtlas'] = doc
        self.referenceAtlas = None

        doc = "\t Output directory where to write atlas-individualized output files,\n"
        doc += "\t ie morphonet selection files or figure files."
        self.doc['outputDir'] = doc
        self.outputDir = "."

        doc = "\t True or False. Performs some diagnosis when reading an additional property file \n"
        doc += "\t into the atlases. Incrementing the verboseness ('-v' in the command line) may give\n"
        doc += "\t more details."
        self.doc['atlas_diagnosis'] = doc
        self.atlas_diagnosis = False

        doc = "\t if True, generate python files (prefixed by 'figures_') that generate figures.\n"
        doc += "\t Those files will be saved into the 'outputDir' directory.\n"
        doc += "\t 'generate_figure' can be\n"
        doc += "\t - a boolean value: if True, all figure files are generated; if False, none of them\n"
        doc += "\t - a string: if 'all', all figure files are generated; else, only the specified\n"
        doc += "\t   figure file is generated (see below for the list)\n"
        doc += "\t - a list of strings: if 'all' is in the list, all figure files are generated;\n"
        doc += "\t   else, only the specified figure files are generated (see below for the list)\n"
        doc += "\t List of figures:\n"
        doc += "\t 'cell-distance-along-branch': plot the cell-to-cell distance between successive\n"
        doc += "\t    along a branch (a cell without division) wrt the distance to the first cell.\n"
        doc += "\t    Cell neighborhoods are expressed with the neighbors of the first cell of the branch\n"
        doc += "\t    (thus it ignores divisions occurring in the cell neighborhood during the cell life).\n"
        doc += "\t 'cell-number-wrt-time': plot the number of cells wrt time point (ie image indices)\n"
        doc += "\t    without and with temporal registration wrt to the total cell count\n"
        doc += "\t    (allows to assess the temporal registration)\n"
        doc += "\t 'epidermis-cell-number-wrt-time': plot the number of epidermis cells wrt time point\n"
        doc += "\t     (ie image indices) without and with temporal registration wrt to the epidermis cell count\n"
        doc += "\t     (allows to assess the temporal registration)\n"
        doc += "\t 'name-composition-wrt-time': plot the number of names wrt time point (normalized time,\n"
        doc += "\t    ie after temporal registration), and separate between names present in all embryos\n"
        doc += "\t    and others"
        doc += "\t 'neighbors-wrt-cell-number': plot the cell number in the cell neighborhood wrt\n"
        doc += "\t    the total cell number in the embryo\n"
        doc += "\t 'cell-distance-histograms': plot cell-to-cell distance histograms.\n"
        doc += "\t    warning: it may be long.\n"
        doc += "\t 'division-distance-histograms': plot division-to-division distance histograms.\n"
        doc += "\t 'distance-histograms': plot cell-to-cell distance histograms, \n"
        doc += "\t    as well as division-to-division distance histograms.\n"
        doc += "\t    warning: it may be long.\n"
        doc += "\t 'division-dendrograms': draw a dendrogram per division where atlases are grouped with\n"
        doc += "\t    distance between divisions\n"
        doc += "\t 'embryo-volume': plot the embryo volume (in voxel)\n"
        doc += "\t    without and with temporal registration (computed from cell number)\n"
        doc += "\t 'symmetry-axis': lot the error of the best symmetry axes (the closest to the one\n"
        doc += "\t    estimated with cell names), as well as its rank with respect to the distribution value\n"
        doc += "\t 'division-timepoint':\n"
        self.doc['generate_figure'] = doc
        self.generate_figure = False

        doc = "\t suffix used to named the above python files as well as the generated figures."
        self.doc['figurefile_suffix'] = doc
        self.figurefile_suffix = ""

        #
        # parameters dedicated to extract neighborhoods
        #

        doc = "\t Delay from the division to extract the neighborhooods used for atlas building,\n"
        doc += "\t and thus for naming.\n"
        doc += "\t 0 means right after the division.\n"
        doc += "\t negative values means that the delay is counted backwards from the end of the branch.\n"
        self.doc['name_delay_from_division'] = doc
        self.name_delay_from_division = 3

        doc = "\t Delay from the division to extract the neighborhooods used for naming confidence.\n"
        doc += "\t 0 means right after the division.\n"
        doc += "\t negative values means that the delay is counted backwards from the end of the branch.\n"
        self.doc['confidence_delay_from_division'] = doc
        self._confidence_delay_from_division = None

        #
        # parameters dedicated to build neighborhoods
        #
        doc = "\t if 'True', add the symmetric neighborhood as additional exemplar.\n"
        doc += "\t It means that left and right embryo hemisphere are considered together"
        self.doc['add_symmetric_neighborhood'] = doc
        self.add_symmetric_neighborhood = True

        doc = "\t if 'True', differentiate the cells of the symmetric half-embryo.\n"
        doc += "\t If 'False', consider all the cells of the symmetric half-embryo\n"
        doc += "\t as a single cell.\n"
        self.doc['differentiate_other_half'] = doc
        self.differentiate_other_half = True

        doc = "\t The same cell has different neighbors from an atlas to the other.\n"
        doc += "\t If 'True' build and keep an unique common neighborhood (set of\n"
        doc += "\t neighbors) for all atlases by keeping the closest ancestor for\n"
        doc += "\t neighboring cells. Eg, if a division has occurred in some embryos\n"
        doc += "\t and not in others, daughter cells will be fused so that all\n"
        doc += "\t neighborhoods only exhibit the parent cell."
        self.doc['use_common_neighborhood'] = doc
        self.use_common_neighborhood = True

        #
        #
        #
        doc = "\t Embryos/atlases have different volumes, and their volume decrease with time.\n"
        doc += "\t To compare surfaces and/or volumes, a normalization is required. I can be chosen among:\n"
        doc += "\t - None: no normalization (for test purpose)\n"
        doc += "\t - 'local': normalization by the cell surface\n"
        doc += "\t   The normalization factor is then different from cell to cell within a embryo,\n"
        doc += "\t   and obviously for the two daughter cells resulting from a division\n"
        doc += "\t - 'global': normalization by embryo volume\n"
        doc += "\t   The normalization factor is for all the cells from the same time point within a embryo.\n"
        doc += "\t   It changes along time to compensate for the volume decrease."
        self.doc['cell_normalization'] = doc
        self.cell_normalization = 'global'

    ############################################################
    #
    # properties
    #
    ############################################################

    @property
    def confidence_delay_from_division(self):
        """
        The cell lineage, as in the property file
        Returns
        -------

        """
        if self._confidence_delay_from_division is None:
            self._confidence_delay_from_division = self.name_delay_from_division
        return self._confidence_delay_from_division

    @confidence_delay_from_division.setter
    def confidence_delay_from_division(self, delay_from_division):
        self._confidence_delay_from_division = delay_from_division
        return

    ############################################################
    #
    # print / write
    #
    ############################################################

    def print_parameters(self):
        print("")
        print('#')
        print('# AtlasParameters')
        print('#')
        print("")

        common.PrefixedParameter.print_parameters(self)

        udiagnosis.DiagnosisParameters.print_parameters(self)
        symmetry.EmbryoSymmetryParameters.print_parameters(self)

        self.varprint('atlasFiles', self.atlasFiles)
        self.varprint('referenceAtlas', self.referenceAtlas)
        self.varprint('outputDir', self.outputDir)

        self.varprint('atlas_diagnosis', self.atlas_diagnosis)

        self.varprint('generate_figure', self.generate_figure)
        self.varprint('figurefile_suffix', self.figurefile_suffix)

        self.varprint('name_delay_from_division', self.name_delay_from_division)
        self.varprint('confidence_delay_from_division', self.confidence_delay_from_division)

        self.varprint('add_symmetric_neighborhood', self.add_symmetric_neighborhood)
        self.varprint('differentiate_other_half', self.differentiate_other_half)
        self.varprint('use_common_neighborhood', self.use_common_neighborhood)

        self.varprint('cell_normalization', self.cell_normalization)
        print("")

    def write_parameters_in_file(self, logfile):
        logfile.write("\n")
        logfile.write("# \n")
        logfile.write("# AtlasParameters\n")
        logfile.write("# \n")
        logfile.write("\n")

        common.PrefixedParameter.write_parameters_in_file(self, logfile)

        udiagnosis.DiagnosisParameters.write_parameters_in_file(self, logfile)
        symmetry.EmbryoSymmetryParameters.write_parameters_in_file(self, logfile)

        self.varwrite(logfile, 'atlasFiles', self.atlasFiles, self.doc.get('atlasFiles', None))
        self.varwrite(logfile, 'referenceAtlas', self.referenceAtlas, self.doc.get('referenceAtlas', None))
        self.varwrite(logfile, 'outputDir', self.outputDir, self.doc.get('outputDir', None))

        self.varwrite(logfile, 'atlas_diagnosis', self.atlas_diagnosis, self.doc.get('atlas_diagnosis', None))

        self.varwrite(logfile, 'generate_figure', self.generate_figure, self.doc.get('generate_figure', None))
        self.varwrite(logfile, 'figurefile_suffix', self.figurefile_suffix, self.doc.get('figurefile_suffix', None))

        self.varwrite(logfile, 'name_delay_from_division', self.name_delay_from_division,
                      self.doc.get('name_delay_from_division', None))
        self.varwrite(logfile, 'confidence_delay_from_division', self.confidence_delay_from_division,
                      self.doc.get('confidence_delay_from_division', None))

        self.varwrite(logfile, 'add_symmetric_neighborhood', self.add_symmetric_neighborhood,
                      self.doc.get('add_symmetric_neighborhood', None))
        self.varwrite(logfile, 'differentiate_other_half', self.differentiate_other_half,
                      self.doc.get('differentiate_other_half', None))
        self.varwrite(logfile, 'use_common_neighborhood', self.use_common_neighborhood,
                      self.doc.get('use_common_neighborhood', None))

        self.varwrite(logfile, 'cell_normalization', self.cell_normalization, self.doc.get('cell_normalization', None))
        logfile.write("\n")
        return

    def write_parameters(self, log_file_name):
        with open(log_file_name, 'a') as logfile:
            self.write_parameters_in_file(logfile)
        return

    ############################################################
    #
    # update
    #
    ############################################################

    def update_from_parameters(self, parameters):

        udiagnosis.DiagnosisParameters.update_from_parameters(self, parameters)
        symmetry.EmbryoSymmetryParameters.update_from_parameters(self, parameters)

        self.atlasFiles = self.read_parameter(parameters, 'atlasFiles', self.atlasFiles)
        self.atlasFiles = self.read_parameter(parameters, 'referenceFiles', self.atlasFiles)
        self.referenceAtlas = self.read_parameter(parameters, 'referenceAtlas', self.referenceAtlas)

        self.outputDir = self.read_parameter(parameters, 'outputDir', self.outputDir)

        self.atlas_diagnosis = self.read_parameter(parameters, 'atlas_diagnosis', self.atlas_diagnosis)
        self.atlas_diagnosis = self.read_parameter(parameters, 'diagnosis_properties', self.atlas_diagnosis)
        self.atlas_diagnosis = self.read_parameter(parameters, 'naming_diagnosis', self.atlas_diagnosis)
        self.atlas_diagnosis = self.read_parameter(parameters, 'diagnosis_naming', self.atlas_diagnosis)

        self.generate_figure = self.read_parameter(parameters, 'generate_figure', self.generate_figure)
        self.figurefile_suffix = self.read_parameter(parameters, 'figurefile_suffix', self.figurefile_suffix)

        self.name_delay_from_division = self.read_parameter(parameters, 'name_delay_from_division',
                                                            self.name_delay_from_division)
        self.name_delay_from_division = self.read_parameter(parameters, 'delay_from_division',
                                                            self.name_delay_from_division)
        self.confidence_delay_from_division = self.read_parameter(parameters, 'confidence_delay_from_division',
                                                                  self.confidence_delay_from_division)
        self.confidence_delay_from_division = self.read_parameter(parameters, 'delay_from_division',
                                                                  self.confidence_delay_from_division)

        self.add_symmetric_neighborhood = self.read_parameter(parameters, 'add_symmetric_neighborhood',
                                                              self.add_symmetric_neighborhood)
        self.differentiate_other_half = self.read_parameter(parameters, 'differentiate_other_half',
                                                            self.differentiate_other_half)
        self.use_common_neighborhood = self.read_parameter(parameters, 'use_common_neighborhood',
                                                           self.use_common_neighborhood)

        self.cell_normalization = self.read_parameter(parameters, 'cell_normalization', self.cell_normalization)

    def update_from_parameter_file(self, parameter_file):
        if parameter_file is None:
            return
        if not os.path.isfile(parameter_file):
            print("Error: '" + parameter_file + "' is not a valid file. Exiting.")
            sys.exit(1)

        parameters = common.load_source(parameter_file)
        self.update_from_parameters(parameters)


############################################################
#
# Atlas = one property file
#
############################################################

class Atlas(object):
    def __init__(self, atlas_properties=None, time_digits_for_cell_id=4, verbose=False):
        proc = "Atlas.init"

        self.time_digits_for_cell_id = time_digits_for_cell_id
        self._properties = {'temporal_alignment': {'default': (1.0, 0.0)}, 'volume_local_estimation': (0.0, 1.0),
                            'target_volume': 6000000}

        if isinstance(atlas_properties, dict):
            if 'cell_lineage' in atlas_properties:
                self.cell_lineage = atlas_properties['cell_lineage']
            elif verbose:
                monitoring.to_log_and_console(str(proc) + ": 'cell_lineage' was not in dictionary")
            if 'cell_name' in atlas_properties:
                self.cell_name = atlas_properties['cell_name']
            elif verbose:
                monitoring.to_log_and_console(str(proc) + ": 'cell_name' was not in dictionary")
            #
            # volume linear fit has to be at the beginning to get the voxel size correction
            #
            if 'cell_volume' in atlas_properties:
                self.cell_volume = atlas_properties['cell_volume']
                self._volume_local_fitting()
                self.rectified_cell_volume = atlas_properties['cell_volume']
            elif verbose:
                monitoring.to_log_and_console(str(proc) + ": 'cell_volume' was not in dictionary")
            if 'cell_contact_surface' in atlas_properties:
                self.cell_contact_surface = atlas_properties['cell_contact_surface']
                self.rectified_cell_contact_surface = atlas_properties['cell_contact_surface']
            elif verbose:
                monitoring.to_log_and_console(str(proc) + ": 'cell_contact_surface' was not in dictionary")
            if 'cell_barycenter' in atlas_properties:
                self.cell_barycenter = atlas_properties['cell_barycenter']
                self.rectified_cell_barycenter = atlas_properties['cell_barycenter']
            elif verbose:
                monitoring.to_log_and_console(str(proc) + ": 'cell_barycenter' was not in dictionary")

    ############################################################
    #
    # Property management
    #
    ############################################################

    def property_list(self):
        return self._properties.keys()

    def get_property(self):
        return self._properties

    def _del_one_property(self, property_name):
        if not isinstance(property_name, str):
            return
        if property_name in self._properties:
            del self._properties[property_name]
        return

    def del_property(self, property_name):
        if isinstance(property_name, str):
            self._del_one_property(property_name)
        elif isinstance(property_name, list):
            for n in property_name:
                self._del_one_property(n)
        return

    ############################################################
    #
    # @property
    # From property file
    # - cell_lineage
    # - cell_name
    # - cell_volume
    # - cell_contact_surface
    # - cell_barycenter
    # Computed ones
    # - temporal_alignment: tuple (a, b). Time (at+b) of the embryo corresponds to
    #   the time t of a reference embryo
    # - volume_local_estimation: tuple (a, b). Embryo volume along time is fitted by (at+b)
    #   allows to compute a time-varying scaling factor to get a constant embryo volume
    #   along time (see self.get_voxelsize_correction())
    # - target_volume: this is the targeted contant volume to get a constant embryo volume
    #   along time (see self.get_voxelsize_correction())
    #
    ############################################################

    @property
    def cell_lineage(self):
        """
        The cell lineage, as in the property file
        Returns
        -------

        """
        if 'cell_lineage' in self._properties:
            return self._properties['cell_lineage']
        return None

    @cell_lineage.setter
    def cell_lineage(self, atlas_properties):
        self._properties['cell_lineage'] = copy.deepcopy(atlas_properties)
        return

    @property
    def cell_name(self):
        """
        The cell names, as in the property file
        Returns
        -------

        """
        if 'cell_name' in self._properties:
            return self._properties['cell_name']
        return None

    @cell_name.setter
    def cell_name(self, atlas_properties):
        self._properties['cell_name'] = copy.deepcopy(atlas_properties)
        return

    @property
    def cell_volume(self):
        """
        The cell volumes, as in the property file
        Returns
        -------

        """
        if 'cell_volume' in self._properties:
            return self._properties['cell_volume']
        return None

    @cell_volume.setter
    def cell_volume(self, atlas_properties):
        self._properties['cell_volume'] = copy.deepcopy(atlas_properties)
        return

    @property
    def rectified_cell_volume(self):
        """
        The cell volumes, as in the property file
        Returns
        -------

        """
        if 'rectified_cell_volume' in self._properties:
            return self._properties['rectified_cell_volume']
        return None

    @rectified_cell_volume.setter
    def rectified_cell_volume(self, atlas_properties):
        correction = {}
        vols = {}
        for c in atlas_properties:
            timepoint = int(c) // (10 ** self.time_digits_for_cell_id)
            if timepoint in correction:
                m = correction[timepoint]
            else:
                voxelsize = self.get_voxelsize_correction(timepoint)
                m = voxelsize * voxelsize * voxelsize
                correction[timepoint] = m
            vols[c] = atlas_properties[c] * m
        self._properties['rectified_cell_volume'] = vols
        return

    @property
    def cell_contact_surface(self):
        """
        The cell contact surfaces, as in the property file
        Returns
        -------

        """
        if 'cell_contact_surface' in self._properties:
            return self._properties['cell_contact_surface']
        return None

    @cell_contact_surface.setter
    def cell_contact_surface(self, atlas_properties):
        self._properties['cell_contact_surface'] = copy.deepcopy(atlas_properties)
        return

    @property
    def rectified_cell_contact_surface(self):
        """
        The cell contact surfaces, as in the property file
        Returns
        -------

        """
        if 'rectified_cell_contact_surface' in self._properties:
            return self._properties['rectified_cell_contact_surface']
        return None

    @rectified_cell_contact_surface.setter
    def rectified_cell_contact_surface(self, atlas_properties):
        correction = {}
        surfs = {}
        for c in atlas_properties:
            timepoint = int(c) // (10 ** self.time_digits_for_cell_id)
            if timepoint in correction:
                m = correction[timepoint]
            else:
                voxelsize = self.get_voxelsize_correction(timepoint)
                m = voxelsize * voxelsize
                correction[timepoint] = m
            surfs[c] = {}
            for d in atlas_properties[c]:
                surfs[c][d] = atlas_properties[c][d] * m
        self._properties['rectified_cell_contact_surface'] = surfs
        return

    @property
    def cell_barycenter(self):
        """
        The cell contact surfaces, as in the property file
        Returns
        -------

        """
        if 'cell_barycenter' in self._properties:
            return self._properties['cell_barycenter']
        return None

    @cell_barycenter.setter
    def cell_barycenter(self, atlas_properties):
        self._properties['cell_barycenter'] = copy.deepcopy(atlas_properties)
        return

    @property
    def rectified_cell_barycenter(self):
        if 'rectified_cell_barycenter' in self._properties:
            return self._properties['rectified_cell_barycenter']
        return None

    @rectified_cell_barycenter.setter
    def rectified_cell_barycenter(self, atlas_properties):
        correction = {}
        bars = {}
        for c in atlas_properties:
            timepoint = int(c) // (10 ** self.time_digits_for_cell_id)
            if timepoint in correction:
                m = correction[timepoint]
            else:
                voxelsize = self.get_voxelsize_correction(timepoint)
                m = voxelsize
                correction[timepoint] = m
            bars[c] = []
            for i, v in enumerate(atlas_properties[c]):
                bars[c] += [v * m]
        self._properties['rectified_cell_barycenter'] = bars
        return

    @property
    def cell_fate(self):
        if 'cell_fate' in self._properties:
            return self._properties['cell_fate']

        if 'cell_name' in self._properties:
            self._properties = properties.set_fate_from_names(self._properties)
            if 'cell_fate' in self._properties:
                return self._properties['cell_fate']
        return None

    #
    # other properties
    #
    @property
    def temporal_alignment(self):
        if 'temporal_alignment' in self._properties:
            if 'default' in self._properties['temporal_alignment']:
                return self._properties['temporal_alignment']['default']
            return None
        return None

    def set_temporal_alignment(self, v, key='default'):
        if 'temporal_alignment' not in self._properties:
            self._properties['temporal_alignment'] = {}
        self._properties['temporal_alignment'][key] = v

    def get_temporal_alignment(self, key='default'):
        if 'temporal_alignment' not in self._properties:
            return None
        if key is None and 'default' in self._properties['temporal_alignment']:
            return self._properties['temporal_alignment']['default']
        if key not in self._properties['temporal_alignment']:
            return None
        return self._properties['temporal_alignment'][key]

    @property
    def volume_local_estimation(self):
        if 'volume_local_estimation' in self._properties:
            return self._properties['volume_local_estimation']
        return None

    @property
    def target_volume(self):
        if 'target_volume' in self._properties:
            return self._properties['target_volume']
        return None

    @target_volume.setter
    def target_volume(self, volume):
        self._properties['target_volume'] = volume
        return

    @property
    def direction_distribution_maxima(self):
        if 'direction_distribution_maxima' not in self._properties:
            self._properties['direction_distribution_maxima'] = {}
        return self._properties['direction_distribution_maxima']

    ############################################################
    #
    # Properties (end)
    #
    ############################################################

    def get_times(self, n_cells=64, mode='floor'):
        """

        :param n_cells:
        :param mode:
        :return:  time array and a number of cells
          The number of cells is the targeted one, if it exists in the embryo development
          else it is the closest one (with the interpolation mode)
          The time array contains the time points with this cell number
        """
        #
        # get the time range with the specified number of cells
        # if it does not exist, get the time range with the immediate upper ('ceil') or lower ('floor') number of cells
        #
        proc = "Atlas.get_times"
        #
        # count the cells per time
        #
        prop = self.cell_volume
        if prop is None:
            prop = self.cell_contact_surface
        if prop is None:
            msg = "   " + str(proc) + ": " + " no properties?!"
            monitoring.to_log_and_console(msg)
            return None, None

        cells = list(prop.keys())
        cells = sorted(cells)
        cells_per_time = {}
        div = 10 ** self.time_digits_for_cell_id
        for c in cells:
            t = int(c) // div
            cells_per_time[t] = cells_per_time.get(t, 0) + 1
        #
        # sort the cells_per_time dictionary by time
        # assume that cell number will also be in increasing order
        #
        cells_per_time = dict(sorted(cells_per_time.items(), key=lambda item: item[0]))

        #
        # if there are times with the specified number of cells, return them
        #
        times = [t for t in cells_per_time if cells_per_time[t] == n_cells]
        if len(times) > 0:
            return times, n_cells

        #
        # if not, find times with immediate lower and upper number of cells
        #

        mincells = [cells_per_time[t] for t in cells_per_time if cells_per_time[t] < n_cells]
        maxcells = [cells_per_time[t] for t in cells_per_time if cells_per_time[t] > n_cells]

        if mode == 'floor':
            if len(mincells) > 0:
                n_cells = max(mincells)
                times = [t for t in cells_per_time if cells_per_time[t] == n_cells]
                return times, n_cells
            if len(maxcells) > 0:
                n_cells = min(maxcells)
                times = [t for t in cells_per_time if cells_per_time[t] == n_cells]
                return times, n_cells
        elif mode == 'ceil':
            if len(maxcells) > 0:
                n_cells = min(maxcells)
                times = [t for t in cells_per_time if cells_per_time[t] == n_cells]
                return times, n_cells
            if len(mincells) > 0:
                n_cells = max(mincells)
                times = [t for t in cells_per_time if cells_per_time[t] == n_cells]
                return times, n_cells
        msg = "   " + str(proc) + ": " + " unknown estimation mode '" + str(mode) + "'"
        monitoring.to_log_and_console(msg)
        return None, None

    def get_timerange(self, cell_number, change_cell_number=False):

        #
        # get the time range of the floating embryo with the specified number of cells
        #
        lowertimerange, lowerncells = self.get_times(cell_number, mode='floor')
        uppertimerange, upperncells = self.get_times(cell_number, mode='ceil')
        if lowerncells <= cell_number <= upperncells:
            retained_cell_number = cell_number
            if cell_number - lowerncells <= upperncells - cell_number:
                timerange = lowertimerange
            else:
                timerange = uppertimerange
            return retained_cell_number, timerange

        if change_cell_number is False:
            return None, None

        if lowerncells == upperncells:
            retained_cell_number = lowerncells
            timerange = lowertimerange
            return retained_cell_number, timerange

        return None, None

    #
    # temporal alignment of an atlas/embryo with the reference atlas/embryo
    # it consists at finding the time lineage warping based on the cell number
    # so that the cell number at (a * t + b) of the atlas is equal at the one
    # of the reference number at (t)
    #
    def temporally_align_with(self, reference, fate=None):
        """

        :param reference:
            reference atlas to be temporally aligned with.
        :param fate:
        :return:
            Tuple (a, b). Time point t of the atlas at hand is equivalent to the time
            point (at+b) of the reference atlas.
        """
        proc = "Atlas.temporally_align_with"
        if not isinstance(reference, Atlas):
            monitoring.to_log_and_console(str(proc) + ": 'reference' should be of 'Atlas' class")
            return

        if fate is None:
            a, b = properties.temporal_alignment(reference.cell_lineage, self.cell_lineage,
                                                 reference.time_digits_for_cell_id, self.time_digits_for_cell_id)

            self.set_temporal_alignment((a, b))
            return

        #
        #
        #
        ref_cellcount = reference.get_cells_per_time(fate=fate)
        cellcount = self.get_cells_per_time(fate=fate)
        a, b = properties.cellcounts_temporal_alignement(ref_cellcount, cellcount)
        self.set_temporal_alignment((a, b), key=fate)
        return

    #
    #
    #

    def _volume_local_fitting(self):
        div = 10 ** self.time_digits_for_cell_id
        volume = self.cell_volume
        volume_along_time = {}
        #
        # compute embryo volume for each timepoint 't'
        #
        for c in volume:
            t = int(c) // div
            volume_along_time[t] = volume_along_time.get(t, 0) + volume[c]

        #
        # get array of time point (x) and array of volumes (y)
        #
        x = list(volume_along_time.keys())
        x = sorted(x)
        y = [volume_along_time[i] for i in x]

        #
        # robust regression via ransac
        #
        xnp = np.array(x)[:, np.newaxis]
        ynp = np.array(y)[:, np.newaxis]
        ransac = sklm.RANSACRegressor()
        ransac.fit(xnp, ynp)
        self._properties['volume_local_estimation'] = (ransac.estimator_.coef_[0][0], ransac.estimator_.intercept_[0])
        v_coefficients = self.volume_local_estimation
        formula = "{:.3f} * acquisition time + {:.3f}".format(v_coefficients[0], v_coefficients[1])
        msg = "   ... volume fitting = " + formula + "\n"
        msg += "       scaling correction = cubic root( target volume / (" + formula + "))"
        monitoring.to_log_and_console(msg)

    #
    #
    #

    def get_voxelsize_correction(self, timepoint, target_volume=60000000):
        """
        Give the scale to be applied to simulate an embryo of volume 'target_volume'
        - volumes have to be multiplied by scale power 3
        - surfaces have to be multiplied by scale power 2
        Parameters
        ----------
        timepoint
        target_volume

        Returns
        -------

        """
        if 'volume_local_estimation' not in self._properties:
            self._volume_local_fitting()
        if target_volume != self.target_volume:
            self.target_volume = target_volume
        v_coefficients = self.volume_local_estimation
        t_volume = v_coefficients[0] * timepoint + v_coefficients[1]
        return np.cbrt(self.target_volume / t_volume)

    def get_rectified_cell_volume(self, cell):
        timepoint = int(cell) // (10 ** self.time_digits_for_cell_id)
        voxelsize = self.get_voxelsize_correction(timepoint)
        vol = self.cell_volume[cell]
        return vol * voxelsize * voxelsize * voxelsize

    #
    #
    #
    def get_embryo_volume(self, timepoint):
        s = 0.0
        volumes = self.cell_volume
        div = 10 ** self.time_digits_for_cell_id
        for c in volumes:
            if int(c) // div != timepoint:
                continue
            if int(c) % div == 1 or int(c) % div == 0:
                continue
            s += volumes[c]
        return s

    def get_cells(self, timepoint):
        lineage = self.cell_lineage
        cells = list(set(lineage.keys()).union(set([v for values in list(lineage.values()) for v in values])))
        div = 10 ** self.time_digits_for_cell_id
        return  sorted([c for c in cells if (int(c) // div == timepoint) and int(c) % div != 1])

    #
    #
    #
    def get_symmetry_axis_from_names(self, timepoint):

        if 'symmetry_axis_from_names' in self._properties:
            if timepoint in self._properties['symmetry_axis_from_names']:
                return self._properties['symmetry_axis_from_names'][timepoint]
        else:
            self._properties['symmetry_axis_from_names'] = {}

        volumes = self.cell_volume
        barycenters = self.cell_barycenter
        names = self.cell_name
        if names is None:
            return np.zeros(3)
        #
        leftb = np.zeros(3)
        lefts = 0.0
        rightb = np.zeros(3)
        rights = 0.0
        div = 10 ** self.time_digits_for_cell_id
        #
        for c in volumes:
            if int(c) // div != timepoint:
                continue
            if int(c) % div == 1 or int(c) % div == 0:
                continue
            if c not in barycenters or c not in names:
                continue
            if names[c].split('.')[1][4] == '_':
                leftb += volumes[c] * barycenters[c]
                lefts += volumes[c]
            elif names[c].split('.')[1][4] == '*':
                rightb += volumes[c] * barycenters[c]
                rights += volumes[c]
        if lefts == 0.0 or rights == 0.0:
            return np.zeros(3)
        symdir = leftb/lefts - rightb/rights
        self._properties['symmetry_axis_from_names'][timepoint] = symdir / np.linalg.norm(symdir)
        return self._properties['symmetry_axis_from_names'][timepoint]

    #
    #
    #
    def get_embryo_barycenter(self, timepoint, rectified=False):
        if rectified is True:
            key = 'embryo_rectified_barycenter'
        else:
            key = 'embryo_barycenter'
        if key in self._properties:
            if timepoint in self._properties[key]:
                return self._properties[key][timepoint]
        else:
            self._properties[key] = {}

        if rectified is True:
            volumes = self.rectified_cell_volume
            barycenters = self.rectified_cell_barycenter
        else:
            volumes = self.cell_volume
            barycenters = self.cell_barycenter
        div = 10 ** self.time_digits_for_cell_id

        b = np.zeros(3)
        s = 0.0
        for c in volumes:
            if int(c) // div != timepoint:
                continue
            if int(c) % div == 1 or int(c) % div == 0:
                continue
            if c not in barycenters:
                continue
            b += volumes[c] * barycenters[c]
            s += volumes[c]
        self._properties[key][timepoint] = b / s
        return self._properties[key][timepoint]

    def get_embryo_covariance(self, timepoint):
        if 'embryo_covariance' in self._properties:
            if timepoint in self._properties['embryo_covariance']:
                return self._properties['embryo_covariance'][timepoint]
        else:
            self._properties['embryo_covariance'] = {}

        volumes = self.cell_volume
        barycenters = self.cell_barycenter
        div = 10 ** self.time_digits_for_cell_id

        b = np.zeros(3)
        m = np.zeros((3, 3))
        s = 0.0
        for c in volumes:
            if int(c) // div != timepoint:
                continue
            if int(c) % div == 1 or int(c) % div == 0:
                continue
            if c not in barycenters:
                continue
            s += volumes[c]
            b += volumes[c] * barycenters[c]
            t = barycenters[c].reshape((1, 3))
            m += volumes[c] * t * t.T
        # end of computation
        b /= s
        m /= s
        t = b.reshape((1, 3))
        m -= t * t.T

        #
        # val, vec = np.linalg.eig(m)
        # norma_mat = np.matmul(vec, np.matmul(np.linalg.inv(np.diag(np.sqrt(val))), vec.T))
        #
        # (re)computing the covariance matrix with the np.matmul(norma_mat, barycenters[c])
        # yields a covariance matrix with all variances equal to 1
        # (somehow makes the embryo spherical)

        self._properties['embryo_covariance'][timepoint] = m
        return self._properties['embryo_covariance'][timepoint]

    #
    #
    #
    def get_direction_distribution_candidates(self, timepoint, parameters=None, verbose=True):
        proc = "get_direction_distribution_candidates"
        if parameters is not None:
            if not isinstance(parameters, symmetry.EmbryoSymmetryParameters):
                msg = "parameters expected type is 'EmbryoSymmetryParameters' but was '"
                msg += type(parameters) + "' instead"
                monitoring.to_log_and_console(proc + ": " + msg)
                return None
            local_parameters = parameters
        else:
            local_parameters = symmetry.EmbryoSymmetryParameters()

        #
        # maxima is an array of dictionaries
        # 'voxel': (i, j, k) voxel coordinates in a sxsxs matrix with s computed by
        #           ir = math.ceil(parameters.distribution_sphere_radius)
        #           s = int(2 * ir + 1 + 2)
        # 'vector': a normalized vector v / np.linalg.norm(v)  with v = 'voxel' - center
        #           center coordinates are (c,c,c) with c = np.double(ir + 1)
        # 'value': the distribution values
        #          the maximal value is 1
        #

        if 'direction_distribution_maxima' not in self._properties:
            self._properties['direction_distribution_maxima'] = {}
        if timepoint not in self.direction_distribution_maxima:
            maxima = symmetry.symmetry_candidates(self.cell_contact_surface, self.cell_barycenter, timepoint,
                                                  local_parameters,
                                                  time_digits_for_cell_id=self.time_digits_for_cell_id,
                                                  verbose=verbose)
            self.direction_distribution_maxima[timepoint] = maxima

        return self.direction_distribution_maxima[timepoint]

    #
    #
    #
    def get_cells_per_time(self, fate=None, nonfate=None):
        proc = "get_cells_per_time"
        div = 10 ** self.time_digits_for_cell_id
        cells_per_time = {}

        if fate is None and nonfate is None:
            lineage = self.cell_lineage
            cells = list(set(lineage.keys()).union(set([v for values in list(lineage.values()) for v in values])))
            cells = sorted(cells)
            for c in cells:
                t = int(c) // div
                cells_per_time[t] = cells_per_time.get(t, 0) + 1
            return cells_per_time

        cell_fate = self.cell_fate
        if cell_fate is None:
            msg = "no cell fate for embryo, unable to compute cells per time"
            monitoring.to_log_and_console(proc + ": " + msg)
            return None

        for c in cell_fate:
            if properties.has_fate(cell_fate[c], fate, nonfate):
                t = int(c) // div
                cells_per_time[t] = cells_per_time.get(t, 0) + 1
        return cells_per_time

    #
    #
    #
    def write_as_graph(self, time=None, atlasname=None):
        #
        # write embryo as a graph at time time
        #
        div = 10 ** self.time_digits_for_cell_id
        contact = copy.deepcopy(self.cell_contact_surface)
        cells = [c for c in contact if c // div == time]

        #
        # add background to the (copied) contact
        #
        ibackground = time * div + 1
        contact = copy.deepcopy(self.cell_contact_surface)
        contact[ibackground] = {}
        for c in cells:
            if ibackground not in contact[c]:
                continue
            contact[ibackground][c] = contact[c][ibackground]

        cells = sorted(cells + [ibackground])
        icells = {}
        for i, c in enumerate(cells):
            icells[c] = i + 1

        voxelsize = self.get_voxelsize_correction(time)
        correction = voxelsize * voxelsize
        filename = "graph-" + str(atlasname) + ".txt"
        with open(filename, 'w') as file:
            for c in icells:
                for d in contact[c]:
                    line = "{:2d} {:2d} {:9.3f}".format(icells[c], icells[d], contact[c][d] * correction)
                    file.write(line + '\n')

        filename = "groundtruth-" + str(atlasname) + ".txt"
        with open(filename, 'w') as file:
            for c in icells:
                if c == ibackground:
                    line = "{:2d} background".format(icells[ibackground])
                else:
                    line = "{:2d} {:s}".format(icells[c], self.cell_name[c])
                file.write(line + '\n')


############################################################
#
# Atlases: set of many atlas
#
############################################################

class Atlases(object):
    def __init__(self, parameters=None):
        # atlases
        self._atlases = {}
        # reference atlas for time alignment
        self._ref_atlas = None

        if parameters is not None:
            self.update_from_parameters(parameters)

    ############################################################
    #
    # getters / setters
    #
    ############################################################

    def n_atlases(self):
        return len(self._atlases)

    def get_atlases(self):
        return self._atlases

    def set_atlases(self, atlases):
        self._atlases = atlases

    def get_reference_atlas(self):
        proc = "get_reference_atlas"
        if self._ref_atlas is None:
            atlases = self.get_atlases()
            if len(atlases) == 0:
                monitoring.to_log_and_console(proc + ": no reference atlas nor registered atlases")
                return None
            names = sorted(list(atlases.keys()))
            monitoring.to_log_and_console("   ... set reference to '" + str(names[0]) + "'")
            self.set_reference_atlas(names[0])
        return self._ref_atlas

    def set_reference_atlas(self, reference_atlas):
        self._ref_atlas = reference_atlas

    ############################################################
    #
    # update
    #
    ############################################################

    def update_from_parameters(self, parameters):
        if not isinstance(parameters, AtlasParameters):
            return
        if parameters.referenceAtlas is not None:
            name = parameters.referenceAtlas.split(os.path.sep)[-1]
            if name.endswith(".xml") or name.endswith(".pkl"):
                name = name[:-4]
            self.set_reference_atlas(name)

    ############################################################
    #
    #
    #
    ############################################################

    def temporal_alignment(self, fate=None):
        proc = "temporal_alignment"
        ref_atlas = self.get_reference_atlas()
        if ref_atlas is None:
            monitoring.to_log_and_console(proc + ": no reference atlas, can not perform temporal alignment")
            return
        atlases = self.get_atlases()
        if ref_atlas not in atlases:
            msg = "'" + str(ref_atlas) + "' is not in registered atlases, can not perform temporal alignment"
            monitoring.to_log_and_console(proc + ": " + msg)
            return

        if fate is None:
            for a in atlases:
                if a == ref_atlas:
                    continue
                atlases[a].temporally_align_with(atlases[ref_atlas])
        else:
            for a in atlases:
                if a == ref_atlas:
                    atlases[ref_atlas].set_temporal_alignment((1.0, 0.0), key=fate)
                    continue
                atlases[a].temporally_align_with(atlases[ref_atlas], fate=fate)
        for n in atlases:
            temporal_alignment = atlases[n].get_temporal_alignment(key=fate)
            msg = "   ... "
            msg += "linear time warping of '" + str(n) + "' wrt '" + str(self._ref_atlas) + "' is "
            msg += "({:.3f}, {:.3f})".format(temporal_alignment[0], temporal_alignment[1])
            if fate is None:
                msg += " [all cells]"
            else:
                msg += " [" + str(fate) + " cells]"
            monitoring.to_log_and_console(msg, 1)

        return

    ############################################################
    #
    #
    #
    ############################################################

    def _add_atlas(self, prop, name, time_digits_for_cell_id=4):
        atlases = self.get_atlases()
        atlases[name] = Atlas(prop, time_digits_for_cell_id=time_digits_for_cell_id)
        self.set_atlases(atlases)

    def add_atlases(self, atlasfiles, parameters, time_digits_for_cell_id=4):
        """
        Method of class Atlases that read property files to build atlases, ie copy properties of interest
        ('cell_lineage', 'cell_name',  'cell_contact_surface', 'cell_barycenter' and 'cell_volume').
        It may also perform some diagnosis (on 'name' and 'contact' properties) if required.
        It also temporally register the read atlases wrt to a reference one (the one one is reference
        is given in the paramters).

        :param atlasfiles: a file name or a list of file names (pkl or xml files containing embryo properties)
        :param parameters: an instance of class AtlasParameters
        :param time_digits_for_cell_id: number of digits used to represent cell label in images; an unique
            cell id is made by concatening 'time' + 'cell label'
        :return: no return. It updates an instance variable
        """
        proc = "add_atlases"

        if not isinstance(parameters, AtlasParameters):
            monitoring.to_log_and_console(str(proc) + ": unexpected type for 'parameters' variable: "
                                          + str(type(parameters)))
            sys.exit(1)

        if isinstance(atlasfiles, str):
            prop = ioproperties.read_dictionary(atlasfiles, inputpropertiesdict={})
            if len(prop) > 0:
                name = atlasfiles.split(os.path.sep)[-1]
                if name.endswith(".xml") or name.endswith(".pkl"):
                    name = name[:-4]
                if parameters.atlas_diagnosis:
                    udiagnosis.diagnosis(prop, ['name', 'contact'], parameters,
                                         time_digits_for_cell_id=time_digits_for_cell_id)
                self._add_atlas(prop, name, time_digits_for_cell_id=time_digits_for_cell_id)
            del prop
        elif isinstance(atlasfiles, list):
            if len(atlasfiles) == 0:
                monitoring.to_log_and_console(str(proc) + ": empty atlas file list ?!")
                sys.exit(1)
            for f in atlasfiles:
                prop = ioproperties.read_dictionary(f, inputpropertiesdict={})
                if len(prop) > 0:
                    name = f.split(os.path.sep)[-1]
                    if name.endswith(".xml") or name.endswith(".pkl"):
                        name = name[:-4]
                    if parameters.atlas_diagnosis:
                        udiagnosis.diagnosis(prop, ['name', 'contact'], parameters,
                                             time_digits_for_cell_id=time_digits_for_cell_id)
                    self._add_atlas(prop, name, time_digits_for_cell_id=time_digits_for_cell_id)
                del prop

        #
        # temporal alignment (done from the cell number)
        #
        if self.n_atlases() > 0:
            monitoring.to_log_and_console("... temporal alignment of lineages", 1)
            self.temporal_alignment()
        else:
            msg = proc + ": no read atlases ?!"
            monitoring.to_log_and_console(msg, 1)

        if parameters.atlas_diagnosis:
            _diagnosis_division_timepoint(self, parameters)

    ############################################################
    #
    #
    #
    ############################################################

    def write_as_graph(self, cell_number=64):
        proc = "write_as_graph"
        atlases = self.get_atlases()
        for n in atlases:
            ncells, timerange = atlases[n].get_timerange(cell_number, change_cell_number=True)
            if ncells is None:
                msg = "weird, requested cell number was " + str(cell_number) + ". "
                msg += "No cell range was found."
                monitoring.to_log_and_console(proc + ": " + msg)
                continue
            if ncells != cell_number:
                msg = "will produce graph at " + str(ncells) + " instead of " + str(cell_number) + " cells"
                monitoring.to_log_and_console(proc + ": " + msg)
            time = statistics.median_low(timerange)
            atlases[n].write_as_graph(time=time, atlasname=str(n))
