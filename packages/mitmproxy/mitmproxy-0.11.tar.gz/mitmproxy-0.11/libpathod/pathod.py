import urllib
import threading
import logging
import os
import sys
from netlib import tcp, http, wsgi, certutils
import netlib.utils

from . import version, app, language, utils


DEFAULT_CERT_DOMAIN = "pathod.net"
CONFDIR = "~/.mitmproxy"
CERTSTORE_BASENAME = "mitmproxy"
CA_CERT_NAME = "mitmproxy-ca.pem"

logger = logging.getLogger('pathod')


class PathodError(Exception):
    pass


class SSLOptions:
    def __init__(self, confdir=CONFDIR, cn=None, not_after_connect=None,
                 request_client_cert=False, sslversion=tcp.SSLv23_METHOD,
                 ciphers=None, certs=None):
        self.confdir = confdir
        self.cn = cn
        self.certstore = certutils.CertStore.from_store(
            os.path.expanduser(confdir),
            CERTSTORE_BASENAME
        )
        for i in certs or []:
            self.certstore.add_cert_file(*i)
        self.not_after_connect = not_after_connect
        self.request_client_cert = request_client_cert
        self.ciphers = ciphers
        self.sslversion = sslversion

    def get_cert(self, name):
        if self.cn:
            name = self.cn
        elif not name:
            name = DEFAULT_CERT_DOMAIN
        return self.certstore.get_cert(name, [])


