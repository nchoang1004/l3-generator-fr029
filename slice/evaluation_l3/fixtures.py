"""Hand-authored facts, not output from the extractor/model/verifier under test.

Evidence here is synthetic identity metadata: it tests preservation, not whether
source proves a claim. No component partition policy is chosen by these fixtures.
"""
from copy import deepcopy
from hashlib import sha256

SNAP = 'snapshot-render-eval-v1'
EID = 'ev-render-eval'


def identity(label):
    return 'fact:' + sha256(label.encode()).hexdigest()


def known(value):
    return {'state': 'known', 'value': value, 'evidence_ids': [EID]}


def unknown(reason='Synthetic case: upstream could not establish this field'):
    return {'state': 'unknown', 'reason': reason}


def na():
    return {'state': 'not_applicable', 'reason': 'Explicitly absent in this synthetic case'}


def evidence():
    return dict(id=EID, snapshot_id=SNAP, file_id='file-api', path='app/api.py',
                sha256=sha256(b'# synthetic evidence, not extraction ground truth\n').hexdigest(),
                start_line=1, end_line=1, start_column=None, end_column=None)


def fact(label, kind, attrs):
    return dict(id=identity(label), unit_id='unit-app', kind=kind, attributes=attrs,
                evidence=[evidence()], resolution='not_applicable', target_fact_ids=[],
                confidence='exact', completeness='full')


def route(label='route', method='GET', path='/v1/orders', status=200):
    return fact(label, 'route', dict(application_id=known('app-main'), method=known(method), path=known(path),
        handler=known('app.api.orders'), registration_context=known('app-main:include-1'),
        declaration_evidence_id=known(EID), request_model_ids=known([]), response_model_ids=known([]),
        status_codes=known([status]), auth=unknown(), parameters=known([]), bodies=known([])))


def column(name='id', type_='INTEGER', pk=True, nullable=False, fk=None):
    return dict(name=known(name), type=known(type_), primary_key=known(pk), nullable=known(nullable),
                foreign_key=na() if fk is None else known(fk))


def table():
    return fact('table', 'table', dict(name=known('orders'), dialect=known('sqlite'),
        declaration_evidence_id=known(EID), columns=known([column(), column('note', 'TEXT', False, True)])))


def event(label='event', action='consume'):
    return fact(label, 'event', dict(action=known(action), topic=known('order-created'), broker=known('kafka-cluster-A'),
        namespace=known('sales'), serialization_context=known('json-v1'), declaration_evidence_id=known(EID),
        payload=known({'type': 'object', 'properties': {'order_id': {'type': 'integer'}}, 'required': ['order_id']})))


def model_fact(label='body'):
    return fact(label, 'request_model', dict(name=known('Order'), fields=known([
        dict(name=known('name'), type=known({'type': 'string'}), required=known(True), nullable=known(False)),
        dict(name=known('note'), type=known({'type': 'string'}), required=known(False), nullable=known(True))])))


def component(i=0, name=None):
    return dict(id=f'cmp-{i:03}', unit_id='unit-app', name=name or f'Component {i}',
                member_file_ids=['file-api' if i == 0 else f'file-{i}'], grouping_source='code',
                confidence='exact', completeness='full', evidence_ids=[EID], label_status='path_fallback')


def decision(subject):
    return dict(subject_id=subject, verdict='accepted', rule_id='synthetic-reviewed', rule_version='eval-v1',
                fact_ids=[], evidence_ids=[EID], reason='Synthetic accepted input for renderer isolation')


def fixture(facts=None, count=1):
    facts = deepcopy(facts if facts is not None else [route(), table(), event()])
    comps = [component(i) for i in range(count)]
    owners = [dict(fact_id=f['id'], contract_kind={'route':'api', 'table':'table', 'event':'event'}[f['kind']],
                   component_id=comps[0]['id'], rule_id='declaration-file', rule_version='1-draft', evidence_ids=[EID])
              for f in facts if f['kind'] in ('route', 'table', 'event')]
    return dict(schema_version='0.1.0', snapshot_id=SNAP,
        inventory=dict(schema_version='0.1.0', snapshot_id=SNAP, support_matrix_version='synthetic-v1',
            grouping_policy_version='synthetic-v1', outcome='ready', units=[dict(id='unit-app', root_path='app',
            language='Python', framework='synthetic', support='partial', file_ids=[x for c in comps for x in c['member_file_ids']],
            flat=False)], excluded=[], limitations=[]),
        facts=dict(schema_version='0.1.0', snapshot_id=SNAP, extractor_version='hand-authored-not-extracted', facts=facts, limitations=[]),
        model=dict(schema_version='0.1.0', snapshot_id=SNAP, partition_version='synthetic-not-D03',
            components=comps, external_systems=[], edges=[], contract_owners=owners, limitations=[], rejected_proposals=[]),
        evidence_index=[evidence()], decisions=[decision(x['id']) for x in facts+comps], limitations=[])


def partial(f, field, state=None):
    f['attributes'][field] = deepcopy(state or unknown())
    f['completeness'] = 'partial'
    f['completeness_reason'] = 'Explicit unknown in synthetic fixture'
    return f


def edge(v, relation='calls', source='cmp-000', target='cmp-001'):
    e = dict(id=f'edge-{len(v["model"]["edges"])}', source_component_id=source, target_component_id=target,
        relation_type=relation, fact_ids=[v['facts']['facts'][0]['id']], evidence_ids=[EID], origin='static',
        confidence='exact', completeness='full', rule_id='resolved-target', rule_version='1-draft')
    v['model']['edges'].append(e)
    v['decisions'].append(decision(e['id']))
    return e
