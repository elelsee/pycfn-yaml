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

    def get_resource(resource):
        r_name = resource.keys()[0]
        r_type = resource[r_name]['Type']
        kwargs = {}
        if 'properties' in resource[r_name].keys():
            kwargs = resource[r_name]['Properties']
        r_module, r_class = r_type.split('.')
        r = getattr(globals()[r_module], r_class)
        return r(r_name, **kwargs)

    def get_output(output):
        name = output.keys()[0]
        value = output[name]['value']
        return Output(name, Value=value)

    def get_parameter(parameter):
        name = parameter.keys()[0]
        kwargs = parameter[name]
        return Parameter(name, **kwargs)

    def build_template(self):
        self.parsed = Template()
        with self.template.get('Resources') as resources:
            for resource in resources:
                self.parsed.add_resource(get_resource(resource))

        with self.template.get('Outputs') as outputs:
            for output in outputs:
                self.parsed.add_output(get_output(output))

        with self.template.get('Parameters') as parameters:
            for parameter in parameters:
                self.parsed.add_parameter(get_parameter(parameter))
