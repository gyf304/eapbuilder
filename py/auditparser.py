#PATTERN = r"[ \t]*((?:[0-9]+)?).*[ \t]*([0-9]{2}\-[0-9]{2,3})[ \t]+([0-9a-zA-Z]+)[ \t]*'([0-9]+)[ \t]*([A-Za-z\*]+)[ \t]*([0-9]+\.?[0-9]*)"

PATTERN = r".*?([0-9]{2}\-[0-9]{2,3})[ \t]+([0-9a-zA-Z]+)[ \t]*'([0-9]+)[ \t]*([A-Za-z\*]+)[ \t]*([0-9]+\.?[0-9]*).*?"
TAG_PATTERN = r"^[ \t]*([0-9]+)\."
#import re
try:
    import _jsre as re
except:
    import re

DESCRIPTION_PATTERN = r"""^[ ]*([0-9]+).[ ]*(.*?)[ ]*\:"""
COMPLETED_PATTEN = r"""^.*([0-9]{2}\-[0-9]{3})[ ]*(.*?) *'([0-9]+)[ ]*([A-Za-z\*\+\-]+)[ ]*([0-9]+\.[0-9]*)"""
INCOMPLETE_PATTERN = r"""^.*?([0-9]+)[ ]*unfilled[ ]*course"""
UNUSED_PATTERN = r"""^.*?([0-9]{2}\-[0-9]{3})[ ]*(.*?)[ ]*'([0-9]{2})[ ]*([A-Za-z\*\+\-]+)[ ]*([0-9]+\.[0-9]*)[ ]*\(Unused\)"""

def parse_audit(audit):
    cur_tag = 0
    #r = re.compile(PATTERN)
    #rt = re.compile(TAG_PATTERN)
    result = []
    result.append({
        'id': 0, 
        'description': 'Unused', 
        'total': 0,
        'totalHidden': True,
        'courses': []
    })
    for line in audit.splitlines():
        mdes = re.match(DESCRIPTION_PATTERN, line)
        if mdes: 
            result.append({
                'id': int(mdes.group(1)), 
                'description': mdes.group(2), 
                'total': 0,
                'totalHidden': False,
                'courses': []
            })
        munused = re.match(UNUSED_PATTERN, line)
        if munused:
            l = result[0]['courses']
            #print(munused.group(3))
            l.append({
                'course_number': munused.group(1),
                'instance': {
                    'year': int(munused.group(3)),
                    'semester': munused.group(2)
                },
                'grade': munused.group(4),
                'units': float(munused.group(5))
            })
            result[0]['total'] += 1
            continue
        mcompl = re.match(COMPLETED_PATTEN, line)
        if mcompl:
            #print("mcompl")
            l = result[-1]['courses']
            l.append({
                'course_number': mcompl.group(1),
                'instance': {
                    'year': int(mcompl.group(3)),
                    'semester': mcompl.group(2)
                },
                'grade': mcompl.group(4),
                'units': float(mcompl.group(5))
            })
            result[-1]['total'] += 1
        minc = re.match(INCOMPLETE_PATTERN, line)
        if minc:
            l = result[-1]['courses']
            n = int(minc.group(1))
            result[-1]['total'] += n
        #print(line)
    return result
