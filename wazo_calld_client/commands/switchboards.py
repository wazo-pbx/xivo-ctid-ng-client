# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..command import CalldCommand


class SwitchboardsCommand(CalldCommand):

    resource = 'switchboards'
    headers = {'Accept': 'application/json'}

    def list_queued_calls(self, switchboard_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, switchboard_uuid, 'calls', 'queued')
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def answer_queued_call_from_user(self, switchboard_uuid, call_id, line_id=None):
        url = self._client.url(
            self.resource, switchboard_uuid, 'calls', 'queued', call_id, 'answer'
        )
        params = {'line_id': line_id} if line_id else None
        r = self.session.put(url, params=params)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def hold_call(self, switchboard_uuid, call_id, tenant_uuid=None):
        headers = self._get_headers(accept=False, tenant_uuid=tenant_uuid)
        url = self._client.url(
            self.resource, switchboard_uuid, 'calls', 'held', call_id
        )
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def list_held_calls(self, switchboard_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url(self.resource, switchboard_uuid, 'calls', 'held')
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def answer_held_call_from_user(self, switchboard_uuid, call_id, line_id=None):
        url = self._client.url(
            self.resource, switchboard_uuid, 'calls', 'held', call_id, 'answer'
        )
        params = {'line_id': line_id} if line_id else None
        r = self.session.put(url, params=params)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def _get_headers(self, accept=True, **kwargs):
        headers = dict(self.headers) if accept else {}
        tenant_uuid = kwargs.pop('tenant_uuid', self._client.tenant())
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid
        return headers
