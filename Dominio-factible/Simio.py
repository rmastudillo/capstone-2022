import sys
sys.path.append("/Osvaldo_le_gano_en_unm_pique")
from Osvaldo_le_gano_en_unm_pique import as ola

def genera(vec, desc, usad):
    while arr.sum() != total_of_1:
    nuevo_vec = np.random.randint(2, size=(r, c))
    while nuevo_vec in desc and nuevo_vec in usad:
        nuevo_vec = np.random.randint(2, size=(r, c))
        usad.append(nuevo_vec)
    return nuevo_vec, usad

vec = np.random.randint(2, size=(r, c))
usado = []
desc = ola.lst_fact
genera(vec, desc, usado)