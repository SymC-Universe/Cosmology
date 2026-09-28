from __future__ import annotations

import pathlib
import sys

import h5py
import numpy as np
import pytest

HERE=pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

from gevolution_particle_lineage import load_particle_snapshot, lineage_report


DTYPE=np.dtype([
    ('ID','<i8'),
    ('positionX','<f8'),('positionY','<f8'),('positionZ','<f8'),
    ('velocityX','<f8'),('velocityY','<f8'),('velocityZ','<f8'),
])


def _write(path,ids,offset=0.0,missing_velocity_z=False):
    dtype=DTYPE
    if missing_velocity_z:
        dtype=np.dtype([x for x in DTYPE.descr if x[0] != 'velocityZ'])
    data=np.zeros(len(ids),dtype=dtype)
    data['ID']=ids
    for i,name in enumerate(('positionX','positionY','positionZ')):
        data[name]=(np.arange(len(ids))+i+offset)/100.0
    for i,name in enumerate(('velocityX','velocityY')):
        data[name]=(np.arange(len(ids))-i+offset)/1000.0
    if 'velocityZ' in data.dtype.names:
        data['velocityZ']=(np.arange(len(ids))+2+offset)/1000.0
    with h5py.File(path,'w') as h:
        h.create_dataset('data',data=data)


def test_lineage_accepts_same_unique_ids_in_different_record_order(tmp_path):
    a=tmp_path/'a.h5'
    b=tmp_path/'b.h5'
    ids=np.array([10,20,30,40],dtype=np.int64)
    _write(a,ids,0.0)
    _write(b,ids[[2,0,3,1]],1.0)
    report=lineage_report([a,b])
    assert report['lineage_qualified'] is True
    assert report['reference_particle_count'] == 4
    assert all(x['ids_unique'] for x in report['snapshots'])


def test_lineage_refuses_duplicate_ids(tmp_path):
    a=tmp_path/'a.h5'
    b=tmp_path/'b.h5'
    _write(a,np.array([1,2,3,4]))
    _write(b,np.array([1,2,2,4]),1.0)
    report=lineage_report([a,b])
    assert report['lineage_qualified'] is False
    assert report['snapshots'][1]['ids_unique'] is False


def test_lineage_refuses_changed_id_set(tmp_path):
    a=tmp_path/'a.h5'
    b=tmp_path/'b.h5'
    _write(a,np.array([1,2,3,4]))
    _write(b,np.array([1,2,3,5]),1.0)
    report=lineage_report([a,b])
    assert report['lineage_qualified'] is False
    assert report['snapshots'][1]['same_id_set_as_snapshot_0'] is False


def test_loader_refuses_missing_required_particle_field(tmp_path):
    p=tmp_path/'bad.h5'
    _write(p,np.array([1,2,3]),missing_velocity_z=True)
    with pytest.raises(ValueError,match='missing particle fields'):
        load_particle_snapshot(p)
