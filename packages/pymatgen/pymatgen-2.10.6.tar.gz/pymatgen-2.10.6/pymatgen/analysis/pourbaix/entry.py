"""
Module which defines basic entries for each ion and oxide to compute a
Pourbaix diagram
"""

from __future__ import division

__author__ = "Sai Jayaraman"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.0"
__maintainer__ = "Sai Jayaraman"
__email__ = "sjayaram@mit.edu"
__status__ = "Development"
__date__ = "December 10, 2012"

import re
import math
import csv

from pymatgen.core.periodic_table import Element
from pymatgen.core.structure import Composition
from pymatgen.serializers.json_coders import MSONable
from pymatgen.core.ion import Ion
from pymatgen.phasediagram.entries import PDEntry

PREFAC = 0.0591


class PourbaixEntry(MSONable):
    """
    An object encompassing all data relevant to an ion in a pourbaix diagram.
    Each bulk solid/ion has a free energy g of the form:
    g = g0_ref + 0.0591 log10(conc) - nO mu_H2O + (nH - 2nO) pH
    + phi (-nH + 2nO + q)

    Args:
        entry (ComputedEntry/ComputedStructureEntry/PDEntry/IonEntry): An
            entry object
        energy: Energy of entry
    """
    def __init__(self, entry, correction=0.0, entry_id=None):
        if isinstance(entry, IonEntry):
            self.entry = entry
            self.conc = 1.0e-6
            self.phase_type = "Ion"
            self.charge = entry.composition.charge
        else:
            self.entry = entry
            self.conc = 1.0
            self.phase_type = "Solid"
            self.charge = 0.0
        self.uncorrected_energy = entry.energy
        self.correction = correction
        nH = 0
        nO = 0
        nM = 0
        for elt in self.entry.composition.elements:
            if elt == Element("H"):
                nH = self.entry.composition[elt]
            elif elt == Element("O"):
                nO = self.entry.composition[elt]
            else:
                nM += self.entry.composition[elt]
        self.nM = nM
        self.npH = (nH - 2 * nO)
        self.nH2O = nO
        self.nPhi = (nH - 2 * nO - self.charge)
        self.name = self.entry.composition.reduced_formula
        if self.phase_type == "Solid":
            self.name += "(s)"
        try:
            self.entry_id = entry.entry_id
        except AttributeError:
            self.entry_id = entry_id

    @property
    def energy(self):
        return self.uncorrected_energy + self.correction

    @property
    def g0(self):
        """
        Return g0 for the entry. Legacy function.
        """
        return self.energy

    @property
    def conc_term(self):
        """
        Returns the concentration contribution to the free energy.
        """
        return self.normalization_factor * PREFAC * math.log10(self.conc)

    def g0_add(self, term):
        """
        Add a correction term to g0.

        Args:
            term: Correction term to add to g0
        """
        self.correction += term

    def g0_replace(self, term):
        """
        Replace g0 by a different value.

        Args:
            term: New value for g0
        """
        self.uncorrected_energy = term
        self.correction = 0.0

    @property
    def to_dict(self):
        """
        Returns dict which contains Pourbaix Entry data.
        Note that the pH, voltage, H2O factors are always calculated when
        constructing a PourbaixEntry object.
        """
        d = {"@module": self.__class__.__module__,
             "@class": self.__class__.__name__}
        if isinstance(self.entry, IonEntry):
            d["entry type"] = "Ion"
        else:
            d["entry type"] = "Solid"
        d["entry"] = self.entry.to_dict
        d["pH factor"] = self.npH
        d["voltage factor"] = self.nPhi
        d["concentration"] = self.conc
        d["H2O factor"] = self.nH2O
        d["energy"] = self.energy
        d["correction"] = self.correction
        d["entry_id"] = self.entry_id
        return d

    @classmethod
    def from_dict(cls, d):
        """
        Returns a PourbaixEntry by reading in an Ion
        """
        entry_type = d["entry type"]
        if entry_type == "Ion":
            entry = IonEntry.from_dict(d["entry"])
        else:
            entry = PDEntry.from_dict(d["entry"])
        correction = d["correction"]
        entry_id = d["entry_id"]
        return PourbaixEntry(entry, correction, entry_id)

    @property
    def normalization_factor(self):
        """
        Normalize each entry by nM
        """
        fact = 1.0 / self.nM
        return fact

    def scale(self, factor):
        """
        Normalize all entries by normalization factor.

        Args:
            factor: Normalization factor
        """
        self.npH *= factor
        self.nPhi *= factor
        self.nH2O *= factor
        self.uncorrected_energy *= factor
        self.correction *= factor

    def normalize(self, factor):
        self.scale(factor)

    @property
    def composition(self):
        """
        Returns composition
        """
        return self.entry.composition

    def reduced_entry(self):
        """
        Calculate reduction factor for composition, and reduce parameters by
        this factor.
        """
        reduction_factor = self.entry.composition.\
            get_reduced_composition_and_factor()[1]
        self.nM /= reduction_factor
        self.scale(1.0 / reduction_factor)

    @property
    def num_atoms(self):
        """
        Return number of atoms in current formula. Useful for normalization
        """
        return self.entry.composition.num_atoms\
            / self.entry.composition.get_reduced_composition_and_factor()[1]

    def __repr__(self):
        return "Pourbaix Entry : {} with energy = {:.4f}, npH = {}, nPhi = {},\
             nH2O = {}".format(self.entry.composition, self.g0, self.npH,
                               self.nPhi, self.nH2O)

    def __str__(self):
        return self.__repr__()


