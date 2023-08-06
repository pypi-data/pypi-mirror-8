# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# For license information, see the LICENSE.txt file

import argparse
import sys
import traceback
import libtaxii as t
import libtaxii.clients as tc
import libtaxii.messages_10 as tm10
import libtaxii.messages_11 as tm11
import libtaxii.taxii_default_query as tdq

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class ProxyAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        """
        Turns the 'None' string argument into the None object
        that the API expects.
        """
        if option_string == "--proxy" and values == "None":
            values = None

        setattr(namespace, self.dest, values)


class TaxiiScript(object):

    #: taxii version to put in the request headers. Defaults to TAXII 1.1
    taxii_version = t.VID_TAXII_XML_11
    #: parser description
    parser_description = ''
    #: default path
    path = '/'

    def get_arg_parser(self,
                       parser_description,
                       path="/services/discovery/",
                       host="taxiitest.mitre.org",
                       port="80",
                       https=False,
                       cert=None,
                       key=None,
                       username=None,
                       password=None,
                       proxy='noproxy',
                       xml_output=False):
        """
        Parser things common to all scripts. Parsers for specific TAXII Services should
        add their own arguments.
        """
        parser = argparse.ArgumentParser(description=parser_description)
        parser.add_argument("--host", dest="host", default=host, help="Host where the TAXII Service is hosted. Defaults to %s." % host)
        parser.add_argument("--port", dest="port", default=port, type=int, help="Port where the TAXII Service is hosted. Defaults to %s." % port)
        parser.add_argument("--path", dest="path", default=path, help="Path where the TAXII Service is hosted. Defaults to %s" % path)
        parser.add_argument("--https", dest="https", default=https, type=bool, help="Whether or not to use HTTPS. Defaults to %s" % https)
        parser.add_argument("--cert", dest="cert", default=cert, help="The file location of the certificate to use. Defaults to %s." % cert)
        parser.add_argument("--key", dest="key", default=key, help="The file location of the private key to use. Defaults to %s." % key)
        parser.add_argument("--username", dest="username", default=username, help="The username to authenticate with. Defaults to %s." % username)
        parser.add_argument("--pass", dest="password", default=password, help="The password to authenticate with. Defaults to %s." % password)
        parser.add_argument("--proxy", dest="proxy", action=ProxyAction, default=proxy,
                            help="The proxy to use (e.g., http://myproxy.example.com:80/), or 'noproxy' to not use any proxy. If omitted, the system's proxy settings will be used.")
        parser.add_argument("--xml-output", dest="xml_output", action='store_true', default=xml_output,
                            help="If present, the raw XML of the response will be printed to standard out. Otherwise, a \"Rich\" output will be presented.")

        return parser

    def handle_response(self, response, args):
        """
        Default response handler. Just prints the response
        """
        print "Response:\n"
        if args.xml_output is False:
            print response.to_text()
        else:
            print response.to_xml(pretty_print=True)

    def create_client(self, args):
        client = tc.HttpClient()
        client.set_use_https(args.https)
        client.set_proxy(args.proxy)
        tls = (args.cert is not None and args.key is not None)
        basic = (args.username is not None and args.password is not None)
        if tls and basic:
            client.set_auth_type(tc.HttpClient.AUTH_CERT_BASIC)
            client.set_auth_credentials({'key_file': args.key, 'cert_file': args.cert, 'username': args.username, 'password': args.password})
        elif tls:
            client.set_auth_type(tc.HttpClient.AUTH_CERT)
            client.set_auth_credentials({'key_file': args.key, 'cert_file': args.cert})
        elif basic:
            client.set_auth_type(tc.HttpClient.AUTH_BASIC)
            client.set_auth_credentials({'username': args.username, 'password': args.password})

        return client

    def create_request_message(self, args):
        """
        This function should create a request message.
        Should be implemented by child classes.
        """
        raise NotImplementedError

    def __call__(self):
        """
        Invoke a TAXII Service based on the arguments
        """
        try:
            parser = self.get_arg_parser(parser_description=self.parser_description, path=self.path)
            args = parser.parse_args()
            request_message = self.create_request_message(args)
            client = self.create_client(args)

            print "Request:\n"
            if args.xml_output is False:
                print request_message.to_text()
            else:
                print request_message.to_xml(pretty_print=True)

            resp = client.call_taxii_service2(args.host, args.path, self.taxii_version, request_message.to_xml(pretty_print=True), args.port)
            r = t.get_message_from_http_response(resp, '0')

            self.handle_response(r, args)
        except Exception as ex:
            traceback.print_exc()
            sys.exit(EXIT_FAILURE)

        sys.exit(EXIT_SUCCESS)

# TODO: These are stubs that will eventually need to be moved out into their own files / scripts


class SubscriptionClient11Script(TaxiiScript):
    parser_description = 'TAXII 1.1 Subscription Management Client'
    path = '/services/collection-management/'
    pass


class InboxClient10Script(TaxiiScript):
    taxii_version = t.VID_TAXII_XML_10
    parser_description = 'TAXII 1.0 Inbox Client'
    path = '/services/inbox/'


class SubscriptionClient10Script(TaxiiScript):
    taxii_version = t.VID_TAXII_XML_10
    parser_description = 'TAXII 1.0 Subscription Management Client'
    path = '/services/feed-management/'


# No poll fulfillment in TAXII 1.0
