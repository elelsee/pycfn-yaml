import importlib
import yaml
import troposphere
from troposphere import Join, Output, GetAtt, Tags
from troposphere import Parameter, Ref, Template, Select

# Add constructors to handle cloudformation helpers in yaml


def ref_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return Ref(fields)


def join_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return Join(delimiter=fields[0], values=fields[1:])


def select_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return Select(fields[0], fields[1])


yaml.add_constructor('!Ref', ref_constructor)
yaml.add_constructor('!Join', join_constructor)
yaml.add_constructor('!Select', select_constructor)


class YamlParser(object):
    def __init__(self, template):
        super(YamlParser, self).__init__()
        self.template = yaml.load(template)
        self.parameters = self.template.get('Parameters')
        self.resources = self.template.get('Resources')
        self.outputs = self.template.get('Outputs')
        self.parsed = None

    def get_resource(self, resource):
        name = resource.keys()[0]
        resource_type = resource[name]['Type']
        kwargs = {}
        if 'Properties' in resource[name].keys():
            kwargs = resource[name].get('Properties')
        module, resource_class = resource_type.split('.')
        troposphere_module = importlib.import_module('.{}'.format(module), package='troposphere')
        r = getattr(troposphere_module, resource_class)
        return r(name, **kwargs)

    def get_output(self, output):
        name = output.keys()[0]
        value = output[name]['value']
        return Output(name, Value=value)

    def get_parameter(self, parameter):
        name = parameter.keys()[0]
        kwargs = parameter[name]
        return Parameter(name, **kwargs)

    def build_template(self):
        self.parsed = Template()
        resources = self.template.get('Resources')
        for resource in resources:
            self.parsed.add_resource(self.get_resource(resource))

        outputs = self.template.get('Outputs')
        for output in outputs:
            self.parsed.add_output(self.get_output(output))

        parameters = self.template.get('Parameters')
        for parameter in parameters:
            self.parsed.add_parameter(self.get_parameter(parameter))
