import yaml
import troposphere


def and_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.And(*fields)

yaml.add_constructor('!And', and_constructor)


def equals_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Equals(*fields)

yaml.add_constructor('!Equals', equals_constructor)


def if_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.If(*fields)

yaml.add_constructor('!If', if_constructor)


def not_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Not(*fields)

yaml.add_constructor('!Not', not_constructor)


def or_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Or(*fields)

yaml.add_constructor('!Or', or_constructor)


def ref_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return troposphere.Ref(fields)

yaml.add_constructor('!Ref', ref_constructor)


def join_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Join(delimiter=fields[0], values=fields[1:])

yaml.add_constructor('!Join', join_constructor)


def select_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.Select(*fields)

yaml.add_constructor('!Select', select_constructor)


def condition_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return troposphere.Condition(fields)

yaml.add_constructor('!Condition', condition_constructor)


def base64_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return troposphere.Base64(fields)

yaml.add_constructor('!Base64', base64_constructor)


def findinmap_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.FindInMap(*fields)

yaml.add_constructor('!FindInMap', findinmap_constructor)


def getatt_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return troposphere.GetAtt(*fields)

yaml.add_constructor('!GetAtt', getatt_constructor)


def getazs_constructor(loader, node):
    fields = loader.construct_scalar(node)
    return troposphere.GetAZs(fields)

yaml.add_constructor('!GetAZs', getazs_constructor)
yaml.add_constructor('!GetAzs', getazs_constructor)


def tags_constructor(loader, node):
    fields = loader.construct_mapping(node)
    return troposphere.Tags(**fields)

yaml.add_constructor('!Tags', tags_constructor)


def accountid_constructor(loader, node):
    return troposphere.Ref(troposphere.AWS_ACCOUNT_ID)

yaml.add_constructor('!AccountId', accountid_constructor)
yaml.add_constructor('!AccountId', accountid_constructor)


def notification_constructor(loader, node):
    return troposphere.Ref(troposphere.AWS_NOTIFICATION_ARNS)

yaml.add_constructor('!NotificationARNs', notification_constructor)
yaml.add_constructor('!NotificationArns', notification_constructor)


def noval_constructor(loader, node):
    return troposphere.Ref(troposphere.AWS_NO_VALUE)

yaml.add_constructor('!NoValue', noval_constructor)


def region_constructor(loader, node):
    return troposphere.Ref(troposphere.AWS_REGION)

yaml.add_constructor('!Region', region_constructor)


def stackid_constructor(loader, node):
    return troposphere.Ref(troposphere.AWS_STACK_ID)

yaml.add_constructor('!StackId', stackid_constructor)


def stackname_constructor(loader, node):
    return troposphere.Ref(troposphere.AWS_STACK_NAME)

yaml.add_constructor('!StackName', stackname_constructor)

