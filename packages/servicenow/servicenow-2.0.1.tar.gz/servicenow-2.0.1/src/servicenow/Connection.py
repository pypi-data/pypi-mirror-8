import requests
import logging
import json

from servicenow import Utils

class Auth(object):

    def __init__(self, username, password, instance, timeout=60, debug=False, api='JSON'):
        self.username = username
        self.password = password
        if 'https://' in instance:
            self.instance = instance
        else:
            self.instance = 'https://%s.service-now.com/' % instance
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.api = api

    def _list(self, table, meta={}, **kwargs):
        query = Utils.format_query(meta, kwargs.get('metaon', {}))
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'getKeys',
            'sysparm_query': query
        })
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _list_by_query(self, table, query, **kwargs):
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'getKeys',
            'sysparm_query':    query
        })
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _get(self, table, meta={}, **kwargs):
        query = Utils.format_query(meta, kwargs.get('metaon', {}))
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'getRecords',
            'sysparm_query': query
        })
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _get_by_query(self, table, query, **kwargs):
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'getRecords',
            'sysparm_query': query
        })
        return self.session.get('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _post(self, table, data, **kwargs):
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'insert'
        })
        return self.session.post('%s/%s' % (self.instance, table), params=params, data=json.dumps(data), timeout=self.timeout)

    def _update(self, table, where, data, **kwargs):
        query = Utils.format_query(where, {})
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'update',
            'sysparm_query':    query
        })
        return self.session.post('%s/%s' % (self.instance, table), params=params, data=json.dumps(data), timeout=self.timeout)

    def _update_by_query(self, table, query, data, **kwargs):
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'update',
            'sysparm_query':    query
        })
        return self.session.post('%s/%s' % (self.instance, table), params=params, data=json.dumps(data), timeout=self.timeout)

    def _delete(self, table, id, **kwargs):
        params = kwargs.get('params', {})
        params.update({
            self.api:             '',
            'sysparm_action':   'deleteRecord',
            'sysparm_sys_id':    id
        })
        return self.session.post('%s/%s' % (self.instance, table), params=params, timeout=self.timeout)

    def _format(self, response):
        return json.loads(response.text)
