# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from util.models import BaseModel
from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from physical.models import Environment
import logging
import simple_audit
from django_extensions.db.fields.encrypted import EncryptedCharField

CACHE_MISS = object()

LOG = logging.getLogger(__name__)

class CredentialType(BaseModel):
    CLOUDSTACK = 1
    NFSAAS = 2
    DBMONITOR = 3
    ZABBIX = 4
    FLIPPER = 5
    VM = 6
    MYSQL = 7
    MONGODB = 8
    DNSAPI = 9
    ACLAPI= 10
    LAAS = 11
    LOGNIT = 12
    NETWORKAPI = 13
    GRAPHITE = 14
    STATSD = 15
    REDIS = 16

    INTEGRATION_CHOICES = (
        (CLOUDSTACK, 'Cloud Stack'),
        (NFSAAS, 'NFS as a Service'),
        (DBMONITOR, 'Database Monitor'),
        (ZABBIX, 'Zabbix'),
        (FLIPPER, 'Flipper'),
        (VM, 'Virtual machine credentials'),
        (MYSQL, 'MySQL credentials'),
        (MONGODB, 'MongoDB credentials'),
        (DNSAPI, 'DNS API'),
        (ACLAPI, 'ACL API'),
        (LAAS, 'Log as a Service'),
        (LOGNIT, 'Lognit'),
        (NETWORKAPI, 'Network API'),
        (GRAPHITE, 'Graphite'),
        (STATSD, 'Statsd'),
        (REDIS, 'Redis credentials'),
    )
    name = models.CharField(verbose_name=_("Name"),
                                         max_length=100,
                                         help_text="Integration Name")
    type = models.IntegerField(choices=INTEGRATION_CHOICES,
                                default=0)

    class Meta:
        permissions = (
            ("view_integrationtype", "Can view integration type."),
        )


class Credential(BaseModel):

    user = models.CharField(verbose_name=_("User"),
                            max_length=100,
                            help_text=_("User used to authenticate."),
                            blank=True,
                            null=True)
    password = EncryptedCharField(verbose_name=_("Password"), max_length=255, blank=True, null=True)
    integration_type = models.ForeignKey(CredentialType, related_name="integration_type", on_delete=models.PROTECT)
    token = models.CharField(verbose_name=_("Authentication Token"),
                            max_length=255,
                            blank=True,
                            null=True)
    secret = EncryptedCharField(verbose_name=_("Secret"), max_length=255, blank=True, null=False)
    endpoint = models.CharField(verbose_name=_("Endpoint"),
                            max_length=255,
                            help_text=_("Usually it is in the form host:port. Authentication endpoint."),
                            blank=False,
                            null=False)
    environments = models.ManyToManyField(Environment)
    project = models.CharField(verbose_name=_("Project"),
                            max_length=255,
                            blank=True,
                            null=True)
    team = models.CharField(verbose_name=_("Team"),
                            max_length=255,
                            blank=True,
                            null=True,
                            default=None)

    def __unicode__(self):
        return "%s" % (self.id)

    def environment(self):
        return ', '.join([e.name for e in self.environments.all()])

    class Meta:
        permissions = (
            ("view_integrationcredential", "Can view integration credential."),
        )

    def get_parameter_by_name(self, name):
        try:
            value = Parameter.objects.get(credential=self, name=name).value
            LOG.debug("Parameter '%s': '%s'", name, value)
            return value
        except Parameter.DoesNotExist:
            LOG.warning("Parameter %s not found" % name)
            return None
        except Exception, e:
            LOG.warning("ops.. could not retrieve parameter value for %s: %s" % (name, e))
            return None



class Parameter(BaseModel):

    name = models.CharField(verbose_name=_("Parameter name"), max_length=100)
    value = models.CharField(verbose_name=_("Parameter value"), max_length=255)
    description = models.CharField(verbose_name=_("Description"), max_length=255, null=True, blank=True)
    credential = models.ForeignKey(Credential, related_name="credential_parameters")

    class Meta:
    	unique_together = (
    		('credential', 'name'),
    	)

simple_audit.register(Credential, CredentialType, Parameter)
