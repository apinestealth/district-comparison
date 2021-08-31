import pandas as pd
from fpdf import FPDF
from PIL import Image

def output_report(district_1, district_2, dist_1_ppe, dist_2_ppe, user_input, sums, dir):
    #load graphics
    district_data = pd.read_csv(dir + 'data/processed/district_data.csv', low_memory=False)
    district_data['nces_schoolID'] = district_data['nces_schoolID'].astype(str)
    major_bar = dir + 'graphics/BarGraph_Major_' + district_1 + '_' + district_2 + '.png'
    sub_bar = dir + 'graphics/BarGraph_Sub_' + district_1 + '_' + district_2 + '.png'
    pie_1 = dir + 'graphics/PieChart_' + district_1 + '.png'
    pie_2 = dir + 'graphics/PieChart_' + district_2 + '.png'
    logo = dir + 'graphics/edstruments_logo2.png'

    #load user inputs
    report_name = user_input[0]
    dist_1_name = user_input[1]
    dist_2_name = user_input[2]
    source = user_input[3]
    comment_1 = user_input[4]
    comment_2 = user_input[5]
    dist_1_full_name = user_input[6]
    dist_2_full_name = user_input[7]

    #run functions/create report
    #name_1, name_2 = get_full_names(district_data, district_1, district_2)
    pdf = FPDF()
    pdf=FPDF(unit='pt')
    pdf.set_auto_page_break(False)
    pdf.add_page()
    print('creating page one of the report...')
    create_title(pdf, dist_1_full_name, dist_2_full_name, logo)
    create_facts(pdf, dist_1_name, dist_2_name, district_1, district_2, district_data, sums)
    page_1_bar(pdf, major_bar, comment_1, comment_2, dist_1_ppe, dist_2_ppe, dist_1_name, dist_2_name)
    footnote(pdf, source)
    pdf.add_page()
    print('creating page two of the report...')
    page_2(pdf, sub_bar, comment_2, pie_1, pie_2)
    pdf.output(dir + 'reports/' + report_name + '.pdf', 'F')
    output_difference(district_data, district_1, district_2, dist_1_ppe, dist_2_ppe, dist_1_name, dist_2_name)

def get_full_names(district_data, district_1, district_2):
    name_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'Agency Name_x'].iloc[0].title()
    name_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'Agency Name_x'].iloc[0].title()

    return name_1, name_2

# creates the title
def create_title(pdf, dist_1_full_name, dist_2_full_name, logo):
    pdf.image(logo, 39, 28, 75, 75.7, '', link = "https://edstruments.com/")

    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_y(44)
    pdf.set_x(133)
    pdf.multi_cell(432, 22, f'{dist_1_full_name} and {dist_2_full_name} Budget Comparison', 0, 0, 'L')

