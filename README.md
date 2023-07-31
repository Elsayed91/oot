# Order of the Template (OOT)

In the sacred halls of Dev, the Order of the Template (OOT) stands as a bastion of structure and order amidst the chaos. The order, founded by the ancients, carries the mission of maintaining harmony between variables and templates, ensuring every template adheres to its rightful structure, and bringing light to the shadowy corners of Jinja and YAML.

The Order of the Template provides a noble toolkit for Python developers, aiding them in their quests to parse YAML files and Jinja templates, resolve environment variables, and validate schemas.

## The Code of the Order
### A Noble Quest

The Templars are trained not only in the ancient art of parsing Jinja templates but also in the mastery of environments, skillfully resolving environment variables. They are the keepers of schemas, using their wisdom to ensure that data structures adhere to their rightful schemas.

Consider a quest where a Templar must decode an ancient manuscript, a YAML file filled with Jinja templates and environment variables:

```yaml
# manuscript.yaml
Templar: {{ TEMPLAR_NAME|default('Unknown Templar') }}
HallOfHonor: ${HALL_OF_HONOR:"Hall of the Wicked"}
```
The Templar starts his task. He replaces the `TEMPLAR_NAME` variable with the name of a famous Templar. He then resolves the `HALL_OF_HONOR` environment variable, revealing the name of the sacred hall. Once the manuscript has been decoded, he validates it, ensuring it adheres to the ancient schema:

```python
from oot import parse_file

file_path = "manuscript.yaml"
variables = {"TEMPLAR_NAME": "Jacques de Molay"}
os.environ["HALL_OF_HONOR"] = "Hall of the Brave" # Environmental variables will be automatically substituted

# The Templar decodes the manuscript
manuscript = parse_file(file_path, context=variables)

# The manuscript is decoded:
assert manuscript == {"Templar": "Jacques de Molay", "HallOfHonor": "Hall of the Brave"}

# The Templar validates the manuscript against the ancient schema
schema_path = "schema.json"
manuscript = parse_file(file_path, context=variables, validation_schema=schema_path)
```

In the above example, `schema.json` might be a JSON schema file that defines the structure of the decoded manuscript:

```json
{
    "type": "object",
    "properties": {
        "Templar": {"type": "string"},
        "HallOfHonor": {"type": "string"}
    }
}
```

## Joining the Order

The Order welcomes all who seek order in their templates and harmony in their variables. To install the Order's toolkit, simple run:

```bash
pip install oot
```

May the Order guide you in your quests. 


## Closing Words

- OOT was born out of the re-occuring necessity to parse Jinja templates and resolve environment variables across multiple projects.
- To separate concerns, enhance productivity and spare myself the need to setup code and tests within each project, I encapsulated the functionality.
- OOT's primary objective is to painlessly handle the resolution of environmental variables and/or templating in your YAML files. 
- I came up with the name and theme. the README is a glorious work of `ChatGPT`.