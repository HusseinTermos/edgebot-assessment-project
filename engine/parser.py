import re
line_pattern = re.compile(
    r'''
    ^\s*
    (?P<main_id>[A-Za-z0-9_\.]+)
    \s*=\s*
    (?P<transformation_id>[A-Za-z0-9_\.]+)
    \s*\{
        \s*(?P<args1>[A-Za-z0-9_\.]+(?:\s*,\s*[A-Za-z0-9_\.]+)*)?\s*
    \}\s*\{
        \s*(?P<args2>[A-Za-z0-9_\.]+(?:\s*,\s*[A-Za-z0-9_\.]+)*)?\s*
    \}
    \s*$
    ''',
    re.VERBOSE
)

def parse_command(line):
    m = line_pattern.match(line)
    if not m:
        raise ValueError(f"Invalid line: '{line}'")

    args1 = m.group("args1")
    args2 = m.group("args2")
    transformation_id = m.group("transformation_id")

    config_str = [x.strip() for x in args1.split(",")] if args1 else []
    if transformation_id == 'Fetch':
        config = config_str
    else:
        config = []
        for x in config_str:
            try:
                config.append(int(x))
            except ValueError:
                config.append(float(x))

    return {
        "main_id": m.group("main_id"),
        "transformation_id": transformation_id,
        "config": config,
        "series_names": [x.strip() for x in args2.split(",")] if args2 else [],
    }


def parse_script(script):
    commands = script.strip().split('\n')
    parsed_commands = []
    for command in commands:
        parsed_commands.append(parse_command(command))

    return parsed_commands
