import io

import pandas as pd

'''select name, dataset.metadata ? 'gqa' as has_gqa, count(dataset.id)
from agdc.dataset
  left join agdc.dataset_type on dataset_type.id = dataset.dataset_type_ref
where name like '%level1%'
group by name, has_gqa
order by name;'''

csv = io.StringIO('''
name,has_gqa,count
ls7_pq_scene,false,130858
ls7_nbar_scene,false,130883
ls5_nbart_scene,false,128734
ls8_pq_scene,false,47817
ls5_level1_scene,true,161173
ls7_level1_scene,true,161894
ls8_level1_oli_scene,true,272
ls8_level1_scene,true,54990
ls8_nbart_scene,false,44514
ls5_nbar_scene,false,128797
ls5_level1_scene,false,65972
ls7_level1_scene,false,55570
ls8_level1_oli_scene,false,56
ls5_pq_scene,false,128766
ls8_nbar_scene,false,47867
ls7_nbart_scene,false,128193
ls8_level1_scene,false,762
''')

df = pd.read_csv(csv)

gqadf = df[df['name'].str.contains('level1')]
total = gqadf.groupby('name', as_index=False).sum().drop(['has_gqa'], axis=1).rename(columns={'count': 'total'})

gqadf = pd.merge(gqadf, total, on='name')

gqadf['pct'] = gqadf['count'] / gqadf['total']

gqadf['indexed_scenes'] = gqadf['count'].sum()

gqadf['pct_all'] = gqadf['count'] / gqadf.indexed_scenes

print(gqadf[['name', 'has_gqa', 'count', 'pct', 'pct_all']].to_html(
    formatters={'pct': '{:,.2%}'.format, 'pct_all': '{:,.2%}'.format}))

print(gqadf.groupby('has_gqa').sum()[['pct_all']].to_string(
    formatters={'pct_all': '{:,.2%}'.format}))
