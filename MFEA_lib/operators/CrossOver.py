from typing import Tuple
import numpy as np


class AbstractCrossOver():
    def __init__(self) -> None:
        pass
    def __call__(self, pa, pb, type = None, *args) -> Tuple[np.ndarray, np.ndarray]:
        pass

class SBX_CrossOver(AbstractCrossOver):
    '''
    pa, pb in [0, 1]^n
    '''
    def __init__(self, nc = 15):
        self.nc = nc
    def __call__(self, pa, pb, type = None, p_swap_inter = 0.1, d_swap = 0.1) -> Tuple[np.ndarray, np.ndarray]:
        '''
        type = 'inter' / 'intra' / ('inter1skf', p_swap_inter)
        '''
        assert type == 'inter' or type == 'intra' or type == 'inter1skf'

        u = np.random.rand(len(pa))

        # ~1
        beta = np.where(u < 0.5, (2*u)**(1/(self.nc +1)), (2 * (1 - u))**(-1 / (1 + self.nc)))
        
        #like pa
        c1 = 0.5*((1 + beta) * pa + (1 - beta) * pb)
        #like pb
        c2 = 0.5*((1 - beta) * pa + (1 + beta) * pb)

        c1, c2 = np.clip(c1, 0, 1), np.clip(c2, 0, 1)

        if type == 'intra':
            idx = np.where(np.random.rand(len(pa)) < 0.5)[0]
            c1[idx], c2[idx] = c2[idx], c1[idx]
            
        elif type == 'inter1skf':
            idx = np.where(np.random.rand(len(pa)) < p_swap_inter)[0]
            # idx = np.where((np.random.rand(len(pa)) < p_swap_inter) * (np.abs(c1 - c2) < d_swap))[0]
            # idx = np.where(np.abs(pa - pb) > d_swap)[0]
            c2[idx] = c1[idx]

        return c1, c2

class SBX_refuseInter(AbstractCrossOver):
    '''
    pa, pb in [0, 1]^n
    '''
    def __init__(self, nc = 15):
        self.nc = nc
    def __call__(self, pa, pb, type = None, p_refuse_inter = 0.1, d_swap = 0.) -> Tuple[np.ndarray, np.ndarray]:
        '''
        type = 'inter' / 'intra' / ('inter1skf', p_swap_inter)
        '''
        assert type == 'inter' or type == 'intra' or type == 'inter1skf'

        u = np.random.rand(len(pa))

        # ~1
        beta = np.where(u < 0.5, (2*u)**(1/(self.nc +1)), (2 * (1 - u))**(-1 / (1 + self.nc)))
        
        #like pa
        c1 = 0.5*((1 + beta) * pa + (1 - beta) * pb)
        #like pb
        c2 = 0.5*((1 - beta) * pa + (1 + beta) * pb)

        c1, c2 = np.clip(c1, 0, 1), np.clip(c2, 0, 1)

        if type == 'intra':
            idx = np.where(np.random.rand(len(pa)) < 0.5)[0]
            c1[idx], c2[idx] = c2[idx], c1[idx]
            
        elif type == 'inter1skf':
            idx_refuse = np.where((np.random.rand(len(pa)) < p_refuse_inter) * (np.abs(c2 - c1) > d_swap))[0]
            c2[idx_refuse] = c1[idx_refuse]

        return c1, c2
