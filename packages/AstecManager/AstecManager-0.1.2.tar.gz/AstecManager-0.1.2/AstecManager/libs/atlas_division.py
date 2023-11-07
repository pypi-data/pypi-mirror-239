import copy
import os
import sys
import operator
import numpy as np
import scipy as sp
import scipy.cluster.hierarchy as sch

import astec.utils.common as common
import astec.utils.ascidian_name as uname
import astec.utils.neighborhood_distance as uneighborhood
import ascidian.core.atlas_embryo as atlasembryo
import ascidian.core.atlas_cell as atlascell

monitoring = common.Monitoring()


###########################################################
#
#
#
############################################################

class DivisionParameters(atlasembryo.AtlasParameters):

    ############################################################
    #
    # initialisation
    #
    ############################################################

    def __init__(self, prefix='atlas_'):

        if "doc" not in self.__dict__:
            self.doc = {}

        atlasembryo.AtlasParameters.__init__(self, prefix=prefix)

        #
        #
        #
        doc = "\t True or False. Exclude inner surfaces from the division-to-division distance calculation\n"
        self.doc['exclude_inner_surfaces'] = doc
        self.exclude_inner_surfaces = False

        #
        #
        #
        doc = "\t True or False. Performs some diagnosis after building the division atlas. \n"
        doc += "\t Incrementing the verboseness ('-v' in the command line) may give more details.\n"
        self.doc['division_diagnosis'] = doc
        self.division_diagnosis = False

        doc = "\t If True, will propose some daughters switches in the atlases. For a given division,\n"
        doc += "\t a global score is computed as the sum of all pairwise division similarity.\n"
        doc += "\t A switch is proposed for an atlas if it allows to decrease this global score.\n"
        self.doc['division_permutation_proposal'] = doc
        self.division_permutation_proposal = False

        #
        #
        #
        doc = "\t Cluster distance used to build dendrograms. Dendrograms are used either for\n"
        doc += "\t diagnosis purpose (if 'diagnosis_properties' is set to True) or to generate\n"
        doc += "\t figures (if 'generate_figure' is set to True)\n"
        doc += "\t - 'single'\n"
        doc += "\t - 'complete'\n"
        doc += "\t - 'average'\n"
        doc += "\t - 'weighted'\n"
        doc += "\t - 'centroid'\n"
        doc += "\t - 'median'\n"
        doc += "\t - 'ward'\n"
        doc += "\t see https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html.\n"
        self.doc['dendrogram_cluster_distance'] = doc
        self.dendrogram_cluster_distance = 'single'

        doc = "\t Write out morphonet selection files."
        self.doc['write_selection'] = doc
        self.write_selection = False

        #
        #
        #
        self.cells_to_be_traced = None
    ############################################################
    #
    # print / write
    #
    ############################################################

    def print_parameters(self):
        print("")
        print('#')
        print('# DivisionParameters')
        print('#')
        print("")

        common.PrefixedParameter.print_parameters(self)

        atlasembryo.AtlasParameters.print_parameters(self)

        self.varprint('exclude_inner_surfaces', self.exclude_inner_surfaces)

        self.varprint('division_diagnosis', self.division_diagnosis)
        self.varprint('division_permutation_proposal', self.division_permutation_proposal)

        self.varprint('dendrogram_cluster_distance', self.dendrogram_cluster_distance)
        self.varprint('write_selection', self.write_selection)

        self.varprint('cells_to_be_traced', self.cells_to_be_traced)
        print("")

    def write_parameters_in_file(self, logfile):
        logfile.write("\n")
        logfile.write("# \n")
        logfile.write("# DivisionParameters\n")
        logfile.write("# \n")
        logfile.write("\n")

        common.PrefixedParameter.write_parameters_in_file(self, logfile)

        atlasembryo.AtlasParameters.write_parameters_in_file(self, logfile)

        self.varwrite(logfile, 'exclude_inner_surfaces', self.exclude_inner_surfaces,
                      self.doc.get('exclude_inner_surfaces', None))

        self.varwrite(logfile, 'division_diagnosis', self.division_diagnosis, self.doc.get('division_diagnosis', None))
        self.varwrite(logfile, 'division_permutation_proposal', self.division_permutation_proposal,
                      self.doc.get('division_permutation_proposal', None))

        self.varwrite(logfile, 'dendrogram_cluster_distance', self.dendrogram_cluster_distance,
                      self.doc.get('dendrogram_cluster_distance', None))
        self.varwrite(logfile, 'write_selection', self.write_selection, self.doc.get('write_selection', None))

        self.varwrite(logfile, 'cells_to_be_traced', self.cells_to_be_traced, self.doc.get('cells_to_be_traced', None))

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

        atlasembryo.AtlasParameters.update_from_parameters(self, parameters)

        self.exclude_inner_surfaces = self.read_parameter(parameters, 'exclude_inner_surfaces',
                                                          self.exclude_inner_surfaces)

        self.division_diagnosis = self.read_parameter(parameters, 'division_diagnosis', self.division_diagnosis)
        self.division_diagnosis = self.read_parameter(parameters, 'diagnosis_properties', self.division_diagnosis)
        self.division_diagnosis = self.read_parameter(parameters, 'naming_diagnosis', self.division_diagnosis)
        self.division_diagnosis = self.read_parameter(parameters, 'diagnosis_naming', self.division_diagnosis)

        self.division_permutation_proposal = self.read_parameter(parameters, 'division_permutation_proposal',
                                                                 self.division_permutation_proposal)
        self.division_permutation_proposal = self.read_parameter(parameters, 'daughter_switch_proposal',
                                                                 self.division_permutation_proposal)

        self.dendrogram_cluster_distance = self.read_parameter(parameters, 'dendrogram_cluster_distance',
                                                               self.dendrogram_cluster_distance)
        self.write_selection = self.read_parameter(parameters, 'write_selection', self.write_selection)

        self.cells_to_be_traced = self.read_parameter(parameters, 'cells_to_be_traced', self.cells_to_be_traced)

    def update_from_parameter_file(self, parameter_file):
        if parameter_file is None:
            return
        if not os.path.isfile(parameter_file):
            print("Error: '" + parameter_file + "' is not a valid file. Exiting.")
            sys.exit(1)

        parameters = common.load_source(parameter_file)
        self.update_from_parameters(parameters)


