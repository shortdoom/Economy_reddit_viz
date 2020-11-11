import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dd = pd.read_pickle('/home/user/reddit_year.pickle')

non_reddit = dd[~dd.url.str.contains('redd')]

economy = non_reddit[(non_reddit.subreddit == 'Economics') | (non_reddit.subreddit == 'economy') | (non_reddit.subreddit == 'finance')]
econ_df = economy[['title', 'subreddit', 'url', 'score']]
good_score = econ_df[econ_df.score > 50]
to_plot = good_score[['url','score']]

urls = good_score.url.str.split('/')

domain_dict = []
for rows in urls:
    domain_dict.append(rows[2])

# good_score['domain'] = domain_dict

df_domain = pd.DataFrame(domain_dict, columns=['domain'])
df_domain.domain = df_domain.domain.str.replace(r'^www.', '')
df_domain.domain = df_domain.domain.str.replace('youtu.be','youtube.com')

good_score['domain'] = list(df_domain.domain)
good_score.loc[good_score['domain'] == 'marketwatch.com', 'score'].sum()
upvotes = good_score.groupby('domain')['score'].sum()

domains = pd.DataFrame(df_domain.domain.value_counts())
domains.reset_index(inplace=True)
domains.rename(columns={'index':'domain','domain':'value'}, inplace=True)
domains = pd.merge(domains, upvotes, on='domain')

domains = domains[0:50]
domains['score'] = domains.score.apply(lambda x: x/1000)
pos = list(range(len(domains)))
width = 0.35
plt.style.use('classic')
fix, ax = plt.subplots(figsize=(30,15))

plt.barh(pos, domains['value'], width, alpha=0.5, label=domains['domain'][0], color='#00229f')
plt.barh([p + width for p in pos], domains['score'], width, alpha=0.5, label=domains['domain'][1], color='#EE3224')

fix.suptitle('     Sources of news on economy oriented subreddits (1yr) / Aggregated no. of upvotes for each domain', fontsize=20, weight='bold')
plt.text(0.64, 0.70, 'Sample size: 2018/10/30 to 2019/11/01 (1 year)', fontsize=14, transform=plt.gcf().transFigure)
plt.text(0.64, 0.65, 'Data source: /r/finance & /r/economy & /r/economics', fontsize=14, transform=plt.gcf().transFigure)
ax.set_xlabel('Frequency & No. of Upvotes (upvotes normalized by /1000)')

ax.set_yticks([p + 0.5 * width for p in pos])
ax.set_yticklabels(domains['domain'])

plt.legend(loc=4, prop={'size': 12})
plt.legend(['Frequency of apperance', 'Total upvotes'], loc='upper right')
text_params = {'ha': 'center', 'va': 'center', 'family': 'sans-serif',
               'fontweight': 'bold'}
plt.text(x=275, y=43, s='@neotokio-3', bbox=dict(facecolor='green', alpha=0.3), **text_params)
plt.grid()
plt.show()
plt.show()


