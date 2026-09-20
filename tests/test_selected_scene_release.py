"""Regression checks for the user's four selected scene figures, not visual approval."""
import hashlib
from pathlib import Path

from modelatlas.common import digest, read_json
from modelatlas.corpus import load_corpus


ROOT = Path(__file__).resolve().parents[1]
SELECTED = (
    '2024-b-deep-sea-rescue',
    '2024-a-lamprey',
    '2026-d-wins-to-worth',
    '2025-f-cyber-policy',
)


def test_four_selected_scenes_keep_order_exact_prompts_and_scope():
    showcase = read_json(ROOT / 'docs/examples/showcase.json')
    standalone = [case for case in showcase['cases'] if case['presentation'] == 'standalone']
    assert [Path(case['brief']).parent.name for case in standalone] == list(SELECTED)
    corpus_cases = {case['id'] for case in load_corpus()['cases']}
    for number, case in enumerate(standalone, 1):
        directory = ROOT / Path(case['brief']).parent
        brief = read_json(directory / 'brief.json')
        assert case['selection_number'] == number
        assert case['approval']['user_message'] == '1234修好后推送'
        assert brief['review']['knowledge_base_admission'] is False
        assert brief['generation']['selected_series'] == 'object-scene-20260921'
        assert all(ref['case_id'] in corpus_cases for ref in brief['references'])
        archive = read_json(directory / 'pre-scene-record.json')
        assert digest(directory / 'overview-before-scene.png') == archive['brief']['generation']['image_sha256']
        records = read_json(directory / 'scene-prompt-records.json')['calls']
        chain = [call for call in brief['generation']['chain'] if call.get('series') == 'object-scene-20260921']
        assert len(records) == len(chain)
        for record, call in zip(records, chain):
            exact = record['submitted_prompt'].encode('utf-8')
            assert exact == (directory / call['prompt']).read_bytes()
            assert hashlib.sha256(exact).hexdigest() == call['prompt_sha256']
            assert digest(directory / call['output']) == call['sha256']
            if call['operation'] == 'generate':
                assert call['prompt_detail']['passed']
                assert call['prompt_detail']['template_bytes_verified']
                assert call['prompt_detail']['submitted_utf8_sha256'] == call['prompt_sha256']
            else:
                assert (directory / call['input']).is_file()
        assert records[-1]['output'] == 'overview.png'
    for name in ('README.md', 'README.en.md'):
        text = (ROOT / name).read_text(encoding='utf-8')
        positions = [text.index(f'id="{key}"') for key in SELECTED]
        assert positions == sorted(positions)


def test_unselected_voting_scene_did_not_replace_the_approved_example():
    directory = ROOT / 'docs/examples/2026-c-ballroom-voting'
    brief = read_json(directory / 'brief.json')
    assert brief['generation']['selected_series'] == 'pdf-reread-20260920'
    assert not (directory / 'scene-prompt-records.json').exists()
