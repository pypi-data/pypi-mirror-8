# -*- coding: utf-8 -*-

"""

  Copyright (c) 2013, 2014 Jaime Soffer

   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

   Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

   Neither the name of the involved organizations nor the names of its
   contributors may be used to endorse or promote products derived from this
   software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
   THE POSSIBILITY OF SUCH DAMAGE.

"""

from urllib.parse import parse_qsl

from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt4.QtCore import QUrl

from eilat.CookieJar import CookieJar
from eilat.libeilat import (is_local, non_whitelisted,
                            is_font, is_numerical,
                            encode_blocked)
from eilat.global_store import database

from pprint import PrettyPrinter
import tldextract

from colorama import Fore, Style

def highlight(qurl, full=False):
    """ Colorizes the address stored in 'qurl'; if 'full' is false,
    it will print only the filename in the end of the path (if any)
    instead of the full path.

    """

    url = qurl.host()
    path = qurl.path()

    if path and not full and qurl.scheme() != 'data':
        path = path.split('/')[-1]

    if path and qurl.scheme() == 'data':
        path = path.split(';')[0]
        return "[data] %s" % (path)

    (subdomain, domain, suffix) = tldextract.extract(url)

    host = "%s.%s%s.%s" % (subdomain,
                           Style.BRIGHT, domain, suffix)
    host = host.strip('.')

    port = ":%s" % (qurl.port()) if qurl.port() >= 0 else ''
    if port:
        host += port

    if qurl.scheme() != 'http':
        host = "[%s] %s" %  (qurl.scheme(), host)

    return "%s%s%s %s" % (
        Style.NORMAL, host, Style.NORMAL,
        path)

def show_labeled(label, url, detail='', color=Fore.RESET, full=False):
    """ Creates a colorized ' LABEL: url path   '
                            '         > details '
        string to display as log output

    """

    result = "%s%s: %s%s" % (Fore.RESET,
                             label,
                             color,
                             highlight(url, full=full))

    if detail:
        result += "\n\t> %s" % (detail)

    result += "%s" % (Fore.RESET)

    print(result)

class InterceptNAM(QNetworkAccessManager):
    """ Reimplements the Network Access Manager to see what's being requested
    by web pages, besides of the page itself. Has primitive support to allow
    requests only from whitelisted sites.

    """

    def __init__(self, options, parent=None):
        super(InterceptNAM, self).__init__(parent)
        print("INIT InterceptNAM")

        self.whitelist = options['host_whitelist']
        self.prefix = options['prefix']

        self.show_detail = self.prefix == ''
        self.show_log = self.prefix == ''

        self.printer = PrettyPrinter(indent=4).pprint

        self.cookie_jar = CookieJar(self, options)
        self.setCookieJar(self.cookie_jar)

        def reply_complete(reply):
            """ Prints when a request completes, handles the filter that
            chooses between successful and filtered requests

            Replies only - if the request is cached and doesn't have to go
            through the network, it will not be reported here

            """

            status = reply.attribute(
                QNetworkRequest.HttpStatusCodeAttribute)

            fil = status is not None and status >= 400
            local = is_local(reply.url())

            color = Fore.RED if fil else Fore.BLUE

            if status is not None and not local:
                if reply.hasRawHeader('X-Cache'):
                    cache_header = (
                        reply.rawHeader('X-Cache').data().decode() +
                        '\t')
                else:
                    cache_header = ''
                if self.show_log:
                    show_labeled(str(status), reply.url(),
                                 color=color,
                                 detail=cache_header)

        self.finished.connect(reply_complete)

        def handle_ssl_error(reply, errors):
            """ Callback to connect when a SSL error happens

            This ignores the error before reporting it; that means all
            "issuer certificate could not be found" and similar will be
            accepted but reported. Until a better way to handle is
            implemented, keep an eye on the console when counting on SSL.
            This can and will create security issues.

            """

            reply.ignoreSslErrors()
            show_labeled("SSL",
                         reply.url(),
                         detail="/".join([k.errorString() for k in errors]),
                         color=Fore.RED)

        self.sslErrors.connect(handle_ssl_error)

    def create_request(self, operation, request, data):
        """ Reimplemented to intercept requests. Stops blacklisted requests

        """

        request.setAttribute(
            QNetworkRequest.HttpPipeliningAllowedAttribute, True)

        qurl = request.url()
        url = qurl.toString()

        # if keeping a log of the POST data, do it before anything else
        try:
            if operation == QNetworkAccessManager.PostOperation:
                post_str = data.peek(4096).data().decode()
                print("_-_-_-_")
                print(url)
                # parse_qsl is imported on a python3-only way;
                # fixable (or maskable) for python2; worth it?
                self.printer(parse_qsl(post_str, keep_blank_values=True))
                print("-_-_-_-")
        except UnicodeDecodeError:
            print("Binary POST upload")

        # stop here if the request is local enough as for not
        # requiring further scrutiny
        if is_local(qurl) and not is_font(qurl):
            if self.show_detail:
                show_labeled("LOCAL", qurl, color=Fore.GREEN)
            return QNetworkAccessManager.createRequest(
                self, operation, request, data)

        # If the request is going to be intercepted a custom request is
        # built and returned after optionally reporting the reason

        for (stop_case, description) in [
                # may still be local
                (is_font(qurl), "TRIM WEBFONT"),
                # it may be an un-dns'ed request; careful here
                (is_numerical(qurl.host()), "NUMERICAL"),
                # whitelist exists, and the requested URL is not in it
                (non_whitelisted(self.whitelist, qurl),
                 "NON WHITELISTED")
        ]:
            if stop_case:
                if self.show_detail:
                    show_labeled(description, qurl, color=Fore.RED)

                return QNetworkAccessManager.createRequest(
                    self,
                    QNetworkAccessManager.GetOperation,
                    QNetworkRequest(QUrl("about:blank")),
                    None)

        # It's not a local request; it should have a proper URL structure
        # then. 'domain' and 'suffix' must be non-None (and non-empty).

        (subdomain, domain, suffix) = tldextract.extract(url)
        subdomain = subdomain if subdomain != '' else None

        for (stop_case, description, detail) in [
                # if 'domain' or 'suffix' are not valid, stop;
                # should never happen (even though it does - some providers
                # don't have a proper 'domain' according to tldextract
                (domain == '' or suffix == '',
                 "SHOULD NOT HAPPEN", " %s|%s|%s " % (subdomain,
                                                      domain,
                                                      suffix)),
                # found the requested URL in the blacklist
                (self.whitelist is None and
                 database().is_blacklisted(domain,
                                           suffix,
                                           subdomain),
                 "FILTER", "%s || %s || %s " % (subdomain,
                                                domain,
                                                suffix))
        ]:
            if stop_case:
                if self.show_detail:
                    show_labeled(description, qurl,
                                 detail=detail, color=Fore.RED)

                return QNetworkAccessManager.createRequest(
                    self,
                    QNetworkAccessManager.GetOperation,
                    QNetworkRequest(QUrl(encode_blocked(description, url))),
                    None)

        return QNetworkAccessManager.createRequest(self, operation,
                                                   request, data)

    # Clean reimplement for Qt
    # pylint: disable=C0103
    createRequest = create_request
    # pylint: enable=C0103