class MultiEntry(PourbaixEntry):
    """
    PourbaixEntry-like object for constructing multi-elemental Pourbaix
    diagrams.
    """
    def __init__(self, entry_list, weights=None):
        """
        Initializes a MultiEntry.

        Args:
            entry_list: List of component PourbaixEntries
            weights: Weights associated with each entry. Default is None
        """
        if weights is None:
            self.weights = [1.0] * len(entry_list)
        else:
            self.weights = weights
        self.entrylist = entry_list
        self.correction = 0.0
        self.uncorrected_energy = 0.0
        self.npH = 0.0
        self.nPhi = 0.0
        self.nH2O = 0.0
        self.nM = 0.0
        self.name = ""
        self.entry_id = list()
        for i in xrange(len(entry_list)):
            entry = entry_list[i]
            self.uncorrected_energy += self.weights[i] * \
                entry.uncorrected_energy
            self.correction += self.weights[i] * entry.correction
            self.npH += self.weights[i] * entry.npH
            self.nPhi += self.weights[i] * entry.nPhi
            self.nH2O += self.weights[i] * entry.nH2O
            self.nM += self.weights[i] * entry.nM
            self.name += entry.name + " + "
            self.entry_id.append(entry.entry_id)
        self.name = self.name[:-3]

    @property
    def normalization_factor(self):
        """
        Normalize each entry by nM
        """
        norm_fac = 0.0
        for i in xrange(len(self.entrylist)):
            entry = self.entrylist[i]
            for el in entry.composition.elements:
                if (el == Element("O")) | (el == Element("H")):
                    continue
                if entry.phase_type == 'Solid':
                    red_fac = entry.composition.\
                        get_reduced_composition_and_factor()[1]
                else:
                    red_fac = 1.0
                norm_fac += self.weights[i] * entry.composition[el] / red_fac
        fact = 1.0 / norm_fac
        return fact

    def __repr__(self):
        str = "Multiple Pourbaix Entry : with energy = {:.4f}, npH = {}, "\
            "nPhi = {}, nH2O = {}".format(
            self.g0, self.npH, self.nPhi, self.nH2O)
        str += ", species: "
        for entry in self.entrylist:
            str += entry.name + " + "
        return str[:-3]

    def __str__(self):
        return self.__repr__()

    @property
    def conc_term(self):
        sum_conc = 0.0
        for i in xrange(len(self.entrylist)):
            entry = self.entrylist[i]
            sum_conc += self.weights[i] * PREFAC * math.log10(entry.conc)
        return sum_conc * self.normalization_factor


