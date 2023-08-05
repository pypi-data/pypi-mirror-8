"""

:synopsis: Wapiti does not provide ranking for the vulnerabilities it has
    found. This file tries to define a ranking for every vulnerability Wapiti
    might find.

"""


from ptp.libptp.constants import HIGH, MEDIUM, LOW, INFO


#: :data: :class:`dict` of the categories with their rank.
SIGNATURES = {
    # High ranked vulnerabilities
    'SQL Injection': HIGH,
    'Blind SQL Injection': HIGH,
    'Command execution': HIGH,

    # Medium ranked vulnerabilities
    'Htaccess Bypass': MEDIUM,
    'Cross Site Scripting': MEDIUM,
    'CRLF Injection': MEDIUM,
    'CRLF': MEDIUM,

    # Low ranked vulnerabilities
    'File Handling': LOW,  # a.k.a Path or Directory listing
    'Resource consumption': LOW,  # TODO: Is this higher than LOW?

    # Informational ranked vulnerabilities
    'Backup file': INFO,
    'Potentially dangerous file': INFO,  # TODO: Is this higher than INFO?
    'Internal Server Error': INFO,
}
