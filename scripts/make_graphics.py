import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import textwrap

def create_visualizations(district_1, district_2, dist_1_name, dist_2_name, dir):
    #load data
    district_data = pd.read_csv(dir + 'data/processed/district_data.csv', low_memory=False)
    district_data['nces_schoolID'] = district_data['nces_schoolID'].astype(str)
    dist_1 = pd.read_csv(dir + 'data/processed/' + district_1 + '_mapped.csv')
    dist_2 = pd.read_csv(dir + 'data/processed/' + district_2 + '_mapped.csv')
    
    #run functions
    dist_1_students, dist_2_students = get_students(district_data, district_1, district_2)
    collection = make_dataframes(dist_1, dist_2, dist_1_students, dist_2_students, dist_1_name, dist_2_name)
    bar_graph_majors(collection[5], district_1, district_2, dir)
    bar_graph_subs(collection[4], district_1, district_2, dir)
    pie_charts(collection[6], collection[7], district_1, district_2, dist_1_name, dist_2_name, dir)
    dist_1_ppe = "${:,.0f}".format(collection[8])
    dist_2_ppe = "${:,.0f}".format(collection[9])
    
    return(dist_1_ppe, dist_2_ppe)

def get_students(district_data, district_1, district_2):
    dist_1_students = float(district_data.loc[district_data['nces_schoolID'] == district_1, 'Total Students, All Grades (Includes AE) [District] 2018-19'].iloc[0])
    dist_2_students = float(district_data.loc[district_data['nces_schoolID'] == district_2, 'Total Students, All Grades (Includes AE) [District] 2018-19'].iloc[0])

    return dist_1_students, dist_2_students

def make_dataframes(dist_1, dist_2, dist_1_students, dist_2_students, dist_1_name, dist_2_name):
    #palette to be used for pie charts
    palette = ['#559C6C', '#9F8EA1', '#6ABBA1', '#3E9AE3', '#B9ABBF', '#90D8D1', '#B1D6E7', '#D4C8DF', '#C1F4FA', '#CB91BD', '#EFE7FF', '#8BD8F1', '#4F86C9', '#D0CCF1', '#5BBAEB', '#D1B8CA', '#ADB3E4', '#857383', '#849BD7', '#857383', '#3e9ae3', '#b1d6e7', '#4f86c9', '#CB91BD', '#559c6c', '#d1b8ca']

    #create dist 1 dataframe of subcategories
    dist_1_subcategories = dist_1.groupby("Category_Edstruments")['Transactions'].sum().reset_index()
    dist_1_subcategories['Per Pupil'] = dist_1_subcategories['Transactions']/dist_1_students
    dist_1_len = len(dist_1_subcategories.index)
    palette_1 = palette[:dist_1_len]
    dist_1_subcategories['palette'] = palette_1
    dist_1_subcategories = dist_1_subcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_1_subcategories['district'] = dist_1_name
    
    #create dist 1 dataframe for the pie chart
    dist_1_other = dist_1_subcategories[10:]['Per Pupil'].sum()
    dist_1_subcategories_pie = dist_1_subcategories[:10]
    dist_1_subcategories_pie.loc[len(dist_1_subcategories_pie.index)] = ['Other', 0, dist_1_other, '#ADB3E4', 'Tolleson']

    #create dist 1 dataframe of aggregated major categories
    dist_1_majorcategories = dist_1.groupby("Major_Category_Edstruments")['Transactions'].sum().reset_index()
    dist_1_majorcategories['Per Pupil'] = dist_1_majorcategories['Transactions']/dist_1_students
    dist_1_majorcategories = dist_1_majorcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_1_majorcategories['district'] = 'Tolleson'
    dist_1_ppe = round(dist_1_majorcategories['Per Pupil'].sum())

    #create dist 2 dataframe of subcategories
    dist_2_subcategories = dist_2.groupby("Category_Edstruments")['Transactions'].sum().reset_index()
    dist_2_subcategories['Per Pupil'] = dist_2_subcategories['Transactions']/dist_2_students
    dist_2_len = len(dist_2_subcategories.index)
    palette_2 = palette[:dist_2_len]
    dist_2_subcategories['palette'] = palette_2
    dist_2_subcategories = dist_2_subcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_2_subcategories['district'] = dist_2_name

    #create dist 2 dataframe for the pie chart
    dist_2_other = dist_2_subcategories[10:]['Per Pupil'].sum()
    dist_2_subcategories_pie = dist_2_subcategories[:10]
    dist_2_subcategories_pie.loc[len(dist_2_subcategories_pie.index) + 1] = ['Other', 0, dist_2_other, '#ADB3E4', 'Atlanta']

    #create dist 2 dataframe of aggregated major categories
    dist_2_majorcategories = dist_2.groupby("Major_Category_Edstruments")['Transactions'].sum().reset_index()
    dist_2_majorcategories['Per Pupil'] = dist_2_majorcategories['Transactions']/dist_2_students
    dist_2_majorcategories = dist_2_majorcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_2_majorcategories['district'] = 'Atlanta'
    dist_2_ppe = round(dist_2_majorcategories['Per Pupil'].sum())

    #create the joined subcategories dataframe for the bar chart
    dists_sub = [dist_1_subcategories, dist_2_subcategories]
    subcategories = pd.concat(dists_sub)

    #sort the subcategories dataframe so it goes from biggest to smallest
    subcategories_indicator = subcategories.groupby("Category_Edstruments")['Per Pupil'].sum().reset_index()
    subcategories_indicator = subcategories_indicator.rename(columns={'Per Pupil': 'Sort'})
    subcategories = subcategories.merge(subcategories_indicator)
    subcategories = subcategories.sort_values(by="Sort",ascending = False)

    #create the joined majorcategories dataframe for the bar chart
    dists_major = [dist_1_majorcategories, dist_2_majorcategories]
    majorcategories = pd.concat(dists_major)

    #sort the majorcategories dataframe so it goes in a specific pre-defined order
    majorcategories_indicator = majorcategories.groupby("Major_Category_Edstruments")['Per Pupil'].sum().reset_index()
    majorcategories_indicator = majorcategories_indicator.rename(columns={'Per Pupil': 'Sort'})
    majorcategories = majorcategories.merge(majorcategories_indicator)
    majorcategories = majorcategories.reindex([0, 1, 4, 5, 12, 13, 2, 3, 8, 9, 10, 11, 6, 7])

    return [dist_1_subcategories, dist_1_majorcategories, dist_2_subcategories, dist_2_majorcategories, subcategories, majorcategories, dist_1_subcategories_pie, dist_2_subcategories_pie, dist_1_ppe, dist_2_ppe]

