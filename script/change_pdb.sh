kubectl patch pdb log-pdb --type='json' -p='[{"op": "replace", "path": "/spec/minAvailable", "value": 0}]'
