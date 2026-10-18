import openmc

def build_triso_materials():
    ## returns a dict of the six materials in a TRISO compact


    ## fuel kernel
    # Modeling Uranium oxycarbide (UCO), assuming it is in use in HTGR core over UO2 type
    # numbers below are relative atom fractions
    # U235/(U235+U238) = 14% enriched, O and C making up the rest of the composition
    fuel = openmc.Material(name='trisofuel')
    fuel.set_density('g/cm3', 10.5)
    fuel.add_nuclide('U235', 10.5)
    fuel.add_nuclide('U238', 2.8697e-01)
    fuel.add_nuclide('O16', 5.0e-01)
    fuel.add_element('C', 1.6667e-01)

    ## porous carbon buffer that absorbs fission recoils and gas swelling
    # intentionally low density 
    buffer = openmc.Material(name='buffer') 
    buffer.set_density('g/cm3', 1.0)
    buffer.add_element('C', 1.0)
    buffer.add_s_alpha_beta('c_Graphite')

    ## inner and outer pyrolytic carbon (dense carbon layers)
    ipyc = openmc.Material(name='ipyc')
    ipyc.set_density('g/cm3', 1.9)
    ipyc.add_element('C', 1.0)
    ipyc.add_s_alpha('c_Grpahite')

    opyc = openmc.Material(name='opyc')
    opyc.set_density('g/cm3', 1.87)
    opyc.add_element('C', 1.0)
    opyc.add_s_alpha('c_Grpahite')

    ## Silicon carbide (SiC), the main Pressure and FP product barrier
    # no S(a,b) here, thats only for moderator-like materials
    sic = openmc.Material(name='sic')
    sic.set_density('g/cm3', 3.2)
    sic.add_element('C', 0.5)
    sic.add_element('Si', 0.5)

    ## matrix graphite
    matrix = openmc.Material(name='matrix')
    matrix.set_density('g/cm3', 1.1995)
    matrix.add_element('C', 1.0)
    matrix.add_s_alpha_beta('c_graphite')

    return {
        'triso_fuel': fuel,
        'buffer' : buffer,
        'ipyc' : ipyc,
        'sic' : sic,
        'opyc' : opyc,
        'matrix' : matrix,        
        }