def bar_graph_majors(majorcategories, district_1, district_2, dir):
    #style things
    sns.set_theme(style="ticks")
    palette = sns.color_palette(["#89C9DC","#CB91BD"], 2)
    
    #size of graphic
    plt.figure(figsize=(19.5, 10.58))

    #create the actual bars
    test = sns.barplot(
        data=majorcategories, x='Major_Category_Edstruments', y='Per Pupil', hue="district", palette=palette)

    #axis labels
    plt.yticks(size=18,)
    plt.xticks(size=18,)
    plt.xlabel('Major Categories', fontsize=25)
    plt.ylabel('Per-Pupil Expenditure', fontsize=25)
    test.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))
    test.set_xticklabels([textwrap.fill(e, 16) for e in majorcategories['Major_Category_Edstruments'][::2]])

    #numbers on top of bars
    for p in test.patches:
        test.annotate(format(p.get_height(), ',.0f'), (p.get_x() + p.get_width() / 2, p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points', size=15)

    #title & legend
    test.set_title('Per-Pupil Expenditure Across Aggregated Categories', fontsize=40, y=1.02)
    test.legend(bbox_to_anchor=(1.00, 1.00), loc=2, borderaxespad=0., prop={"size":18})
    
    #some style things
    sns.despine()
    test.tick_params(bottom=False)

    #save graph
    plt.savefig(dir + "graphics/BarGraph_Major_" + district_1 + '_' + district_2 + ".png", bbox_inches='tight')

def bar_graph_subs(subcategories, district_1, district_2, dir):
    #style things
    sns.set_theme(style="ticks")
    palette = sns.color_palette(["#89C9DC","#CB91BD"], 2)

    #size of graphic
    plt.figure(figsize=(16.5, 20))

    #create the actual bars
    test = sns.barplot(
        data=subcategories.head(40), y='Category_Edstruments', x='Per Pupil', hue="district", palette=palette
    )
    #axis labels
    plt.yticks(horizontalalignment='right', size=20,)
    plt.xticks(size=25,)
    test.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))
    plt.ylabel('')
    plt.xlabel('Per-Pupil Expenditure', fontsize=30)

    #numbers to right of bars
    for p in test.patches:
        width = p.get_width()
        plt.text(290+p.get_width(), p.get_y()+0.55*p.get_height(),
        '{:,.0f}'.format(width), ha='center', va='center', size=20)

    #title & legend
    test.set_title('Per-Pupil Expenditure Across Twenty Largest Categories', fontsize=40, y=1.02)
    test.legend(bbox_to_anchor=(1.1, .98), loc=2, borderaxespad=0., prop={"size":20})
    
    #style things
    sns.despine()
    test.tick_params(bottom=False)
    
    #save graph
    plt.savefig(dir + "graphics/BarGraph_Sub_" + district_1 + '_' + district_2 + ".png", bbox_inches='tight')

def pie_charts(dist_1_subcategories, dist_2_subcategories, district_1, district_2, dist_1_name, dist_2_name, dir):
    #dist 1 pie chart
    palette=dist_1_subcategories["palette"]
    sizes=dist_1_subcategories["Per Pupil"]/11956

    fig1, ax1 = plt.subplots(figsize=(10, 10))

    patches, texts, autotexts = ax1.pie(sizes, labels=dist_1_subcategories["Category_Edstruments"], autopct='%1.1f%%',
        shadow=False, startangle=0, colors=palette, normalize=True, labeldistance=1.05, pctdistance=.9)
     
    for text in texts:
        text.set_size(18)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_size(12)
    
    ax1.axis('equal')
    ax1.set_title(dist_1_name.capitalize(), fontsize=34)
    plt.savefig(dir + "graphics/PieChart_" + district_1 + ".png", bbox_inches='tight')

    #dist 2 pie chart
    palette=dist_2_subcategories["palette"]
    sizes = dist_2_subcategories["Per Pupil"]/11956

    fig1, ax1 = plt.subplots(figsize=(10, 10))

    patches, texts, autotexts = ax1.pie(sizes, labels=dist_2_subcategories["Category_Edstruments"], autopct='%1.1f%%',
        shadow=False, startangle=0, colors=palette, normalize=True, labeldistance=1.05, pctdistance=.9)

    for text in texts:
        text.set_size(18)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_size(12)
    
    ax1.axis('equal')
    ax1.set_title(dist_2_name.capitalize(), fontsize=34)
    plt.savefig(dir + "graphics/PieChart_" + district_2 + ".png", bbox_inches='tight')

if __name__ == '__main__':
    create_visualizations()