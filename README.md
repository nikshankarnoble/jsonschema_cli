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

>>> parser = jsonschema_cli.build_cli(schema)
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
>>> args = parser.parse_args(['--width', '2248.5', '--playblast-type', 'internal'])
>>> jsonschema.validate(args.__dict__, schema)
```
