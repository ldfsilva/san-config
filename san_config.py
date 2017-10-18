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


def main():
    pass


if __name__ == '__main__':
    main()