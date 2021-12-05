# %run ../src/tree_spider.py
# %run ../src/utils.py

import sys
sys.path.insert(1, '../src/')

from tree_spider import *
from utils import *

all_meta_data = pd.read_csv('../data/ordinates_meta_data.csv', sep = '*')
all_meta_data_ecode_360 = all_meta_data.query('Site == "General Code"').reset_index(drop = True)
all_meta_data_ecode_360['href'] = all_meta_data_ecode_360.Ordinance.apply(lambda x: x.split('/')[-1]).values
all_meta_data_ecode_360['unique_id'] = range(all_meta_data_ecode_360.shape[0])
# all_meta_data_ecode_360.head(2)
meta_data = all_meta_data_ecode_360


print('=> Processing first 100 webs...')
all_error_signals = []
for row_idx in (range(100)):
    curr_row = meta_data.iloc[row_idx]
    ts = TreeSpider('/' + curr_row.href)
    ts.run()
    all_error_signals.append(ts.error_signals)
    print(' =>', row_idx)
    if sum(ts.error_signals.values()) == 0:
    	print('  => No error!')
    else:
    	print(ts.error_signals)
    print()
    #pickle.dump(ts, open('../data/scrapped/' + str(curr_row.unique_id) + '.pkl', 'wb'))