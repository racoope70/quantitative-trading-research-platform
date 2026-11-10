#!/usr/bin/env python3
"""Bounded real S04 neutral, identity-only size-25 manifest build.

NEVER calls Codex or invokes scientific stages. The real construction command
requires explicit --build and a fresh historical preservation audit on the Mac.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
from collections import Counter
from pathlib import Path

from partition_contract_nonproduction_v1 import (build_partition_manifest,
    verify_manifest, digest, canonical_json, validate_population)

PIN_S04_MANIFEST='ade0a453cc6030d27cb0f1924eb17abe15eb082f55b3fd47af53f52927c543cc'
PIN_S04_EVIDENCE='0a92b5086a07972bdeb1c8210d50ed6c9c6e43d968b993165d06724c76372dc0'
PIN_SEMANTIC='a424085098e871e7f555b29caf3641c5317ac581c9130ba28971385f98aa4fa3'
PIN_PRECEDENCE='57a7827a23b4c7aa47c19ad950b59871dcff7301addf84f7a2fca580a90f9445'
PIN_V3='fe3079dd77d47099b80500f666e6549dfb0ee96ee209df368bb3d1559a65b1f0'
PIN_FIREWALL='09cf139fc69b43d43e734f966c549ddb13efd113a57bafd0e982f675785371b4'
PIN_CHECKPOINT='63500740e08ed2bda817f062a83e8c12b256674f18cf81a771f376281efd574d'
PIN_SCHEMA='b67b0baff0efe3fa67acbb60d14f7654cbe1410fae92795c7cab608f00336268'
RULE='SORT_AUTHORIZED_POSITION_ASCENDING__CONTIGUOUS_FIXED_SIZE_25'
RULE_OBJ={'assignment_rule':RULE,'partition_size':25,'partition_count':20,
          'position_start':1501,'position_end':2000,'content_dependent':False,
          'rule_version':'BATCH0004_SIZE25_REAL_PARTITION_RULE_V1'}
RULE_SHA=digest(RULE_OBJ)
ARTIFACT_ID='BATCH0004_REAL_IDENTITY_BOUND_PARTITION_MANIFEST_V1'
class ManifestStop(RuntimeError): pass
def ensure(ok,label):
    if not ok: raise ManifestStop(label)
def sha_file(p):
    p=Path(p); ensure(p.is_file() and not p.is_symlink(),'FILE_MISSING_OR_SYMLINK__'+str(p))
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def safe_s04_member(root, name):
    ensure(isinstance(name,str) and name and '\\' not in name,'INVALID_RELATIVE_NAME')
    rel=Path(name);ensure(not rel.is_absolute() and '..' not in rel.parts,'INVALID_RELATIVE_PATH')
    p=root/rel
    ensure(p.resolve().is_relative_to(root.resolve()) and p.is_file() and not p.is_symlink(),'INVALID_S04_MEMBER')
    return p

def verify_s04(root, *, real=True):
    root=Path(root)
    ensure(root.is_dir() and not root.is_symlink(),'S04_ROOT_INVALID')
    mp=safe_s04_member(root,'s04_primary_input_manifest.json')
    ep=safe_s04_member(root,'neutral_semantic_evidence.jsonl')
    msha=sha_file(mp);esha=sha_file(ep)
    if real:
        ensure(msha==PIN_S04_MANIFEST and esha==PIN_S04_EVIDENCE,'S04_FROZEN_IDENTITY_MISMATCH')
    manifest=json.loads(mp.read_text())
    ensure(manifest.get('artifact_id')=='BATCH0004_S04_PRIMARY_INPUT_FREEZE','INVALID_S04_ARTIFACT')
    ensure(manifest.get('batch_id')=='BATCH_0004' and manifest.get('row_count')==500
           and manifest.get('unique_source_identities')==500,'INVALID_S04_DOMAIN')
    rows=[json.loads(line) for line in ep.read_text().splitlines() if line.strip()]
    ordered=validate_population(rows)
    ensure(manifest.get('canonical_order')=='AUTHORIZED_POPULATION_POSITION_ASCENDING', 'S04_ORDER_MISMATCH')
    ensure(manifest.get('semantic_answers_present') is False,'S04_SEMANTIC_ANSWERS_PRESENT')
    ensure([r['authorized_population_position'] for r in rows]==list(range(1501,2001)), 'S04_ROWS_OUT_OF_ORDER')
    hashes=manifest['file_hashes']
    ensure(isinstance(hashes,dict) and len(hashes)==1003,'S04_FILE_HASH_COUNT')
    seen=set()
    for r in ordered:
        for suffix,field,key in [('body','body_evidence_member','extracted_body_sha256'),('header','header_evidence_member','extracted_header_sha256')]:
            rel=r[field]
            ensure(rel.startswith('bodies/') and rel.endswith('_'+suffix+'.txt'),'BODY_HEADER_RELATIVE_PATH_INVALID')
            ensure(rel not in seen,'DUPLICATE_S04_MEMBER');seen.add(rel)
            dg=sha_file(safe_s04_member(root,rel))
            ensure(dg==r[key] and dg==hashes[rel],'S04_EVIDENCE_MEMBER_HASH_FAILURE')
    ensure(len(seen)==1000 and set(hashes)==seen|{'neutral_semantic_evidence.jsonl','semantic_rule_v2.json','reason_precedence_v2.json'},'S04_FILES_MISMATCH')
    for n,v in hashes.items():ensure(sha_file(safe_s04_member(root,n))==v,'S04_HASH_MISMATCH__'+n)
    ensure(hashes['neutral_semantic_evidence.jsonl']==esha,'S04_EVIDENCE_HASH_MISMATCH')
    ensure(manifest['source_hashes']['semantic_rule']==hashes['semantic_rule_v2.json'],'S04_SEMANTIC_SOURCE_DRIFT')
    ensure(manifest['source_hashes']['reason_precedence']==hashes['reason_precedence_v2.json'],'S04_REASON_SOURCE_DRIFT')
    if real:
        ensure(hashes['semantic_rule_v2.json']==PIN_SEMANTIC,'REAL_SEMANTIC_RULE_MISMATCH')
        ensure(hashes['reason_precedence_v2.json']==PIN_PRECEDENCE,'REAL_REASON_PRECEDENCE_MISMATCH')
    sums=safe_s04_member(root,'SHA256SUMS.txt').read_text().splitlines()
    sumdict={}
    for line in sums:
        bits=line.split('  ',1);ensure(len(bits)==2 and bits[1] not in sumdict,'INVALID_S04_SUMS')
        sumdict[bits[1]]=bits[0]
    ensure(set(sumdict)==set(hashes)|{'s04_primary_input_manifest.json'},'S04_CHECKSUM_COVERAGE')
    for name,want in sumdict.items():ensure(sha_file(safe_s04_member(root,name))==want,'S04_CHECKSUM_MISMATCH')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    ensure(actual==set(sumdict)|{'SHA256SUMS.txt'},'UNEXPECTED_S04_FILES')
    return {'root':str(root),'manifest_sha256':msha,'neutral_sha256':esha,
            'semantic_rule_sha256':hashes['semantic_rule_v2.json'],
            'precedence_sha256':hashes['reason_precedence_v2.json'],
            'rows':ordered,'body_header_verified':len(seen)}

def build_identity_manifest(info):
    rows=info['rows']
    contract=build_partition_manifest(rows,25,info['manifest_sha256'])
    verify_manifest(contract,rows)
    units=[]
    for entry in contract['units']:
        bound={**entry,
            's04_manifest_sha256':info['manifest_sha256'],
            's04_neutral_evidence_sha256':info['neutral_sha256'],
            'semantic_rule_sha256':info['semantic_rule_sha256'],
            'reason_precedence_sha256':info['precedence_sha256'],
            'partition_rule_sha256':RULE_SHA,
            'identity_sequence_sha256':digest(entry['canonical_source_identities'])}
        units.append(bound)
    out={'artifact_id':ARTIFACT_ID,'batch_id':'BATCH_0004','partition_rule':RULE,
         'partition_rule_sha256':RULE_SHA,'partition_size':25,'partition_count':20,
         'position_domain':[1501,2000],'record_count':500,
         'unique_canonical_identities':500,'coverage_count':500,'overlap_count':0,
         'omission_count':0,'duplicate_identity_count':0,'duplicate_position_count':0,
         'content_dependent_assignment':False,
         's04_manifest_sha256':info['manifest_sha256'],
         's04_evidence_sha256':info['neutral_sha256'],
         'semantic_rule_sha256':info['semantic_rule_sha256'],
         'reason_precedence_sha256':info['precedence_sha256'],
         'contract_sha256':digest(contract),'units':units}
    verify_identity_manifest(out,info)
    return out,contract

def verify_identity_manifest(out, info):
    fresh,contract = _expected_manifest(info)
    ensure(out==fresh,'REAL_PARTITION_MANIFEST_CONTENT_TAMPERED')
    ensure(contract['partition_count']==20 and all(x['row_count']==25 for x in contract['units']),'WRONG_PARTITION_UNITS')
    return True

def _expected_manifest(info):
    contract=build_partition_manifest(info['rows'],25,info['manifest_sha256'])
    units=[{**u, 's04_manifest_sha256':info['manifest_sha256'],
           's04_neutral_evidence_sha256':info['neutral_sha256'],
           'semantic_rule_sha256':info['semantic_rule_sha256'],
           'reason_precedence_sha256':info['precedence_sha256'],
           'partition_rule_sha256':RULE_SHA,
           'identity_sequence_sha256':digest(u['canonical_source_identities'])} for u in contract['units']]
    obj={'artifact_id':ARTIFACT_ID,'batch_id':'BATCH_0004','partition_rule':RULE,
         'partition_rule_sha256':RULE_SHA,'partition_size':25,'partition_count':20,
         'position_domain':[1501,2000],'record_count':500,
         'unique_canonical_identities':500,'coverage_count':500,'overlap_count':0,
         'omission_count':0,'duplicate_identity_count':0,'duplicate_position_count':0,
         'content_dependent_assignment':False,
         's04_manifest_sha256':info['manifest_sha256'],
         's04_evidence_sha256':info['neutral_sha256'],
         'semantic_rule_sha256':info['semantic_rule_sha256'],
         'reason_precedence_sha256':info['precedence_sha256'],
         'contract_sha256':digest(contract),'units':units}
    return obj,contract

def verify_local_release():
    release=Path(__file__).resolve().parent
    mf=release/'release_integrity_manifest_v1.json'
    ensure(mf.is_file() and not mf.is_symlink(),'RELEASE_INTEGRITY_MANIFEST_MISSING')
    obj=json.loads(mf.read_text(encoding='utf-8'))
    ensure(obj.get('task_id')=='POST_C6_Q1_2027_D1_BODY_BATCH0004_SIZE25_REAL_PARTITION_MANIFEST_AND_LIVE_INTEGRATION_BUILD_V1',
           'RELEASE_TASK_ID_MISMATCH')
    files=obj.get('file_sha256')
    ensure(isinstance(files,dict) and len(files)>=10,'RELEASE_INTEGRITY_INCOMPLETE')
    for rel,want in files.items():
        ensure(isinstance(rel,str) and '..' not in Path(rel).parts and not Path(rel).is_absolute(),'RELEASE_RELATIVE_PATH_UNSAFE')
        ensure(sha_file(release/rel)==want,'RELEASE_ARTIFACT_DRIFT__'+rel)
    ensure(sha_file(release/'checkpoint_resume_nonproduction_v1.py')==PIN_CHECKPOINT,'CHECKPOINT_REFERENCE_HASH_DRIFT')
    ensure(sha_file(release/'checkpoint_manifest_schema_v1.json')==PIN_SCHEMA,'SCHEMA_REFERENCE_HASH_DRIFT')
    ensure(sha_file(release/'frozen_v3_orchestrator_reference.py')==PIN_V3,'V3_REFERENCE_HASH_DRIFT')
    ensure(sha_file(release/'firewall_v2.py')==PIN_FIREWALL,'FIREWALL_REFERENCE_HASH_DRIFT')
    print('RELEASE_INTEGRITY_HASHES = PASS')

def historical_mac_precheck():
    home=Path.home()/'Downloads'
    old=home/'batch0004_real_semantic_recovery_attempt_v3'/'real_batch0004_semantic_recovery_v3_driver.py'
    ensure(old.is_file() and not old.is_symlink(),'ACCEPTED_REAL_V3_DRIVER_MISSING')
    spec=importlib.util.spec_from_file_location('preserved_real_v3_driver',old)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    state=module.verify_preserved_state()  # READ ONLY; checks historical S03, S04, stopped attempts, repo.
    v3_root=home/'batch0004_s05_completion_gate_recovery_v3'
    ensure(sha_file(v3_root/module.V3_NAME)==PIN_V3,'LIVE_V3_SOURCE_NOT_ACCEPTED')
    ensure(sha_file(v3_root/'firewall_v2.py')==PIN_FIREWALL,'LIVE_FIREWALL_NOT_ACCEPTED')
    ck=home/'batch0004_checkpoint_resume_nonproduction_v1'
    if ck.exists():
        ensure(sha_file(ck/'checkpoint_resume_nonproduction_v1.py')==PIN_CHECKPOINT,'CHECKPOINT_BASELINE_MISMATCH')
        ensure(sha_file(ck/'checkpoint_manifest_schema_v1.json')==PIN_SCHEMA,'CHECKPOINT_SCHEMA_MISMATCH')
    current_run=state['attempt']/'real_batch0004_v3_run'
    s04=current_run/'S04_PRIMARY_INPUT_FREEZE'
    ensure(current_run.is_dir() and s04.is_dir(), 'STOPPED_REAL_V3_S04_MISSING')
    failed_s05=current_run/'S05_PRIMARY_SEMANTIC_ADJUDICATION'
    for filename,pin in (
        ('primary_executor_attempt_manifest.json','cd1b2572d8dd7015b8438144236fb1cf268129f1830f640f0459fe4a04c5053d'),
        ('primary_executor_raw_stdout.jsonl','a70da9f0d4e169cfec906609007e36f54378d64211e08d97c06f3c223f801308'),
        ('primary_executor_attempt_final_message.txt','0479ee06a1f0a6a25d66dc2256aaaae11428af391cb10bd06b4427000b047d46')):
        ensure(sha_file(failed_s05/filename)==pin,'STOPPED_V3_S05_EVIDENCE_DRIFT__'+filename)
    transitions=[json.loads(x) for x in (current_run/'state_transition_log.jsonl').read_text().splitlines() if x.strip()]
    ensure(len(transitions)==1 and transitions[0]['STATE']=='S04_PRIMARY_INPUT_FREEZE' and transitions[0]['STATUS']=='PASS','REAL_V3_ATTEMPT_STATE_DRIFT')
    ensure(not (current_run/'S06_PRIMARY_LEDGER_FREEZE').exists(),'REAL_V3_DOWNSTREAM_UNEXPECTED')
    # Advisory process check; protects against an accidentally active same-task runner.
    processes=subprocess.run(['ps','-axo','command'],capture_output=True,text=True,check=True).stdout.splitlines()
    for proc in processes:
        if ('real_batch0004_semantic_recovery_v3_driver.py --execute' in proc
            or 'd1_batch0004_s04_s16_executable_orchestrator_v3.py --execute' in proc
            or 'd1_batch0004_s04_s16_executable_orchestrator_v3.py --config' in proc):
            raise ManifestStop('REAL_SEMANTIC_EXECUTION_PROCESS_DETECTED')
    return s04

def exclusive_write(p, data):
    ensure(not p.exists() and not p.is_symlink(),'OUTPUT_ALREADY_EXISTS')
    with p.open('xb') as f:
        f.write(data);f.flush();os.fsync(f.fileno())
    ensure(p.read_bytes()==data,'OUTPUT_READBACK_FAIL')
    return sha_file(p)

def main():
    ap=argparse.ArgumentParser()
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--preflight-only',action='store_true')
    group.add_argument('--build-real-manifest',action='store_true')
    group.add_argument('--verify-built-manifest',action='store_true')
    args=ap.parse_args()
    # Mandatory release identity and historical checks before artifact mutation.
    verify_local_release()
    s04=historical_mac_precheck()
    info=verify_s04(s04,real=True)
    out,contract=build_identity_manifest(info)
    print('FRESH_HISTORICAL_PRESERVATION = PASS')
    print('REAL_S04_MANIFEST_SHA256 =',info['manifest_sha256'])
    print('REAL_S04_EVIDENCE_SHA256 =',info['neutral_sha256'])
    print('REAL_PARTITION_ROWS = 500')
    print('REAL_PARTITION_COUNT = 20')
    print('REAL_PARTITION_COVERAGE = 500 / 500')
    print('REAL_PARTITION_OVERLAP = 0')
    print('REAL_PARTITION_OMISSIONS = 0')
    print('REAL_PARTITION_DUPLICATES = 0')
    print('PARTITION_RULE_SHA256 =',RULE_SHA)
    out_dir=Path.home()/'Downloads'/'batch0004_REAL_size25_identity_bound_partition_manifest_v1'
    if args.preflight_only:
        print('REAL_PARTITION_MANIFEST_BUILD_STATUS = PENDING__PREFLIGHT_PASS')
        print('REAL_PARTITION_MANIFEST_CREATED =', 'YES__PRESERVED' if out_dir.exists() else 'NO')
        return
    if args.verify_built_manifest:
        ensure(out_dir.is_dir() and not out_dir.is_symlink(),'FROZEN_MANIFEST_OUTPUT_MISSING')
        att=json.loads((out_dir/'freeze_attestation.json').read_text())
        a=out_dir/'real_partition_manifest.json';b=out_dir/'partition_contract.json'
        ensure(sha_file(a)==att['manifest_sha256'] and sha_file(b)==att['contract_sha256'],
               'FROZEN_PARTITION_FILE_HASH_DRIFT')
        ensure(json.loads(a.read_text())==out and json.loads(b.read_text())==contract,
               'FROZEN_PARTITION_CONTENT_DRIFT')
        ensure(att['rule_sha256']==RULE_SHA and
               att['source_s04_manifest_sha256']==info['manifest_sha256'] and
               att['source_s04_evidence_sha256']==info['neutral_sha256'],
               'FROZEN_PARTITION_BINDING_DRIFT')
        print('REAL_PARTITION_MANIFEST_BUILD_STATUS = PASS__READ_ONLY_VERIFIED')
        print('PARTITION_RULE_FROZEN = YES')
        print('REAL_PARTITION_MANIFEST_SHA256 =',att['manifest_sha256'])
        print('REAL_SEMANTIC_EXECUTION_PERFORMED = NO')
        return
    ensure(not out_dir.exists() and not out_dir.is_symlink(),'REAL_MANIFEST_OUTPUT_PREEXISTS__STOP')
    out_dir.mkdir(mode=0o700,exist_ok=False)
    manifest_bytes=(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    contract_bytes=(json.dumps(contract,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    h1=exclusive_write(out_dir/'real_partition_manifest.json',manifest_bytes)
    h2=exclusive_write(out_dir/'partition_contract.json',contract_bytes)
    metadata={'manifest_sha256':h1,'contract_sha256':h2,'rule_sha256':RULE_SHA,
              'source_s04_manifest_sha256':info['manifest_sha256'],
              'source_s04_evidence_sha256':info['neutral_sha256'],
              'semantic_rule_sha256':info['semantic_rule_sha256'],
              'reason_precedence_sha256':info['precedence_sha256'],
              'validation':'PASS','semantic_execution_performed':False}
    exclusive_write(out_dir/'freeze_attestation.json',(json.dumps(metadata,sort_keys=True,indent=2)+'\n').encode())
    reread=json.loads((out_dir/'real_partition_manifest.json').read_text())
    verify_identity_manifest(reread,info)
    ensure(sha_file(out_dir/'real_partition_manifest.json')==h1,'MANIFEST_FROZEN_BYTES_CHANGED')
    print('REAL_PARTITION_MANIFEST_BUILD_STATUS = PASS')
    print('PARTITION_RULE_FROZEN = YES')
    print('REAL_PARTITION_MANIFEST_SHA256 =',h1)
    print('REAL_PARTITION_MANIFEST_PATH =',out_dir/'real_partition_manifest.json')
    print('REAL_SEMANTIC_EXECUTION_PERFORMED = NO')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('CONTROLLED_STOP__'+type(exc).__name__+'__'+str(exc),flush=True)
        raise SystemExit(2)
