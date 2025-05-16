import subprocess
import tempfile
import os
import shutil

IS_WINDOWS = os.name == 'nt'

LANG_CONFIG = {
    'c': {
        'ext': '.c',
        'cmd': lambda filename: (
            ['cmd', '/c', f"gcc {filename} -o {filename}.exe && {filename}.exe"] if IS_WINDOWS else
            ['sh', '-c', f"gcc {filename} -o {filename}.out && {filename}.out"]
        ),
        'check': lambda: shutil.which('gcc')
    },
    'cpp': {
        'ext': '.cpp',
        'cmd': lambda filename: (
            ['cmd', '/c', f"g++ {filename} -o {filename}.exe && {filename}.exe"] if IS_WINDOWS else
            ['sh', '-c', f"g++ {filename} -o {filename}.out && {filename}.out"]
        ),
        'check': lambda: shutil.which('g++')
    },
    'java': {
        'ext': '.java',
        'cmd': lambda filename: (
            ['cmd', '/c', f"javac {filename} && java -cp {os.path.dirname(filename)} {os.path.splitext(os.path.basename(filename))[0]}"] if IS_WINDOWS else
            ['sh', '-c', f"javac {filename} && java -cp {os.path.dirname(filename)} {os.path.splitext(os.path.basename(filename))[0]}"]
        ),
        'check': lambda: shutil.which('javac') and shutil.which('java')
    },
    'python': {
        'ext': '.py',
        'cmd': lambda filename: ['python', filename],
        'check': lambda: shutil.which('python')
    },
    'javascript': {
        'ext': '.js',
        'cmd': lambda filename: ['node', filename],
        'check': lambda: shutil.which('node')
    }
}

def get_available_languages():
    return [lang for lang, cfg in LANG_CONFIG.items() if cfg['check']()]

def run_code_in_language(code, stdin, language):
    config = LANG_CONFIG.get(language)
    if not config:
        return {'error': f'Language {language} not supported.'}
    ext = config['ext']
    try:
        if language == 'java':
            with tempfile.TemporaryDirectory() as tmpdir:
                filename = os.path.join(tmpdir, 'Main.java')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(code)
                output_file = None
                try:
                    proc = subprocess.run(
                        config['cmd'](filename),
                        input=stdin.encode('utf-8'),
                        capture_output=True,
                        timeout=10,
                        cwd=tmpdir
                    )
                    output = proc.stdout.decode('utf-8')
                    error = proc.stderr.decode('utf-8')
                    if proc.returncode != 0:
                        return {'error': error or 'Unknown error.'}
                    return {'output': output}
                except subprocess.TimeoutExpired:
                    return {'error': 'Execution timed out.'}
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(code.encode('utf-8'))
                tmp.flush()
                filename = tmp.name
            output_file = filename + '.out' if language in ['c', 'cpp'] else None
            try:
                proc = subprocess.run(
                    config['cmd'](filename),
                    input=stdin.encode('utf-8'),
                    capture_output=True,
                    timeout=10
                )
                output = proc.stdout.decode('utf-8')
                error = proc.stderr.decode('utf-8')
                if proc.returncode != 0:
                    return {'error': error or 'Unknown error.'}
                return {'output': output}
            except subprocess.TimeoutExpired:
                return {'error': 'Execution timed out.'}
            finally:
                os.remove(filename)
                if output_file and os.path.exists(output_file):
                    os.remove(output_file)
    except Exception as e:
        return {'error': str(e)} 