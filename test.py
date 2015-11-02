from pycfn_yaml import parser
y = open("examples/vpc.yaml")
p = parser.YamlParser(y)
print p.parsed.to_json()
