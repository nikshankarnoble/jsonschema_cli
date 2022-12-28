# jsonschema_cli
Basic Python module for generating an argparse CLI from a JSON-Schema document.


```
>>> schema = {
    'description': 'Nuke template for generating playblasts.',
    'properties': {
        'width': {
            'type': 'integer', 'minimum': 0,
            'description': 'Width of the output image',
            'default': 1920,
        },
        'height': {
            'type': 'integer', 'minimum': 0,
            'description': 'Height of the output image.',
            'default': 1080,
        },
        'playblast_type': {
            'type': 'string',
            'enum': ['client', 'internal'],
        }
    },
    'required': ['playblast_type'],
}

>>> parser = jsonschema_cli.create_parser(schema)
```
```
>>> parser.print_help()
usage: ipython [-h] [--width WIDTH] [--height HEIGHT] --playblast-type {client,internal}

Nuke template for generating playblasts.

options:
  -h, --help            show this help message and exit
  --width WIDTH         Width of the output image
  --height HEIGHT       Height of the output image.
  --playblast-type {client,internal}
```
```
>>> args = parser.parse_args(['--width', '-2248', '--playblast-type', 'internal'])
>>> jsonschema.validate(args.__dict__, schema)
ValidationError: -2248 is less than the minimum of 0

Failed validating 'minimum' in schema['properties']['width']:
    {'default': 1920,
     'description': 'Width of the output image',
     'minimum': 0,
     'type': 'integer'}

On instance['width']:
    -2248
```
