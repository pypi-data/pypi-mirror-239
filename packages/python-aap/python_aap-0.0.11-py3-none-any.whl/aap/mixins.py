import time
from .base import APIObject


class WaitableMixin:
    _states = {
        'successful': True,
        'failed': False,
        'canceled': False,
        'error': False,
        'never_updated': False
    }

    @property
    def is_running(self):
        return self.status == "running"

    @property
    def is_finished(self):
        return self.status in self._states

    @property
    def is_successfull(self):
        return self._states.get(self.status)

    def wait(self, timeout=None, poll=1):
        started = time.time()
        while not self.is_finished:
            if timeout and time.time() - started > timeout:
                break
            time.sleep(poll)
            self._reload()
        return self._states.get(self.status)


class LaunchableMixin:
    _schedule_class = None

    def launch(self, extra_vars={}, limit=[], tags=[], **kwargs):
        data = {'extra_vars': extra_vars}
        data.update(kwargs)
        if limit:
            data['limit'] = ','.join(limit)
        if tags:
            data['job_tags'] = ','.join(tags)
        result = self.api.request(
            'POST', self._path + f"{self.id}/launch/", data)
        return APIObject.load_url(result['url'], self.api)

    def schedule(self, name, rrule, **kwargs):
        """
        Schedule launch
        required:
         name: Name of this schedule. (string, required)
         rrule: A value representing the schedules iCal recurrence rule. (string, required)
        optional:
         job_tags: list
         extra_vars: dict
         limit: list/str
        """
        if type(kwargs.get('limit')) == list:
            kwargs['limit'] = ",".join(kwargs['limit'])

        if type(kwargs.get('job_tags')) == list:
            kwargs['job_tags'] = ",".join(kwargs['job_tags'])

        kwargs['name'] = name
        kwargs['rrule'] = rrule
        response = self.api.request(
            "POST", self._path + f"{self.id}/schedules/", kwargs)
        return self._schedule_class(response, self.api)
