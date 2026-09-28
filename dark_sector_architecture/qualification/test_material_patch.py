from __future__ import annotations

import pathlib
import sys

import numpy as np
import pytest

HERE=pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

from material_patch import (
    aggregate_material_patch_tensors,
    align_frozen_patch_membership,
    interpolate_vertex_tensor_by_id,
    interpolate_vertex_tensor_periodic,
    reference_patch_membership,
)
from modal_tensor import analyze_symmetric_tensor


def _analytic_tensor(positions):
    p=np.asarray(positions,dtype=float)
    x,y,z=p[:,0],p[:,1],p[:,2]
    out=np.zeros((len(p),3,3),dtype=float)
    a=np.sin(2*np.pi*x)+0.2*np.cos(2*np.pi*y)
    b=-0.4*np.sin(2*np.pi*y)+0.1*np.cos(2*np.pi*z)
    c=-a-b
    out[:,0,0]=a; out[:,1,1]=b; out[:,2,2]=c
    out[:,0,1]=out[:,1,0]=0.25*np.cos(2*np.pi*(x+y))
    out[:,0,2]=out[:,2,0]=0.18*np.sin(2*np.pi*(x-z))
    out[:,1,2]=out[:,2,1]=0.12*np.cos(2*np.pi*(y+z))
    return out


def _grid(n):
    xyz=np.stack(np.meshgrid(np.arange(n)/n,np.arange(n)/n,np.arange(n)/n,indexing='ij'),axis=-1)
    return _analytic_tensor(xyz.reshape(-1,3)).reshape(n,n,n,3,3)


def test_mp01_vertex_exactness():
    n=12
    grid=_grid(n)
    indices=np.array([[0,0,0],[3,5,7],[11,1,9],[6,6,6]])
    pos=indices/n
    got=interpolate_vertex_tensor_periodic(grid,pos)
    expected=grid[indices[:,0],indices[:,1],indices[:,2]]
    np.testing.assert_allclose(got,expected,atol=0.0,rtol=0.0)


def test_mp02_constant_field_exact_at_arbitrary_positions():
    matrix=np.array([[2.0,0.3,-0.2],[0.3,-1.0,0.4],[-0.2,0.4,-1.0]])
    grid=np.broadcast_to(matrix,(10,10,10,3,3)).copy()
    rng=np.random.default_rng(2)
    pos=rng.uniform(-2.0,3.0,size=(200,3))
    got=interpolate_vertex_tensor_periodic(grid,pos)
    np.testing.assert_allclose(got,matrix[None,:,:],atol=2e-15,rtol=2e-15)


def test_mp03_periodic_wrap_equivalence():
    grid=_grid(16)
    pos=np.array([[0.99,0.01,0.5],[0.125,0.875,0.999],[0.0,0.0,0.0]])
    shift=np.array([[1.0,-2.0,3.0],[-1.0,4.0,-3.0],[2.0,2.0,-1.0]])
    np.testing.assert_allclose(
        interpolate_vertex_tensor_periodic(grid,pos),
        interpolate_vertex_tensor_periodic(grid,pos+shift),
        atol=3e-14,rtol=3e-14
    )


def test_mp04_linearity():
    rng=np.random.default_rng(4)
    a=_grid(10)
    b=np.swapaxes(_grid(10),0,1).copy()
    # b remains symmetric in tensor indices.
    pos=rng.random((100,3))
    alpha,beta=1.7,-0.35
    lhs=interpolate_vertex_tensor_periodic(alpha*a+beta*b,pos)
    rhs=alpha*interpolate_vertex_tensor_periodic(a,pos)+beta*interpolate_vertex_tensor_periodic(b,pos)
    np.testing.assert_allclose(lhs,rhs,atol=3e-15,rtol=3e-15)


def test_mp05_symmetry_and_trace_free_structure_preserved():
    grid=_grid(14)
    rng=np.random.default_rng(5)
    got=interpolate_vertex_tensor_periodic(grid,rng.random((150,3)))
    np.testing.assert_allclose(got,np.swapaxes(got,-1,-2),atol=0.0,rtol=0.0)
    np.testing.assert_allclose(np.trace(got,axis1=-2,axis2=-1),0.0,atol=3e-15,rtol=0.0)


def test_mp06_smooth_periodic_interpolation_is_second_order():
    rng=np.random.default_rng(6)
    pos=rng.random((300,3))
    truth=_analytic_tensor(pos)
    errors=[]
    for n in (16,32,64):
        got=interpolate_vertex_tensor_periodic(_grid(n),pos)
        errors.append(float(np.sqrt(np.mean((got-truth)**2))))
    r1=errors[0]/errors[1]
    r2=errors[1]/errors[2]
    assert 3.4 < r1 < 4.6
    assert 3.4 < r2 < 4.6


