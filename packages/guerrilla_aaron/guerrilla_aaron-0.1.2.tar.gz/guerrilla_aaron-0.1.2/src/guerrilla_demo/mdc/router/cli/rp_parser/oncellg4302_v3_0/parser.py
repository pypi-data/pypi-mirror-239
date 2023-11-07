def parse_ping(content: str) -> dict:
    # SAMPLE OUTPUT
    # Ping to 1.1.1.1:
    # Packets: Sent = 4, Received = 4, Lost = 0
    idx_s = content.find('Sent = ')
    idx_r = content.find('Received = ')
    idx_l = content.find('Lost = ')
    if -1 in (idx_s, idx_r, idx_l):
        raise ValueError('Cannot parse ping content')
    return {
        'sent': int(content[idx_s:idx_r].split()[2].strip(', ')),
        'received': int(content[idx_r:idx_l].split()[2].strip(', ')),
        'lost': int(content[idx_l:].split()[2].strip())
    }


def parse_colon_fields(content: str) -> dict:
    """
    Input:
    content: str, string to parse
    ex:
    null-scan               : Disable
    xmas-scan               : Disable
    nmap-xmas-scan          : Disable
    syn/fin-scan            : Disable
    fin-scan                : Disable
    nmap-id-scan            : Disable
    syn/rst-scan            : Disable
    new-tcp-without-syn-scan: Disable
    Flash                   : Disable
    Syslog                  : Disable
    Trap                    : Disable

    Output:
    dict
    ex:
    {
        'null-scan':'Disable'
        'xmas-scan':'Disable'
        'nmap-xmas-scan':'Disable'
        'syn/fin-scan':'Disable'
        'fin-scan':'Disable'
        'nmap-id-scan':'Disable'
        'syn/rst-scan':'Disable'
        'new-tcp-without-syn-scan':'Disable'
        'Flash':'Disable'
        'Syslog':'Disable'
        'Trap':'Disable'
    }
    """
    ret = {}
    for line in content.split('\n'):
        try:
            k, v = line.split(':', 1)
        except ValueError:
            # if no char ':', split will raise
            # ValueError: not enough values to unpack (expected 2, got 1)
            continue
        ret[k.strip()] = v.strip()
    return ret


def parse_colon_fields_structure(content: str) -> dict:
    ret = {}
    lvs = [[ret, None]]  # levels information. list of [root, indent]
    pk, pv = None, None

    for line in content.split('\n'):
        parts = line.rstrip().split(':')
        if len(parts) != 2:
            continue
        # print('parts', parts)  # debug

        # get indent legth of current line
        _indent = len(parts[0]) - len(parts[0].lstrip())

        # get 1st level indent
        if lvs[0][1] is None:
            lvs[0][1] = _indent

        root, indent = lvs[-1]
        k = parts[0].strip()
        v = parts[1].strip()

        # print('root, indent, _indent', root, indent, _indent)  # debug
        # print('pk, pv', pk, pv)  # debug
        if _indent == indent:
            root[k] = v
        elif _indent < indent:
            # find upper level
            try:
                lvs.pop()
                root, indent = lvs[-1]
                while _indent != indent:
                    lvs.pop()
                    root, indent = lvs[-1]
            except IndexError as e:
                raise ValueError(
                    f'cannot align upper level at line: "{line}"') from e
            lvs[-1][0][k] = v
        else:  # _indent > indent
            if pv == '':
                new = {k: v}
                lvs[-1][0][pk] = new
                lvs.append([new, _indent])
            else:
                raise ValueError(
                    f'indent too long to align previous line: "{line}"')
        pk, pv = k, v

    return ret


def parse_show_ipsec(content: str) -> dict:

    def parse(line):
        ret = {}
        # support max line length is 200
        fields_align = ((0, 20), (22, 36), (37, 57), (59, 200))
        for i in range(0, len(fields_align), 2):
            kch, kct = fields_align[i]  # key column head/tail
            vch, vct = fields_align[i + 1]
            k = line[kch:kct].strip()
            v = line[vch:vct].strip()
            ret[k] = v
        return ret

    ret = {}
    cur = ret
    for line in content.split('\n'):
        colon_count = line.count(':')
        if colon_count == 2:
            cur |= parse(line)
        elif colon_count == 1:
            k, v = line.split(':')
            cur[k.strip()] = v.strip()
        else:
            section = line.strip()
            if len(section) == 0:
                continue  # skip empty line
            cur = {}
            ret[section] = cur
    return ret


