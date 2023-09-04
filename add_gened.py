import csv

def add_gened_data(gened, permalinked, final):
    # gened_dict is a dictionary OF dictionaries where the key is the course code and the object is the course data
    gened_dict = dict()
    with open(gened, newline='') as gened_list:
        gened_reader = csv.DictReader(gened_list)
        for gened_row in gened_reader:
            gened_dict[gened_row['Course Code']] = gened_row

    with open(final, 'w', newline='') as final_list:
        fieldnames = ['Title', 'Course Prefix', 'Course Code', 'Section', 'ISBN', 'Permalink',
                      'Access', 'GenEd', 'Other Curriculum']  # update based on the values used in Drupal
        final_writer = csv.DictWriter(final_list, fieldnames=fieldnames)
        final_writer.writeheader()

        with open(permalinked, newline='') as permalinked_list:
            permalinked_reader = csv.DictReader(permalinked_list)

            for permalinked_row in permalinked_reader:
                course_code = permalinked_row['Prefix'] + \
                    permalinked_row['Number']
                
                course_record = gened_dict.get(course_code)
                genedValue = ''
                otherValue = ''
                # checks to see if there is a gened/curriculum value for the given eTextbook row                
                # if matching value was found in the GenEd csv, adds that value in
                if course_record != None:#maybe figure more robust way to write this
                    #TODO: change to actual found values
                    if course_record['General Education Area'] != 'Not Gen Ed':
                        genedValue += course_record['General Education Area']
                    if course_record['2nd General Education Area'] != '':
                        genedValue += ';' + course_record['2nd General Education Area']
                    
                    #combining all the curriculum values into a single attribute
                    if course_record['Statewide Core'] == 'Yes':
                        otherValue += 'Statewide Core;'
                    if course_record['E-Series/W (State-Mandated Writing)'] == 'Yes':
                        otherValue += 'E-Series/W (State-Mandated Writing);'
                    if course_record['Scholarship in Practice'] == 'Yes':
                        otherValue += 'Scholarship in Practice;'
                    if course_record['Formative Experiences'] == 'Yes':
                        otherValue += 'Formative Experiences;'
                    if course_record['Diversity Requirement'] == 'Yes':
                        otherValue += 'Diversity Requirement;'
                    if course_record['Oral Communication Competency'] == 'Yes':
                        otherValue += 'Oral Communication Competency;'
                    if course_record['Computer Competency'] == 'Yes':
                        otherValue += 'Computer Competency;'
                    if course_record['Digital Literacy'] == 'Yes':
                        otherValue += 'Digital Literacy;'
                    if course_record['Natural Sciences Laboratory'] == 'Yes':
                        otherValue += 'Natural Sciences Laboratory;'
                    if course_record['Upper Division Writing Competency'] == 'Yes':
                        otherValue += 'Upper Division Writing Competency;'

                final_writer.writerow({
                    'Title': permalinked_row['Title'],
                    'Course Prefix': permalinked_row['Prefix'],
                    'Course Code': permalinked_row['Number'],
                    'Section': permalinked_row['Section'],
                    'ISBN': permalinked_row['ISBN'],
                    'Permalink': permalinked_row['Permalink'],
                    'Access': permalinked_row['Access'],
                    'GenEd': genedValue,
                    'Other Curriculum': otherValue
                })

add_gened_data('data/gened.csv', 'data/permalinked_list.csv', 'data/final_etextbooks.csv')