###########################################################
#
#
#
############################################################

def _build_common_neighborhoods(neighborhoods):
    """
    Build a new neighborhood dictionary where both a cell and its sister have
    the same neighbors.

    :param neighborhoods: dictionary of dictionaries
        ['cell name']['reference name']['neighboring cell']
        first key is a cell name;
        second key is a reference name (ie an atlas):  neighborhoods['cell name']['reference name'] is then
        the neighborhood of 'cell name' extracted from 'reference name';
        the neighborhood itself is a dictionary, indexed by the neighboring cell names, whose values are
        contact surfaces.
    :return:
        The neighborhood dictionary where both a cell and its sister have the same neighbors.
    """

    proc = "_build_common_neighborhoods"

    common_neighborhoods = {}

    for cell in neighborhoods:
        if cell in common_neighborhoods:
            continue
        sister = uname.get_sister_name(cell)
        if sister in common_neighborhoods:
            msg = "weird, '" + str(sister) + "' is in neighborhoods while '" + str(cell) + "' is not"
            monitoring.to_log_and_console(proc + ": " + msg)
        new_neighborhoods = uneighborhood.build_same_contact_surfaces(neighborhoods, [cell, sister])
        for n in new_neighborhoods:
            common_neighborhoods[n] = copy.deepcopy(new_neighborhoods[n])
    return common_neighborhoods


########################################################################################
#
#
#
########################################################################################

def _write_list(listtobeprinted, firstheader="", otherheader="", maxlength=112, verboseness=0):
    txt = ""
    n = 0
    for i, item in enumerate(listtobeprinted):
        if i == 0:
            txt = firstheader
            n = 0
        if len(txt) + len(str(item)) <= maxlength:
            if n >= 1:
                txt += ","
            txt += " " + str(item)
            n += 1
        else:
            monitoring.to_log_and_console(txt, verboseness=verboseness)
            txt = otherheader + " " + str(item)
            n = 1
        if i == len(listtobeprinted) - 1:
            monitoring.to_log_and_console(txt, verboseness=verboseness)


def _write_summary_pairwise_switches(atlases, summary):
    divisions = atlases.get_divisions()
    percents = []
    mother_names = list(summary.keys())

    for n in mother_names:
        percents.append(100.0 * float(len(summary[n]['disagreement'])) / float(summary[n]['tested_couples']))
    [sorted_percents, sorted_mothers] = list(zip(*sorted(zip(percents, mother_names), reverse=True)))

    majority = {}
    equality = {}
    for n in sorted_mothers:
        majority[n] = {}
        equality[n] = {}
        if len(summary[n]['disagreement']) == 0:
            continue
        msg = " - " + str(n) + " cell division into "
        msg += str(uname.get_daughter_names(n)) + " has " + str(len(summary[n]['disagreement']))
        if len(summary[n]['disagreement']) > 1:
            msg += " disagreements"
        else:
            msg += " disagreement"
        percent = 100.0 * float(len(summary[n]['disagreement'])) / float(summary[n]['tested_couples'])
        msg += " (" + "{:2.2f}%".format(percent) + ")"
        monitoring.to_log_and_console(msg)
        msg = "\t over " + str(summary[n]['tested_couples']) + " tested configurations "
        msg += "and over " + str(len(divisions[n]))
        msg += " references: "
        monitoring.to_log_and_console(msg)
        #
        # print references
        #
        _write_list(sorted(divisions[n]), firstheader="\t     ", otherheader="\t     ", maxlength=112, verboseness=0)
        #
        # count the cases where one atlas disagrees
        #
        for a in divisions[n]:
            s = 0
            for pair in summary[n]['disagreement']:
                if a in pair:
                    s += 1
            if 2 * s > len(divisions[n]):
                majority[n][a] = s
            elif 2 * s == len(divisions[n]):
                equality[n][a] = s
        #
        # print detailed disagreements
        #
        _write_list(sorted(summary[n]['disagreement']), firstheader="\t - disagreement list:", otherheader="\t     ",
                    maxlength=112, verboseness=3)

    nitems = 0
    for n in sorted_mothers:
        nitems += len(majority[n]) + len(equality[n])
    if nitems == 0:
        return
    monitoring.to_log_and_console("")
    monitoring.to_log_and_console(" --- atlases pairwise disagreements: summary ---")
    for n in sorted(mother_names):
        if len(majority[n]) > 0:
            msg = " - " + str(n) + " division, atlas that mostly disagrees:"
            akeys = sorted(list(majority[n].keys()))
            for i, a in enumerate(akeys):
                msg += " " + str(a) + " (" + str(majority[n][a]) + "/" + str(len(divisions[n])) + ")"
                if i < len(akeys) - 1:
                    msg += ","
            monitoring.to_log_and_console(msg)
    for n in sorted(mother_names):
        if len(equality[n]) > 0:
            msg = " - " + str(n) + " division, atlas that equally disagrees:"
            akeys = sorted(list(equality[n].keys()))
            for i, a in enumerate(akeys):
                msg += " " + str(a) + " (" + str(equality[n][a]) + "/" + str(len(divisions[n])) + ")"
                if i < len(akeys) - 1:
                    msg += ","
            monitoring.to_log_and_console(msg)


