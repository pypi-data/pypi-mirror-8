from __future__ import unicode_literals
import codecs
import json
from conceptnet5.formats.msgpack_stream import MsgpackStreamWriter
from conceptnet5.nodes import normalized_concept_uri
from conceptnet5.edges import make_edge
from conceptnet5.util import get_support_data_filename


FRAME_DATA = json.load(
    codecs.open(get_support_data_filename('zh_frames.json'), encoding='utf-8')
)


def handle_raw_assertion(line):
    parts = line.split(', ')
    user, frame_id, concept1, concept2 = parts
    fdata = FRAME_DATA[frame_id]
    ftext = fdata['text']
    rel = fdata['relation']

    surfaceText = ftext.replace('{1}', '[[' + concept1 + ']]').replace('{2}', '[[' + concept2 + ']]')
    start = normalized_concept_uri('zh_TW', concept1)
    end = normalized_concept_uri('zh_TW', concept2)
    sources = ['/s/activity/ptt/petgame', '/s/contributor/petgame/' + user]
    yield make_edge(rel, start, end, dataset='/d/conceptnet/4/zh',
                    license='/l/CC/By', sources=sources,
                    surfaceText=surfaceText, weight=1)

def handle_file(input_filename, output_file):
    out = MsgpackStreamWriter(output_file)
    for line in codecs.open(input_filename, encoding='utf-8'):
        line = line.strip()
        if line:
            for new_obj in handle_raw_assertion(line):
                out.write(new_obj)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='msgpack file of input')
    parser.add_argument('output', help='msgpack file to output to')
    args = parser.parse_args()
    handle_file(args.input, args.output)


if __name__ == '__main__':
    main()

