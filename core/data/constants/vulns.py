'''
vulns.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
VULNS = {
         00000: 'TestCase',
         
         # Audit
         10000: 'Blind SQL injection vulnerability',
         10001: 'Buffer overflow vulnerability',
         10002: 'Multiple CORS misconfigurations',
         10003: 'Sensitive and strange CORS methods enabled',
         10004: 'Sensitive CORS methods enabled',
         10005: 'Uncommon CORS methods enabled',
         10006: 'Access-Control-Allow-Origin set to "*"',
         10007: 'Insecure Access-Control-Allow-Origin with credentials',
         10008: 'Insecure Access-Control-Allow-Origin',
         10009: 'Incorrect withCredentials implementation',
         10010: 'CSRF vulnerability',
         10011: 'Insecure DAV configuration',
         10012: 'DAV incorrect configuration',
         10013: 'DAV insufficient privileges',
         10014: 'eval() input injection vulnerability',
         10015: 'Insecure file upload',
         10016: 'Format string vulnerability',
         10017: 'Insecure Frontpage extensions configuration',
         10018: 'Unidentified vulnerability',
         10019: 'Potential unidentified vulnerability',
         10020: 'Insecure redirection',
         10021: 'Misconfigured access control',
         10022: 'LDAP injection vulnerability',
         10023: 'Local file inclusion vulnerability',
         10024: 'File read error',
         10025: 'MX injection vulnerability',
         10026: 'OS commanding vulnerability',
         10027: 'Phishing vector',
         10028: 'Unsafe preg_replace usage',
         10029: 'ReDoS vulnerability',
         10030: 'Potential ReDoS vulnerability',
         10031: 'Response splitting vulnerability',
         10032: 'Remote code execution',
         10033: 'Remote file inclusion',
         10034: 'Potential remote file inclusion',
         10035: 'SQL injection',
         10036: 'Server side include vulnerability',
         10037: 'Persistent server side include vulnerability',
         10038: 'Insecure SSL version',
         10039: 'Invalid SSL certificate',
         10041: 'Invalid SSL connection',
         10042: 'Soon to expire SSL certificate',
         10043: 'SSL Certificate dump',
         10044: 'Secure content over insecure channel',
         10045: 'XPATH injection vulnerability',
         10046: 'Permanent cross site scripting vulnerability',
         10047: 'Cross site scripting vulnerability',
         10048: 'Cross site tracing vulnerability',

         # Crawl
         20000: 'phpinfo() file found',
         20001: 'PHP register_globals: On',
         20002: 'PHP allow_url_fopen: On',
         20003: 'PHP allow_url_include: On',
         20004: 'PHP display_errors: On',
         20005: 'PHP expose_php: On',
         20006: 'PHP lowest_privilege_test:fail',
         20007: 'PHP disable_functions:few',
         20008: 'PHP curl_file_support:not_fixed',
         20009: 'PHP cgi_force_redirect: Off',
         20010: 'PHP session.cookie_httponly: Off',
         20011: 'PHP session_save_path:Everyone',
         20012: 'PHP session_use_trans: On',
         20013: 'PHP default_charset: Off',
         20014: 'PHP enable_dl: On',
         20015: 'PHP memory_limit:high',
         20016: 'PHP post_max_size:high',
         20017: 'PHP upload_max_filesize:high',
         20018: 'PHP upload_tmp_dir:Everyone',
         20019: 'PHP file_uploads: On',
         20020: 'PHP magic_quotes_gpc: On',
         20021: 'PHP magic_quotes_gpc: Off',
         20022: 'PHP open_basedir:disabled',
         20023: 'PHP open_basedir:enabled',
         20024: 'PHP session.hash_function:md5',
         20025: 'PHP session.hash_function:sha',
         20026: 'Insecure resource',
         20027: '.listing file found',
         20028: 'Operating system username and group leak',
         20029: 'Google hack database match',
         20030: 'Phishing scam',
         20031: 'Source code repository',
         20032: 'Insecure RIA settings',
         20033: 'Cross-domain allow ACL',
         20034: 'Potential web backdoor',
         20035: '',
         20036: '',
         20037: '',
         20038: '',
         
         # Grep
         30001: 'US Social Security Number disclosure',
         30002: 'DOM Cross site scripting',
         30003: 'Parameter has SQL sentence',
         30004: 'Uncommon query string parameter',
         30005: 'Credit card number disclosure',
         30006: 'Code disclosure vulnerability',
         30007: 'Code disclosure vulnerability in 404 page',
         30008: 'Unhandled error in web application',
         30009: 'Basic HTTP credentials',
         30010: 'Authentication without www-authenticate header',
         30011: 'NTLM authentication',
         30012: 'HTTP Basic authentication',
         30013: 'Basic HTTP credentials',
         30014: 'Cookie without HttpOnly',
         30015: 'Secure cookie over HTTP',
         30016: 'Secure flag missing in HTTPS cookie',
         30017: 'Secure cookies over insecure channel',
         30018: 'Identified cookie',
         30019: 'Cookie',
         30020: 'Invalid cookie',
         30021: 'Click-Jacking vulnerability',
         30022: 'Private IP disclosure vulnerability',
         30023: 'Directory indexing',
         30024: 'Path disclosure vulnerability',
         30025: 'Missing cache control for HTTPS content',
         30026: 'SVN user disclosure vulnerability',
         
         # Infrastructure
         40000: 'Potential XSS vulnerability',
         40000: '',
         40000: '',
         40000: 'Apache Server version',
         40000: 'Shared hosting',
         40000: 'Virtual host identified',
         40000: 'Previous defacements',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         40000: '',
         
         # Bruteforce
         50000: 'Guessable credentials',
         50001: '',
         
                                    
         }

def is_valid_name(name):
    return name in VULNS.values()