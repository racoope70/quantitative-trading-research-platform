"""Fresh-process verification using the existing checkpoint engine."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import np_support as n
c=n.bootstrap()
import checkpoint_resume_activation_trusted_v1 as core
root=n.ROOT/'fixtures'/sys.argv[1]/'state'
engine=core.CheckpointEngine(root,'PRIMARY');engine.verify()
u=engine.state['units'][11]
print(json.dumps({'checkpoint_sequence':engine.state['checkpoint_sequence'],
    'checkpoint_identity':engine.state['checkpoint_manifest_sha256'],
    'U0012':u['state'],'attempt_count':u['attempt_count'],
    'U0013':engine.state['units'][12]['state'],'U0013_attempt_count':engine.state['units'][12]['attempt_count'],
    'frozen_units':sum(x['state']=='FROZEN' for x in engine.state['units']),
    'engine_verification':'PASS','read_only':True,'audit':n.AUDIT},sort_keys=True))
