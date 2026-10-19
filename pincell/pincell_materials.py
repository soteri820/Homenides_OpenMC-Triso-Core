import openmc


def build_materials():
       
    ## setting up uranium oxide fuel
    # defines a uo2 new material with id tag and label passed as arguments to function
    uo2 = openmc.Material(1, "uo2")
    # adds nuclides as atom ratios
    #   0.03 to 0.97 is 3% enrichment
    uo2.add_nuclide('U235', 0.03)
    uo2.add_nuclide('U238', 0.97)
    #   2 oxygen atoms per uranium atom
    uo2.add_nuclide('O16', 2.0)
    #   sets density of uo2 mixture
    uo2.set_density('g/cm3', 10.0)


    ## setting up zirconium cladding
    #  add_element takes natural Zr, OpenMC splits it into its isotopes
    #  no id tag passed as shown in demo, tag is automatically added anyway
    zirconium = openmc.Material(name="zirconium")
    zirconium.add_element('Zr', 1.0)
    #   sets density of zirconium
    zirconium.set_density('g/cm3', 6.6)

    
    ## setting up water
    water = openmc.Material(name="h2o")
    water.add_nuclide('H1',  2.0)
    water.add_nuclide('O16', 1.0)
    water.set_density('g/cm3', 1.0)
    #   thermal scattering table for hydrogen bound in water
    water.add_s_alpha_beta('c_H_in_H2O')


    return {"uo2": uo2, "zirconium": zirconium, "water": water}

#    mats = build_materials()
#    for m in mats.values():
#        print(m)

### ODDLY ENOUGH, OPENMC DOESNT HOLD VALUES OF MATERIAL DENSITY, OR OTHER ENGINEERING INPUTS (GEOMETRY OR COMPOSITION)
### ONLY CONTAINS REACTOR PHYSICS RELATED STUFF LIKE PHOTON DATA, NEUTRON DATA, THERMAL SCATTERING