def create_facts(pdf, dist_1_name, dist_2_name, district_1, district_2, district_data, sums):
    #title
    pdf.set_font('Helvetica', '', 14)
    pdf.set_y(112)
    pdf.set_x(240)
    pdf.cell(0, 26, 'District Fast Facts', 0, 0, 'L')

    #footnote numbers
    pdf.set_font('Helvetica', '', 5)
    pdf.set_y(117)
    pdf.set_x(353)
    pdf.cell(0, 6, '1, 2', 0, 0, 'L')
    
    #box
    pdf.rect(53, 139, 490, 267)

    #names of districts
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_y(143)
    pdf.set_x(277)
    pdf.cell(42, 19, f'{dist_1_name}', 0, 0, 'L')
    pdf.set_y(143)
    pdf.set_x(427)
    pdf.cell(34, 19, f'{dist_2_name}', 0, 0, 'L')

    #table labels
    labels = "Location \nType of Region \n# of Schools \nGrade Range \nTotal Yearly Expenditures \n# of Students \n% FRL // IEP // LEP \n% Non-White\n # of FTE Teachers \n# of Total Staff \nStudent/Teacher Ratio \n% Local // State // Federal Revenue"
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_y(162)
    pdf.set_x(43)
    pdf.multi_cell(166, 20, labels, 0, 'R', 0)

    #get info for dist 1 list
    city_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'Location City [District] 2018-19_x'].iloc[0].title()
    if city_1 == '' or city_1 == '-':
        city_1 = 'n/a'
    state_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'State Name [District] 2018-19_x'].iloc[0].title()
    if state_1 == '' or state_1 == '-':
        state_1 = 'n/a'
    region_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'Urban-centric Locale [District] 2018-19_x'].iloc[0][3:]
    if region_1 == '' or region_1 == '-':
        region_1 = 'n/a'
    schools_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'Total Number of Public Schools [Public School] 2018-19'].iloc[0]
    if schools_1 == '' or schools_1 == '-':
        schools_1 = 'n/a'
    grade_1a = district_data.loc[district_data['nces_schoolID'] == district_1, 'Lowest Grade Offered [District] 2018-19'].iloc[0]
    if grade_1a == '' or grade_1a == '-':
        grade_1a = 'n/a'
    grade_1b = district_data.loc[district_data['nces_schoolID'] == district_1, 'Highest Grade Offered [District] 2018-19'].iloc[0]
    if grade_1b == '' or grade_1b == '-':
        grade_1b = 'n/a'
    expenditures_1 = "${:,.0f}".format(sums[0])
    if expenditures_1 == '$0':
        expenditures_1 = 'n/a'
    students_1 = "{:,.0f}".format(int(district_data.loc[district_data['nces_schoolID'] == district_1, 'Total Students, All Grades (Includes AE) [District] 2018-19'].iloc[0]))
    if students_1 == '0':
        students_1 = 'n/a'
    FRL_1 = "{:.2f}%".format(district_data.loc[district_data['nces_schoolID'] == district_1, '% Free and Reduced Lunch Students [Public School] 2018-19'].iloc[0] * 100)
    if FRL_1 == '0.00%':
        FRL_1 = 'n/a'
    IEP_1 = "{:.2f}%".format(district_data.loc[district_data['nces_schoolID'] == district_1, '% IEP Students [District] 2018-19'].iloc[0] * 100)
    if IEP_1 == '0.00%':
        IEP_1 = 'n/a'
    LEP_1 = "{:.2f}%".format(district_data.loc[district_data['nces_schoolID'] == district_1, '% LEP / ELL [District] 2018-19'].iloc[0] * 100)
    if LEP_1 == '0.00%':
        LEP_1 = 'n/a'
    notwhite_1 = "{:.2f}%".format(100 - district_data.loc[district_data['nces_schoolID'] == district_1, '% White Students [District] 2018-19'].iloc[0] * 100)
    if notwhite_1 == '0.00%':
        notwhite_1 = 'n/a'
    FTE_1 = "{:,.0f}".format(float(district_data.loc[district_data['nces_schoolID'] == district_1, 'Full-Time Equivalent (FTE) Teachers [Public School] 2018-19'].iloc[0]))
    if FTE_1 == '0':
        FTE_1 = 'n/a'
    staff_1 = "{:,.0f}".format(float(district_data.loc[district_data['nces_schoolID'] == district_1, 'Total Staff [District] 2018-19_x'].iloc[0]))
    if staff_1 == '0':
        staff_1 = 'n/a'
    ratio_1 = district_data.loc[district_data['nces_schoolID'] == district_1, 'Pupil/Teacher Ratio [Public School] 2018-19'].iloc[0]
    if ratio_1 == '' or ratio_1 == '-':
        ratio_1 = 'n/a'
    local_1 = "{:.0f}%".format(float(district_data.loc[district_data['nces_schoolID'] == district_1, 'Local Revenue PP %'].iloc[0]) * 100)
    if local_1 == '0%':
        local_1 = 'n/a'
    statefunds_1 = "{:.0f}%".format(float(district_data.loc[district_data['nces_schoolID'] == district_1, 'State Revenue PP %'].iloc[0]) * 100)
    if statefunds_1 == '0%':
        statefunds_1 = 'n/a'
    federal_1 = "{:.0f}%".format(float(district_data.loc[district_data['nces_schoolID'] == district_1, 'Federal Revenue PP %'].iloc[0]) * 100)
    if federal_1 == '0%':
        federal_1 = 'n/a'

    #put dist 1 list on page
    dist_1_list = f"{city_1}, {state_1}\n{region_1}\n{schools_1}\n{grade_1a} - {grade_1b}\n{expenditures_1}\n{students_1}\n{FRL_1} // {IEP_1} // {LEP_1}\n{notwhite_1}\n{FTE_1}\n{staff_1}\n{ratio_1}\n{local_1} // {statefunds_1} // {federal_1}"
    pdf.set_font('Helvetica', '', 9)
    pdf.set_y(162)
    pdf.set_x(223)
    pdf.multi_cell(150, 20, dist_1_list, 0, 'C', 0)

    #get info for dist 2 list
    city_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'Location City [District] 2018-19_x'].iloc[0].title()
    if city_2 == '' or city_2 == '-':
        city_2 = 'n/a'
    state_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'State Name [District] 2018-19_x'].iloc[0].title()
    if state_2 == '' or state_2 == '-':
        state_2 = 'n/a'
    region_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'Urban-centric Locale [District] 2018-19_x'].iloc[0][3:]
    if region_2 == '' or region_2 == '-':
        region_2 = 'n/a'
    schools_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'Total Number of Public Schools [Public School] 2018-19'].iloc[0]
    if schools_2 == '' or schools_2 == '-':
        schools_2 = 'n/a'
    grade_2a = district_data.loc[district_data['nces_schoolID'] == district_2, 'Lowest Grade Offered [District] 2018-19'].iloc[0]
    if grade_2a == '' or grade_2a == '-':
        grade_2a = 'n/a'
    grade_2b = district_data.loc[district_data['nces_schoolID'] == district_2, 'Highest Grade Offered [District] 2018-19'].iloc[0]
    if grade_2b == '' or grade_2b == '-':
        grade_2b = 'n/a'
    expenditures_2 = "${:,.0f}".format(sums[1])
    if expenditures_2 == '$0':
        expenditures_2 = 'n/a'
    students_2 = "{:,.0f}".format(int(district_data.loc[district_data['nces_schoolID'] == district_2, 'Total Students, All Grades (Includes AE) [District] 2018-19'].iloc[0]))
    if students_2 == '0':
        students_2 = 'n/a'
    FRL_2 = "{:.2f}%".format(district_data.loc[district_data['nces_schoolID'] == district_2, '% Free and Reduced Lunch Students [Public School] 2018-19'].iloc[0] * 100)
    if FRL_2 == '0.00%':
        FRL_2 = 'n/a'
    IEP_2 = "{:.2f}%".format(district_data.loc[district_data['nces_schoolID'] == district_2, '% IEP Students [District] 2018-19'].iloc[0] * 100)
    if IEP_2 == '0.00%':
        IEP_2 = 'n/a'
    LEP_2 = "{:.2f}%".format(district_data.loc[district_data['nces_schoolID'] == district_2, '% LEP / ELL [District] 2018-19'].iloc[0] * 100)
    if LEP_2 == '0.00%':
        LEP_2 = 'n/a'
    notwhite_2 = "{:.2f}%".format(100 - district_data.loc[district_data['nces_schoolID'] == district_2, '% White Students [District] 2018-19'].iloc[0] * 100)
    if notwhite_2 == '0.00%':
        notwhite_2 = 'n/a'
    FTE_2 = "{:,.0f}".format(float(district_data.loc[district_data['nces_schoolID'] == district_2, 'Full-Time Equivalent (FTE) Teachers [Public School] 2018-19'].iloc[0]))
    if FTE_2 == '0':
        FTE_2 = 'n/a'
    staff_2 = "{:,.0f}".format(float(district_data.loc[district_data['nces_schoolID'] == district_2, 'Total Staff [District] 2018-19_x'].iloc[0]))
    if staff_2 == '0':
        staff_2 = 'n/a'
    ratio_2 = district_data.loc[district_data['nces_schoolID'] == district_2, 'Pupil/Teacher Ratio [Public School] 2018-19'].iloc[0]
    if ratio_2 == '' or ratio_2 == '-':
        ratio_2 = 'n/a'
    local_2 = "{:.0f}%".format(float(district_data.loc[district_data['nces_schoolID'] == district_2, 'Local Revenue PP %'].iloc[0]) * 100)
    if local_2 == '0%':
        local_2 = 'n/a'
    statefunds_2 = "{:.0f}%".format(float(district_data.loc[district_data['nces_schoolID'] == district_2, 'State Revenue PP %'].iloc[0]) * 100)
    if statefunds_2 == '0%':
        statefunds_2 = 'n/a'
    federal_2 = "{:.0f}%".format(float(district_data.loc[district_data['nces_schoolID'] == district_2, 'Federal Revenue PP %'].iloc[0]) * 100)
    if federal_2 == '0%':
        federal_2 = 'n/a'

    #put dist 2 list on page
    dist_2_list = f"{city_2}, {state_2}\n{region_2}\n{schools_2}\n{grade_2a} - {grade_2b}\n{expenditures_2}\n{students_2}\n{FRL_2} // {IEP_2} // {LEP_2}\n{notwhite_2}\n{FTE_2}\n{staff_2}\n{ratio_2}\n{local_2} // {statefunds_2} // {federal_2}"
    pdf.set_font('Helvetica', '', 9)
    pdf.set_y(162)
    pdf.set_x(369)
    pdf.multi_cell(150, 20, dist_2_list, 0, 'C', 0)

