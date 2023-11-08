from lxml import etree

# https://stackoverflow.com/questions/3310614/remove-whitespaces-in-xml-string
PARSER = etree.XMLParser(remove_blank_text=True)


def etree_from_string(string):
    return etree.XML(string, parser=PARSER)


def parse_response(response):
    if isinstance(response, (str, bytes)):
        response = etree.fromstring(response)
    data = response.xpath('/response/result/*')
    for d in data:
        detach(d)
    return data


def detach(e):
    parent = e.getparent()
    if parent is not None:
        parent.remove(e)
    return e


def delete_nat_membership(client, ):
    pass


def delete_policy_membership(element):
    entry = element.entry
    # TODO: Check type
    element.remove()  # Remove element from tree
    print(element.dumps(True))
    with entry.as_dict() as d:
        d.target.negate = 'no'
        d['destination-hip'].member = 'any'
    print(element.dumps(True))

    # client.update(e.xpath, e.dumps())
    # client.create(e.xpath, e.dumps())


def map_dicts(a, b):
    """
        Combine values from b with the value in a having the same key.
    """
    for uuid, u in a.items():
        r = b.get(uuid)
        if r is None:
            continue
        yield u, r


def extend_element(dest, elements):
    """
        Only add element that are not already in the destination
        element.extend(...) is causing duplicates entries because
        the merge is not controlled
    """
    children = {c.tag for c in dest.getchildren()}
    for e in elements:
        if e.tag in children:
            continue
        dest.append(e)
    return dest
