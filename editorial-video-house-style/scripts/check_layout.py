#!/usr/bin/env python3
"""Validate measured overlay samples, not CSS intentions or person detection.

Input: {canvas:[w,h], safe:[x,y,w,h], samples:[{time:0,
scene:'talking-face', protected:[[x,y,w,h]], overlays:[{id:'brand',
role:'brand-card', box:[x,y,w,h], anchor:'bottom', text_align:'center'}]}]}.
Protected boxes must already include head/gesture breathing room. Supply only
 top-level overlay units, not their nested text children. Set phase='transition'
 for animation midpoints: anchoring is strict at holds, clearance at every sample.
A sample-only pass cannot prove full-timeline clearance. Use --self-test for synthetic tests.
"""
import argparse
import copy
import json
import math
from pathlib import Path


def rect(value):
    if not isinstance(value,list) or len(value)!=4:
        raise ValueError('Expected rectangle [x,y,w,h]')
    if any(not isinstance(v,(int,float)) or not math.isfinite(v) for v in value):
        raise ValueError('Rectangle values must be finite numbers')
    x,y,w,h=value
    if w<=0 or h<=0:
        raise ValueError('Rectangle size must be positive')
    return x,y,x+w,y+h


def overlaps(a,b):
    return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]


def check(data):
    w,h=data['canvas'];frame=rect([0,0,w,h]);safe=rect(data['safe'])
    if safe[0]<0 or safe[1]<0 or safe[2]>w or safe[3]>h:
        raise ValueError('Safe region outside canvas')
    if not data['samples']:
        raise ValueError('No measured samples')
    errors=[];count=0;tol=2*w/1080
    for sample in data['samples']:
        t=sample['time']
        if not isinstance(t,(int,float)) or not math.isfinite(t) or t<0:
            raise ValueError('Invalid sample time')
        scene=sample['scene']
        if scene not in ('talking-face','graphic'):
            raise ValueError('Unknown scene type')
        phase=sample.get('phase','hold')
        if phase not in ('hold','transition'):
            raise ValueError('Unknown sample phase')
        protected=[rect(b) for b in sample['protected']]
        if scene=='talking-face' and not protected:
            raise ValueError('Talking-face sample lacks protected regions')
        boxes=[]
        for overlay in sample['overlays']:
            count+=1;b=rect(overlay['box']);name=f'{t}s:{overlay["id"]}'
            if overlay['role'] not in ('brand-card','info-card','caption','diagram'):
                raise ValueError('Unknown overlay role')
            if b[0]<safe[0]-tol or b[1]<safe[1]-tol or b[2]>safe[2]+tol or b[3]>safe[3]+tol:
                errors.append(name+': outside safe region')
            if any(overlaps(b,p) for p in protected):
                errors.append(name+': crowds protected person/gesture region')
            if overlay['role']=='caption' and not 1<=overlay['lines']<=2:
                errors.append(name+': caption line count')
            centered=overlay['role']=='caption' or (scene=='talking-face' and overlay['role'] in ('brand-card','info-card'))
            if centered:
                if abs((b[0]+b[2])/2-w/2)>tol:
                    errors.append(name+': container not horizontally centered')
                if overlay.get('text_align')!='center':
                    errors.append(name+': inner text not centered')
                anchor=overlay.get('anchor')
                if anchor not in ('top','bottom'):
                    errors.append(name+': unresolved edge anchor')
                elif phase=='hold' and abs((b[1]-safe[1]) if anchor=='top' else (b[3]-safe[3]))>tol:
                    errors.append(name+': not attached to resolved safe edge')
            for old_name,old_box in boxes:
                if overlaps(b,old_box):
                    errors.append(name+': overlaps '+old_name)
            boxes.append((overlay['id'],b))
    if not count:
        raise ValueError('No overlays measured')
    return errors


def self_test():
    good={'canvas':[1080,1920],'safe':[120,250,840,1270],'samples':[{'time':1,'scene':'talking-face','protected':[[300,400,480,900]],'overlays':[{'id':'brand','role':'brand-card','box':[160,1340,760,180],'anchor':'bottom','text_align':'center'}]}]}
    assert not check(good)
    bad=copy.deepcopy(good);bad['samples'][0]['overlays'][0]['box']=[90,1120,760,180]
    errors=check(bad)
    assert any('not horizontally centered' in e for e in errors)
    assert any('not attached' in e for e in errors)
    assert any('crowds' in e for e in errors)
    top=copy.deepcopy(good);top['samples'][0]['overlays'][0].update(box=[160,250,760,120],anchor='top')
    assert not check(top)
    moving=copy.deepcopy(top);moving['samples'][0]['phase']='transition';moving['samples'][0]['overlays'][0]['box'][1]+=16
    assert not check(moving)
    bad=copy.deepcopy(good);bad['samples'][0]['overlays'].append({'id':'caption','role':'caption','box':[130,1360,820,160],'lines':2,'anchor':'bottom','text_align':'center'})
    assert any('overlaps' in e for e in check(bad))
    try:rect([0,0,float('nan'),10])
    except ValueError:pass
    else:raise AssertionError('Nonfinite rectangle accepted')
    print('PASS: synthetic top/bottom, center, protected-region, overlap and invalid-input checks. No footage assessed.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('measurements',nargs='?',type=Path);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    if args.self_test:self_test()
    else:
        if not args.measurements:parser.error('Provide measured layout JSON or --self-test')
        errors=check(json.loads(args.measurements.read_text()))
        print(json.dumps({'ok':not errors,'errors':errors,'scope':'supplied samples only'},indent=2))
        raise SystemExit(bool(errors))