def page_1_bar(pdf, major_bar, comment_1, comment_2, dist_1_ppe, dist_2_ppe, dist_1_name, dist_2_name):
    #add chart title
    pdf.set_font('Helvetica', '', 14)
    pdf.set_y(448)
    pdf.set_x(80)
    pdf.cell(0, 26, 'Per-Pupil Expenditure Across Aggregated Categories', 0, 0, 'L')

    #add footnote label #3
    pdf.set_font('Helvetica', '', 5)
    pdf.set_y(454)
    pdf.set_x(412)
    pdf.cell(0, 6, '3', 0, 0, 'L')
    
    #add bar chart
    pdf.image(major_bar, 37, 476, 431, 0)

    #add ppe sums
    #ppe for dist 1
    pdf.set_font('Helvetica', '', 22)
    pdf.set_y(524)
    pdf.set_x(474)
    pdf.cell(0, 26, f'{dist_1_ppe}', 0, 0, 'L')
    #ppe for dist 2
    pdf.set_y(600)
    pdf.set_x(474)
    pdf.cell(0, 26, f'{dist_2_ppe}', 0, 0, 'L')
    #name of dist 1
    pdf.set_text_color(137, 201, 220)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_y(550)
    pdf.set_x(476)
    pdf.cell(0, 9, f'{dist_1_name} PPE', 0, 0, 'L')
    #name of dist 2
    pdf.set_text_color(203, 145, 189)
    pdf.set_y(626)
    pdf.set_x(476)
    pdf.cell(0, 9, f'{dist_2_name} PPE', 0, 0, 'L')

    #add comment
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_y(721)
    pdf.set_x(83)
    pdf.multi_cell(430, 10, f'{comment_1}', 0, 'L')