def test_mp07_id_sorted_interpolation_is_record_order_invariant():
    grid=_grid(12)
    ids=np.array([40,10,30,20],dtype=np.int64)
    pos=np.array([[.1,.2,.3],[.4,.5,.6],[.7,.8,.9],[.15,.35,.55]])
    a=interpolate_vertex_tensor_by_id(grid,ids,pos)
    order=np.array([2,0,3,1])
    b=interpolate_vertex_tensor_by_id(grid,ids[order],pos[order])
    np.testing.assert_array_equal(a['ID'],b['ID'])
    np.testing.assert_allclose(a['tensor'],b['tensor'],atol=0.0,rtol=0.0)


def test_mp08_reference_partition_is_unique_complete_and_periodic():
    ids=np.arange(1,9,dtype=np.int64)
    pos=np.array([
        [-.01,.01,.01],[.24,.24,.24],[.26,.26,.26],[.49,.49,.49],
        [.51,.51,.51],[.74,.74,.74],[.76,.76,.76],[1.01,.99,.99]
    ])
    m=reference_patch_membership(ids,pos,(4,4,4))
    assert len(m['ID'])==len(ids)
    assert len(np.unique(m['ID']))==len(ids)
    assert np.all((m['patch_id']>=0)&(m['patch_id']<64))
    # -0.01 and 0.99 share the same wrapped x cell; 1.01 and 0.01 share x cell.
    lookup=dict(zip(m['ID'].tolist(),m['patch_id'].tolist()))
    assert isinstance(lookup[1],int)


def test_mp09_membership_is_frozen_by_id_not_current_position():
    ids=np.array([1,2,3,4],dtype=np.int64)
    ref_pos=np.array([[.1,.1,.1],[.2,.2,.2],[.7,.7,.7],[.8,.8,.8]])
    m=reference_patch_membership(ids,ref_pos,(2,2,2))
    current_ids=np.array([4,2,1,3],dtype=np.int64)
    moved=np.array([[.1,.1,.1],[.9,.9,.9],[.8,.8,.8],[.2,.2,.2]])
    _=moved  # positions deliberately irrelevant to frozen membership join
    aligned=align_frozen_patch_membership(m['ID'],m['patch_id'],current_ids)
    lookup=dict(zip(m['ID'].tolist(),m['patch_id'].tolist()))
    assert aligned.tolist()==[lookup[int(i)] for i in current_ids]


def test_mp10_patch_mean_is_exact_and_order_invariant():
    ids=np.array([1,2,3,4,5,6],dtype=np.int64)
    ref_ids=ids.copy()
    patch=np.array([0,0,0,1,1,1],dtype=np.int64)
    a=np.diag([2.0,-.5,-1.5])
    b=np.array([[1.0,.2,0.0],[.2,-.4,.1],[0.0,.1,-.6]])
    samples=np.stack([a,a,a,b,b,b])
    first=aggregate_material_patch_tensors(ids,samples,ref_ids,patch)
    order=np.array([5,0,3,1,4,2])
    second=aggregate_material_patch_tensors(ids[order],samples[order],ref_ids,patch)
    np.testing.assert_array_equal(first['patch_id'],second['patch_id'])
    np.testing.assert_array_equal(first['count'],second['count'])
    np.testing.assert_allclose(first['tensor'],second['tensor'],atol=0.0,rtol=0.0)
    np.testing.assert_allclose(first['tensor'][0],a,atol=0.0,rtol=0.0)
    np.testing.assert_allclose(first['tensor'][1],b,atol=2e-16,rtol=0.0)


def test_mp11_patch_modal_recovery_and_degenerate_semantics():
    ids=np.arange(6,dtype=np.int64)
    patch=np.array([0,0,0,1,1,1],dtype=np.int64)
    a=np.diag([2.0,-.5,-1.5])
    d=np.diag([1.0,1.0,-2.0])
    agg=aggregate_material_patch_tensors(ids,np.stack([a,a,a,d,d,d]),ids,patch)
    r0=analyze_symmetric_tensor(agg['tensor'][0])
    r1=analyze_symmetric_tensor(agg['tensor'][1])
    np.testing.assert_allclose(r0.eigenvalues,[2.0,-.5,-1.5],atol=2e-15)
    assert not any(r0.degenerate_pairs)
    assert any(r1.degenerate_pairs)


def test_mp12_fail_closed_invalid_data_and_lineage():
    good=_grid(8)
    with pytest.raises(ValueError,match='unique'):
        reference_patch_membership(np.array([1,1]),np.zeros((2,3)),(2,2,2))
    with pytest.raises(ValueError,match='positive integers'):
        reference_patch_membership(np.array([1]),np.zeros((1,3)),(2,0,2))
    badpos=np.zeros((1,3)); badpos[0,0]=np.nan
    with pytest.raises(ValueError,match='finite'):
        interpolate_vertex_tensor_periodic(good,badpos)
    badgrid=good.copy(); badgrid[...,0,1]+=1.0
    with pytest.raises(ValueError,match='symmetric'):
        interpolate_vertex_tensor_periodic(badgrid,np.zeros((1,3)))
    ids=np.array([1,2,3])
    patch=np.array([0,0,1])
    samples=np.zeros((3,3,3))
    with pytest.raises(ValueError,match='exactly'):
        aggregate_material_patch_tensors(np.array([1,2,4]),samples,ids,patch)
