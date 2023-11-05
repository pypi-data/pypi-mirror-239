try:
    from sage_lib.StatesGeneratorManager import StatesGeneratorManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing StatesGeneratorManager: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    import copy
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing copy: {str(e)}\n")
    del sys

class SurfaceStatesGenerator(StatesGeneratorManager):
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        super().__init__(name=name, file_location=file_location)   

    def generate_adsorption_states(self, parameter:str, values:np.array=None, file_location:str = None) -> bool:
        containers = []
        directories = ['' for _ in self.containers]
        parameter = parameter.upper().strip()

        for container_index, container in enumerate(self.containers):
            if parameter.upper() == 'MONOATOMIC':
                containers += self.handle_monoatomic_specie(container, values, container_index, file_location)
                directories[container_index] = 'MONOATOMIC'

        self.containers = containers
        return containers

    def handle_monoatomic_specie(self, container, values, container_index, file_location=None):
        # values = ['O']
        sub_directories, containers = [], []

        reaction_sites = container.AtomPositionManager.get_adsorption_sites() 
        offsets = {al: np.array([0, 0, self._covalent_radii[al]*2]) for al in values}
        
        for position_group, direction in [('top', 1), ('bottom', -1)]:
            for position_id, position in enumerate(reaction_sites[position_group]):
                for al in values:
                    container_copy = self.copy_and_update_container(container, f'/adsorption_states/{position_group}_{position_id}', file_location)
                    offset = offsets[al] * direction
                    new_position = position + offset
                    container_copy.AtomPositionManager.add_atom(atomLabels=al, 
                                                                atomPosition=new_position, 
                                                                atomicConstraints=[1, 1, 1])
                    containers.append(container_copy)
                    
                    sub_directories.append(f'{position_group}_{position_id}')

        self.generate_execution_script_for_each_container(sub_directories, container.file_location + '/adsorption_states')
        return containers

path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/OUTCAR'
path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/dataset/CoFeNiOOH_jingzhu/surf_CoFe_4H_4OH/MAG'
SSG = SurfaceStatesGenerator(path)
SSG.readVASPFolder(v=False)

containers = SSG.generate_adsorption_states('MONOATOMIC', ['O'])
SSG.exportVaspPartition()
print( len(SSG.containers) )


