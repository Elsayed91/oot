# Order of the Template (OOT)

In the sacred halls of software development, the Order of the Template (OOT) stands as a bastion of structure and order amidst the chaos. The order, founded by the ancients, carries the mission of maintaining harmony between variables and templates, ensuring every template adheres to its rightful structure, and bringing light to the shadowy corners of Jinja and YAML.

The Order of the Template provides a noble toolkit for Python developers, aiding them in their quests to parse YAML files and Jinja templates, resolve environment variables, and validate JSON schemas.

## The Code of the Order
### A Noble Quest

The Templars are trained not only in the ancient art of parsing Jinja templates but also in the mastery of environments, skillfully resolving environment variables. They are the keepers of schemas, using their wisdom to ensure that data structures adhere to their rightful schemas.

Consider a quest where a Templar must decode an ancient manuscript, a YAML file filled with Jinja templates and environment variables:

```yaml
Templar: {{ TEMPLAR_NAME|default('Unknown Templar') }}
HallOfHonor: ${HALL_OF_HONOR:"Hall of the Wicked"}
```
The Templar starts his task. He replaces the `TEMPLAR_NAME` variable with the name of a famous Templar. He then resolves the `HALL_OF_HONOR` environment variable, revealing the name of the sacred hall. Once the manuscript has been decoded, he validates it, ensuring it adheres to the ancient schema:

```python
from oot import parse_file

file_path = "manuscript.yaml"
variables = {"TEMPLAR_NAME": "Jacques de Molay"}
os.environ["HALL_OF_HONOR"] = "Hall of the Brave"

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

The Order welcomes all who seek order in their templates and harmony in their variables. To install the Order's toolkit, use pip:

```bash
pip install oot
```

May the Order guide you in your quests. 



## Closing Words

Jinja2 is parse-able. There are some packages that help with env substitution in YAML/tpl files. 
In my work I usually make use of both. So instead of creating the functions and tests for each project, I decided to just create a package that provides me this functionality.

The name was my idea, the readme is ChatGPT's. I love it. 