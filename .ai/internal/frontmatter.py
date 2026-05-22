import re
import yaml


# Custom YAML loader that prevents timestamp parsing
class NoDatesSafeLoader(yaml.SafeLoader):
    pass


# Remove YAML timestamp auto-parsing
NoDatesSafeLoader.yaml_implicit_resolvers = {
    key: [
        resolver
        for resolver in resolvers
        if resolver[0] != 'tag:yaml.org,2002:timestamp'
    ]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def parse_frontmatter(content: str) -> dict:
    frontmatter_match = re.match(
        r'^---\s*\n(.*?)\n---\s*\n?',
        content,
        re.DOTALL
    )

    if not frontmatter_match:
        return {}

    try:
        return yaml.load(
            frontmatter_match.group(1),
            Loader=NoDatesSafeLoader
        ) or {}
    except yaml.YAMLError:
        return {}
