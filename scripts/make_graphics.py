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
    mapping = pd.read_csv(dir + 'data/processed/mapping.csv')
    
    #run functions
    dist_1_students, dist_2_students = get_students(district_data, district_1, district_2)
    collection = make_dataframes(dist_1, dist_2, dist_1_students, dist_2_students, dist_1_name, dist_2_name, mapping)
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

def make_dataframes(dist_1, dist_2, dist_1_students, dist_2_students, dist_1_name, dist_2_name, mapping):
    #create palette
    palette_list = ['#b1d6e7', '#9bcfdd', '#86c7d1', '#58af9a', '#54a684', '#559c6c', '#9f8ea1', '#a08fa8', '#a090af', '#9e91b7', '#9b93bf', '#9595c7', '#8e98cf', '#849bd7', '#cb91bd', '#c08ec1', '#b38cc4', '#a48ac7', '#9389c9', '#8088cb', '#72c0c1', '#62b8af', '#6a87cb', '#4f86c9', '#dd9fa2',  '#d8abba', '#c9a9c7', '#b7aed4', '#a0b3db', '#88b9da', '#76bdd1']
    categories = mapping['Category_Edstruments'].unique()
    categories_list = categories.tolist()

    p = {'Category_Edstruments': categories_list, 'palette': palette_list}
    palette_df = pd.DataFrame(data=p)
    
    #create dist 1 dataframe of subcategories
    dist_1_subcategories = dist_1.groupby("Category_Edstruments")['Transactions'].sum().reset_index()
    dist_1_subcategories['Per Pupil'] = dist_1_subcategories['Transactions']/dist_1_students
    dist_1_subcategories = dist_1_subcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_1_subcategories['district'] = dist_1_name
    
    #create dist 1 dataframe for the pie chart
    dist_1_other = dist_1_subcategories[10:]['Per Pupil'].sum()
    dist_1_subcategories_pie = dist_1_subcategories[:10]
    dist_1_subcategories_pie = dist_1_subcategories_pie.merge(palette_df, how='left', on='Category_Edstruments')
    dist_1_subcategories_pie.loc[len(dist_1_subcategories_pie.index)] = ['Other', 0, dist_1_other, 'Tolleson', '#EFCFE7']

    #create dist 1 dataframe of aggregated major categories
    dist_1_majorcategories = dist_1.groupby("Major_Category_Edstruments")['Transactions'].sum().reset_index()
    dist_1_majorcategories['Per Pupil'] = dist_1_majorcategories['Transactions']/dist_1_students
    dist_1_majorcategories = dist_1_majorcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_1_majorcategories['district'] = 'Tolleson'
    dist_1_ppe = round(dist_1_majorcategories['Per Pupil'].sum())

    #create dist 2 dataframe of subcategories
    dist_2_subcategories = dist_2.groupby("Category_Edstruments")['Transactions'].sum().reset_index()
    dist_2_subcategories['Per Pupil'] = dist_2_subcategories['Transactions']/dist_2_students
    dist_2_subcategories = dist_2_subcategories.sort_values(by = 'Per Pupil', ascending = False )
    dist_2_subcategories['district'] = dist_2_name

    #create dist 2 dataframe for the pie chart
    dist_2_other = dist_2_subcategories[10:]['Per Pupil'].sum()
    dist_2_subcategories_pie = dist_2_subcategories[:10]
    dist_2_subcategories_pie = dist_2_subcategories_pie.merge(palette_df, how='left', on='Category_Edstruments')
    dist_2_subcategories_pie.loc[len(dist_2_subcategories_pie.index) + 1] = ['Other', 0, dist_2_other, 'Atlanta', '#EFCFE7']

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
    plt.yticks(size=20,)
    plt.xticks(size=20,)
    plt.xlabel('Major Categories', fontsize=28)
    plt.ylabel('Per-Pupil Expenditure', fontsize=28)
    test.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))
    test.set_xticklabels([textwrap.fill(e, 15) for e in majorcategories['Major_Category_Edstruments'][::2]])

    #numbers on top of bars
    for p in test.patches:
        test.annotate(format(p.get_height(), ',.0f'), (p.get_x() + p.get_width() / 2, p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points', size=18)

    #title & legend
    #test.set_title('Per-Pupil Expenditure Across Aggregated Categories', fontsize=40, y=1.04)
    test.legend(bbox_to_anchor=(1.02, 1.00), loc=2, borderaxespad=0., prop={"size":20})
    
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
    #test.set_title('Per-Pupil Expenditure Across Twenty Largest Categories', fontsize=40, y=1.02)
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

    patches, texts, autotexts = ax1.pie(sizes, labels=dist_1_subcategories["Category_Edstruments"], autopct='%.1f',
        shadow=False, startangle=0, colors=palette, normalize=True, labeldistance=1.05, pctdistance=.92)
     
    for text in texts:
        text.set_size(18)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_size(15)
    
    ax1.axis('equal')
    ax1.set_title(dist_1_name.capitalize() + ' (%)', fontsize=34)
    plt.savefig(dir + "graphics/PieChart_" + district_1 + ".png", bbox_inches='tight')

    #dist 2 pie chart
    palette=dist_2_subcategories["palette"]
    sizes = dist_2_subcategories["Per Pupil"]/11956

    fig1, ax1 = plt.subplots(figsize=(10, 10))

    patches, texts, autotexts = ax1.pie(sizes, labels=dist_2_subcategories["Category_Edstruments"], autopct='%.1f',
        shadow=False, startangle=0, colors=palette, normalize=True, labeldistance=1.05, pctdistance=.92)

    for text in texts:
        text.set_size(18)
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_size(15)
    
    ax1.axis('equal')
    ax1.set_title(dist_2_name.capitalize() + ' (%)', fontsize=34)
    plt.savefig(dir + "graphics/PieChart_" + district_2 + ".png", bbox_inches='tight')

if __name__ == '__main__':
    create_visualizations()