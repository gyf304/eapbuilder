def merge_audits(audits):
    merged_audit_dict = {}
    for audit in audits:
        for item in audit:
            course_id = '|'.join([item['course_number'], item['semester'], item['year']])
            merged_audit_dict[course_id] = (
                 {'course_number':item['course_number'], 
                  'semester':item['semester'], 
                  'year':item['year'], 
                  'grade':item['grade'], 
                  'units':item['units'],
                  'tags': []})
    for i in range(len(audits)):
        dctr = dict()
        for item in audits[i]:
            t = item['tag']
            if t in dctr:
                dctr[t] += 1
            else:
                dctr[t] = 1
        dctr2 = dict()
        for item in audits[i]:
            course_id = '|'.join([item['course_number'], item['semester'], item['year']])
            t = item['tag']
            if t in dctr2:
                dctr2[t] += 1
            else:
                dctr2[t] = 1
            new_tag = ''
            if t != 0:
                new_tag = str(t) if dctr[t] == 1 else str(t) + '.' + str(dctr2[t])
                if len(audits) > 1:
                    new_tag = str(i+1) + '.' + new_tag
            #merged_audit.append()
            if new_tag:
                merged_audit_dict[course_id]['tags'].append(new_tag)
    merged_audit = list(zip(*merged_audit_dict.items()))[1]
    return merged_audit

def structure_audit(audits):
    merged_audit_dict = {}
    for audit in audits:
        for item in audit:
            course_id = '|'.join([item['course_number'], item['semester'], item['year']])
            merged_audit_dict[course_id] = (
                 {'course_number':item['course_number'], 
                  'semester':item['semester'], 
                  'year':item['year'], 
                  'grade':item['grade'], 
                  'units':item['units'],
                  'tags': []})
    for i in range(len(audits)):
        dctr = dict()
        for item in audits[i]:
            t = item['tag']
            if t in dctr:
                dctr[t] += 1
            else:
                dctr[t] = 1
        dctr2 = dict()
        for item in audits[i]:
            course_id = '|'.join([item['course_number'], item['semester'], item['year']])
            t = item['tag']
            if t in dctr2:
                dctr2[t] += 1
            else:
                dctr2[t] = 1
            new_tag = ''
            if t != 0:
                new_tag = str(t) if dctr[t] == 1 else str(t) + '.' + str(dctr2[t])
                if len(audits) > 1:
                    new_tag = str(i+1) + '.' + new_tag
            #merged_audit.append()
            if new_tag:
                merged_audit_dict[course_id]['tags'].append(new_tag)
    merged_audit = list(zip(*merged_audit_dict.items()))[1]
    #course_dict = get_course_dict()
    
    #print(merged_audit)
    structured_audit_dict = {}
    for item in merged_audit:
        semester = (item['semester'], item['year'])
        if semester not in structured_audit_dict:
            structured_audit_dict[semester] = []
        structured_audit_dict[semester].append(
                {'course_number':item['course_number'], 
                  'grade':item['grade'], 
                  'units':item['units'], 
                  'tags':item['tags'],
                  'course_name': course_dict.get(item['course_number'], ('',0.0))[0]})
    def semester_to_tuple(semester):
        (s, y) = semester
        s_num = 0
        y_num = int(y)
        if s == 'Fall':
            s_num = 1
        else:
            y_num -= 1
            if s == 'Spring':
                s_num = 2
            if s == 'Sum1':
                s_num = 3
            if s == 'Sum2':
                s_num = 4
        return (y_num, s_num)
    structured_audit = sorted(list(structured_audit_dict.items()), key=lambda k: semester_to_tuple(k[0]))

    # for semester_record in structured_audit:
    #     (s, y) = semester_record[0]
    #     courses = semester_record[1]
    #     print(s, y)
    #     for course in courses:
    #         print('{course_number:8s}{course_name:20s}{units:5.1f}'.format(**course))
    return structured_audit
    
def structured_audit_to_tables(audit):
    tables = []
    for semester_record in audit:
        (s, y) = semester_record[0]
        courses = semester_record[1]
        table = []
        for course in courses:
            table.append([course['course_name'], course['course_number'], course['tags'], course['units']])
        tables.append(((s, y), table))
    print(tables)
    return tables


def format_tables(tables):
    result = []
    i = 0
    while i < len(tables):
        (sr, table) = tables[i]
        (semester, year) = sr
        if semester == "Fall" and i+1 < len(tables):
            (sr2, table2) = tables[i+1]
            (semester2, year2) = sr2
            if semester2 == "Spring" and year2 == year+1:
                # dual row mode
                result.append()
                table.append(['{:} {:}'.format(*sr), '{:} {:}'.format(*sr2)])
                table.append

        i += 1