def _diagnosis_pairwise_switches(atlases, parameters):
    proc = "_diagnosis_pairwise_switches"

    divisions = atlases.get_divisions()
    ccs = not parameters.use_common_neighborhood
    neighborhoods = atlases.get_cell_neighborhood(delay_from_division=parameters.name_delay_from_division)

    summary = {}
    innersurfaces = []

    for n in divisions:
        #
        # only one reference/atlas for mother cell 'n': nothing to do
        #
        if len(divisions[n]) <= 1:
            continue
        summary[n] = {}
        summary[n]['tested_couples'] = 0
        summary[n]['disagreement'] = []

        d = uname.get_daughter_names(n)
        if parameters.exclude_inner_surfaces:
            innersurfaces = [d[0], d[1]]

        for r1 in divisions[n]:
            for r2 in divisions[n]:
                if r2 <= r1:
                    continue
                summary[n]['tested_couples'] += 1
                #
                # test reference r1 versus r2
                # it is assumed that (r1, switched(r2)) is similar to (switched(r1), r2)
                # so only (r1, switched(r2)) is tested
                #
                switch_neighs = {d[0]: copy.deepcopy(neighborhoods[d[1]][r2]),
                                 d[1]: copy.deepcopy(neighborhoods[d[0]][r2])}
                if d[0] in switch_neighs[d[0]]:
                    switch_neighs[d[0]][d[1]] = switch_neighs[d[0]][d[0]]
                    del switch_neighs[d[0]][d[0]]
                if d[1] in switch_neighs[d[1]]:
                    switch_neighs[d[1]][d[0]] = switch_neighs[d[1]][d[1]]
                    del switch_neighs[d[1]][d[1]]
                #
                # same
                #
                same_dist = division_distance(neighborhoods[d[0]][r1], neighborhoods[d[1]][r1],
                                              neighborhoods[d[0]][r2], neighborhoods[d[1]][r2],
                                              change_contact_surfaces=ccs, innersurfaces=innersurfaces)
                swit_dist = division_distance(neighborhoods[d[0]][r1], neighborhoods[d[1]][r1],
                                              switch_neighs[d[0]], switch_neighs[d[1]],
                                              change_contact_surfaces=ccs, innersurfaces=innersurfaces)
                if same_dist < swit_dist:
                    continue
                summary[n]['disagreement'] += [(r1, r2)]

    divisions_with_disagreement = [n for n in summary if len(summary[n]['disagreement']) > 0]

    msg = "tested divisions = " + str(len(summary))
    monitoring.to_log_and_console(str(proc) + ": " + msg)
    msg = "divisions with pairwise disagreement =  " + str(len(divisions_with_disagreement))
    monitoring.to_log_and_console("\t " + msg)
    msg = "  A disagreement means that a division from a reference is closer to the\n"
    msg += "  switched division of an other reference than the division itself."
    monitoring.to_log_and_console(msg)
    monitoring.to_log_and_console("")
    if len(divisions_with_disagreement) > 0:
        _write_summary_pairwise_switches(atlases, summary)
    monitoring.to_log_and_console("")

    return summary


###########################################################
#
#
#
############################################################


def division_scipy_linkage(config, cluster_distance='single', change_contact_surfaces=True, innersurfaces=[],
                           distance='distance'):
    """

    Parameters
    ----------
    config: dictionary of dictionary of neighborhoods indexed by [reference] then by [0,1],
        where 0 stands for one daughter, and 1 for the other
    cluster_distance
    change_contact_surfaces
    innersurfaces

    Returns
    -------
    conddist: the squareform vector built from the distance matrice
       (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.squareform.html)
    z: the hierarchical clustering encoded as a linkage matrix
       (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html)
    labels: the list of atlas names

    """

    labels = []
    #
    # build a square matrix of distances
    #
    dist = np.zeros((len(config), len(config)))
    for i, r in enumerate(config):
        labels += [r]
        for j, s in enumerate(config):
            if r == s:
                dist[i][i] = 0.0
                continue
            if r > s:
                continue
            # if r == 'switched-' + str(s) or s == 'switched-' + str(r):
            #    continue
            dist[i][j] = 0.0
            if distance == 'signature':
                dist[i][j] = 100.0 * division_signature(config[r][0], config[r][1], config[s][0], config[s][1],
                                                        change_contact_surfaces=change_contact_surfaces,
                                                        innersurfaces=innersurfaces)
            else:
                dist[i][j] = 100.0 * division_distance(config[r][0], config[r][1], config[s][0], config[s][1],
                                                       change_contact_surfaces=change_contact_surfaces,
                                                       innersurfaces=innersurfaces)
            dist[j][i] = dist[i][j]

    conddist = sp.spatial.distance.squareform(dist)
    z = sch.linkage(conddist, method=cluster_distance)

    return conddist, z, labels


def switched_division_neighborhoods(config, mother_name):
    #
    # copy neighborhoods from atlases and add switched neighborhoods
    #
    daughters = uname.get_daughter_names(mother_name)
    swconfig = {}
    for r in config:
        swconfig[r] = {}
        swconfig[r][0] = copy.deepcopy(config[r][0])
        swconfig[r][1] = copy.deepcopy(config[r][1])
        sr = 'switched-' + str(r)
        swconfig[sr] = {}
        swconfig[sr][0] = copy.deepcopy(config[r][1])
        swconfig[sr][1] = copy.deepcopy(config[r][0])
        if daughters[1] in swconfig[sr][0] and swconfig[sr][0][daughters[1]] > 0:
            msg = "  weird, " + str(daughters[1]) + " was found in its neighborhood for reference " + str(r)
            monitoring.to_log_and_console("      " + msg)
        if daughters[0] in swconfig[sr][0]:
            swconfig[sr][0][daughters[1]] = swconfig[sr][0][daughters[0]]
            del swconfig[sr][0][daughters[0]]
        if daughters[0] in swconfig[sr][1] and swconfig[sr][1][daughters[0]] > 0:
            msg = "  weird, " + str(daughters[0]) + " was found in its neighborhood for reference " + str(r)
            monitoring.to_log_and_console("      " + msg)
        if daughters[1] in swconfig[sr][1]:
            swconfig[sr][1][daughters[0]] = swconfig[sr][1][daughters[1]]
            del swconfig[sr][1][daughters[1]]
    return swconfig


