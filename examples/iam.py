from troposphere.cloudformation import AWSCustomObject
from awacs.aws import Policy
from pycfn_yaml.parser import YamlParser

policytypes = (dict, Policy)


class ElasticsearchDomain(AWSCustomObject):
    resource_type = "Custom::ElasticsearchDomain"

    props = {
        'ServiceToken': (basestring, True),
        'DomainName': (basestring, True),
        'ElasticsearchClusterConfig': (dict, False),
        'EBSOptions': (dict, False),
        'AccessPolicies': (policytypes, False),
        'SnapshotOptions': (dict, False),
        'AdvancedOptions': (dict, False)
    }


class CustomParser(YamlParser):
    def custom_resource(self, custom_resource):
        return ElasticsearchDomain

if __name__ == '__main__':
    f = open('iam.yaml')
    p = CustomParser(f)
    print p.parsed.to_json()