class PathodHandler(tcp.BaseHandler):
    wbufsize = 0
    sni = None

    def info(self, s):
        logger.info("%s:%s: %s" % (self.address.host, self.address.port, str(s)))

    def handle_sni(self, connection):
        self.sni = connection.get_servername()

    def serve_crafted(self, crafted):
        c = self.server.check_policy(crafted, self.server.request_settings)
        if c:
            err = language.make_error_response(c)
            language.serve(err, self.wfile, self.server.request_settings)
            log = dict(
                type="error",
                msg=c
            )
            return False, log

        if self.server.explain and not isinstance(crafted, language.PathodErrorResponse):
            crafted = crafted.freeze(self.server.request_settings, None)
            self.info(">> Spec: %s" % crafted.spec())
        response_log = language.serve(
            crafted,
            self.wfile,
            self.server.request_settings,
            None
        )
        if response_log["disconnect"]:
            return False, response_log
        return True, response_log

    def handle_request(self):
        """
            Returns a (again, log) tuple.

            again: True if request handling should continue.
            log: A dictionary, or None
        """
        line = self.rfile.readline()
        if line == "\r\n" or line == "\n":  # Possible leftover from previous message
            line = self.rfile.readline()
        if line == "":
            # Normal termination
            return False, None

        m = utils.MemBool()
        if m(http.parse_init_connect(line)):
            headers = http.read_headers(self.rfile)
            self.wfile.write(
                'HTTP/1.1 200 Connection established\r\n' +
                ('Proxy-agent: %s\r\n' % version.NAMEVERSION) +
                '\r\n'
            )
            self.wfile.flush()
            if not self.server.ssloptions.not_after_connect:
                try:
                    cert, key, chain_file = self.server.ssloptions.get_cert(m.v[0])
                    self.convert_to_ssl(
                        cert, key,
                        handle_sni=self.handle_sni,
                        request_client_cert=self.server.ssloptions.request_client_cert,
                        cipher_list=self.server.ssloptions.ciphers,
                        method=self.server.ssloptions.sslversion,
                    )
                except tcp.NetLibError, v:
                    s = str(v)
                    self.info(s)
                    return False, dict(type="error", msg=s)
            return True, None
        elif m(http.parse_init_proxy(line)):
            method, _, _, _, path, httpversion = m.v
        elif m(http.parse_init_http(line)):
            method, path, httpversion = m.v
        else:
            s = "Invalid first line: %s" % repr(line)
            self.info(s)
            return False, dict(type="error", msg=s)

        headers = http.read_headers(self.rfile)
        if headers is None:
            s = "Invalid headers"
            self.info(s)
            return False, dict(type="error", msg=s)

        clientcert = None
        if self.clientcert:
            clientcert = dict(
                cn=self.clientcert.cn,
                subject=self.clientcert.subject,
                serial=self.clientcert.serial,
                notbefore=self.clientcert.notbefore.isoformat(),
                notafter=self.clientcert.notafter.isoformat(),
                keyinfo=self.clientcert.keyinfo,
            )

        retlog = dict(
            type="crafted",
            request=dict(
                path=path,
                method=method,
                headers=headers.lst,
                httpversion=httpversion,
                sni=self.sni,
                remote_address=self.address(),
                clientcert=clientcert,
            ),
            cipher=None,
        )
        if self.ssl_established:
            retlog["cipher"] = self.get_current_cipher()

        try:
            content = http.read_http_body(
                self.rfile, headers, None,
                method, None, True
            )
        except http.HttpError, s:
            s = str(s)
            self.info(s)
            return False, dict(type="error", msg=s)

        for i in self.server.anchors:
            if i[0].match(path):
                self.info("crafting anchor: %s" % path)
                again, retlog["response"] = self.serve_crafted(i[1])
                return again, retlog

        if not self.server.nocraft and path.startswith(self.server.craftanchor):
            spec = urllib.unquote(path)[len(self.server.craftanchor):]
            self.info("crafting spec: %s" % spec)
            try:
                crafted = language.parse_response(spec)
            except language.ParseException, v:
                self.info("Parse error: %s" % v.msg)
                crafted = language.make_error_response(
                    "Parse Error",
                    "Error parsing response spec: %s\n" % v.msg + v.marked()
                )
            again, retlog["response"] = self.serve_crafted(crafted)
            return again, retlog
        elif self.server.noweb:
            crafted = language.make_error_response("Access Denied")
            language.serve(crafted, self.wfile, self.server.request_settings)
            return False, dict(
                type="error",
                msg="Access denied: web interface disabled"
            )
        else:
            self.info("app: %s %s" % (method, path))
            req = wsgi.Request("http", method, path, headers, content)
            flow = wsgi.Flow(self.address, req)
            sn = self.connection.getsockname()
            a = wsgi.WSGIAdaptor(
                self.server.app,
                sn[0],
                self.server.address.port,
                version.NAMEVERSION
            )
            a.serve(flow, self.wfile)
            return True, None

    def _log_bytes(self, header, data, hexdump):
        s = []
        if hexdump:
            s.append("%s (hex dump):" % header)
            for line in netlib.utils.hexdump(data):
                s.append("\t%s %s %s" % line)
        else:
            s.append("%s (unprintables escaped):" % header)
            s.append(netlib.utils.cleanBin(data))
        self.info("\n".join(s))

    def handle(self):
        if self.server.ssl:
            try:
                cert, key, chain_file = self.server.ssloptions.get_cert(None)
                self.convert_to_ssl(
                    cert, key,
                    handle_sni=self.handle_sni,
                    request_client_cert=self.server.ssloptions.request_client_cert,
                    cipher_list=self.server.ssloptions.ciphers,
                    method=self.server.ssloptions.sslversion,
                )
            except tcp.NetLibError, v:
                s = str(v)
                self.server.add_log(
                    dict(
                        type="error",
                        msg=s
                    )
                )
                self.info(s)
                return
        self.settimeout(self.server.timeout)
        while not self.finished:
            if self.server.logreq:
                self.rfile.start_log()
            if self.server.logresp:
                self.wfile.start_log()
            again, log = self.handle_request()
            if log:
                if self.server.logreq:
                    log["request_bytes"] = self.rfile.get_log().encode("string_escape")
                    self._log_bytes("Request", log["request_bytes"], self.server.hexdump)
                if self.server.logresp:
                    log["response_bytes"] = self.wfile.get_log().encode("string_escape")
                    self._log_bytes("Response", log["response_bytes"], self.server.hexdump)
                self.server.add_log(log)
            if not again:
                return


