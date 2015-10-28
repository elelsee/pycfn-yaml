import importlib
import troposphere
import constructors


class YamlParser(object):
    def __init__(self, template):
        super(YamlParser, self).__init__()
        self._template = template.read()
        self.template = constructors.yaml.load(self._template)
        self.description = self.template.get('Description')
        self.metadata = self.template.get('Metadata')
        self.mappings = self.template.get('Mappings')
        self.parameters = self.template.get('Parameters')
        self.resources = self.template.get('Resources')
        self.outputs = self.template.get('Outputs')
        self.conditions = self.template.get('Conditions')
        self.parsed = None
        self.build_template()

    def get_mapping(self, mapping):
        name = mapping.keys()[0]
        value = mapping[name]
        return name, value

    def get_parameter(self, parameter):
        name = parameter.keys()[0]
        kwargs = parameter[name]
        return troposphere.Parameter(name, **kwargs)

    def get_condition(self, condition):
        name = condition.keys()[0]
        value = condition[name]
        return name, value

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

    def get_output(self, output):
        name = output.keys()[0]
        value = output[name]['value']
        return troposphere.Output(name, Value=value)

    def append_tags(self, tags, append_tags):
        for tag in append_tags.tags:
            tags.tags.append(tag)
        return tags

    def add_global_tags(self):
        global_tags = self.metadata.get('GlobalTags')
        resources = self.parsed.resources
        if global_tags:
            for i in resources:
                if 'Tags' in resources[i].props:
                    if 'Tags' in resources[i].properties:
                        current_tags = resources[i].properties['Tags']
                        resources[i].properties['Tags'] = self.append_tags(current_tags, global_tags)
                    else:
                        resources[i].properties['Tags'] = global_tags
        return 

    def build_template(self):
        self.parsed = troposphere.Template()
        self.parsed.add_version()

        description = self.description
        self.parsed.add_description(description)

        metadata = self.metadata
        self.parsed.add_metadata(metadata)

        mappings = self.mappings
        if mappings:
            for mapping in mappings:
                self.parsed.add_mapping(*self.get_mapping(mapping))

        parameters = self.parameters
        if parameters:
            for parameter in parameters:
                self.parsed.add_parameter(self.get_parameter(parameter))

        conditions = self.conditions
        if conditions:
            for condition in conditions:
                self.parsed.add_condition(*self.get_condition(condition))

        resources = self.resources
        if resources:
            for resource in resources:
                self.parsed.add_resource(self.get_resource(resource))

        outputs = self.outputs
        if outputs:
            for output in outputs:
                self.parsed.add_output(self.get_output(output))

        self.add_global_tags()
