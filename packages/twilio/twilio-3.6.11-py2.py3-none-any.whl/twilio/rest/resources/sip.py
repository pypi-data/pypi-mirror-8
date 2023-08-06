from twilio.rest.resources.sip_credential_lists import Credentials
from twilio.rest.resources.sip_credential_lists import SipCredentialLists
from twilio.rest.resources.sip_domains import CredentialListMappings
from twilio.rest.resources.sip_domains import IpAccessControlListMappings
from twilio.rest.resources.sip_domains import SipDomains
from twilio.rest.resources.sip_ip_access_control_lists import IpAddresses
from twilio.rest.resources.sip_ip_access_control_lists import SipIpAccessControlLists


class Sip(object):
    """Holds all the SIP resources."""
    def __init__(self, base_uri, auth, timeout):
        self.uri = "%s/SIP" % base_uri
        self.auth = auth
        self.timeout = timeout
        self.domains = SipDomains(self.uri, auth, timeout)
        self.credential_lists = SipCredentialLists(self.uri, auth, timeout)
        self.ip_access_control_lists = SipIpAccessControlLists(
            self.uri,
            auth,
            timeout,
        )

    def ip_access_control_list_mappings(self, domain_sid):
        """
        Return a :class:`IpAccessControlListMappings` instance for the
        :class:`SipDomain` with the given domain_sid
        """
        base_uri = "{}/Domains/{}".format(self.uri, domain_sid)
        return IpAccessControlListMappings(base_uri, self.auth, self.timeout)

    def credential_list_mappings(self, domain_sid):
        """
        Return a :class:`CredentialListMappings` instance for the
        :class:`SipDomain` with the given domain_sid
        """
        base_uri = "{}/Domains/{}".format(self.uri, domain_sid)
        return CredentialListMappings(base_uri, self.auth, self.timeout)

    def ip_addresses(self, ip_access_control_list_sid):
        """
        Return a :class:`IpAddresses` instance for the
        :class:`IpAccessControlList` with the given ip_access_control_list_sid
        """
        base_uri = "{}/IpAccessControlLists/{}".format(
            self.uri,
            ip_access_control_list_sid,
        )
        return IpAddresses(base_uri, self.auth, self.timeout)

    def credentials(self, credential_list_sid):
        """
        Return a :class:`Credentials` instance for the
        :class:`CredentialList` with the given credential_list_sid
        """
        base_uri = "{}/CredentialLists/{}".format(
            self.uri,
            credential_list_sid,
        )
        return Credentials(base_uri, self.auth, self.timeout)
