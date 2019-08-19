from sqlalchemy import create_engine
import pandas as pd

df = pd.read_excel('n11.xlsx')
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
print(engine)
df.to_sql('n11', engine,if_exists='replace', index=False)