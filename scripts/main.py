'''INPUT COMMENTS BELOW'''
#please put in a custom report name here - name MUST be in quotation marks
report_name = 'Sample Tolleson & Atlanta District Comparison Report'

#this is where you input the ncis id for the districts you are comparing - ID MUST be in quotation marks
dist_1_id = '408520'
dist_2_id = '1300120'

#this is where you input the full school district name to be used in the report title
dist_1_full_name = 'Tolleson Union High School District'
dist_2_full_name = 'Atlanta Public Schools'

#this is where you input the short district name to be used in visualizations - name MUST be in quotation marks
#for example Auburn City Schools would be shortened to just "Auburn"
dist_1_short_name = 'Tolleson'
dist_2_short_name = 'Atlanta'

#this is where you add in the source of the district data used
source = "The visualizations and graphics data for the Tolleson District data was sourced from an 'Account Details' spreadsheet provided by the school district. The Atlanta data was sourced from the Georgia Department of Education's Financial Review Data Collection System Budget Analysis Report for the year ending June 30, 2019."

#this is where you add in comments for the report - comments MUST be in quotation marks
comment_1 = 'This is sample comment about the bar chart that shows the 7 major categories'
comment_2 = 'This is sample comment about the two pie charts and the one large bar chart that show the some of the largest subcategories'

"""DO NOT EDIT THE BELOW CODE"""
import os

from map_districts import create_map
from make_graphics import create_visualizations
from make_report import output_report

cwd = os.getcwd()
size = len(cwd)
dir = cwd[:size - 7]
user_input = [report_name, dist_1_short_name, dist_2_short_name, source, comment_1, comment_2, dist_1_full_name, dist_2_full_name]

#these two blocks of code run the whole pipline
def main():
    sums = create_map(dist_1_id, dist_2_id, dir)
    print('mapping district data to edstruments categories...')
    dist_1_ppe, dist_2_ppe = create_visualizations(dist_1_id, dist_2_id, dist_1_short_name, dist_2_short_name, dir)
    print('creating data visualizations... (and ignore above warnings)')
    output_report(dist_1_id, dist_2_id, dist_1_ppe, dist_2_ppe, user_input, sums, dir)
    print('all done!')

if __name__ == '__main__':
    main()