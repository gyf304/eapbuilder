from auditparser import parse_audit
#from courselistdata import course_dict
import browser
from courselist import get_course_dict
from browser import window
import json

courses_dict = get_course_dict()

def load_audit(audit_string):
    audit = parse_audit(audit_string)
    for cat_index in range(len(audit)):
        cat = audit[cat_index]
        courses = cat['courses']
        for course in courses:
            course_number = course['course_number']
            course['course_name'] = courses_dict[course_number]['course_name'] if course_number in courses_dict else ''
    return audit

def flatten_audits(audits):
    flatten_dict = {}
    for audit_index in range(len(audits)):
        audit = audits[audit_index]
        for cat_index in range(len(audit)):
            cat = audit[cat_index]
            cat_id = cat['id']
            courses = cat['courses']
            for course_index in range(len(courses)):
                course = courses[course_index]
                course_number = course['course_number']
                course_id = course_number + \
                            course['instance']['semester'] + \
                            str(course['instance']['year'])
                instance = {
                    'semester': course['instance']['semester'],
                    'year': course['instance']['year']
                }
                if (course_id not in flatten_dict.keys()):
                    flatten_dict[course_id] = {
                        'tags': [],
                    }
                if cat_id != 0:
                    tag = '{:}.{:}.{:}'.format(audit_index+1, cat_id, course_index+1) \
                            if cat['total'] > 1 or len(courses) > 1 \
                            else '{:}.{:}'.format(audit_index+1, cat_id)
                    flatten_dict[course_id]['tags'].append(tag)
                prev_course_name = flatten_dict[course_id].get('course_name', '')
                new_course_name = course.get('course_name', '')
                flatten_dict[course_id].update(course)
                flatten_dict[course_id]['course_name'] = new_course_name if len(new_course_name) > len(prev_course_name) else prev_course_name
    courses_list = list(flatten_dict.values())
    return courses_list

def filter_flattened(courses, requirements):
    results = []
    for course in courses:
        is_valid = True
        for (key, req) in requirements.items():
            if course[key] != req:
                is_valid = False
                break
            if is_valid:
                results.append(course)
    return results

def filter_audits(audits, requirement):
    faudits = flatten_audits(audits)
    return filter_flattened(faudits, requirement)

def gen_eap(audits):
    flattened = flatten_audits(audits)
    transfer_courses = []
    non_transfer_courses = []
    instance_dict = {}
    for course in flattened:
        grade = course['grade']
        if grade == 'TR':
            transfer_courses.append(course)
        else:
            non_transfer_courses.append(course)
    for course in non_transfer_courses:
        instance = course['instance']['semester'] + str(course['instance']['year'])
        if instance not in instance_dict:
            instance_dict[instance] = []
        instance_dict[instance].append(course)
    year_dict = {} # Sum16, F16, S17 -> 16
    for (instance, courses) in instance_dict.items():
        semester = courses[0]['instance']['semester']
        year = int(courses[0]['instance']['year'])
        if semester == "Spring":
            year -= 1
        if year not in year_dict:
            year_dict[year] = {}
        year_dict[year][semester] = courses
    result_list = []
    result_list.append({
        'type': '2col',
        'newPage': False,
        'data': {
            'left': {
                'title': 'Transfer Credits',
                'courses': transfer_courses[:len(transfer_courses)//2]
            },
            'right': {
                'title': 'Transfer Credits',
                'courses': transfer_courses[len(transfer_courses)//2:]
            }
        }
    })
    for (year, semesters) in sorted(list(year_dict.items())):
        if 'Sum1' in semesters or 'Sum2' in semesters:
            result_list.append({
                'type': '2col',
                'newPage': False,
                'data': {
                    'left': {
                        'title': 'Summer1 {:}'.format(year),
                        'courses': semesters.get('Sum1', [])
                    },
                    'right': {
                        'title': 'Summer2 {:}'.format(year),
                        'courses': semesters.get('Sum2', [])
                    }
                }
            })
        if 'Spring' in semesters or 'Fall' in semesters:
            result_list.append({
                'type': '2col',
                'newPage': True,
                'data': {
                    'left': {
                        'title': 'Fall {:}'.format(year),
                        'courses': semesters.get('Fall', [])
                    },
                    'right': {
                        'title': 'Spring {:}'.format(year+1),
                        'courses': semesters.get('Spring', [])
                    }
                }
            })
    return result_list

interface = {
    'loadAudit': load_audit,
    'parseAudit': load_audit,
    'flattenAudits': flatten_audits,
    'filterAudits': filter_audits,
    'genEap': gen_eap
}

def invoke(func, argstr):
    argp = json.loads(argstr)
    args = argp[0] if argp[0] else []
    kwargs = argp[1] if argp[1] else {}
    return json.dumps((interface[func])(*args, **kwargs))

window.rawInvokePython = invoke

print("Loaded")
