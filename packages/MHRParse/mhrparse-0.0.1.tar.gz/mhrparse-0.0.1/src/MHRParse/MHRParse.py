from struct import pack, unpack
import io


def mhr_to_json(data: bytes):
    # preparing parsing
    final = {}
    final["_"] = "Generated using MHRParse"
    f = io.BytesIO(data)

    # metadata
    f.seek(8)
    meta_size = unpack("i", f.read(4))[0]
    metadata = unpack("i", f.read(meta_size))[0]

    # event info
    f.seek(8, 1)
    event_size = unpack("i", f.read(4))[0]
    event_count = unpack("i", f.read(4))[0]

    # events
    events = []
    for _ in range(event_count):
        json = {}
        f.seek(2, 1)
        json["down"] = unpack("?", f.read(1))[0]
        json["p2"] = unpack("?", f.read(1))[0]
        json["frame"] = unpack("I", f.read(4))[0]
        json["x"] = unpack("f", f.read(4))[0]
        json["y"] = unpack("f", f.read(4))[0]
        json["r"] = unpack("f", f.read(4))[0]
        f.seek(event_size - 20, 1)
        events.append(json)

    # remove useless player 2 entries
    player2 = True
    for event in events:
        if event["p2"]:
            player2 = False
    if player2:
        for event in events:
            event.pop("p2")

    # join final json
    final["events"] = events
    final["meta"] = {"fps": metadata}
    return final


def json_to_mhr(json):
    pass