def _diagnosis_linkage(atlases, parameters):
    proc = "_diagnosis_linkage"
    divisions = atlases.get_divisions()
    ccs = not parameters.use_common_neighborhood

    ref_atlases = atlases.get_atlases()
    output_selections = atlases.get_output_selections()

    merge_values = {}
    lastmerge_values = {}

    swmerge_values = {}
    swlastmerge_values = {}

    division_lastmerge_values = {}

    innersurfaces = []

    for n in divisions:
        stage = n.split('.')[0][1:]
        if len(divisions[n]) <= 2:
            continue

        d = uname.get_daughter_names(n)
        if parameters.exclude_inner_surfaces:
            innersurfaces = [d[0], d[1]]
        #
        # config is a dictionary indexed by [reference][0|1]
        # -> [reference][i] gives the neighborhood of daughter #i of division/mother n
        # swconfig contains the same neighborhoods than config plus the "switched" neighborhoods
        #
        config = atlases.extract_division_neighborhoods(n, delay_from_division=parameters.name_delay_from_division)
        swconfig = switched_division_neighborhoods(config, n)

        #
        # distance array for couples of atlases/references
        #
        conddist, z, labels = division_scipy_linkage(config, change_contact_surfaces=ccs, innersurfaces=innersurfaces)

        merge_values[stage] = merge_values.get(stage, []) + list(z[:, 2])
        lastmerge_value = z[:, 2][-1]
        lastmerge_values[stage] = lastmerge_values.get(stage, []) + [lastmerge_value]

        #
        # set the lastmerge_value in morphonet selection
        #
        for r in divisions[n]:
            if r not in ref_atlases:
                if not (r[:4] == 'sym-' and r[4:] in ref_atlases):
                    monitoring.to_log_and_console(proc + ": weird, '" + str(r) + "' is not in reference atlases.", 4)
                continue
            keyselection = "morphonet_float_" + str(r) + "_last_dendrogram_value"
            output_selections[keyselection] = output_selections.get(keyselection, {})
            lineage = ref_atlases[r].cell_lineage
            name = ref_atlases[r].cell_name
            cells = list(set(lineage.keys()).union(set([v for values in list(lineage.values()) for v in values])))
            for c in cells:
                if c not in name:
                    continue
                if name[c] == n:
                    output_selections[keyselection][c] = round(lastmerge_value)

        #
        # distance array for couples of atlases/references plus the switched ones
        #
        swconddist, swz, swlabels = division_scipy_linkage(swconfig, change_contact_surfaces=ccs,
                                                          innersurfaces=innersurfaces)

        swmerge_values[stage] = swmerge_values.get(stage, []) + list(swz[:, 2])
        swlastmerge_value = swz[:, 2][-1]
        swlastmerge_values[stage] = swlastmerge_values.get(stage, []) + [swlastmerge_value]

        division_lastmerge_values[n] = [lastmerge_value, swlastmerge_value]

    nochanges = {n: v for n, v in division_lastmerge_values.items() if v[1] <= v[0]}
    mother_with_nochanges = [n for n, v in division_lastmerge_values.items() if v[1] <= v[0]]
    #
    # set the lastmerge_value in morphonet selection
    #
    for n in mother_with_nochanges:
        for r in divisions[n]:
            if r not in ref_atlases:
                if not (r[:4] == 'sym-' and r[4:] in ref_atlases):
                    monitoring.to_log_and_console(proc + ": weird, '" + str(r) + "' is not in reference atlases.", 4)
                continue
            keyselection = "morphonet_selection_" + str(r) + "_dendrogram_warning"
            output_selections[keyselection] = output_selections.get(keyselection, {})
            lineage = ref_atlases[r].cell_lineage
            name = ref_atlases[r].cell_name
            cells = list(set(lineage.keys()).union(set([v for values in list(lineage.values()) for v in values])))
            for c in cells:
                if c not in name:
                    continue
                if name[c] == n:
                    output_selections[keyselection][c] = 100

    monitoring.to_log_and_console("------ division with same dendrogram last values (without and with switch)")
    msg = str(len(nochanges)) + "/" + str(len(division_lastmerge_values)) + " divisions"
    monitoring.to_log_and_console("\t " + msg)

    monitoring.to_log_and_console("------ cell-based view")
    division_by_generation = {}
    for m in mother_with_nochanges:
        g = m.split('.')[0][1:]
        division_by_generation[g] = division_by_generation.get(g, []) + [m]
    for g in division_by_generation:
        monitoring.to_log_and_console("  - generation " + str(g))
        mothers = list(division_by_generation[g])
        mothers.sort()
        for m in mothers:
            msg = "    - division of '" + str(m) + "': " + str(division_lastmerge_values[m])
            monitoring.to_log_and_console(msg)

    monitoring.to_log_and_console("------ dendrogram last-value view")
    sorted_nochanges = sorted(nochanges.items(), key=lambda v: v[1][0], reverse=True)
    for s in sorted_nochanges:
        msg = "    - division of '" + str(s[0]) + "': " + str(s[1])
        monitoring.to_log_and_console(msg)
    monitoring.to_log_and_console("")


########################################################################################
#
#
#
########################################################################################

def _dpp_switch_contact_surfaces(neighbors, reference, daughters):
    """
    Switch contact surfaces for the two daughters and atlas 'reference'.
    Parameters
    ----------
    neighbors
    reference
    daughters

    Returns
    -------

    """
    #
    # contact surfaces of daughters[0] for atlas 'reference'
    # replace contact surface with daughters[1] with a contact surface with daughters[0]
    #
    neighs = {0: copy.deepcopy(neighbors[1][reference]), 1: copy.deepcopy(neighbors[0][reference])}
    if daughters[0] in neighs[0]:
        neighs[0][daughters[1]] = neighs[0][daughters[0]]
        del neighs[0][daughters[0]]
    if daughters[1] in neighs[1]:
        neighs[1][daughters[0]] = neighs[1][daughters[1]]
        del neighs[1][daughters[1]]

    neighbors[0][reference] = neighs[0]
    neighbors[1][reference] = neighs[1]
    return neighbors