class IonEntry(PDEntry):
    """
    Object similar to PDEntry, but contains an Ion object instead of a
    Composition object.

    Args:
        comp: Ion object
        energy: Energy for composition.
        name: Optional parameter to name the entry. Defaults to the
            chemical formula.

    .. attribute:: name

        A name for the entry. This is the string shown in the phase diagrams.
        By default, this is the reduced formula for the composition, but can be
        set to some other string for display purposes.
    """
    def __init__(self, ion, energy, name=None):
        self.energy = energy
        self.composition = ion
        self.name = name if name else self.composition.reduced_formula

    @classmethod
    def from_dict(cls, d):
        """
        Returns an IonEntry object from a dict.
        """
        return IonEntry(Ion.from_dict(d["composition"]), d["energy"])

    @property
    def to_dict(self):
        """
        Creates a dict of composition, energy, and ion name
        """
        d = {"composition": self.composition.to_dict, "energy": self.energy}
        return d

    @property
    def energy_per_atom(self):
        """
        Return final energy per atom
        """
        return self.energy / self.composition.num_atoms

    def __repr__(self):
        return "IonEntry : {} with energy = {:.4f}".format(self.composition,
                                                           self.energy)

    def __str__(self):
        return self.__repr__()


class PourbaixEntryIO(object):
    """
    Class to import and export Pourbaix entries from a csv file
    """
    @staticmethod
    def to_csv(filename, entries, latexify_names=False):
        """
        Exports Pourbaix entries to a csv

        Args:
            filename: Filename to write to.
            entries: Entries to export.
            latexify_names: Format entry names to be LaTex compatible, e.g.,
                Li_{2}O
        """
        elements = set()
        map(elements.update, [entry.entry.composition.elements
                              for entry in entries])
        elements = sorted(list(elements), key=lambda a: a.X)
        writer = csv.writer(open(filename, "wb"), delimiter=",",
                            quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Name"] + elements + ["Energy"] + ["Entry Type"]
                        + ["Charge"] + ["Concentration"])
        for entry in entries:
            row = [entry.name if not latexify_names
                   else re.sub(r"([0-9]+)", r"_{\1}", entry.name)]
            if entry.phase_type == "Solid":
                reduction_fac = entry.entry.composition.\
                    get_reduced_composition_and_factor()[1]
            else:
                reduction_fac = 1.0
            row.extend([entry.entry.composition[el] / reduction_fac
                        for el in elements])
            if entry.phase_type == "Solid":
                reduction_fac = 1.0
            row.append(entry.g0 / reduction_fac)
            row.append(entry.phase_type)
            row.append(entry.charge / reduction_fac)
            row.append(entry.conc)
            writer.writerow(row)

    @staticmethod
    def from_csv(filename):
        """
        Imports PourbaixEntries from a csv.

        Args:
            filename: Filename to import from.

        Returns:
            List of Entries
        """
        reader = csv.reader(open(filename, "rb"), delimiter=",",
                            quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        entries = list()
        header_read = False
        for row in reader:
            if not header_read:
                elements = row[1:(len(row) - 4)]
                header_read = True
            else:
                name = row[0]
                energy = float(row[-4])
                conc = float(row[-1])
                comp = dict()
                for ind in range(1, len(row) - 4):
                    if float(row[ind]) > 0:
                        comp[Element(elements[ind - 1])] = float(row[ind])
                phase_type = row[-3]
                if phase_type == "Ion":
                    PoE = PourbaixEntry(IonEntry(Ion.from_formula(name),
                                                 energy))
                    PoE.conc = conc
                    PoE.name = name
                    entries.append(PoE)
                else:
                    entries.append(PourbaixEntry(PDEntry(Composition(comp),
                                                         energy)))
        elements = [Element(el) for el in elements]
        return elements, entries


def ion_or_solid_comp_object(formula):
    """
    Returns either an ion object or composition object given
    a formula.

    Args:
        formula: String formula. Eg. of ion: NaOH(aq), Na[+];
            Eg. of solid: Fe2O3(s), Fe(s), Na2O

    Returns:
        Composition/Ion object
    """
    m = re.search(r"\[([^\[\]]+)\]|\(aq\)", formula)
    if m:
        comp_obj = Ion.from_formula(formula)
    elif re.search(r"\(s\)", formula):
        comp_obj = Composition(formula[:-3])
    else:
        comp_obj = Composition(formula)
    return comp_obj
