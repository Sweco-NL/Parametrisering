import numpy as np
#terugrekenen van rekenwaarde naar karakteristiek (D-stability)

def check_rc(gamma_rc : str):
    if gamma_rc < 1:
        return 'rc factor too low'
    else:
        return 'rc_factor validated'

def partialfactor_phi(phi : float, gamma_phi : float):
    phi_k = np.round(np.degrees(np.arctan(np.tan(np.radians(phi))/gamma_phi)), 2)
    return phi_k

def partialfactor_cohesion(cohesion: float, gamma_cohesion : float):
    cohesion_k = np.round(cohesion / gamma_cohesion, 2)
    return cohesion_k

def partialfactor_su(su: float, gamma_su : float):
    su_k = np.round(su / gamma_su, 2)
    return su_k