"""Durable P0-Q report for material-patch tensor interpolation qualification."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

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
    xyz=np.stack(np.meshgrid(np.arange(n)/n,np.arange(n)/n,np.arange(n)/n,indexing="ij"),axis=-1)
    return _analytic_tensor(xyz.reshape(-1,3)).reshape(n,n,n,3,3)


def _pass(case_id,purpose,**metrics):
    return {"case_id":case_id,"purpose":purpose,"status":"PASS",**metrics}


def build_report():
    cases=[]

    n=12; grid=_grid(n)
    idx=np.array([[0,0,0],[3,5,7],[11,1,9],[6,6,6]])
    pos=idx/n
    got=interpolate_vertex_tensor_periodic(grid,pos)
    expected=grid[idx[:,0],idx[:,1],idx[:,2]]
    err=float(np.max(np.abs(got-expected)))
    cases.append(_pass("MP-01","vertex exactness",max_abs_error=err) if err==0.0 else {"case_id":"MP-01","purpose":"vertex exactness","status":"FAIL","max_abs_error":err})

    matrix=np.array([[2.0,.3,-.2],[.3,-1.0,.4],[-.2,.4,-1.0]])
    const=np.broadcast_to(matrix,(10,10,10,3,3)).copy()
    rng=np.random.default_rng(22)
    arbitrary=rng.uniform(-2.0,3.0,size=(300,3))
    cerr=float(np.max(np.abs(interpolate_vertex_tensor_periodic(const,arbitrary)-matrix)))
    cases.append(_pass("MP-02","constant tensor exactness",max_abs_error=cerr) if cerr<1e-13 else {"case_id":"MP-02","purpose":"constant tensor exactness","status":"FAIL","max_abs_error":cerr})

    p=np.array([[.99,.01,.5],[.125,.875,.999],[0.,0.,0.]])
    shift=np.array([[1.,-2.,3.],[-1.,4.,-3.],[2.,2.,-1.]])
    wrap=float(np.max(np.abs(interpolate_vertex_tensor_periodic(_grid(16),p)-interpolate_vertex_tensor_periodic(_grid(16),p+shift))))
    cases.append(_pass("MP-03","periodic wrap equivalence",max_abs_error=wrap) if wrap<1e-12 else {"case_id":"MP-03","purpose":"periodic wrap equivalence","status":"FAIL","max_abs_error":wrap})

    a=_grid(10); b=np.swapaxes(_grid(10),0,1).copy(); pts=rng.random((150,3)); alpha=1.7; beta=-.35
    lhs=interpolate_vertex_tensor_periodic(alpha*a+beta*b,pts)
    rhs=alpha*interpolate_vertex_tensor_periodic(a,pts)+beta*interpolate_vertex_tensor_periodic(b,pts)
    lin=float(np.max(np.abs(lhs-rhs)))
    cases.append(_pass("MP-04","linearity",max_abs_error=lin) if lin<1e-13 else {"case_id":"MP-04","purpose":"linearity","status":"FAIL","max_abs_error":lin})

    vals=interpolate_vertex_tensor_periodic(_grid(14),rng.random((200,3)))
    sym=float(np.max(np.abs(vals-np.swapaxes(vals,-1,-2))))
    trace=float(np.max(np.abs(np.trace(vals,axis1=-2,axis2=-1))))
    status="PASS" if sym<1e-13 and trace<1e-13 else "FAIL"
    cases.append({"case_id":"MP-05","purpose":"symmetry and trace-free preservation","status":status,"symmetry_max_abs":sym,"trace_max_abs":trace})

    sample=rng.random((400,3)); truth=_analytic_tensor(sample); errors=[]
    for n in (16,32,64):
        interp=interpolate_vertex_tensor_periodic(_grid(n),sample)
        errors.append(float(np.sqrt(np.mean((interp-truth)**2))))
    ratios=[errors[0]/errors[1],errors[1]/errors[2]]
    status="PASS" if all(3.4<x<4.6 for x in ratios) else "FAIL"
    cases.append({"case_id":"MP-06","purpose":"second-order smooth periodic interpolation","status":status,"grid_sizes":[16,32,64],"rms_errors":errors,"refinement_error_ratios":ratios})

    ids=np.array([40,10,30,20]); p=np.array([[.1,.2,.3],[.4,.5,.6],[.7,.8,.9],[.15,.35,.55]])
    first=interpolate_vertex_tensor_by_id(_grid(12),ids,p); order=np.array([2,0,3,1]); second=interpolate_vertex_tensor_by_id(_grid(12),ids[order],p[order])
    reorder=float(np.max(np.abs(first["tensor"]-second["tensor"])))
    ok=np.array_equal(first["ID"],second["ID"]) and reorder==0.0
    cases.append({"case_id":"MP-07","purpose":"ID-keyed reorder invariance","status":"PASS" if ok else "FAIL","max_abs_error":reorder})

    ids8=np.arange(1,9,dtype=np.int64); refp=np.array([[-.01,.01,.01],[.24,.24,.24],[.26,.26,.26],[.49,.49,.49],[.51,.51,.51],[.74,.74,.74],[.76,.76,.76],[1.01,.99,.99]])
    membership=reference_patch_membership(ids8,refp,(4,4,4))
    complete=(len(membership["ID"])==8 and len(np.unique(membership["ID"]))==8 and np.all((membership["patch_id"]>=0)&(membership["patch_id"]<64)))
    cases.append({"case_id":"MP-08","purpose":"deterministic complete reference partition","status":"PASS" if complete else "FAIL","particle_count":8,"nonempty_patch_count":int(len(np.unique(membership["patch_id"])))})

    ids4=np.array([1,2,3,4]); rp=np.array([[.1,.1,.1],[.2,.2,.2],[.7,.7,.7],[.8,.8,.8]])
    frozen=reference_patch_membership(ids4,rp,(2,2,2)); current=np.array([4,2,1,3]); aligned=align_frozen_patch_membership(frozen["ID"],frozen["patch_id"],current)
    lookup=dict(zip(frozen["ID"].tolist(),frozen["patch_id"].tolist())); expected=np.array([lookup[int(i)] for i in current])
    cases.append({"case_id":"MP-09","purpose":"ID-frozen material membership","status":"PASS" if np.array_equal(aligned,expected) else "FAIL","aligned_patch_ids":aligned.tolist()})

    ids6=np.array([1,2,3,4,5,6]); patch=np.array([0,0,0,1,1,1]); ta=np.diag([2.0,-.5,-1.5]); tb=np.array([[1.0,.2,0.0],[.2,-.4,.1],[0.0,.1,-.6]])
    samples=np.stack([ta,ta,ta,tb,tb,tb]); agg=aggregate_material_patch_tensors(ids6,samples,ids6,patch); ord2=np.array([5,0,3,1,4,2]); agg2=aggregate_material_patch_tensors(ids6[ord2],samples[ord2],ids6,patch)
    meanerr=float(np.max(np.abs(agg["tensor"]-np.stack([ta,tb])))); ordererr=float(np.max(np.abs(agg["tensor"]-agg2["tensor"])))
    cases.append({"case_id":"MP-10","purpose":"patch mean exactness and order invariance","status":"PASS" if meanerr<1e-13 and ordererr<1e-13 else "FAIL","mean_max_abs_error":meanerr,"reorder_max_abs_error":ordererr})

    deg=np.diag([1.0,1.0,-2.0]); agg=aggregate_material_patch_tensors(ids6,np.stack([ta,ta,ta,deg,deg,deg]),ids6,patch); r0=analyze_symmetric_tensor(agg["tensor"][0]); r1=analyze_symmetric_tensor(agg["tensor"][1])
    modal_ok=(not any(r0.degenerate_pairs) and any(r1.degenerate_pairs) and np.max(np.abs(r0.eigenvalues-np.array([2.0,-.5,-1.5])))<1e-13)
    cases.append({"case_id":"MP-11","purpose":"patch modal recovery and degeneracy semantics","status":"PASS" if modal_ok else "FAIL","nondegenerate_eigenvalues":r0.eigenvalues.tolist(),"degenerate_pairs_control":list(r1.degenerate_pairs)})

    refusals={}
    trials=[]
    try: reference_patch_membership(np.array([1,1]),np.zeros((2,3)),(2,2,2)); refusals["duplicate_ids"]="FAILED_TO_REFUSE"
    except ValueError as e: refusals["duplicate_ids"]=str(e)
    try: reference_patch_membership(np.array([1]),np.zeros((1,3)),(2,0,2)); refusals["patch_shape"]="FAILED_TO_REFUSE"
    except ValueError as e: refusals["patch_shape"]=str(e)
    badpos=np.zeros((1,3)); badpos[0,0]=np.nan
    try: interpolate_vertex_tensor_periodic(_grid(8),badpos); refusals["nonfinite_position"]="FAILED_TO_REFUSE"
    except ValueError as e: refusals["nonfinite_position"]=str(e)
    badgrid=_grid(8); badgrid[...,0,1]+=1.0
    try: interpolate_vertex_tensor_periodic(badgrid,np.zeros((1,3))); refusals["nonsymmetric_grid"]="FAILED_TO_REFUSE"
    except ValueError as e: refusals["nonsymmetric_grid"]=str(e)
    try: aggregate_material_patch_tensors(np.array([1,2,4]),np.zeros((3,3,3)),np.array([1,2,3]),np.array([0,0,1])); refusals["changed_id_set"]="FAILED_TO_REFUSE"
    except ValueError as e: refusals["changed_id_set"]=str(e)
    ok=all(v!="FAILED_TO_REFUSE" for v in refusals.values())
    cases.append({"case_id":"MP-12","purpose":"fail-closed lineage and invalid data","status":"PASS" if ok else "FAIL","refusals":refusals})

    outcome="MATERIAL_PATCH_INTERPOLATION_QUALIFIED_P0Q" if all(x["status"]=="PASS" for x in cases) else "MATERIAL_PATCH_INTERPOLATION_REFUSED"
    return {"protocol":"MATERIAL_PATCH_INTERPOLATION_QUALIFICATION_v0.1","stage":"P0-Q","scientific_claim_tested":False,"patch_scale_selected":False,"case_count":len(cases),"cases":cases,"outcome":outcome,"next_gate":"APQ/freeze late-time Band-L material relational development design"}


def main():
    p=argparse.ArgumentParser(); p.add_argument("--output",required=True); a=p.parse_args()
    report=build_report(); out=pathlib.Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"outcome":report["outcome"],"output":str(out)},sort_keys=True))


if __name__=="__main__": main()
