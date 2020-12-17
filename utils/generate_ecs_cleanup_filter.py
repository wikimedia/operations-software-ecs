"""
Generate Logstash cleanup filter with allow list based on generated ECS fields
"""

import argparse
import yaml
import os
import jinja2


def get_ecs_data(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f.read())


def get_template(filename='../templates/ecs_cleanup_filter.j2'):
    with open(filename, 'r') as f:
        return jinja2.Template(f.read())


def write_template(filename, data):
    if isinstance(filename, str):
        parent_dir = os.path.split(filename)[0]
        if not os.path.isdir(parent_dir):
            os.mkdir(parent_dir)
        with open(filename, 'w') as f:
            f.write(data)
    else:
        print(data)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate Logstash cleanup filter based on generated ECS data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', dest='input_file', default='dist/ecs/ecs_flat.yml',
                        help='generated ecs_flat.yml input file')
    parser.add_argument('-o', dest='output_file', default=None,
                        help='Logstash Filter Output File')
    parser.add_argument('-v', dest='ecs_version', default='0.0',
                        help='ECS Version.')
    parser.add_argument('-t', dest='template_file', default='templates/ecs_cleanup_filter.j2',
                        help='Logstash Filter Template.')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    ecs_data = get_ecs_data(args.input_file)
    template = get_template(args.template_file)
    allowed_fields = set([x.split('.')[0] for x in ecs_data.keys()])
    write_template(
        args.output_file,
        template.render(ecs_version=args.ecs_version, allowed_fields=sorted(allowed_fields))
    )


if __name__ == '__main__':
    main()
