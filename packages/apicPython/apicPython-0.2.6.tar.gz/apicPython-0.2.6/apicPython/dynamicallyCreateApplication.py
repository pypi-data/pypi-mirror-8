from labScript import *
from cobra.model.fv import AEPg

# TODO from apicPython
from apicPython import createTenant
from apicPython import addSecurityDomain
from apicPython import createPrivateNetwork
from apicPython import createBridgeDomain
from apicPython import createFilter
from apicPython import createContract
from apicPython import createApplication
from apicPython import createApplicationEpg
from apicPython import connectEpgContract


class DynamicallyCreateApplication(LabScript):

    def __init__(self):
        self.description = 'This script helps you to create an application from zero'
        self.tenant_required = True
        self.security_domains = []
        self.private_network = None
        self.bridge_domains = []
        self.filters = []
        self.contracts = []
        self.application_optional_args = None
        self.epgs = []
        self.applied_contracts = []
        super(DynamicallyCreateApplication, self).__init__()

    def run_yaml_mode(self):
        super(DynamicallyCreateApplication, self).run_yaml_mode()
        self.security_domains = self.args['security_domains']
        self.private_network = self.args['private_network']
        self.bridge_domains = self.args['bridge_domains']
        self.filters = self.args['filters']
        self.contracts = self.args['contracts']
        self.application = self.args['application']['name']
        self.application_optional_args = self.args['application']['optional_args']
        self.epgs = self.args['epgs']
        self.applied_contracts = self.args['applied_contracts']

    def run_wizard_mode(self):
        print 'Wizard mode is not supported in this method. Please try Yaml mode.'
        sys.exit()

    def main_function(self):
        fv_tenant = self.check_if_tenant_exist(return_boolean=True)
        # if not fv_tenant:
        #     # create a tenant
        #     self.mo = self.modir.lookupByDn('uni')
        #     fv_tenant = createTenant.create_tenant(self.mo, self.tenant)
        #     self.commit_change(changed_object=fv_tenant)
        #
        # # add security domains
        # for security_domain in self.security_domains:
        #     addSecurityDomain.add_security_domain(fv_tenant, security_domain)
        #
        # # create private network
        # createPrivateNetwork.create_private_network(fv_tenant, self.private_network)
        #
        # # create bridge domains
        # for bridge_domain in self.bridge_domains:
        #     createBridgeDomain.createBridgeDomain(fv_tenant, bridge_domain['name'], bridge_domain['subnet_ip'], self.private_network)
        #
        # create filters
        # for filter in self.filters:
        #     createFilter.create_filter(fv_tenant, filter['name'], optional_args=return_valid_optional_args(filter))
        #
        # # create contracts
        for contract in self.contracts:
            print '====', type(contract)
            createContract.create_contract(fv_tenant, contract['name'], optional_args=contract['optional_args'])
        #
        # # create application
        # fv_ap = createApplication.create_application(fv_tenant, self.application, optional_args=self.application_optional_args)
        #
        # # create EPGs
        # for epg in self.epgs:
        #     createApplicationEpg.create_application_epg(fv_ap, epg['name'], optional_args=epg['optional_args'])
        # self.commit_change(changed_object=fv_tenant)
        #
        # # build n-tier application
        # for contract in self.applied_contracts:
        #     fv_aepg = self.check_if_mo_exist('uni/tn-' + self.tenant + '/ap-' + self.application + '/epg-', contract['epg'], AEPg, description='Application EPG')
        #     connectEpgContract.connect_epg_contract(fv_aepg, contract['contract'], contract['type'])
        #     self.commit_change(changed_object=fv_aepg)

if __name__ == '__main__':
    mo = DynamicallyCreateApplication()
