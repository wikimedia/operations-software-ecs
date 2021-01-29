#!/usr/bin/env python3
"""
Attempts to generate an ElasticSearch mapping template from a JSONSchema template.

!!!
    This tool is intended to generate a starting point template, not the final template.

    JSONSchema and ElasticSearch mapping templates are not 1-to-1 compatible.  Users of this
    tool should _not_ expect that it will output a perfect mapping template. It is up to the
    end user of this tool to amend and validate that the output meets requirements and is a
    valid ElasticSearch mapping template.

    Please refer to the ElasticSearch documentation for further information:
    https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
!!!
"""
import argparse
import json
import yaml
import sys

# https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-templates.html
DYNAMIC_TEMPLATES = {
    'strings': [{
        "strings_as_keyword": {
            "mapping": {
                "ignore_above": 1024,
                "type": "keyword"
            },
            "match_mapping_type": "string"
        }
    }]
}

TYPES_MAPPING = {
    # ElasticSearch type -> JSONSchema types mapping
    'boolean': ['null'],
    'keyword': ['string', 'array'],
    'integer': [],
    'double': ['number'],
    'object': [],
}


def convert_type(t):
    for es_type, jss_types in TYPES_MAPPING.items():
        if t in jss_types:
            return es_type
    if t in TYPES_MAPPING.keys():
        return t
    raise KeyError('Unable to ascertain ElasticSearch type for provided type: {}'.format(t))


def get_mapping(o):
    output = {'type': convert_type(o['type'])}
    if output['type'] == 'keyword':
        output['ignore_above'] = 1024
    return output


def build_branch(o):
    output = {}
    for k, v in o['properties'].items():
        output[k] = get_mapping(v)
        if not is_leaf(v):
            output[k]['properties'] = build_branch(v)
    return output


def is_leaf(o):
    return o.get('properties') is None


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert JSONSchema to ES Index Mapping Template',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', dest='input_file', type=argparse.FileType(), default=sys.stdin,
                        help='JSONSchema Input File')
    parser.add_argument('-o', dest='output_file', type=argparse.FileType(), default=sys.stdout,
                        help='ES Template Output File')
    parser.add_argument('-i', dest='index_pattern', default='test-*',
                        help='ES Template Index Pattern.')
    parser.add_argument('-v', dest='version', default='0.0',
                        help='JSONSchema Version.')
    parser.add_argument('-t', dest='template_file', type=argparse.FileType(), default='templates/default.json',
                        help='ES Template Base File.')
    parser.add_argument('-d', dest='dynamic_template', default='strings',
                        help='Dynamic template to use.')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    jsonschema = yaml.safe_load(args.input_file.read())
    template = json.loads(args.template_file.read())
    template['index_patterns'] = [args.index_pattern]
    template['mappings'] = {
        '_meta': {'version': args.version},
        'date_detection': False,
        'dynamic_templates': DYNAMIC_TEMPLATES.get(args.dynamic_template),
        'properties': build_branch(jsonschema)
    }
    args.output_file.write(json.dumps(template, indent=2))


if __name__ == '__main__':
    main()
