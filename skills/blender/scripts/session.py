"""Local, persistent Blender Python. No add-on, network listener or dependency.

python session.py start --blender /path/to/blender --session /new/session/dir
python session.py status --session /session/dir
python session.py exec --session /session/dir --script edit.py [--expect-file path]
python session.py result --session /session/dir --id REQUEST_ID
python session.py stop --session /session/dir
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid


def atomic_json(path, data):
    path = Path(path)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def submit(root, code, expected=None, timeout=30, op='exec'):
    """At most one outstanding command. Timeout means UNKNOWN, never resubmit."""
    root = Path(root).resolve()
    info = read(root / 'session.json')
    if info['state'] != 'ready' or time.time() - info['heartbeat'] > 10:
        raise RuntimeError('Session not ready or heartbeat stale; inspect status/log/result.')
    lock = root / 'submit.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        if list(root.glob('*.pending')) or list(root.glob('*.running')):
            raise RuntimeError('Outstanding command; retrieve its result before another edit.')
        request_id = uuid.uuid4().hex
        req = {'id': request_id, 'session': info['session'], 'op': op, 'code': code,
               'expected_file': info['file'] if expected is None else str(Path(expected).resolve()) if expected else ''}
        atomic_json(root / (request_id + '.pending'), req)
    finally:
        os.close(fd)
        lock.unlink()
    print(json.dumps({'submitted': request_id}), flush=True)
    deadline = time.monotonic() + timeout
    result_path = root / (request_id + '.json')
    while time.monotonic() < deadline:
        if result_path.exists():
            return read(result_path)
        time.sleep(0.1)
    return {'id': request_id, 'status': 'unknown',
            'message': 'Wait/read result for this ID. Do not repeat the operation.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['start', 'status', 'exec', 'result', 'stop'])
    p.add_argument('--session', required=True, type=Path)
    p.add_argument('--blender')
    p.add_argument('--script', type=Path)
    p.add_argument('--expect-file')
    p.add_argument('--id')
    p.add_argument('--timeout', type=float, default=30)
    args = p.parse_args()
    root = args.session.resolve()
    if args.command == 'start':
        if not args.blender:
            p.error('start requires --blender')
        root.mkdir(parents=True, exist_ok=True)
        if any(root.iterdir()):
            raise RuntimeError('Use a new empty session directory; existing sessions are not overwritten.')
        server = Path(__file__).with_name('live.py')
        with (root / 'blender.log').open('w', encoding='utf-8') as log:
            proc = subprocess.Popen([args.blender, '--factory-startup', '--disable-autoexec', '--python', str(server),
                                     '--', str(root)], stdout=log, stderr=subprocess.STDOUT)
        print(json.dumps({'pid': proc.pid, 'session_dir': str(root)}), flush=True)
        deadline = time.monotonic() + args.timeout
        while time.monotonic() < deadline:
            if (root / 'session.json').exists():
                print(json.dumps(read(root / 'session.json'), ensure_ascii=False))
                return
            if proc.poll() is not None:
                raise RuntimeError('Blender exited. Inspect blender.log.')
            time.sleep(0.2)
        raise RuntimeError('Startup uncertain. Inspect session.json/log; do not start again here.')
    elif args.command == 'status':
        info = read(root / 'session.json')
        info['heartbeat_age_seconds'] = time.time() - info['heartbeat']
        info['outstanding'] = [f.name for pattern in ('*.pending', '*.running') for f in root.glob(pattern)]
        print(json.dumps(info, ensure_ascii=False, indent=2))
    elif args.command == 'result':
        if not args.id or len(args.id) != 32 or any(c not in '0123456789abcdef' for c in args.id):
            p.error('result requires a 32-character hexadecimal --id')
        path = root / (args.id + '.json')
        result = read(path) if path.exists() else {'id': args.id, 'status': 'unknown'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result['status'] != 'ok':
            sys.exit(2)
    else:
        if args.command == 'exec' and not args.script:
            p.error('exec requires --script')
        code = args.script.read_text(encoding='utf-8-sig') if args.script else ''
        result = submit(root, code, args.expect_file, args.timeout,
                        'stop' if args.command == 'stop' else 'exec')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result['status'] != 'ok':
            sys.exit(2)


if __name__ == '__main__':
    main()
