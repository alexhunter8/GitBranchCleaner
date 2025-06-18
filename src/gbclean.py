#!/usr/bin/env python3
import subprocess, sys, argparse, re

VERSION='0.1.0'

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def list_local():
    out = run('git branch --format="%(refname:short)"')
    return [l.strip() for l in out.splitlines() if l.strip()]

def last_commit_date(branch):
    try:
        return run(f'git log -1 --format=%cI {branch}')
    except subprocess.CalledProcessError:
        return ''

def is_protected(branch, protected):
    return any(re.fullmatch(p, branch) for p in protected)

def main():
    ap = argparse.ArgumentParser(description='Clean stale local branches safely')
    ap.add_argument('--days', type=int, default=90, help='stale if no commit in N days')
    ap.add_argument('--protected', action='append', default=['main','master','develop','release/.+','hotfix/.+'], help='regex of branches to keep')
    ap.add_argument('--dry-run', action='store_true', help='only show actions')
    ap.add_argument('--delete-merged', action='store_true', help='also delete branches fully merged into current')
    ap.add_argument('--yes', action='store_true', help='do not prompt')
    ap.add_argument('--version', action='store_true')
    args = ap.parse_args()
    if args.version:
        print(VERSION); return 0

    branches = list_local()
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=args.days)

    stale = []
    for b in branches:
        if is_protected(b, args.protected):
            continue
        d = last_commit_date(b)
        if not d:
            continue
        try:
            dt = datetime.fromisoformat(d.replace('Z','+00:00')).replace(tzinfo=None)
        except ValueError:
            continue
        if dt < cutoff:
            stale.append((b, d))

    if args.delete_merged:
        try:
            merged = set(run('git branch --merged').replace('*','').split())
        except Exception:
            merged = set()
    else:
        merged = set()

    targets = []
    for b,d in stale:
        if args.delete_merged:
            if b in merged:
                targets.append((b,d))
        else:
            targets.append((b,d))

    if not targets:
        print('No stale branches found.'); return 0

    print('Candidates for deletion:')
    for b,d in targets:
        print(f'  {b}  (last: {d})')

    if not args.yes and not args.dry_run:
        ans = input('Delete these branches? [y/N] ')
        if ans.lower() != 'y':
            print('Aborted.'); return 0

    if args.dry_run:
        print('Dry run: no branches deleted.')
        return 0

    failed = []
    for b,_ in targets:
        try:
            run(f'git branch -D {b}')
            print(f'Deleted {b}')
        except Exception as e:
            failed.append((b,str(e)))

    if failed:
        print('Some branches failed to delete:')
        for b,err in failed:
            print(f'  {b}: {err}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