def _dpp_global_generic_distance(mother, neighbors, references, parameters, debug=False):
    """
    Compute a global score. The global score is the average of local similarities over all
    couples of references/atlases.

    Parameters
    ----------
    neighbors: neighborhoods for the two daughters (dictionary indexed by [0,1] then by the references
    references: set of references
    debug

    Returns
    -------

    """

    innersurfaces = []
    d = uname.get_daughter_names(mother)
    if parameters.exclude_inner_surfaces:
        innersurfaces = [d[0], d[1]]

    ccs = not parameters.use_common_neighborhood
    score = 0
    n = 0
    distances = {}
    for r1 in references:
        if debug:
            distances[r1] = {}
        for r2 in references:
            if r2 <= r1:
                continue
            dist = division_distance(neighbors[0][r1], neighbors[1][r1], neighbors[0][r2], neighbors[1][r2],
                                     change_contact_surfaces=ccs, innersurfaces=innersurfaces)
            if debug:
                distances[r1][r2] = dist
            score += dist
            n += 1
    if debug:
        print("---- _dpp_global_generic_distance")
        refs1 = distances.keys()
        refs1 = sorted(refs1)
        for r1 in refs1:
            refs2 = distances[r1].keys()
            refs2 = sorted(refs2)
            for r2 in refs2:
                print("   - dist[" + str(r1) + ", " + str(r2) + "] = " + str(distances[r1][r2]))
    return score / n


def _dpp_test_one_division(atlases, mother, parameters):
    """
    Test whether any daughter switch (for a given reference) improve a global score
    Parameters
    ----------
    atlases
    mother
    parameters

    Returns
    -------

    """
    divisions = atlases.get_divisions()
    if len(divisions[mother]) <= 1:
        return {}, []

    daughters = uname.get_daughter_names(mother)
    neighborhoods = atlases.get_cell_neighborhood(delay_from_division=parameters.name_delay_from_division)
    neighbors = {0: copy.deepcopy(neighborhoods[daughters[0]]), 1: copy.deepcopy(neighborhoods[daughters[1]])}

    # score before any changes
    debug = False
    if debug:
        print("")
        print("===== test division " + str(mother) + " : " + str(divisions[mother]))
    score = _dpp_global_generic_distance(mother, neighbors, divisions[mother], parameters, debug=debug)

    returned_scores = [(None, score)]
    corrections = []
    i = 1
    while True:
        newscore = {}
        for r in sorted(divisions[mother]):
            #
            # switch contact surfaces for the daughters in atlas 'r'
            #
            tmp = copy.deepcopy(neighbors)
            tmp = _dpp_switch_contact_surfaces(tmp, r, daughters)
            if debug:
                print("===== test switch " + str(mother) + " / " + str(r))
            # compute a new score, keep it if it better than the one before any changes
            newscore[r] = _dpp_global_generic_distance(mother, tmp, divisions[mother], parameters, debug=debug)
            if debug:
                print("     new score = " + str(newscore[r]) + " - original score = " + str(score))
            if newscore[r] > score:
                del newscore[r]
        # no found correction at this iteration
        if len(newscore) == 0:
            return corrections, returned_scores
        # found several correction
        # 1. pick the only one (if only one is found)
        # 2. or pick the one with maximal score change
        elif len(newscore) == 1:
            ref = list(newscore.keys())[0]
        else:
            ref = min(newscore, key=lambda key: newscore[key])
        # first iteration, keep the value of the global score decrease
        if i == 1:
            for r in newscore:
                returned_scores += [(r, score - newscore[r])]
        corrections += [(ref, score - newscore[ref])]
        i += 1
        # if one correction has been found, apply it
        # and look for an other additional correction
        tmp = copy.deepcopy(neighbors)
        tmp = _dpp_switch_contact_surfaces(tmp, ref, daughters)
        neighbors[0] = copy.deepcopy(tmp[0])
        neighbors[1] = copy.deepcopy(tmp[1])
        score = newscore[ref]


