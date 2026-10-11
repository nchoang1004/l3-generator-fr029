"""Versioned case catalogue. Small parameter matrices are explicit contract boundaries,
not multiple votes for product quality. Review case.json beside every retained run.
"""
from dataclasses import dataclass, field
from copy import deepcopy
from .fixtures import *


@dataclass
class Case:
    id: str
    group: str
    title: str
    requirement: str
    input: dict
    mode: str = 'render'
    expect: dict = field(default_factory=dict)
    invalid_mutation: str | None = None
    repository_name: str = 'Review shop'


def catalog():
    cases = []
    def add(id, group, title, v=None, expect=None, mode='render', mutation=None, name='Review shop'):
        req = {'api':'AC-L3GEN-027-01; API-008 §5', 'table':'AC-L3GEN-027-02; API-008 §6.1',
               'event':'AC-L3GEN-027-03; API-008 §6.2', 'graph':'AC-L3GEN-025-02/04; API-008 §3',
               'boundary':'AC-L3GEN-025-02; API-008 §3/7', 'publish':'AC-L3GEN-025-03; API-008 §7',
               'security':'SEC-002; API-008 §4/7', 'bundle':'AC-L3GEN-025-01/02/04; API-008 §3/4'}[group]
        cases.append(Case(id, group, title, req, v if v is not None else fixture(), mode, expect or {}, mutation, name))
    add('bundle-complete', 'bundle', 'API + TBL + EVT + JSON + README + Mermaid + SVG from frozen input')
    add('bundle-repeat', 'bundle', 'Two renders with identical input produce identical bytes', mode='repeat')
    add('bundle-no-upstream', 'bundle', 'Renderer cannot call extraction, verification, LLM or network', mode='offline')
    for method in ['GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS','TRACE']:
        add('api-method-'+method.lower(), 'api', method+' preserves full route and explicit 201', fixture([route(method=method,status=201)]))
    for fld in ['path','status_codes','method','application_id','registration_context']:
        r = partial(route(), fld)
        add('api-unknown-'+fld, 'api', 'Unknown '+fld+' stays visible and operation is omitted', fixture([r]), {'api_ops':0})
    r = partial(route(), 'path'); r['attributes']['path_suffix'] = known('/orders')
    add('api-prefix-unknown', 'api', 'Known suffix is not promoted to a full path', fixture([r]), {'api_ops':0, 'text_contains':'/orders'})
    r1, r2 = route('one'), route('two')
    r2['attributes']['application_id'] = known('app-other'); r2['attributes']['registration_context'] = known('app-other:1')
    add('api-app-collision', 'api', 'Two apps same method/path: retain two rows, omit both operations', fixture([r1,r2]), {'api_ops':0})
    r1, r2 = route('mount1',path='/a/orders'), route('mount2',path='/b/orders')
    r2['attributes']['registration_context'] = known('app-main:include-2')
    add('api-two-mounts', 'api', 'Two registrations with different prefixes remain two operations', fixture([r1,r2]), {'api_ops':2})
    r = route(path='/orders/{id}')
    add('api-missing-path-parameter', 'api', 'Unrepresented path parameter cannot become a valid operation', fixture([r]), {'api_ops':0})
    r['attributes']['parameters'] = known([dict(name=known('id'), **{'in':known('path')}, required=known(True), type=known({'type':'integer'})),
        dict(name=known('q'), **{'in':known('query')}, required=known(False), type=known({'type':'string'}))])
    add('api-parameters', 'api', 'Path/query parameters retain names, required flags and types', fixture([r]))
    r = route(); m = model_fact()
    r['attributes']['request_model_ids'] = known([m['id']])
    r['attributes']['bodies'] = known([dict(direction='request', model_id=m['id'], status=None, media_type='application/json')])
    add('api-body', 'api', 'Model fields and nullable retained; no invented body-required assertion', fixture([r,m]))
    r = route(); m = model_fact(); m['kind'] = 'response_model'
    r['attributes']['response_model_ids'] = known([m['id']])
    r['attributes']['bodies'] = known([dict(direction='response', model_id=m['id'], status=200, media_type='application/json')])
    add('api-response-model', 'api', 'Response model associated only to evidenced status/media', fixture([r,m]))
    nested = model_fact('nested'); nested['attributes']['name'] = known('Nested')
    m['attributes']['fields']['value'][0]['type'] = known({'anyOf':[{'x-model-fact':nested['id']}, {'type':'string'}]})
    add('api-nested-union', 'api', 'Nested model reference inside anyOf resolves locally', fixture([r,m,nested]))
    for field in ['dialect','name','columns']:
        add('table-unknown-'+field, 'table', 'Unknown '+field+' omits whole DDL table with reason', fixture([partial(table(),field)]), {'ddl_tables':0})
    for field in ['type','nullable','primary_key','foreign_key','name']:
        t = table(); t['attributes']['columns']['value'][1][field] = unknown()
        t['completeness']='partial'; t['completeness_reason']='Unknown column attribute'
        add('table-column-unknown-'+field,'table','Unknown column '+field+' does not silently drop a column',fixture([t]),{'ddl_tables':0})
    for dialect, typ in [('sqlite','BLOB'),('postgresql','VARCHAR(20)'),('postgresql','NUMERIC(12,2)'),('postgresql','TIMESTAMP WITH TIME ZONE')]:
        t=table(); t['attributes']['dialect']=known(dialect);t['attributes']['columns']['value'][1]['type']=known(typ)
        add('table-type-'+str(len(cases)),'table',dialect+' '+typ+' formats and preserves semantics',fixture([t]),{'ddl_tables':1})
    for typ in ['VARCHAR(0)','NUMERIC(2,3)','TEXT); DROP TABLE users; --']:
        t=table();t['attributes']['dialect']=known('postgresql');t['attributes']['columns']['value'][1]['type']=known(typ)
        add('table-invalid-type-'+str(len(cases)),'table','Unsupported/hostile type must omit whole table',fixture([t]),{'ddl_tables':0})
    t=table();t['attributes']['columns']['value'][1]=column('customer_id','INTEGER',False,False,{'table':'customers','column':'id'})
    add('table-foreign-key','table','Explicit FK table and column retained',fixture([t]),{'ddl_tables':1})
    t['attributes']['columns']['value'][1]['foreign_key']=known({'table':'bad\x01name','column':'id'})
    add('table-fk-control','table','Control character in FK target must not become a fake identifier',fixture([t]),{'ddl_tables':0})
    t=table();t['attributes']['name']=known('odd"orders');t['attributes']['columns']['value'][1]['name']=known('quote"note')
    add('table-quoted-identifiers','table','Quoted identifiers round-trip without executable SQL injection',fixture([t]),{'ddl_tables':1})
    t=table();t['attributes']['columns']['value'][1]=column('other_id','INTEGER',True,False)
    add('table-compound-pk','table','Unsupported compound primary key omits whole table',fixture([t]),{'ddl_tables':0})
    t=table();t['attributes']['columns']['value'][0]['nullable']=known(True)
    add('table-nullable-pk','table','Contradictory nullable primary key cannot yield DDL',fixture([t]),{'ddl_tables':0})
    for action in ['publish','consume']:
        add('event-'+action,'event','Standalone '+action+' keeps unknown counterpart and partial label',fixture([event(action=action)]),{'event_files':1,'text_contains':'unknown'})
    add('event-payload-unknown','event','Unknown payload stays open schema, not null or closed object',fixture([partial(event(),'payload')]))
    for field in ['broker','namespace','serialization_context','topic']:
        e1,e2=partial(event('e1'),field),partial(event('e2'),field)
        add('event-unknown-'+field,'event','Two unknown '+field+' bindings must stay in separate files',fixture([e1,e2]),{'event_files':2})
    e1,e2=event('e1'),event('e2');e2['attributes']['broker']=known('cluster-B')
    add('event-different-brokers','event','Same topic, different broker: separate contracts, no inferred edge',fixture([e1,e2]),{'event_files':2})
    e2['attributes']['broker']=known('kafka-cluster-A')
    add('event-same-binding','event','Fully known same binding may group facts in one owner file',fixture([e1,e2]),{'event_files':1})
    v=fixture([event('send','publish'),event('receive','consume')],2)
    v['model']['contract_owners'][1]['component_id']='cmp-001'
    v['facts']['facts'][1]['evidence'][0]['file_id']='file-1'
    # Evidence metadata may be shared in synthetic fixtures; ownership is supplied, never inferred here.
    add('event-two-owners','event','Producer and consumer each receive their own file',v,{'event_files':2})
    for n in [0,1,50]:
        add('graph-nodes-'+str(n),'graph',str(n)+' nodes retain exact graph membership',fixture([],n))
    add('graph-nodes-51','boundary','51 nodes rejected, no silent truncation',fixture([],51),mode='reject',expect={'codes':['INVALID_INPUT']})
    v=fixture([route()],2);edge(v);edge(v,'depends')
    add('graph-parallel-types','graph','Same endpoints, distinct relation types are retained',v)
    v=fixture([route()],2);edge(v,source='cmp-001',target='cmp-000')
    add('graph-directed','graph','Edge direction is preserved in both diagram formats',v)
    v=fixture();v['model']['contract_owners'][0].update(component_id=None,reason='No validated owner')
    add('bundle-owner-unknown','bundle','Unknown owner has notice and no guessed API file',v,{'api_files':0})
    for label in ['Đơn hàng','CON','../../x | <script>alert(1)</script>','A'*64]:
        v=fixture([route()],2);v['model']['components'][0]['name']=label;v['model']['components'][1]['name']=label
        add('names-'+str(len(cases)),'security','Stable safe unique component slugs: '+label[:24],v,{'slug_max':64})
    for mutation in ['missing-schema','wrong-schema','cross-snapshot','dangling-edge','rejected-component','duplicate-fact','missing-evidence','dangling-owner']:
        add('input-'+mutation,'boundary','Reject '+mutation+' before publishing',fixture(),mode='reject',mutation=mutation,
            expect={'codes':['INVALID_INPUT','SNAPSHOT_MISMATCH','REFERENCE_INVALID','PARITY_FAILED']})
    for mode,title in [('nonempty','Existing output is not overwritten'),('svg-failure','SVG failure leaves all other artifacts ready'),
                       ('retry','Retry only failed SVG, preserve ready bytes'),('retry-ready','Retry ready artifact is an exact no-op'),
                       ('retry-version','Version drift rejects retry'),('retry-tamper','Tampered ready bytes reject retry'),
                       ('retry-crash','Crash after target install leaves old failed manifest; later retry recovers'),
                       ('retry-nonretryable','Deterministically unsafe SVG is not retryable'),('publish-failure','Injected staging write failure publishes nothing')]:
        add('publish-'+mode,'publish',title,mode=mode)
    return cases


def corrupt(v, mutation):
    """Only applied after validating the base fixture. These are intentionally invalid inputs."""
    if mutation == 'missing-schema': del v['schema_version']
    elif mutation == 'wrong-schema': v['schema_version']='99.0.0'
    elif mutation == 'cross-snapshot': v['evidence_index'][0]['snapshot_id']='wrong-snapshot'
    elif mutation == 'dangling-edge': edge(v,target='not-a-component')
    elif mutation == 'rejected-component':
        next(d for d in v['decisions'] if d['subject_id']=='cmp-000')['verdict']='rejected'
    elif mutation == 'duplicate-fact': v['facts']['facts'].append(deepcopy(v['facts']['facts'][0]))
    elif mutation == 'missing-evidence': v['evidence_index']=[]
    elif mutation == 'dangling-owner': v['model']['contract_owners'][0]['component_id']='missing'
    elif mutation is not None: raise ValueError(mutation)
