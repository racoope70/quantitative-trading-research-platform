"""Separate cooperative Owner publication process; the executor has no approval FD."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import np_support as support
c=support.bootstrap()
import owner_publication as owner
fd=int(sys.argv[1]);candidate=Path(sys.argv[2]);directory=Path(sys.argv[3]);pin=sys.argv[4];length=int(sys.argv[5])
print(json.dumps(owner.publish_model_b(candidate,pin,length,approval_fd=fd,directory=directory),sort_keys=True))