def division_permutation_proposal(atlases, parameters):

    # neighborhoods is a dictionary of dictionaries
    # ['cell name']['reference name']
    # first key is a cell name (daughter cell)
    # second key is the reference from which the neighborhood has been extracted

    #
    # mother cell name dictionary indexed by stage
    # stage 6: 32 cells
    # stage 7: 64 cells
    #

    proc = "division_permutation_proposal"

    divisions = atlases.get_divisions()
    mothers = {}
    for n in divisions:
        stage = n.split('.')[0][1:]
        mothers[stage] = mothers.get(stage, []) + [n]
    for s in mothers:
        mothers[s] = sorted(mothers[s])

    stages = list(mothers.keys())
    stages.sort()
    corrections = {}
    selection = {}

    for s in stages:
        corrections[s] = {}
        # if int(s) != 7:
        #    continue
        for m in mothers[s]:
            # if m != 'a7.0002_':
            #     continue
            correction, returned_score = _dpp_test_one_division(atlases, m, parameters)
            #
            # correction is a dictionary indexed by the iteration index
            # each value is a tuple ('atlas name', score increment)
            #
            if len(correction) > 0:
                corrections[s][m] = correction
                selection[m] = returned_score

    #
    # build output selections
    #
    ref_atlases = atlases.get_atlases()
    output_selections = atlases.get_output_selections()

    for m in selection:
        if len(selection[m]) <= 1:
            continue
        (a, score) = selection[m][0]

        for i, (ref, ds) in enumerate(selection[m]):

            if i == 0:
                continue

            # check if the reference is registered
            # discard symmetrical neighborhood for warning
            if ref not in ref_atlases:
                if not (ref[:4] == 'sym-' and ref[4:] in ref_atlases):
                    monitoring.to_log_and_console(proc + ": weird, '" + str(ref) + "' is not in reference atlases.", 4)
                continue

            keyscore = "morphonet_float_" + str(ref) + "_distance_average_before_permutation_proposal"
            keydecre = "morphonet_float_" + str(ref) + "_distance_decrement_percentage_after_permutation_proposal"
            output_selections[keyscore] = output_selections.get(keyscore, {})
            output_selections[keydecre] = output_selections.get(keydecre, {})

            lineage = ref_atlases[ref].cell_lineage
            name = ref_atlases[ref].cell_name
            cells = list(set(lineage.keys()).union(set([v for values in list(lineage.values()) for v in values])))

            for c in cells:
                if c not in name:
                    continue
                if name[c] == m:
                    output_selections[keyscore][c] = score
                    output_selections[keydecre][c] = ds / score

    #
    # reporting
    #
    monitoring.to_log_and_console("====== division permutation proposal =====")
    monitoring.to_log_and_console("------ cell-based view")
    corrections_by_atlas = {}
    for s in stages:
        if len(corrections[s]) == 0:
            continue
        msg = "  - generation " + str(s)
        monitoring.to_log_and_console(msg)
        mothers = list(corrections[s].keys())
        mothers.sort()
        for m in mothers:
            if len(corrections[s][m]) == 0:
                continue
            tmp = [c[0] for c in corrections[s][m]]
            tmp.sort()
            for a in tmp:
                corrections_by_atlas[a] = corrections_by_atlas.get(a, []) + [m]
            msg = "    - division of '" + str(m) + "': "
            for i, r in enumerate(tmp):
                msg += str(r)
                if i < len(tmp)-1:
                    msg += ", "
            monitoring.to_log_and_console(msg)
    if len(corrections_by_atlas) > 0:
        monitoring.to_log_and_console("------ atlas-based view")
        refs = list(corrections_by_atlas.keys())
        refs.sort()
        for r in refs:
            msg = "  - reference '" + str(r) + "': " + str(corrections_by_atlas[r])
            monitoring.to_log_and_console(msg)

    if len(selection) > 0:
        quadruplet = []
        for m in selection:
            (a, score) = selection[m][0]
            if len(selection[m]) <= 1:
                continue
            for i, (ref, ds) in enumerate(selection[m]):
                if i == 0:
                    continue
                quadruplet += [(m, ref, score, 100.0 * ds / score)]
        quadruplet = sorted(quadruplet, key=operator.itemgetter(1))
        quadruplet = sorted(quadruplet, key=operator.itemgetter(3), reverse=True)
        monitoring.to_log_and_console("------ average distance percentage decrease view")
        for q in quadruplet:
            msg = "  - division of '" + str(q[0]) + "' in '" + str(q[1]) + "': "
            msg += "{:2.2f}% decrease of {:1.2f} average distance".format(q[3], q[2])
            monitoring.to_log_and_console(msg)

    monitoring.to_log_and_console("==========================================")


########################################################################################
#
#
#
########################################################################################

def _print_common_neighborhoods(neighborhood0, neighborhood1, title=None):
    #
    # used by get_score(), to display neighborhoods after being put in a common frame
    #
    msg = ""
    if title is not None and isinstance(title, str):
        msg += title + " = "
    msg += "{"
    key_list = sorted(list(set(neighborhood0.keys()).union(set(neighborhood1.keys()))))
    for k in key_list:
        msg += str(k) + ": "
        if k in neighborhood0.keys():
            msg += str(neighborhood0[k])
        else:
            msg += "NULL"
        msg += " <-> "
        if k in neighborhood1.keys():
            msg += str(neighborhood1[k])
        else:
            msg += "NULL"
        if k != key_list[-1]:
            msg += ",\n\t "
        else:
            msg += "}"
    monitoring.to_log_and_console(msg)


def _division_distance(daughter00, daughter01, daughter10, daughter11, innersurfaces=[], debug=False):
    """
    Compute distance between two contact surface vectors. Do not compute 'common' neighborhood.
    Parameters
    ----------
    daughter00
    daughter01
    daughter10
    daughter11
    innersurfaces

    Returns
    -------

    """

    #
    # get the sum of difference, as well as the sums of contact surfaces
    # cells in 'innersurfaces' are excluded
    #
    nm0, n00, n10 = uneighborhood.cell_distance_elements(daughter00, daughter10, innersurfaces=innersurfaces)
    nm1, n01, n11 = uneighborhood.cell_distance_elements(daughter01, daughter11, innersurfaces=innersurfaces)
    score = (nm0 + nm1) / (n00 + n10 + n01 + n11)
    return score


def division_distance(daughter00, daughter01, daughter10, daughter11, change_contact_surfaces=True, innersurfaces=[],
                      debug=False):
    """
    Compute the distance between two divisions (a division is a couple of daughter cells) with paired
        daughter cells (daughter00 is paired with daughter10 and daughter01 is paired with daughter11).
        The distance between two cells (ie two neighborhood) is defined by the ratio between the
        sum of absolute differences of (eligible) contact surfaces over the two sums of (eligible)
        contact surfaces for each neighborhood.
        The distance between two divisions is defined by the ratio between the sums of absolute differences
        of (eligible) contact surfaces for each couple of paired cells over the four sums of (eligible)
        contact surfaces for each neighborhood.
    Parameters
    ----------
    daughter00: dictionary depicting the neighborhood of daughter #0 of ref #0.
        Each key is a named neighbor, and the associated dictionary value give the contact surface.
    daughter01: dictionary depicting the neighborhood of daughter daughter #1 of ref #0
    daughter10: dictionary depicting the neighborhood of daughter daughter #0 of ref #1
    daughter11: dictionary depicting the neighborhood of daughter daughter #1 of ref #1
    change_contact_surfaces: True or False
    innersurfaces: name of the cells that define the innersurface; typically, they are the two names
        of the daughter cells when computing the distance between two divisions, which is built
        upon the distances between the neighborhood of each daughter. It comes to exclude the
        contact surface with the sister cell.
    debug

    Returns
    -------

    """

    if change_contact_surfaces:
        tmp = {'foo': {0: daughter00, 1: daughter10}}
        v0 = uneighborhood.build_same_contact_surfaces(tmp, ['foo'], debug=debug)
        tmp = {'foo': {0: daughter01, 1: daughter11}}
        v1 = uneighborhood.build_same_contact_surfaces(tmp, ['foo'], debug=debug)
        score = _division_distance(v0['foo'][0], v1['foo'][0], v0['foo'][1], v1['foo'][1], innersurfaces=innersurfaces)
    else:
        score = _division_distance(daughter00, daughter01, daughter10, daughter11, innersurfaces=innersurfaces)

    return score


