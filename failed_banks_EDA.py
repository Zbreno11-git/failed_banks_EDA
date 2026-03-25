import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

#Basic web scraping, I tried to use...
# ...read_html(), and actually found the full link to download the table.
""""
url = 'https://www.fdic.gov/bank-failures/download-data.csv'
df_banks = pd.read_csv(url, encoding='latin1')
df_banks.to_csv('failed_banks_EDA.csv', index=False)
"""""
df_banks = pd.read_csv('failed_banks_EDA.csv')

    #Data info, data is clean(non-null), 573 entries, 2020 - 2026.
print(df_banks.info())
print(df_banks.describe())
print(df_banks.head())
print(df_banks.tail())

    #How many banks were closed each year:

#There was some whitespace in almost every column
df_banks.columns = df_banks.columns.str.strip()

#Turning 'Closing Date' into a datetime
df_banks['Closing Date'] = pd.to_datetime(df_banks['Closing Date'], format='%d-%b-%y')
df_banks['Year'] = df_banks['Closing Date'].dt.year

#Checking how many banks failed per year
per_year = df_banks.Year.value_counts().sort_index()
pct_2010 = (per_year.loc[2010] - per_year.median()) / per_year.median() * 100

sns.set_style('white')
ax = per_year.plot(kind='bar', figsize=(10, 4), color='green')
sns.despine()
plt.xlabel('Year')
plt.ylabel('Number of Failed Banks')
ax.legend([f'2010: +{pct_2010:.2f}% vs normal'], loc='upper right', frameon=False, fontsize=11)
plt.tight_layout()
#plt.savefig('/Users/luanabreno/Desktop/Images/banks_pyear.png', dpi=150, bbox_inches='tight')

"""
Insight:
# 2010 shows a significant spike in bank failures,
# likely reflecting the aftermath of the 2008 financial crisis.
"""

    #Increase on funds from 2000 to 2026:
media_ano = df_banks.groupby('Year')['Fund'].mean().reset_index()
m = media_ano.set_index('Year')['Fund']
m2004, m2007 = m.loc[2004], m.loc[2007]
pct = (m2007 - m2004) / m2004 * 100

"""
Insight:
# The increase in funds between 2004 and 2007 suggests
# pre-crisis expansion before the financial collapse.
"""

plt.figure(figsize=(8, 6))
sns.lineplot(media_ano, x='Year', y='Fund', color='green')
plt.legend([f'{pct:.2f}% increase from 2004 to 2007'], loc='lower right', frameon=False, fontsize=9)
plt.ylabel('Funds')
plt.xlim(2000, 2026)
plt.ylim(4000,11000)
#plt.savefig('/Users/luanabreno/Desktop/Images/increase_on_funds.png', dpi=300, bbox_inches='tight')

    #Same visualization but using plotly, so the User can interact with the plot.
fig = px.line(data_frame=media_ano, x='Year', y='Fund')
fig.write_html('/Users/luanabreno/Downloads/failed_banksplotly.html')
fig.show()