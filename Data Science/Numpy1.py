''' Both .loc[ ] and .iloc[ ] 
	may be used with a boolean 
	array to subset the data.
'''

import pandas as pd
import numpy as np

presidents_df = pd.read_csv('https://sololearn.com/uploads/files/president_heights_party.csv', index_col='name')

# testing label indexing:
loc_arr = np.array(('George Washington',
                    'Abraham Lincoln',
                    'Theodore Roosevelt'))
print(presidents_df.loc[loc_arr])
print('\n\n')

# testing integer indexing:
iloc_arr = np.array((0, 15, 25))
print(presidents_df.iloc[iloc_arr])
print('\n\n')

# testing boolean array subset:
bool_arr = np.full(45, False, dtype=bool)
bool_arr[iloc_arr] = True
print(bool_arr)
print('\n\n')
print(presidents_df.loc[bool_arr])
print('\n\n')
print(presidents_df.iloc[bool_arr])