def parse_dos_fields(content: str) -> dict:
    """
    Input:
    content: str, string to parse
    ex:
    null-scan               : Disable
    xmas-scan               : Disable
    nmap-xmas-scan          : Disable
    syn/fin-scan            : Disable
    fin-scan                : Disable
    icmp-death              : Disable    Limit: 1000(pkt/s)
    syn-flood               : Disable    Limit: 1000(pkt/s)
    arp-flood               : Disable    Limit: 1000(pkt/s)

    Output:
    dict
    ex:
    {
        'null-scan':'Disable',
        'xmas-scan':'Disable',
        'nmap-xmas-scan':'Disable',
        'syn/fin-scan':'Disable',
        'fin-scan':'Disable',
        'nmap-id-scan':'Disable',
        'syn/rst-scan':'Disable',
        'new-tcp-without-syn-scan':'Disable',
        'icmp-death':{'Status': 'Disable', 'Limit': '1000(pkt/s)'},
        'syn-flood':{'Status': 'Disable', 'Limit': '1000(pkt/s)'},
        'arp-flood':{'Status': 'Disable', 'Limit': '1000(pkt/s)'},
        'Severity':'<0> Emergency',
        'Flash':'Disable',
        'Syslog':'Disable',
        'Trap':'Disable',
    }
    """

    result = parse_colon_fields(content)
    for dos_name, value in result.items():
        if dos_name in ['icmp-death', 'syn-flood', 'arp-flood']:
            content = value.split(' ')
            status = content[0].strip()
            limit = content[-1].strip()
            result[dos_name] = {'Status': status, 'Limit': limit}

    return result


def parse_event_log(content: str) -> list:
    """
    parse the log event type of info.
    First, find the headers by searching for "--------------".
    Second, record the start index of each head.
    Third, parse the meaningful line with the indexes.
    Fourth, make each event as a dict and add to the ret.

    Input:
    content: str, the raw data

    Output:
    list of dict
        ex:
        [
            {'Index': '1', 'Date': '2022/06/09',
             'Time': '01:59:00',
             'Severity': '<0>',
             'Event': '[Auth Ok, Login Success]'},
            {'Index': '2',
             'Date': '2022/06/09',
             'Time': '01:56:07',
             'Severity': '<0>',
             'Event': '[Auth Ok, Login Success]'}
        ]
    """
    fields = ['Index', 'Date', 'Time', 'Severity', 'Event']
    result = []
    for line in content.splitlines():
        parts = line.split(None, 4)
        if len(parts) != 5 or parts[0].isdigit() is False:
            continue  # skip if bad format
        result.append(dict(zip(fields, parts)))
    return result


def parse_event_log_v2(content: str) -> list:
    ret = []
    delimiter = '-' * 76
    for block in content.split(delimiter):
        if len(block.strip()) == 0:
            continue  # TODO: improve format check
        ret.append(parse_dos_fields(block))
    return ret


def parse_table(content) -> list:

    def is_title_separator(line: str):
        chars = set()
        for c in line.strip():  # strip \r \n etc
            chars.add(c)
        return chars == {' ', '-'}

    def get_columns(separator):
        columns = []
        h = t = 0
        for i, c in enumerate(separator):
            t = i
            if c == ' ':
                columns.append((h, t))
                h = t + 1
        t += 1
        columns.append((h, t))
        return list(filter(lambda c: c[0] < c[1], columns))

    def parse(columns, line):
        items = []
        for c in columns:
            items.append(line[c[0]:c[1]].strip())
        return items

    fields = None
    columns = None
    result = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if columns is None:
            if is_title_separator(line):
                columns = get_columns(line)
                fields = parse(columns, lines[i - 1])
        else:
            _line = line.rstrip()
            if len(_line) == 0:
                continue  # ignore empty line
            result.append(dict(zip(fields, parse(columns, _line))))
    return result
