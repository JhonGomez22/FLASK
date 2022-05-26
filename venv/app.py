from Flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import request, redirect
import os, json

app = Flask(__name__)

libros = {}
nuevo_id = 0
archivo = os.path.join(app.static_folder,'datos','libros.json')

def guardar_libros(libros):
	global archivo
	with open(archivo,'w') as outfile:
		json.dump(libros,outfile)

@app.route('/biblioteca/')
def biblioteca():
	return render_template("biblioteca.html")

@app.route('/')
def principal():
	global archivo
	global libros
	if not os.path.exists(archivo):
		guardar_libros(libros)
	with open(archivo) as json_file:
		libros = json.load(json_file)
	return render_template("libros/libros.html",libros=libros)

@app.route('/libro/<int:id_libro>/')
def mostrar_libro(id_libro):
	global archivo
	libro_elegido={}
	with open(archivo) as json_file:
		libros = json.load(json_file)
	for key, value in libros.items():
			if libros[key]['id'] == id_libro:
				libro_elegido=value


	return render_template("/libros/ver_libro.html",libro=libro_elegido)

@app.route("/libros/libro/",methods=["GET","POST"])
@app.route("/libros/libro/<int:libro_e>/",methods=["GET","POST"])
def form_libro(libro_e=None):
	libro={}
	if request.method == "POST":
		global nuevo_id
		global libros
		if libro_e:
			nuevo_id = libro_e
		else:
			nuevo_id += 1

		libro["id"] = nuevo_id
		libro["titulo"] = request.form['titulo']
		libro["description"] = request.form['descripcion']
		libro["editorial"] = request.form['editorial']
		libro["numero_paginas"] = request.form['numero_paginas']
		libro["año"] = request.form['año']
		libros[libro["id"]] = libro
		guardar_libros(libros)
		return redirect(url_for("principal"))
	else:
		if libro_e:
			with open(archivo) as json_file:
				libros = json.load(json_file)
			for key, value in libros.items():
				if libros[key]['id']==libro_e:
					libro_e=value
		


	return render_template("/libros/form_libro.html",libro_e=libro_e)




@app.route('/biblioteca/mision/')
def mision():
	return render_template("mision.html")

@app.route('/biblioteca/vision/')
def vision():
	return render_template("vision.html")

@app.route('/biblioteca/contactenos/')
def contactenos():
	return render_template("contactenos.html")


if __name__ == '__main__':
	#app.run()
	app.run(debug=True)
