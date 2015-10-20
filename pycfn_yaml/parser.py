import importlib
import yaml
import troposphere

# Add constructors to handle cloudformation helpers in yaml


def and_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.And(*fields)


def equals_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Equals(*fields)


def if_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.If(*fields)


def not_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Not(*fields)


def or_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Or(*fields)


def ref_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return troposphere.Ref(fields)


def join_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Join(delimiter=fields[0], values=fields[1:])


def select_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Select(*fields)


def condition_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return troposphere.Condition(fields)


def base64_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return troposphere.Base64(fields)


def findinmap_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.FindInMap(*fields)


def getatt_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.GetAtt(*fields)


yaml.add_constructor('!Ref', ref_constructor)
yaml.add_constructor('!Join', join_constructor)
yaml.add_constructor('!Select', select_constructor)
yaml.add_constructor('!And', and_constructor)
yaml.add_constructor('!Equals', equals_constructor)
yaml.add_constructor('!If', if_constructor)
yaml.add_constructor('!Not', not_constructor)
yaml.add_constructor('!Or', or_constructor)
yaml.add_constructor('!Condition', condition_constructor)
yaml.add_constructor('!Base64', base64_constructor)
yaml.add_constructor('!FindInMap', findinmap_constructor)
yaml.add_constructor('!GetAtt', getatt_constructor)


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
        kwargs = resource[name]
        resource_type = kwargs.pop('Type')
        properties = None
        if 'Properties' in kwargs:
            properties = kwargs.pop('Properties')
            kwargs.update(properties)
        module, resource_class = resource_type.split('.')
        troposphere_module = importlib.import_module('.{}'.format(module),
                                                     package='troposphere')
        r = getattr(troposphere_module, resource_class)
        return r(name, **kwargs)

    def get_condition(self, condition):
        name = condition.keys()[0]
        value = condition[name]
        return name, value

    def get_output(self, output):
        name = output.keys()[0]
        value = output[name]['value']
        return troposphere.Output(name, Value=value)

    def get_parameter(self, parameter):
        name = parameter.keys()[0]
        kwargs = parameter[name]
        return troposphere.Parameter(name, **kwargs)

    def build_template(self):
        self.parsed = troposphere.Template()

        resources = self.template.get('Resources')
        if resources:
            for resource in resources:
                self.parsed.add_resource(self.get_resource(resource))

        outputs = self.template.get('Outputs')
        if outputs:
            for output in outputs:
                self.parsed.add_output(self.get_output(output))

        parameters = self.template.get('Parameters')
        if parameters:
            for parameter in parameters:
                self.parsed.add_parameter(self.get_parameter(parameter))

        conditions = self.template.get('Conditions')
        if conditions:
            for condition in conditions:
                self.parsed.add_condition(*self.get_condition(condition))
