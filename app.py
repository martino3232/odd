
from flask import Flask, render_template, request, Response, stream_with_context
import subprocess
import os
import sys
import time
import threading

app = Flask(__name__)
SCRIPT_DIR = os.path.dirname(__file__)
script_path = os.path.join(SCRIPT_DIR, 'Zeuz.py')
cmd = ['python', script_path]


params = {}  # Variables globales temporales para compartir datos entre rutas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    global params
    params['opcion'] = request.form.get('opcion')
    params['cp'] = request.form.get('cp')
    params['localidad'] = request.form.get('localidad')
    return render_template('index.html')

@app.route('/stream')
def stream():
    def generate():
        opcion = params.get('opcion')
        cp = params.get('cp')
        localidad = params.get('localidad')
        
        cmd = ['python', os.path.join(SCRIPT_DIR, 'zeuz.py')]
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        # Simulamos entradas para zeuz.py
        if opcion == '1':
            simulated_input = f"1\n{cp}\n"
        elif opcion == '2':
            simulated_input = f"2\n{localidad}\n"
        elif opcion == '3':
            simulated_input = f"3\n"
        else:
            simulated_input = "\n"

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True, env=env)
        try:
            # Enviamos los datos simulados al stdin del proceso
            process.stdin.write(simulated_input)
            process.stdin.flush()
            process.stdin.close()

            for line in iter(process.stdout.readline, ''):
                yield f"data: {line.strip()}\n\n"
        except Exception as e:
            yield f"data: Error ejecutando: {str(e)}\n\n"
        finally:
            process.stdout.close()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5501, host='0.0.0.0')