def footnote(pdf, source):
    pdf.set_text_color(57, 57, 57)
    pdf.set_font('Helvetica', '', 6)
    pdf.set_y(777)
    pdf.set_x(32)
    pdf.multi_cell(527, 8, "1. The data for the District Fast Facts table was sourced from NCIS School District Data from 2018-2019 with the exception of the 'Total Yearly Expenditures' numbers which were sourced from the data noted in footnote #3.", 0, 'L')
    pdf.set_y(796)
    pdf.set_x(32)
    pdf.multi_cell(527, 8, "2. If data in this table is marked with 'n/a' then the data is missing from NCIS records.", 0, 'L')
    pdf.set_y(807)
    pdf.set_x(32)
    pdf.multi_cell(527, 8, f"3. {source}", 0, 'L')

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
    pdf.set_y(296)
    pdf.set_x(83)
    pdf.set_font('Helvetica', '', 8)
    pdf.multi_cell(430, 10, f'{comment_2}', 0, 'L')

    #add chart title
    pdf.set_font('Helvetica', '', 14)
    pdf.set_y(357)
    pdf.set_x(120)
    pdf.cell(0, 26, 'Per-Pupil Expenditure Across Twenty Largest Categories', 0, 0, 'L')

    #add bar chart
    pdf.image(sub_bar, 46, 386, 504, 0)

"""
Calculates and prints out in terminal the difference
in ppe between ncis data and the calculations made by this tool.
"""
def output_difference(district_data, district_1, district_2, dist_1_ppe, dist_2_ppe, dist_1_name, dist_2_name):
    dist_1_ppe_reported = district_data.loc[district_data['nces_schoolID'] == district_1, 'District Per Pupil Total Expense_x'].iloc[0]
    numeric_filter_1 = filter(str.isdigit, dist_1_ppe)
    numeric_string_1 = "".join(numeric_filter_1)
    dist_1_diff = int(numeric_string_1) - int(dist_1_ppe_reported)
    if dist_1_diff < 0:
        more_less_1 = 'less'
    if dist_1_diff > 0:
        more_less_1 = 'more'
    dist_1_diff = "${:,.0f}".format(abs(dist_1_diff))
    print(f"The NCIS Data reports that {dist_1_name}'s per-pupil expenditures are {dist_1_diff} {more_less_1} than calculated with this tool.")

    dist_2_ppe_reported = district_data.loc[district_data['nces_schoolID'] == district_2, 'District Per Pupil Total Expense_x'].iloc[0]
    numeric_filter_2 = filter(str.isdigit, dist_2_ppe)
    numeric_string_2 = "".join(numeric_filter_2)
    dist_2_diff = int(numeric_string_2) - int(dist_2_ppe_reported)
    if dist_2_diff < 0:
        more_less_2 = 'less'
    if dist_2_diff > 0:
        more_less_2 = 'more'
    dist_2_diff = "${:,.0f}".format(abs(dist_2_diff))
    print(f"The NCIS Data reports that {dist_2_name}'s per-pupil expenditures are {dist_2_diff} {more_less_2} than calculated with this tool.")

if __name__ == '__main__':
    output_report()