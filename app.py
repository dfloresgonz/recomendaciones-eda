from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para un formulario
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Procesa los datos enviados
        name = request.form.get('name')
        return redirect(url_for('greet', name=name))
    return render_template('form.html')

# Ruta para saludar al usuario
@app.route('/greet/<name>')
def greet(name):
    return f'¡Hola, {name}!'

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)
