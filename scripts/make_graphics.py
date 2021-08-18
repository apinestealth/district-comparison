import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import sys

#clean input
args = sys.argv[1:]
district_1 = args[0].lower()
district_2 = args[1].lower()

#load data
data_dir = '/Users/annagreene/code/district-comparison/data/'
dist_1 = pd.read_csv(data_dir + 'processed/' + district_1 + '_mapped.csv')
dist_2 = pd.read_csv(data_dir + 'processed/' + district_2 + '_mapped.csv')

def main():
    collection = make_dataframes(dist_1, dist_2)
    sean_bar_graph(collection[1])
    anna_bar_graph(collection[3])

def make_dataframes(dist_1, dist_2):
    dist_1_subcategories = dist_1.groupby("Category_Edstruments")['Transactions'].sum().reset_index()
    dist_1_majorcategories = dist_1.groupby("Major_Category_Edstruments")['Transactions'].sum().reset_index()
    dist_1_majorcategories['Per Pupil'] = dist_1_majorcategories['Transactions']/11956
    dist_1_majorcategories = dist_1_majorcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_1_majorcategories['district'] = 'Tolleson'

    dist_2_subcategories = dist_2.groupby("Category_Edstruments")['Transactions'].sum().reset_index()
    dist_2_majorcategories = dist_2.groupby("Major_Category_Edstruments")['Transactions'].sum().reset_index()
    dist_2_majorcategories['Per Pupil'] = dist_2_majorcategories['Transactions']/52000
    dist_2_majorcategories = dist_2_majorcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_2_majorcategories['district'] = 'Atlanta'

    dists_sub = [dist_1_subcategories, dist_2_subcategories]
    subcategories = pd.concat(dists_sub)

    dists_major = [dist_1_majorcategories, dist_2_majorcategories]
    majorcategories = pd.concat(dists_major)

    return [dist_1_subcategories, dist_1_majorcategories, subcategories, majorcategories]

def sean_bar_graph(dist_1_majorcategories):
    size = (14.5, 12)
    fig, ax1 = plt.subplots(figsize=size)

    # plot bars
    ax1.bar(x='Major_Category_Edstruments', height='Per Pupil', data=dist_1_majorcategories,
            color='#b1d6e7', label='Per Pupil Expense')
    #ax1.set_xticklabels(
        #dist_1_majorcategories['Major_Category_Edstruments'], rotation=65, horizontalalignment='right')
    ax1.set_ylabel('Per-Pupil Expenditure', fontsize=16, color='black', labelpad = 10)
    ax1.set_title('Per-Pupil Expenditure Across Major Categories', fontsize=25)
    fmt = '{x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax1.yaxis.set_major_formatter(tick)
    plt.savefig("BarGraph_sean.png")

def anna_bar_graph(majorcategories):
    sns.set_theme(style="whitegrid")
    palette = sns.color_palette(["#89C9DC","#CB91BD"], 2)
    plt.figure(figsize=(14.5, 12))

    test = sns.barplot(
        data=majorcategories, x='Major_Category_Edstruments', y='Per Pupil', hue="district", palette=palette
    )

    plt.xticks(
        rotation=60, 
        horizontalalignment='right',
    )

    test.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

    for p in test.patches:
        test.annotate(format(p.get_height(), ',.0f'), (p.get_x() + p.get_width() / 2, p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')

    test.set_title('Per-Pupil Expenditure Across Major Categories', fontsize=20, y=1.01)
    sns.despine(left=True)
    test.set(xlabel='', ylabel='Per-Pupil Expenditure')
    test.legend(bbox_to_anchor=(.89, .96), loc=2, borderaxespad=0.)
    plt.savefig("BarGraph.png", bbox_inches='tight')

if __name__ == '__main__':
    main()