def _division_signature(daughter00, daughter01, daughter10, daughter11, innersurfaces=[]):
    neighbors = set(daughter00.keys()).union(set(daughter01.keys()), set(daughter10.keys()), set(daughter11.keys()))
    den = 0.0
    num = 0.0
    for k in neighbors:
        if k in innersurfaces:
            continue
        if k in daughter00 and k in daughter10:
            num += abs(daughter00[k] - daughter10[k])
        elif k in daughter00 and k not in daughter10:
            num += abs(daughter00[k])
        elif k not in daughter00 and k in daughter10:
            num += abs(daughter10[k])
        if k in daughter01 and k in daughter11:
            num += abs(daughter01[k] - daughter11[k])
        elif k in daughter01 and k not in daughter11:
            num += abs(daughter01[k])
        elif k not in daughter01 and k in daughter11:
            num += abs(daughter11[k])
        mnum0 = 0.0
        if k in daughter00:
            mnum0 += daughter00[k]
        if k in daughter01:
            mnum0 += daughter01[k]
        mnum1 = 0.0
        if k in daughter10:
            mnum1 += daughter10[k]
        if k in daughter11:
            mnum1 += daughter11[k]
        num -= abs(mnum0 - mnum1)
        den += mnum0 + mnum1
    score = num / den
    if score < 0.0:
        return 0.0
    return score


def division_signature(daughter00, daughter01, daughter10, daughter11, change_contact_surfaces=True, innersurfaces=[],
                       debug=False):
    """
    Compute the distance increment between two divisions (a division is a couple of daughter cells) with paired
        daughter cells (daughter00 is paired with daughter10 and daughter01 is paired with daughter11).
        The distance between two cells (ie two neighborhood) is defined by the ratio between the
        sum of absolute differences of (eligible) contact surfaces over the two sums of (eligible)
        contact surfaces for each neighborhood.
        The distance increment between two divisions is defined as the division distance (between the
        neighborhoods of the daughter cells) minus the mother cell distance (between the
        neighborhoods of the mother cells). It is computed by the ratio between the sums of absolute
        differences of (eligible) contact surfaces for each couple of paired cells *minus* the sum of absolute
        differences of (eligible) contact surfaces for the mother cell (it comes to fuse daughter00 and daughter01
        on the one hand, and daughter10 and daughter11 on the other hand) over the four sums of (eligible)
        contact surfaces for each neighborhood.

    Parameters
    ----------
    daughter00: dictionary depicting the neighborhood of daughter #0 of ref #0.
        Each key is a named neighbor, and the associated dictionary value give the contact surface.
    daughter01: dictionary depicting the neighborhood of daughter daughter #1 of ref #0
    daughter10: dictionary depicting the neighborhood of daughter daughter #0 of ref #1
    daughter11: dictionary depicting the neighborhood of daughter daughter #1 of ref #1
    change_contact_surfaces: True or False
    innersurfaces: name of the cells that define the innersurface; typically, they are the two names
        of the daughter cells when computing the distance between two divisions, which is built
        upon the distances between the neighborhood of each daughter. It comes to exclude the
        contact surface with the sister cell.
    debug

    Returns
    -------

    """

    if change_contact_surfaces:
        tmp = {'foo': {0: daughter00, 1: daughter10}}
        v0 = uneighborhood.build_same_contact_surfaces(tmp, ['foo'], debug=debug)
        tmp = {'foo': {0: daughter01, 1: daughter11}}
        v1 = uneighborhood.build_same_contact_surfaces(tmp, ['foo'], debug=debug)
        score = _division_signature(v0['foo'][0], v1['foo'][0], v0['foo'][1], v1['foo'][1], innersurfaces=innersurfaces)
    else:
        score = _division_signature(daughter00, daughter01, daughter10, daughter11, innersurfaces=innersurfaces)

    return score

###########################################################
#
#
#
############################################################

