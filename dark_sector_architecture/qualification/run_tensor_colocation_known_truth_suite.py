"""Durable P0-Q known-truth report for native tensor vertex co-location."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from tensor_colocation import (
    colocate_offdiagonal_component_to_vertices,
    colocate_symmetric_tensor_to_vertices,
    colocation_transfer_factor,
)


def _coords(n: int, shifts=(0.0,0.0,0.0)):
    axes=[(np.arange(n)+shifts[i])/n for i in range(3)]
    return np.meshgrid(*axes,indexing="ij")


def _mode_field(n, mode, shifts=(0.0,0.0,0.0)):
    x,y,z=_coords(n,shifts)
    return np.cos(2*np.pi*(mode[0]*x+mode[1]*y+mode[2]*z))


def _smooth_native_tensor(n: int):
    x,y,z=_coords(n)
    native=np.zeros((n,n,n,3,3),dtype=float)
    truth=np.zeros_like(native)
    d0=np.sin(2*np.pi*x)+0.2*np.cos(2*np.pi*y)
    d1=-0.3*np.sin(2*np.pi*y)+0.1*np.cos(2*np.pi*z)
    d2=-d0-d1
    for i,d in enumerate((d0,d1,d2)):
        native[...,i,i]=d
        truth[...,i,i]=d
    funcs={
        (0,1):lambda a,b,c:0.4*np.cos(2*np.pi*(a+2*b))+0.1*np.sin(2*np.pi*c),
        (0,2):lambda a,b,c:0.3*np.sin(2*np.pi*(a-c))+0.05*np.cos(4*np.pi*b),
        (1,2):lambda a,b,c:0.25*np.cos(2*np.pi*(b+c))+0.07*np.sin(2*np.pi*a),
    }
    for (i,j),fn in funcs.items():
        vertex=fn(x,y,z)
        shifts=[0.0,0.0,0.0]
        shifts[i]=0.5
        shifts[j]=0.5
        xs,ys,zs=_coords(n,shifts)
        staggered=fn(xs,ys,zs)
        truth[...,i,j]=truth[...,j,i]=vertex
        native[...,i,j]=native[...,j,i]=staggered
    return native,truth


def build_report():
    cases=[]

    rng=np.random.default_rng(11)
    tensor=np.zeros((8,8,8,3,3))
    for i in range(3):
        tensor[...,i,i]=rng.normal(size=(8,8,8))
    out=colocate_symmetric_tensor_to_vertices(tensor)
    diag_error=max(float(np.max(np.abs(out[...,i,i]-tensor[...,i,i]))) for i in range(3))
    cases.append({"case_id":"TC-01","purpose":"diagonal passthrough","status":"PASS" if diag_error==0.0 else "FAIL","max_abs_error":diag_error})

    n=7
    base=np.arange(n**3,dtype=float).reshape(n,n,n)
    actual=colocate_offdiagonal_component_to_vertices(base,0,2)
    expected=0.25*(base+np.roll(base,1,0)+np.roll(base,1,2)+np.roll(np.roll(base,1,0),1,2))
    err=float(np.max(np.abs(actual-expected)))
    cases.append({"case_id":"TC-02","purpose":"four-point periodic formula","status":"PASS" if err==0.0 else "FAIL","max_abs_error":err})

    native,_=_smooth_native_tensor(12)
    sym=colocate_symmetric_tensor_to_vertices(native)
    sym_err=float(np.max(np.abs(sym-np.swapaxes(sym,-1,-2))))
    cases.append({"case_id":"TC-03","purpose":"symmetry preservation","status":"PASS" if sym_err==0.0 else "FAIL","max_abs_error":sym_err})

    n=32; mode=(3,5,0)
    staggered=_mode_field(n,mode,(0.5,0.5,0.0))
    actual=colocate_offdiagonal_component_to_vertices(staggered,0,1)
    factor=colocation_transfer_factor(mode,n,0,1)
    expected=factor*_mode_field(n,mode)
    fourier_err=float(np.max(np.abs(actual-expected)))
    cases.append({"case_id":"TC-04","purpose":"single-mode phase removal and cosine transfer","status":"PASS" if fourier_err <= 2e-13 else "FAIL","transfer_factor":factor,"max_abs_error":fourier_err})

    errors=[]
    for n in (16,32,64):
        native,truth=_smooth_native_tensor(n)
        diff=colocate_symmetric_tensor_to_vertices(native)-truth
        errors.append(float(np.sqrt(np.mean(diff*diff))))
    ratios=[errors[0]/errors[1],errors[1]/errors[2]]
    smooth_pass=all(3.7<x<4.3 for x in ratios)
    cases.append({"case_id":"TC-05","purpose":"second-order smooth-field recovery","status":"PASS" if smooth_pass else "FAIL","grid_sizes":[16,32,64],"rms_errors":errors,"refinement_error_ratios":ratios})

    n=32; mode=(n//2,2,0)
    staggered=_mode_field(n,mode,(0.5,0.5,0.0))
    filtered=colocate_offdiagonal_component_to_vertices(staggered,0,1)
    factor=colocation_transfer_factor(mode,n,0,1)
    max_abs=float(np.max(np.abs(filtered)))
    cases.append({"case_id":"TC-06","purpose":"Nyquist attenuation without inversion","status":"PASS" if abs(factor)<1e-15 and max_abs<2e-13 else "FAIL","transfer_factor":factor,"filtered_max_abs":max_abs,"inverse_attempted":False})

    rng=np.random.default_rng(17)
    a=rng.normal(size=(9,9,9)); b=rng.normal(size=(9,9,9)); alpha=1.3; beta=-0.4
    lhs=colocate_offdiagonal_component_to_vertices(alpha*a+beta*b,1,2)
    rhs=alpha*colocate_offdiagonal_component_to_vertices(a,1,2)+beta*colocate_offdiagonal_component_to_vertices(b,1,2)
    lin_err=float(np.max(np.abs(lhs-rhs)))
    cases.append({"case_id":"TC-07","purpose":"linearity","status":"PASS" if lin_err<1e-13 else "FAIL","max_abs_error":lin_err})

    refusals={}
    good=np.zeros((8,8,8,3,3))
    trials=[]
    bad=good.copy(); bad[0,0,0,0,0]=np.nan; trials.append(("nonfinite",bad))
    trials.append(("shape",np.zeros((8,8,8,6))))
    trials.append(("noncubic",np.zeros((8,7,8,3,3))))
    badsym=good.copy(); badsym[...,0,1]=1.0; trials.append(("nonsymmetric",badsym))
    for name,value in trials:
        try:
            colocate_symmetric_tensor_to_vertices(value)
            refusals[name]="FAILED_TO_REFUSE"
        except ValueError as exc:
            refusals[name]=str(exc)
    refuse_pass=all(v!="FAILED_TO_REFUSE" for v in refusals.values())
    cases.append({"case_id":"TC-08","purpose":"explicit invalid-input refusals","status":"PASS" if refuse_pass else "FAIL","refusals":refusals})

    outcome="TENSOR_COLOCATION_QUALIFIED_P0Q" if all(c["status"]=="PASS" for c in cases) else "TENSOR_COLOCATION_REFUSED"
    return {
        "protocol":"NATIVE_TENSOR_VERTEX_COLOCATION_v0.1",
        "stage":"P0-Q",
        "scientific_claim_tested":False,
        "local_weyl_eigensystem_tested":False,
        "case_count":len(cases),
        "cases":cases,
        "outcome":outcome,
        "near_nyquist_policy":"FILTER_REPORT_DO_NOT_INVERT",
        "next_gate":"focused co-located N32/N64/N128 Weyl fixed-band eigensystem qualification",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    report=build_report()
    p=pathlib.Path(args.output)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"outcome":report["outcome"],"output":str(p)},sort_keys=True))


if __name__=="__main__":
    main()
