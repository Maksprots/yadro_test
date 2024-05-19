from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json

from exceptions import generator as eg
from const.consts import Constants as cs


class Generator(object):
    def __init__(self, xml_path):
        self.aggregations = defaultdict(list)
        try:
            tree = ET.parse(xml_path)
            self.tree = tree.getroot()
        except FileNotFoundError:
            raise eg.XmlFileError
        except ET.ParseError:
            raise eg.ParserError
        self.roots = []
        self.verticals = {}
        self.multiplicity = {}

    def _dfs(self, graph, start, visited=None, parent=None):
        if visited is None:
            visited = set()
        visited.add(start)

        if start != parent.tag:
            element = ET.SubElement(parent, start)
            # paste sub trees
            for i in self.verticals[start].iter('Attribute'):
                atr = ET.SubElement(element, i.attrib['name'])
                atr.text = i.attrib['type']
            next_parent = element
        else:
            next_parent = parent
        for next in graph[start]:
            if next not in visited:
                self._dfs(graph, next, visited, next_parent)
        return visited

    def parse_file(self):
        try:
            aggregations = self.tree.findall('Aggregation')
            self.roots = self.tree.findall(cs.root_path_expression)
            verticals = self.tree.findall('Class')
            for ag in aggregations:
                self.aggregations[ag.attrib['target']].append(ag.attrib['source'])
        except KeyError:
            raise eg.ParserError('No aggregation or aggregation is not correct')

        self.verticals = {i.attrib['name']: i for i in verticals}

        # parse add data for metafile
        for ag in aggregations:
            self.multiplicity[ag.attrib['source']] = ag.attrib['sourceMultiplicity']

        if len(self.roots) > 1:
            raise eg.ParserError('To many roots')

    def generate_xml(self, path):
        root_name = self.roots[0].attrib['name']
        base_element = ET.Element(root_name)
        for i in self.verticals[root_name].iter('Attribute'):
            atr = ET.SubElement(base_element, i.attrib['name'])
            atr.text = i.attrib['type']

        self._dfs(
            self.aggregations,
            root_name,
            None,
            base_element
        )
        #  make indents for best view
        string_to_file = minidom.parseString(
            ET.tostring(base_element)
        ).childNodes[0].toprettyxml(indent="   ")

        with open(path, 'w') as f:
            f.write(string_to_file)

    def generate_json(self, path):
        elements = []
        for element in self.verticals.values():
            data = element.attrib
            # if we have min and max attributs
            if self.multiplicity.get(element.attrib['name'], 0):
                max_min = self.multiplicity[element.attrib['name']]
                max_min = max_min.split('..')
                max_min = [int(i) for i in max_min]
                if len(max_min) == 1:
                    data['max'], data['min'] = max_min[0], max_min[0]
                else:
                    data['min'], data['max'] = max_min[0], max_min[1]

            data['parameters'] = []
            for i in element.iter('Attribute'):
                dct = {
                    'name': i.attrib['name'],
                    'type': i.attrib['type']
                }

                data['parameters'].append(dct.copy())
            for ag in self.aggregations[element.attrib['name']]:
                data['parameters'].append({
                    'name': ag,
                    'type': self.verticals[ag].tag
                })
            elements.append(data)
        with open(path, 'w') as file:
            json.dump(elements, file, indent=4)


if __name__ == '__main__':
    g = Generator('../input/impulse_test_input.xml')
    g.parse_file()
    g.generate_xml(cs.path_out_config)
    g.generate_json(cs.path_out_config)
