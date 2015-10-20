from pycfn_yaml import parser
y = open("examples/test.yaml")
p = parser.YamlParser(y)
p.build_template()
print p.parsed.to_json()
