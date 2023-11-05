# dns_powerdns_bbr.py

# Copyright (c) 2023 BugbearR
# License: MIT

import json
import logging

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

import requests
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=120
        )
        add("credentials", help="PowerDNS credentials INI file.")

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the PowerDNS Remote REST API."
        )

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "PowerDNS credentials INI file",
            {
                "endpoint": "URL of the PowerDNS Remote REST API. (e.g. http://localhost:8081/)",
                "server_id": "ID of the PowerDNS server. (e.g. localhost)",
                "api_key": "API key for the PowerDNS Remote REST API."
            },
        )

    def _perform(self, domain, validation_name, validation):
        self._get_powerdns_client().add_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _cleanup(self, domain, validation_name, validation):
        self._get_powerdns_client().del_txt_record(
            domain, validation_name, validation, self.ttl
        )

    def _get_powerdns_client(self):
        return _PowerDNSClient(
            self.credentials.conf("endpoint"),
            self.credentials.conf("server_id"),
            self.credentials.conf("api_key")
        )

class _PowerDNSClient(object):
    def __init__(self, endpoint, server_id, api_key):
        logger.debug("creating PowerDNSClient")
        self.endpoint = endpoint
        self.server_id = server_id
        self.api_key = api_key
        self.zones = None

    def add_txt_record(self, domain, record_name, record_content, record_ttl):
        self._add_rr(record_name, 'TXT', f"\"{record_content}\"", record_ttl)

    def del_txt_record(self, domain, record_name, record_content, record_ttl):
        self._del_rr(record_name, 'TXT', f"\"{record_content}\"", record_ttl)

    def _get_zones_zone_id_url(self, domain):
        logger.debug(f"_get_zones_zone_id_url('{domain}')")
        zone_id = self._find_zone_id(self._get_zones_cache(), domain)
        url = urljoin(self.endpoint, f'api/v1/servers/{self.server_id}/zones/{zone_id}')
        logger.debug(f"return '{url}'")
        return url

    def _find_zone_id(self, zones, domain):
        logger.debug(f"_find_zone_id(zones, '{domain}')")
        domain_lower = domain.lower()
        if not domain_lower.endswith('.'):
            domain_lower += '.'
        condition = lambda record: domain_lower == record['name'].lower()
        matching_zone = next(filter(condition, zones), None)
        if matching_zone == None:
            matching_zones = [zone for zone in zones if domain_lower.endswith('.' + zone['name'].lower())]
            if (len(matching_zones) == 0):
                raise errors.PluginError("Domain not known")

            matching_zone = max(matching_zones, key=lambda zone: len(zone['name']), default=None)
        logger.debug(f"zone_id found. zone_id:{matching_zone['id']} domain:{domain}")
        return matching_zone['name']

    def _get_zones_cache(self):
        if self.zones == None:
            self.zones = self._get_zones()
        return self.zones

    def _get_zones(self):
        logger.debug(f"_get_zones()")
        url = urljoin(self.endpoint, f'api/v1/servers/{self.server_id}/zones')
        response = self._call_api('GET', url)
        zones = self._parse_response_json(response)
        return zones

    def _add_rr(self, name, type, content, ttl):
        logger.debug(f"_add_rr('{name}', '{type}', '{content}', {ttl})")
        rrsets = self._search_data(name, 100, 'record')
        type_rrsets = self._find_type_from_rrsets(rrsets, type)
        logger.debug(f"type_rrsets:\n{json.dumps(type_rrsets)}")
        content_rrsets = self._find_content_from_rrsets(type_rrsets, content)
        if (len(content_rrsets) > 0):
            print("content is already exsits.")
            return
        type_rrsets.insert(0, {
            'name': name,
            'type': type,
            'content': content,
            'ttl': ttl
        })
        self._replace_rrsets(type_rrsets)

    def _del_rr(self, name, type, content, ttl):
        logger.debug(f"_del_rr('{name}', '{type}', '{content}', {ttl})")
        rrsets = self._search_data(name, 100, 'record')
        if (len(rrsets) == 0):
            print("content is already deleted. no rrsets found.")
            return
        type_rrsets = self._find_type_from_rrsets(rrsets, type)
        logger.debug(f"type_rrsets:\n{json.dumps(rrsets)}")
        if (len(type_rrsets) == 0):
            print("content is already deleted. no type_rrsets found.")
            return
        logger.debug(f"type_rrsets:{json.dumps(type_rrsets)}")
        content_rrsets = self._find_content_from_rrsets(type_rrsets, content)
        if (len(content_rrsets) == 0):
            print("content is already deleted. no content_rrsets found.")
            return
        if (len(type_rrsets) == 1):
            print("delete all rrsets.")
            self._del_rrsets(name, type)
            return
        print("delete target rr.")
        remain_rrsets = self._remove_content_from_rrsets(type_rrsets, content)
        self._replace_rrsets(remain_rrsets)

    def _replace_rrsets(self, rrsets):
        logger.debug(f"_replace_rrsets(rrsets)")
        logger.debug(f"rrsets:\n{json.dumps(rrsets)}")
        name = rrsets[0]['name']
        if not name.endswith('.'):
            name += '.'
        data = {
            'rrsets': [
                {
                    'name': name,
                    'type': rrsets[0]['type'],
                    'ttl': rrsets[0]['ttl'],
                    'changetype': 'REPLACE',
                    'records': []
                }
            ]
        }

        for rrset in rrsets:
            data['rrsets'][0]['records'].append({
                'content': rrset['content'],
                'disabled': False
            })

        zone_id = self._find_zone_id(self._get_zones_cache(), rrsets[0]['name'])
        url = urljoin(self.endpoint, f'api/v1/servers/{self.server_id}/zones/{zone_id}')
        self._call_api('PATCH', url, data)

    def _del_rrsets(self, name, type):
        logger.debug(f"_del_rrsets('{name}', '{type}')")
        url = self._get_zones_zone_id_url(name)
        if not name.endswith('.'):
            name += '.'
        data = {
            'rrsets': [
                {
                    'name': name,
                    'type': type,
                    'changetype': 'DELETE'
                }
            ]
        }
        self._call_api('PATCH', url, data)

    def _remove_content_from_rrsets(self, rrsets, content):
        logger.debug(f"_remove_content_from_rrsets(rrsets, '{content}')")
        matching_rrsets = [record for record in rrsets if content != record['content']]
        return matching_rrsets

    def _find_content_from_rrsets(self, rrsets, content):
        logger.debug(f"_find_content_from_rrsets(rrsets)")
        matching_rrsets = [record for record in rrsets if content == record['content']]
        return matching_rrsets

    def _find_type_from_rrsets(self, rrsets, type):
        logger.debug(f"_find_type_from_rrsets(rrsets, '{type}')")
        matching_rrsets = [record for record in rrsets if type == record['type']]
        return matching_rrsets

    def _search_data(self, q, max, object_type):
        logger.debug(f"_search_data('{q}', {max}, '{object_type}')")
        if q.endswith('.'):
            q = q[:-1]
        url = urljoin(self.endpoint, f'api/v1/servers/{self.server_id}/search-data?q={q}&max={max}&object_type={object_type}')
        logger.debug(f"url: {url}")
        response = self._call_api('GET', url)
        if str(response.status_code)[0] != '2':
            msg = f"HTTP Error during search data. status_code:{response.status_code} q:{q} max:{max} object_type:{object_type}"
            logger.error(msg)
            raise errors.PluginError(msg)

        return self._parse_response_json(response)

    def _parse_response_json(self, response):
        logger.debug(f"_parse_response_json(response)")
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            msg = "Error decoding JSON response."
            logger.info(f"response.text: {response.text}")
            logger.error(msg)
            raise errors.PluginError(msg)

        logger.debug(f"return: {json.dumps(data) if data != None else 'None'}")
        return data

    def _call_api(self, method, url, data=None):
        logger.debug(f"_call_api('{method}', '{url}', data)")
        logger.debug(f"data: {json.dumps(data) if data != None else 'None'}")
        headers = {
            'X-API-Key': self.api_key
        }

        text_data = None
        if data != None:
            headers['Content-Type'] = 'application/json'
            text_data = json.dumps(data)

        response = requests.request(method, url, data=text_data, headers=headers)
        if str(response.status_code)[0] != '2':
            msg = f"API Error. method:{method} url:{url} status_code:{response.status_code}"
            logger.error(msg)
            logger.info(f"headers: {json.dumps(headers)}")
            if data != None:
                logger.info(f"data: {json.dumps(data, indent=4)}")
            logger.info(f"response.text: {response.text}")
            raise errors.PluginError(msg)

        return response
