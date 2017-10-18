import re


def extract_defined_config(config):
    """Extract defined configuration out of SAN config."""

    # matches everything starting with  "Defined configuration"
    # text until it finds an empty line.
    regex = r'^(Defined configuration:.+?\n)$'
    match = re.search(regex, config, re.M|re.S)
    defined_config = match.group(1)

    return defined_config


def extract_effective_config(config):
    """Extract effective configuration out of SAN config."""

    # matches everything starting with  "Effective configuration"
    # text until it finds an empty line
    regex = r'^(Effective configuration:.+?\n)$'
    match = re.search(regex, config, re.M|re.S)
    defined_config = match.group(1)

    return defined_config


def get_alias(config):
    """Get the aliases out of the effective configuration."""

    aliases = []
    alias = {}

    # matches starting with alias until next (not greedy) alias or
    # an empty line, last two conditions would end the search.
    # In case there is a match the following two groups are expected:
    # group 1: contains the alias_name
    # group 2: contains the alias WWPNs
    # discard some "white spaces" and '\n' to facilitate parsing
    regex = r'^ alias:\s(\w+)\n\s+(.+?)(^ alias:|\n$)'
    match = re.search(regex, config, re.M|re.S)

    if not match:
        return False

    alias_name = match.group(1)
    wwpns = match.group(2).strip('\n')
    wwpns = wwpns.replace(' ', '').split('\n')

    alias.update({alias_name: wwpns})

    aliases.append(alias)

    return aliases


def main():
    pass


if __name__ == '__main__':
    main()