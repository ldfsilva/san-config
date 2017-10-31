import re
import argparse
import paramiko
from getpass import getpass
from datetime import datetime


def get_config(switchname, username, password):
    """Get the SAN configuration from the remote SAN switch."""

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=switchname, username=username, password=password)
    command = 'cfgshow\n'
    stdin, stdout, stderr = client.exec_command(command)
    config = stdout.read()

    return config


def save_config(switchname, config):
    """Save SAN configuration onto a file."""

    # build the file name
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M%S')
    filename = 'sanconfig_%s_%s.bckup' % (switchname, timestamp)

    with open(filename, 'w') as fp:
        fp.write(config)

    print('Configuration saved at %s' % filename)


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


def extract_alias_config(defined_config):
    """Extract alias configuration block out the defined configuration."""

    regex = '(^ alias.*?\n)$'
    match = re.search(regex, defined_config, re.M|re.S)

    return match.group(1)


def parse_alias(alias):
    """Parse an alias string and return it as a dictionary.

    Input:
    alias01
        AA:AA:AA:AA:AA:AA:AA:AA
        BB:BB:BB:BB:BB:BB:BB:BB

    Output:
    {'alias01': [
        'AA:AA:AA:AA:AA:AA:AA:AA',
        'BB:BB:BB:BB:BB:BB:BB:BB',
    ]}
    """

    # Clean up the string and split values onto a list
    alias = alias.strip('\n').replace(' ', '').replace('\t', '')
    alias = alias.split('\n')
    # Alias name is contained in the first element of the list
    alias_name = alias[0]
    # All elements but first will be WWPNs for that alias
    wwpns = alias[1:]

    return {alias_name: wwpns}


def get_aliases(config):
    """Get all aliases of the given SAN configuration and returns them as a
    dictionary with their respective WWPNs.
    """

    aliases = {}
    # Extract the defined configuration
    defined_config = extract_defined_config(config)
    # Extract the section containing the aliases
    alias_block = extract_alias_config(defined_config)

    # Separate each alias onto an item of a list and proceed with parsing
    # discard the first element as there is no need to build the original
    # content back
    match = re.split(' alias:\s+', alias_block)

    for alias in match[1:]:
        aliases.update(parse_alias(alias))

    return aliases


def alias_exist(alias, aliases):
    """Check if the alias name exist on the defined aliases config."""

    if alias in aliases:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(
        prog='san_config',
        description='A python script for managing SAN configurations.')

    # login arguments
    parser.add_argument('--switchname', '-s', required=True,
        help='SAN switch hostname/IP address')
    parser.add_argument('--username', '-u', required=True, help='Username')
    parser.add_argument('--password', '-p', help='Password')

    # action arguments
    parser.add_argument('--backup', '-b', action='store_true',
        help='Backup the current SAN configuration to a file.')

    args = parser.parse_args()
    password = args.password or getpass("Provide %s's password: " % args.username)

    if args.backup:
        config = get_config(args.switchname, args.username, password)
        save_config(args.switchname, config)


if __name__ == '__main__':
    main()