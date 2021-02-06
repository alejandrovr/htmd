from htmd.ui import *
from htmd.vmdviewer import getCurrentViewer
import random
import sys
import click

def LJ_potential(prot,lig):
    from scipy.spatial.distance import cdist
    pcoords = prot.coords.squeeze()
    ligcoords = lig.coords.squeeze()
    pl_dists = cdist(pcoords,ligcoords)
    return np.min(pl_dists)

if __name__ == "__main__":

    KEYS_MAPPING = {'w': 'movx', 's': 'mov-x',
                    'd': 'movy', 'a': 'mov-y',
                    'q': 'movz', 'e': 'mov-z',
                    '\t': 'nextdih', '<': 'switch_dir',
                    ' ':  'updatedih'}

    levels = {'3iej.pdb':('A','599'),}
    levels_keys = list(levels.keys())
    selected_level = random.choice(levels_keys)

    crystal = Molecule(selected_level)
    prot = crystal.copy()
    prot.filter('protein and chain {} and noh and (same residue as within 5 of resname {})'.format(levels[selected_level][0], levels[selected_level][1]))
    prot = prot.copy()
    prot.view(style='Licorice')

    mol = crystal.copy()
    mol.filter('chain {} and resname {}'.format(levels[selected_level][0], levels[selected_level][1]))
    mol.get_rot_bonds()
    print('Crystal LJ:', LJ_potential(prot, mol))
    mol.view()    

    [mol._moveVMD(action='scaleout') for i in range(3)]
    mol._moveVMD(action='nextdih')
            

    ljpot = LJ_potential(prot, mol)

    finished = False
    while not finished:
        try:
            pressed_key = click.getchar()
            target = KEYS_MAPPING[pressed_key]
            mol._moveVMD(action=target)
        except KeyError:
            print('Bad key! Pay attention dude, we are trying to put a drug in the market!')