class Pathod(tcp.TCPServer):
    LOGBUF = 500

    def __init__(
        self,
        addr,
        confdir=CONFDIR,
        ssl=False,
        ssloptions=None,
        craftanchor="/p/",
        staticdir=None,
        anchors=(),
        sizelimit=None,
        noweb=False,
        nocraft=False,
        noapi=False,
        nohang=False,
        timeout=None,
        logreq=False,
        logresp=False,
        explain=False,
        hexdump=False
    ):
        """
            addr: (address, port) tuple. If port is 0, a free port will be
            automatically chosen.
            ssloptions: an SSLOptions object.
            craftanchor: string specifying the path under which to anchor
            response generation.
            staticdir: path to a directory of static resources, or None.
            anchors: List of (regex object, language.Request object) tuples, or
            None.
            sizelimit: Limit size of served data.
            nocraft: Disable response crafting.
            noapi: Disable the API.
            nohang: Disable pauses.
        """
        tcp.TCPServer.__init__(self, addr)
        self.ssl = ssl
        self.ssloptions = ssloptions or SSLOptions()
        self.staticdir = staticdir
        self.craftanchor = craftanchor
        self.sizelimit = sizelimit
        self.noweb, self.nocraft = noweb, nocraft
        self.noapi, self.nohang = noapi, nohang
        self.timeout, self.logreq = timeout, logreq
        self.logresp, self.hexdump = logresp, hexdump
        self.explain = explain

        self.app = app.make_app(noapi)
        self.app.config["pathod"] = self
        self.log = []
        self.logid = 0
        self.anchors = anchors

    def check_policy(self, req, settings):
        """
            A policy check that verifies the request size is withing limits.
        """
        try:
            l = req.maximum_length(settings)
        except language.FileAccessDenied:
            return "File access denied."
        if self.sizelimit and l > self.sizelimit:
            return "Response too large."
        if self.nohang and any([isinstance(i, language.PauseAt) for i in req.actions]):
            return "Pauses have been disabled."
        return False

    @property
    def request_settings(self):
        return dict(
            staticdir=self.staticdir
        )

    def handle_client_connection(self, request, client_address):
        h = PathodHandler(request, client_address, self)
        try:
            h.handle()
            h.finish()
        except tcp.NetLibDisconnect:  # pragma: no cover
            h.info("Disconnect")
            self.add_log(
                dict(
                    type="error",
                    msg="Disconnect"
                )
            )
            return
        except tcp.NetLibTimeout:
            h.info("Timeout")
            self.add_log(
                dict(
                    type="timeout",
                )
            )
            return

    def add_log(self, d):
        if not self.noapi:
            lock = threading.Lock()
            with lock:
                d["id"] = self.logid
                self.log.insert(0, d)
                if len(self.log) > self.LOGBUF:
                    self.log.pop()
                self.logid += 1
            return d["id"]

    def clear_log(self):
        lock = threading.Lock()
        with lock:
            self.log = []

    def log_by_id(self, id):
        for i in self.log:
            if i["id"] == id:
                return i

    def get_log(self):
        return self.log


def main(args):
    ssloptions = SSLOptions(
        cn = args.cn,
        confdir = args.confdir,
        not_after_connect = args.ssl_not_after_connect,
        ciphers = args.ciphers,
        sslversion = utils.SSLVERSIONS[args.sslversion],
        certs = args.ssl_certs
    )

    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    log = logging.getLogger('pathod')
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        '%(asctime)s: %(message)s',
        datefmt='%d-%m-%y %H:%M:%S',
    )
    if args.logfile:
        fh = logging.handlers.WatchedFileHandler(args.logfile)
        fh.setFormatter(fmt)
        log.addHandler(fh)
    if not args.daemonize:
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        log.addHandler(sh)

    try:
        pd = Pathod(
            (args.address, args.port),
            craftanchor = args.craftanchor,
            ssl = args.ssl,
            ssloptions = ssloptions,
            staticdir = args.staticdir,
            anchors = args.anchors,
            sizelimit = args.sizelimit,
            noweb = args.noweb,
            nocraft = args.nocraft,
            noapi = args.noapi,
            nohang = args.nohang,
            timeout = args.timeout,
            logreq = args.logreq,
            logresp = args.logresp,
            hexdump = args.hexdump,
            explain = args.explain,
        )
    except PathodError, v:
        print >> sys.stderr, "Error: %s"%v
        sys.exit(1)
    except language.FileAccessDenied, v:
        print >> sys.stderr, "Error: %s"%v

    if args.daemonize:
        utils.daemonize()

    try:
        print "%s listening on %s:%s"%(
            version.NAMEVERSION,
            pd.address.host,
            pd.address.port
        )
        pd.serve_forever()
    except KeyboardInterrupt:
        pass
