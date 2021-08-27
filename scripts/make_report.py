import pandas as pd
from fpdf import FPDF
from PIL import Image

def output_report(district_1, district_2, dist_1_ppe, dist_2_ppe, comment_1, comment_2, report_name, dist_1_name, dist_2_name, source_1, source_2, sums, dir):
    #load graphics
    district_data = pd.read_csv(dir + 'data/processed/district_data.csv', low_memory=False)
    district_data['nces_schoolID'] = district_data['nces_schoolID'].astype(str)
    major_bar = dir + 'graphics/BarGraph_Major_' + district_1 + '_' + district_2 + '.png'
    sub_bar = dir + 'graphics/BarGraph_Sub_' + district_1 + '_' + district_2 + '.png'
    pie_1 = dir + 'graphics/PieChart_' + district_1 + '.png'
    pie_2 = dir + 'graphics/PieChart_' + district_2 + '.png'
    logo = dir + 'graphics/edstruments_logo2.png'

    #run functions/create report
    name_1, name_2 = get_full_names(district_data, district_1, district_2)
    pdf = FPDF()
    pdf=FPDF(unit='pt')
    pdf.add_page()
    print('creating page one of the report...')
    create_title(pdf, name_1, name_2, logo)
    page_1_info(pdf, district_data, district_1, district_2, name_1, name_2, sums, dist_1_name, dist_2_name, source_1, source_2)
    page_1_bar(pdf, major_bar, comment_1, comment_2, dist_1_ppe, dist_2_ppe, dist_1_name, dist_2_name)
    pdf.add_page()
    print('creating page two of the report...')
    page_2(pdf, sub_bar, comment_2, pie_1, pie_2)
    pdf.output(dir + 'reports/' + report_name + '.pdf', 'F')

def get_full_names(district_data, district_1, district_2):
    name_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'Agency Name_x'].iloc[0].title()
    name_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'Agency Name_x'].iloc[0].title()

    return name_1, name_2

# creates the title
def create_title(pdf, name_1, name_2, logo):
    pdf.image(logo, 39, 28, 75, 75.7, '', link = "https://edstruments.com/")

    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_y(44)
    pdf.set_x(133)
    pdf.multi_cell(432, 22, f'{name_1} and {name_2} Budget Comparison', 0, 0, 'L')

def page_1_info(pdf, district_data, district_1, district_2, name_1, name_2, sums, dist_1_name, dist_2_name, source_1, source_2):
    #get dist 1 info
    city_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'Location City [District] 2018-19_x'].iloc[0].title()
    state_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'State Name [District] 2018-19_x'].iloc[0].title()
    dist_1_students = "{:,.0f}".format(int(district_data.loc[district_data['nces_schoolID'] == district_1, 'Total Students, All Grades (Includes AE) [District] 2018-19'].iloc[0]))
    dist_1_sum = "${:,.0f}".format(sums[0])
    
    #set dist 1 info
    pdf.set_font('Helvetica', '', 10)
    pdf.set_y(125)
    pdf.set_x(39)
    pdf.multi_cell(521, 16, f'{name_1}, located in {city_1}, {state_1}, has {dist_1_students} students. The total yearly expenditures for the district were {dist_1_sum}. The data for {dist_1_name} was sourced from {source_1}.', 0, 0, 'L')

    #get dist 2 info
    city_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'Location City [District] 2018-19_x'].iloc[0].title()
    state_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'State Name [District] 2018-19_x'].iloc[0].title()
    dist_2_students = "{:,.0f}".format(int(district_data.loc[district_data['nces_schoolID'] == district_2, 'Total Students, All Grades (Includes AE) [District] 2018-19'].iloc[0]))
    dist_2_sum = "${:,.0f}".format(sums[1])
    
    #set dist 2 info
    pdf.set_font('Helvetica', '', 10)
    pdf.set_y(190)
    pdf.set_x(39)
    pdf.multi_cell(521, 16, f'{name_2}, located in {city_2}, {state_2}, has {dist_2_students} students. The total yearly expenditures for the district were {dist_2_sum}. The data for {dist_2_name} was sourced from {source_2}.', 0, 0, 'L')

def page_1_bar(pdf, major_bar, comment_1, comment_2, dist_1_ppe, dist_2_ppe, dist_1_name, dist_2_name):
    #add major categories bar chart
    pdf.image(major_bar, 48, 353, 499, 276)

    #add ppe sums
    #ppe for dist 1
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_y(266)
    pdf.set_x(166)
    pdf.cell(0, 26, f'{dist_1_ppe}', 0, 0, 'L')
    #ppe for dist 2
    pdf.set_y(266)
    pdf.set_x(350)
    pdf.cell(0, 26, f'{dist_2_ppe}', 0, 0, 'L')
    #name of dist 1
    pdf.set_text_color(137, 201, 220)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_y(292)
    pdf.set_x(168)
    pdf.cell(0, 9, f'{dist_1_name} PPE', 0, 0, 'L')
    #name of dist 2
    pdf.set_text_color(203, 145, 189)
    pdf.set_y(292)
    pdf.set_x(352)
    pdf.cell(0, 9, f'{dist_2_name} PPE', 0, 0, 'L')

    #add comment
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_y(666)
    pdf.set_x(83)
    pdf.multi_cell(430, 10, f'{comment_1}', 0, 'C')

def page_2(pdf, sub_bar, comment_2, pie_1, pie_2):
    #add pie chart label
    pdf.set_y(30)
    pdf.set_x(167)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(262, 17, 'Comparison of Ten Largest Categories')

    #add first pie chart
    image_1 = Image.open(pie_1)
    og_width_1 = image_1.width
    og_height_1 = image_1.height
    image_1_final = image_1.resize((int(og_width_1/4.3), int(og_height_1/4.3)))
    width_1 = image_1_final.width
    height_1 = image_1_final.height
    pdf.image(pie_1, 29, 62, width_1, height_1)

    #add second pie chart
    image_2 = Image.open(pie_2)
    og_width_2 = image_2.width
    og_height_2 = image_2.height
    image_2_final = image_2.resize((int(og_width_2/4.3), int(og_height_2/4.3)))
    width_2 = image_2_final.width
    height_2 = image_2_final.height
    pdf.image(pie_2, 566 - width_2, 62, width_2, height_2)

    #add comment
    pdf.set_y(301)
    pdf.set_x(83)
    pdf.set_font('Helvetica', '', 8)
    pdf.multi_cell(430, 10, f'{comment_2}', 0, 'C')

    #add bar chart
    pdf.image(sub_bar, 46, 376, 504, 0)

if __name__ == '__main__':
    output_report()