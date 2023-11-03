from .hy3 import load as hy3_load
from .sd3 import load as sd3_load
from .yaml import load as yaml_load
from .scb import load as scb_load
from .ev3 import load as ev3_load
import urllib.request, zipfile, io

def load(filename, fo=None):
    """
    Load a swim results file and return a dictionary object with the parsed contents.

    @param filename the filename or URL of the results file to parse
    @param fo the file object (optional) of the file to parse (if None, then filename will be opened)
    """
    if fo is None:
        if filename.startswith("http:") or filename.startswith("https:"):
            cio = io.BytesIO(urllib.request.urlopen(filename).read())
        else:
            with open(filename,"rb") as fo:
                cio = io.BytesIO(fo.read())
        fo = cio

    if filename.lower().endswith(".zip"):
        zfo = zipfile.ZipFile(fo)
        scb_files = []
        for zfn in zfo.namelist():
            if zfn.endswith(".sd3") or zfn.endswith(".hy3") or zfn.endswith(".ev3"):
                zio = io.BytesIO(zfo.read(zfn))
                return load(zfn,zio)
            elif zfn.lower().endswith(".scb"):
                scb_files.append(zfn)
        if len(scb_files)>0:
            return scb_load([io.BytesIO(zfo.read(zfn)) for zfn in scb_files])
    elif filename.lower().endswith(".sd3"):
        return sd3_load(fo)
    elif filename.lower().endswith(".hy3"):
        return hy3_load(fo)
    elif filename.lower().endswith(".ev3"):
        return ev3_load(fo)
    elif filename.lower().endswith(".yml"):
        return yaml_load(fo)
    raise ValueError("no valid file found for parsing")

def _event_key_from_event(event):
    if event['type'] is None:
        event_prefix="A"
    elif event['type']=='Prelim':
        event_prefix="B"
    elif event['type']=="Final":
        event_prefix="C"

    # pad some 0s on the event_str to make a lexicographic sort possible
    event_str = event['event']
    while len(event_str)<6:
        event_str = "0"+event_str
    return event_prefix+"-"+event_str

def _event_key_from_entry(entry):
    if 'event_type' not in entry:
        event_prefix="0"
    elif entry['event_type'] is None:
        event_prefix="A"
    elif entry['event_type']=='Prelim':
        event_prefix="B"
    elif entry['event_type']=="Final":
        event_prefix="C"

    # pad some 0s on the event_str to make a lexicographic sort possible
    event_str = entry['event']
    while len(event_str)<6:
        event_str = "0"+event_str
    return event_prefix+"-"+event_str

def get_events(meetinfo):
    if 'teams' in meetinfo:
        teams_by_short_name = {}
        events_by_key = {}
        swimmers_by_code = {} # swimmer codes apply across the entire file (relay can be made up of swimmers from multiple teams)
        # so we have to do 2 passes, first to find all swimmer codes (so we can resolve them in the 2nd step)
        # then to pull the entries
        for team in meetinfo['teams']:
            teams_by_short_name[team['short_name']] = team
            for swimmer in team['swimmers']:
                assert swimmer['swimmer_code'] not in swimmers_by_code # make sure our swimmer codes are unique across the file!
                swimmers_by_code[swimmer['swimmer_code']] = swimmer
        for team in meetinfo['teams']:
            for entry in team['entries']:
                try:
                    event_key = _event_key_from_entry(entry)
                    if event_key not in events_by_key:
                        events_by_key[event_key] = {
                            "event":entry['event'],
                            "date":entry.get('event_date',None),
                            "gender":entry['event_gender'],
                            "gendercode":entry['event_gendercode'],
                            "course":entry['event_course'],
                            "coursecode":entry['event_coursecode'],
                            "stroke":entry['stroke'],
                            "strokeshort":entry['strokeshort'],
                            "distance":entry['distance'],
                            "relay":entry['relay'],
                            "type":entry.get('event_type',None),
                            "entries":[],
                            "num_heats":None
                        }
                        event = events_by_key[event_key]
                        name = "%s %d %s"%(event['gender'],event['distance'],event['strokeshort'])
                        if entry['relay']:
                            name += " Relay"
                        event['name'] = name

                    entry = entry.copy()
                    entry['swimmers'] = [swimmers_by_code[s] for s in entry['swimmer_codes']]

                    events_by_key[event_key]['entries'].append(entry)
                    if entry['heat'] is not None:
                        if events_by_key[event_key]['num_heats'] is None or \
                                events_by_key[event_key]['num_heats']<entry['heat_number']:
                            events_by_key[event_key]['num_heats'] = entry['heat_number']
                except TypeError:
                    print("invalid entry",entry)
                    raise

        return [events_by_key[event_key] for event_key in sorted([event_key for event_key in events_by_key.keys()])]
    elif 'events' in meetinfo:
        events = [e.copy() for e in meetinfo['events']]
        for e in events:
            if 'entries' not in e:
                e['entries'] = []
        return events
    else:
        raise ValueError("meetinfo doesn't have entries or events keys")

def populate_heats(event):
    event['heats'] = []
    heats_by_key = {}
    if 'entries' in event:
        for entry in event['entries']:
            if entry['heat'] is not None:
                if entry['heat_number'] not in heats_by_key:
                    heats_by_key[entry['heat_number']] = {
                        "heat":entry['heat'],
                        "heat_number":entry['heat_number'],
                        "entries":[]
                    }
                heats_by_key[entry['heat_number']]['entries'].append(entry)
        for heat_num in sorted([hnum for hnum in heats_by_key.keys()]):
            heats_by_key[heat_num]['entries'].sort(key=lambda e:e['lane'])
            event['heats'].append(heats_by_key[heat_num])
    return event

def get_lanes(meetinfo):
    if 'teams' in meetinfo:
        lanes = []
        for team in meetinfo['teams']:
            for entry in team['entries']:
                if entry['lane'] is not None and entry['lane'] not in lanes:
                    lanes.append(entry['lane'])
        lanes.sort()
        return lanes
    else:
        raise ValueError("meetinfo doesn't have entries")
