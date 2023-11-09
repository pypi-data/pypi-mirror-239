"""
Simple library for creating pythonic way of accessing AAP objects

based on:
https://docs.ansible.com/ansible-tower/latest/html/towerapi/api_ref.html#/Jobs/Jobs_jobs_job_events_list
"""

from .endpoints import *
from .base import APIError
from .base import API
