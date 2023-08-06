#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zabbix_api import ZabbixAPI
from physical.models import DatabaseInfra
import logging

LOG = logging.getLogger(__name__)

class ZabbixProvider(object):

    @classmethod
    def get_credentials(self, environment):
        LOG.info("Getting credentials...")
        from dbaas_credentials.credential import Credential
        from dbaas_credentials.models import CredentialType
        integration = CredentialType.objects.get(type= CredentialType.ZABBIX)
        return Credential.get_credentials(environment= environment, integration= integration)

    @classmethod
    def auth(self, dbinfra):
        credentials = self.get_credentials(environment = dbinfra.environment)

        zapi = ZabbixAPI(server=credentials.endpoint, path="", log_level=6, timeout=60)
        zapi.login(credentials.user, credentials.password)
        return zapi

    @classmethod
    def create_monitoring(self, dbinfra, dbtype="mysql"):
        if isinstance(dbinfra, DatabaseInfra):
            zapi = self.auth(dbinfra=dbinfra)
            LOG.info("Creating zabbix monitoring for hosts...")
            self.create_basic_monitors(zapi= zapi, dbinfra=dbinfra)

            LOG.info("Creating zabbix monitoring for database...")
            if dbtype == "redis":
                self.create_db_monitors_redis(zapi= zapi, dbinfra=dbinfra, dbtype=dbtype)
            else:
                self.create_db_monitors(zapi= zapi, dbinfra=dbinfra, dbtype=dbtype)

    @classmethod
    def destroy_monitoring(self, dbinfra, dbtype="mysql"):
        if isinstance(dbinfra, DatabaseInfra):
            LOG.info("Destroying zabbix monitoring...")
            zapi = self.auth(dbinfra=dbinfra)

            self.destroy_basic_monitors(zapi= zapi, dbinfra= dbinfra)
            if dbtype == "redis":
                self.destroy_db_monitors_redis(zapi= zapi, dbinfra= dbinfra)
            else:
                self.destroy_db_monitors(zapi= zapi, dbinfra= dbinfra)

            for attrs in dbinfra.cs_dbinfra_attributes.all():
                self.destroy_flipper_db_monitors(zapi= zapi, host=attrs.dns)

    @classmethod
    def destroy_db_monitors(self, zapi, dbinfra):
        instances = dbinfra.instances.all()
        for instance in instances:
            LOG.info("Destroying instance %s" % instance)
            zapi.globo.deleteMonitors({"host":instance.dns,})

    @classmethod
    def destroy_db_monitors_redis(self, zapi, dbinfra):
        instances = dbinfra.instances.all()
        for instance in instances:
            LOG.info("Destroying instance %s" % instance)
            zapi.globo.deleteMonitors({"host": "webmonitor_%s-80-redis-mem" % instance.address })
            zapi.globo.deleteMonitors({"host": "webmonitor_%s-80-redis-con" % instance.address})

    @classmethod
    def destroy_flipper_db_monitors(self, zapi, host):
        LOG.info("Destroying host %s" % host)
        zapi.globo.deleteMonitors({"host": host,})

    @classmethod
    def destroy_basic_monitors(self, zapi, dbinfra):
        instances = dbinfra.instances.all()
        for instance in instances:
            host = instance.hostname
            LOG.info("Destroying host %s" % host)
            zapi.globo.deleteMonitors({"host":host.hostname,})
    
    @classmethod
    def create_db_monitors(self, zapi, dbinfra, dbtype):        
        instances = dbinfra.instances.all()
        flipper = 0
        for instance in instances:
            LOG.info("Monitoring %s db instance %s" % (dbtype, instance))

            if instance.is_arbiter:
                arbiter = 1
            else:
                arbiter = 0

            params = {"host" : instance.dns, "dbtype" : dbtype, "alarm" : "yes", "arbiter":arbiter}

            if instances.count() > 1 and dbtype=="mysql":
                params['healthcheck'] = {
                    'host' : instance.dns,
                    'port' : '80',
                    'string' : 'WORKING',
                    'uri' : 'health-check/'
                }
                params['healthcheck_monitor'] = {
                    'host' : instance.dns,
                    'port' : '80',
                    'string' : 'WORKING',
                    'uri' : 'health-check/monitor/'
                }
                zapi.globo.createDBMonitors(params)

                if flipper == 0 and dbtype=="mysql":
                    LOG.info("Creating zabbix monitoring for flipper ips...")
                    self.create_flipper_db_monitors(zapi= zapi, dbinfra=dbinfra)
                    flipper=1
            else:
                zapi.globo.createDBMonitors(params)

    @classmethod
    def create_db_monitors_redis(self, zapi, dbinfra, dbtype):
        instances = dbinfra.instances.all()
        for instance in instances:
            params = {
                "address" : instance.address,
                "port" : "80",
                "regexp" : "WORKING",
                "uri": "/health-check/redis-con/",
                "var": "redis-con",
                "alarm" : "yes",
                "notes": dbinfra.name,
            }
            zapi.globo.createWebMonitors(params)
            
            params = {
                "address" : instance.address,
                "port" : "80",
                "regexp" : "WORKING",
                "uri": "/health-check/redis-mem/",
                "var": "redis-mem",
                "alarm" : "yes",
                "notes": dbinfra.name,
            }
            zapi.globo.createWebMonitors(params)

    @classmethod
    def create_basic_monitors(self, zapi, dbinfra):
        for instance in dbinfra.instances.all():
            LOG.info("Monitoring instances %s" % instance)
            host = instance.hostname
            zapi.globo.createBasicMonitors({"host": host.hostname, "ip": host.address})

    @classmethod
    def create_flipper_db_monitors(self, zapi, dbinfra):
        for instance in dbinfra.cs_dbinfra_attributes.all():
            LOG.info("Monitoring flipper ip instance %s" % instance)
            params = {"host" : instance.dns, "dbtype" : "mysql", "alarm" : "yes"}
            zapi.globo.createDBMonitors(params)