class DivisionAtlases(atlascell.CellAtlases):
    def __init__(self, parameters=None):

        atlascell.CellAtlases.__init__(self, parameters)

        self._use_common_neighborhood = False

        # dictionary indexed by 'cell name' where 'cell name' is a mother cell giving the list
        # of references/atlases available for the two daughters
        self._divisions = {}

        # dictionary indexed by [delay_from_division]['cell name']
        # values are the pair of daughter cells (the largest first)
        # this is the set of divisions where the same daughter is always larger than the other
        # (and there are at least 5 atlases)
        self._unequal_divisions = {}

        # dictionary index by atlas name
        # to keep trace of some output (kept as morphonet selection)
        self._output_selections = {}

    ############################################################
    #
    # getters / setters
    #
    ############################################################

    def get_use_common_neighborhood(self):
        return self._use_common_neighborhood

    def get_divisions(self):
        return self._divisions

    def get_unequal_divisions(self, delay_from_division=None):
        if delay_from_division is None:
            delay = self.get_default_delay()
        else:
            delay = delay_from_division
        if delay not in self._unequal_divisions:
            self._unequal_divisions[delay] = {}
        return self._unequal_divisions[delay]

    def get_output_selections(self):
        return self._output_selections

    ############################################################
    #
    #
    #
    ############################################################

    def _build_divisions(self, delay_from_division=None):
        """
        Build a dictionary index by mother cell name. Each entry contains reference names
        for which the both daughters exist
        Returns
        -------

        """
        proc = "_build_divisions"

        if self._divisions is not None:
            del self._divisions
            self._divisions = {}

        #
        # get all references per division/mother cells
        #
        neighborhoods = self.get_cell_neighborhood(delay_from_division=delay_from_division)
        cell_names = sorted(list(neighborhoods.keys()))
        references = {}
        for cell_name in cell_names:
            mother_name = uname.get_mother_name(cell_name)
            references[mother_name] = references.get(mother_name, set()).union(set(neighborhoods[cell_name].keys()))

        #
        # remove references that does not exist for one daughter
        #
        mother_names = sorted(references.keys())
        for n in mother_names:
            daughters = uname.get_daughter_names(n)
            #
            # check whether each reference has the two daughters
            #
            refs = list(references[n])
            for r in refs:
                if daughters[0] in neighborhoods and r in neighborhoods[daughters[0]] and \
                        daughters[1] in neighborhoods and r in neighborhoods[daughters[1]]:
                    self._divisions[n] = self._divisions.get(n, []) + [r]
                else:
                    msg = "    " + str(proc) + ": remove atlas '" + str(r) + "' for division '" + str(n) + "'"
                    monitoring.to_log_and_console(msg)

    #
    #
    #

    def _build_unequal_divisions(self, delay_from_division=None):
        """
        Build a dictionary index by mother cell name. Each entry contains reference names
        for which the both daughters exist
        Returns
        -------

        """

        minimal_references = 5

        delay = delay_from_division
        if delay is None:
            delay = self.get_default_delay()

        if self._unequal_divisions is None:
            self._unequal_divisions = {}
        if delay in self._unequal_divisions:
            del self._unequal_divisions[delay]
        self._unequal_divisions[delay] = {}

        divisions = self.get_divisions()

        volumes = self.get_volumes(delay_from_division=delay)

        for mother in divisions:
            d = uname.get_daughter_names(mother)
            vol01 = 0
            vol10 = 0
            for r in divisions[mother]:
                if volumes[d[0]][r] > volumes[d[1]][r]:
                    vol01 += 1
                elif volumes[d[0]][r] < volumes[d[1]][r]:
                    vol10 += 1
            if vol01 > minimal_references and vol10 == 0:
                self._unequal_divisions[delay][mother] = [d[0], d[1]]
            elif vol10 > minimal_references and vol01 == 0:
                self._unequal_divisions[delay][mother] = [d[1], d[0]]

        msg = "found " + str(len(self._unequal_divisions[delay])) + " unequal divisions "
        msg += "at delay = " + str(delay) + " "
        msg += "(more than " + str(minimal_references) + " atlases) in " + str(len(divisions)) + " divisions"
        monitoring.to_log_and_console("\t" + msg)
        return

    #
    #
    #

    def build_division_atlases(self, parameters):

        #
        # cell based part
        # extract daughter cell neighborhoods for required delays
        #
        delays = [parameters.name_delay_from_division]
        if parameters.confidence_delay_from_division is not None and \
                parameters.confidence_delay_from_division not in delays:
            delays += [parameters.confidence_delay_from_division]
        self.set_default_delay(parameters.name_delay_from_division)
        for d in delays:
            self.build_cell_atlases(parameters, delay_from_division=d)

        #
        # build common neighborhood reference (for both daughter cells) if required
        #
        delays = self.get_cell_neighborhood_delays()
        if parameters.use_common_neighborhood:
            monitoring.to_log_and_console("... build common neighborhoods", 1)
            for d in delays:
                neighborhoods = self.get_cell_neighborhood(delay_from_division=d)
                self.set_cell_neighborhood(_build_common_neighborhoods(neighborhoods), delay_from_division=d)
            self._use_common_neighborhood = True
            monitoring.to_log_and_console("    done", 1)

        #
        # dictionary indexed by mother cell names,
        # give list of references for which both daughter cells exist
        #
        monitoring.to_log_and_console("... build division list", 1)
        self._build_divisions(delay_from_division=parameters.name_delay_from_division)
        monitoring.to_log_and_console("    done", 1)

        #
        # dictionary indexed by mother cell names,
        # give list of daughter cells, the largest one being the first one
        #
        monitoring.to_log_and_console("... build unequal division list", 1)
        for d in delays:
            self._build_unequal_divisions(delay_from_division=d)
        monitoring.to_log_and_console("    done", 1)

        if parameters.division_diagnosis:
            monitoring.to_log_and_console("")
            monitoring.to_log_and_console("============================================================")
            monitoring.to_log_and_console("===== diagnosis: atlases pairwise disagreements")
            _diagnosis_pairwise_switches(self, parameters)
            monitoring.to_log_and_console("===== diagnosis: dendrogram/linkage diagnosis")
            _diagnosis_linkage(self, parameters)
            monitoring.to_log_and_console("============================================================")
            monitoring.to_log_and_console("")

        #
        # look for daughter that may improve a global score
        # report it in the console/log file
        # as well as in morphonet selection file
        #
        if parameters.division_permutation_proposal:
            division_permutation_proposal(self, parameters)

    ############################################################
    #
    #
    #
    ############################################################

    def extract_division_neighborhoods(self, mother_name, delay_from_division=None):
        """
        Extract a sub-dictionary built from the daughter cell neighborhoods only for the references where
        the division of the targeted mother cell exists

        :param mother_name: cell name for which the divisions are searched;
        :param delay_from_division: neighborhoods are extracted after some delay from the division
        :return:
            A dictionary of cell neighborhoods indexed by [reference][0|1] where 'reference' is the atlas name
            (where the division occurs) and 0|1 corresponds to daughter names issued from uname.get_daughter_names()
        """

        delay = delay_from_division
        if delay is None:
            delay = self.get_default_delay()

        divisions = self.get_divisions()
        neighborhoods = self.get_cell_neighborhood(delay_from_division=delay)
        daughters = uname.get_daughter_names(mother_name)

        config = {}
        for r in divisions[mother_name]:
            config[r] = {}
            config[r][0] = copy.deepcopy(neighborhoods[daughters[0]][r])
            config[r][1] = copy.deepcopy(neighborhoods[daughters[1]][r])
        return config
