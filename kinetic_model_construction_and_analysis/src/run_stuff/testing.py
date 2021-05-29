import cobra
import pandas as pd
from cobra import Model, Reaction, Metabolite

reactions = pd.read_excel('/home/mrama/Postdoc/putida_project/models/putica_TCA_OP_reg_no_gth_cobra.xlsx')

model = Model('putida_no_gth')
for i in range(reactions['rxn_id'].shape[0]):
    r = Reaction(reactions['rxn_id'][i])
    model.add_reaction(r)
    r.build_reaction_from_string(reactions['rxn_stoic'][i])
    model.reactions.get_by_id(reactions['rxn_id'][i]).lower_bound = reactions['lb'][i]-100
    model.reactions.get_by_id(reactions['rxn_id'][i]).upper_bound = reactions['ub'][i]+100


#rxn_id = 'R_ENO'
#model.reactions.get_by_id(rxn_id).lower_bound = -10000
#model.reactions.get_by_id(rxn_id).upper_bound = 10000
#print(model.reactions.get_by_id(rxn_id).reversibility)

for rxn in model.reactions:
    if rxn.lower_bound >=rxn.upper_bound:
        print(rxn.lower_bound, rxn.upper_bound, rxn.lower_bound >=rxn.upper_bound)

from cobra.sampling import sample

s = sample(model, 100)
print(s)