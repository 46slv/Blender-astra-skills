"""Runs inside Blender's main thread. Trusted local scripts, NOT a sandbox."""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import time
import traceback
import uuid

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from session import atomic_json, read


def start(directory):
    root = Path(directory).resolve()
    root.mkdir(parents=True, exist_ok=True)
    if (root / 'session.json').exists():
        raise RuntimeError('Session already exists. Choose a fresh directory.')
    session_id = uuid.uuid4().hex
    namespace = {'__name__': '__astra_live__', 'bpy': bpy, 'SESSION_DIR': root}
    info = {'session': session_id, 'pid': os.getpid(), 'version': bpy.app.version_string,
            'file': bpy.data.filepath, 'state': 'ready', 'heartbeat': time.time()}

    def publish(state='ready'):
        info.update(file=bpy.data.filepath, state=state, heartbeat=time.time())
        atomic_json(root / 'session.json', info)

    def tick():
        try:
            pending = sorted(root.glob('*.pending'))
            if not pending:
                if time.time() - info['heartbeat'] > 1:
                    publish()
                return 0.1
            path = pending[0]
            running = path.with_suffix('.running')
            path.replace(running)  # Claim before execution; never replay after failure/crash.
            request = read(running)
            result = {'id': request['id'], 'status': 'error'}
            stop = False
            stream = io.StringIO()
            started = time.monotonic()
            try:
                if request['session'] != session_id:
                    raise RuntimeError('Session identity mismatch')
                if os.path.normcase(request['expected_file']) != os.path.normcase(bpy.data.filepath):
                    raise RuntimeError('File changed since observation; inspect before editing')
                publish('busy')
                if request['op'] == 'stop':
                    stop = True
                elif request['op'] == 'exec':
                    with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                        exec(compile(request['code'], '<astra:' + request['id'] + '>', 'exec'), namespace)
                        bpy.context.view_layer.update()
                else:
                    raise ValueError('Unknown operation')
                result['status'] = 'ok'
            except BaseException:
                result['traceback'] = traceback.format_exc()
                result['message'] = 'May have partially changed Blender; inspect before recovery.'
            result.update(output=stream.getvalue(), seconds=time.monotonic() - started,
                          file=bpy.data.filepath, session=session_id)
            atomic_json(root / (request['id'] + '.json'), result)
            running.unlink()
            publish('stopped' if stop else 'ready')
            return None if stop else 0.1
        except Exception:
            # Leave evidence and disarm, rather than retry an unknown mutation.
            (root / 'server-error.txt').write_text(traceback.format_exc(), encoding='utf-8')
            publish('error')
            return None

    publish()
    bpy.app.timers.register(tick, first_interval=0.2, persistent=True)
    return session_id


if __name__ == '__main__':
    start(sys.argv[sys.argv.index('--') + 1])
