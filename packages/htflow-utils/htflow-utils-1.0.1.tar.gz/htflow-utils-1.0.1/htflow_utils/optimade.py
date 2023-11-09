from datetime import datetime

from pymatgen.core.structure import Structure
from pymatgen.core.surface import Slab

optimade_fields = [
    "id",
    "last_modified",
    "chemsys",
    "elements",
    "nelements",
    "elements_ratios",
    "pretty_formula",
    "chemical_formula_hill",
    "formula_anonymous",
    "dimension_types",
    "nperiodic_dimensions",
    "lattice_vectors",
    "cartesian_site_positions",
    "nsites",
    "species",
    "species_at_sites",
    "assemblies",
    "structure_features",
]

fields_to_keep = {
    "surface": [
        "surface_energy",
        "structure",
        "fully_relaxed_slab",
        "comp_params",
        "hkl",
        "sg_params",
        "slab_params",
        "terminations",
        "mpid",
    ]
}


def optimadeify_document(document, document_type):
    if document_type == "bulk":
        struct = document.get("structure_fromMP")
        struct = Structure.from_dict(struct)
    elif document_type == "surface":
        struct = document.get("structure")
        if not struct:
            raise KeyError(f'Structure is missing from {document["_id"]}')
        struct = Slab.from_dict(struct)
    else:
        raise ValueError("Entry type must be either 'bulk' or 'slab'.")

    species = struct.species
    comp = struct.composition
    optimade_doc = {}
    for field in optimade_fields:
        if field == "id":
            optimade_doc[field] = document["uid"]
        if field == "elements":
            optimade_doc[field] = sorted([str(i) for i in comp])
        if field == "nelements":
            optimade_doc[field] = len(comp)
        if field == "chemsys":
            optimade_doc[field] = "-".join([a for a in sorted([str(i) for i in comp])])
        if field == "elements_ratios":
            species_str = [str(i) for i in species]
            ratios = [
                species_str.count(a) / len(species_str)
                for a in sorted([str(i) for i in comp])
            ]
            optimade_doc[field] = ratios
        if field == "pretty_formula":
            optimade_doc[field] = "".join(sorted([str(i) for i in comp]))
        if field == "formula_anonymous":
            optimade_doc[field] = comp.anonymized_formula
        if field == "dimension_types":
            optimade_doc[field] = [1, 1, 1]
        if field == "nperiodic_dimensions":
            optimade_doc[field] = 3
        if field == "lattice_vectors":
            lat_list = [a.tolist() for a in struct.lattice.matrix]
            optimade_doc[field] = lat_list
        if field == "cartesian_site_positions":
            coord_list = [a.tolist() for a in struct.cart_coords]
            optimade_doc[field] = coord_list
        if field == "nsites":
            optimade_doc[field] = struct.num_sites
        if field == "species":
            optimade_doc[field] = [
                {"name": a, "chemical_symbols": [a], "concentration": [1.0]}
                for a in sorted([str(i) for i in comp])
            ]
        if field == "species_at_sites":
            optimade_doc[field] = [str(i) for i in species]
        if field == "task_id":
            optimade_doc[field] = document["mpid"]
        if field == "structure_features":
            optimade_doc[field] = []
        if field == "last_modified":
            optimade_doc[field] = datetime.now()

    # reduce document to only the fields we want to keep
    document = {
        f"_surfflow_{k}": v
        for k, v in document.items()
        if k in fields_to_keep[document_type]
    }
    document.update(optimade_doc)

    return document
