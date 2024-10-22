from flask import Flask, request, render_template,redirect,url_for,session

app=Flask(__name__)
app.secret_key='unaclavesecreta'

#funcion
def generar_id():                   #sesion el objeto seminarios
    if 'seminarios' in session and len(session['seminarios'])>0:
        #el id de inscrito mayor y le sumamos +1
        return max(item['id'] for item in session['seminarios'])+1
    else:
        return 1


@app.route("/")
def index():
    if 'seminarios' not in session:
        session['seminarios']=[]
    seminarios=session.get('seminarios',[])
    return render_template('index.html',seminarios=seminarios)


@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method=='POST':
        fecha=request.form['fecha']
        nombre=request.form['nombre']
        apellidos=request.form['apellidos']
        turno=request.form['turno']
        disponibles=request.form.getlist('disponibles')
        disponibles_texto = ', '.join(disponibles)
        #diccionario
        nuevo_inscrito={
            'id':generar_id(),
            'fecha':fecha,
            'nombre':nombre,
            'apellidos':apellidos,
            'turno':turno,
            'disponible':disponibles_texto
        }
        if 'seminarios' not in session:
            #en caso de que no exista lista de seminarios en la sesion
            session['seminarios']=[]#objeto lista sesion 
            
        session['seminarios'].append(nuevo_inscrito)
        session.modified=True
        return redirect(url_for('index'))
    return render_template("nuevo.html")
                #parametro
@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_seminarios=session.get('seminarios',[])
    #realiza un recorrido a los seminarios y si no lo encuentra no muestra na, next extrae
    inscrito=next((c for c in lista_seminarios if c['id']==id),None)
    if not inscrito:
        return redirect(url_for('index'))
    if request.method=='POST':
        inscrito['fecha']=request.form['fecha']
        inscrito['nombre']=request.form['nombre']
        inscrito['apellidos']=request.form['apellidos']
        inscrito['turno']=request.form['turno']
        disponible=request.form.getlist('disponibles')
        disponibles_texto = ', '.join(disponible)
        inscrito['disponible']=disponibles_texto
        session.modified=True
        return redirect(url_for('index'))
    return render_template('editar.html',inscrito=inscrito)#le manda un diccionario al html

@app.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    lista_seminarios=session.get('seminarios',[])
                #sacar lo elementos de la lista de seminarios 
    inscrito=next((c for c in lista_seminarios if c['id']==id),None)
    if inscrito:
        #remover esa informacion de la sesion
        session['seminarios'].remove(inscrito)
        session.modified=True
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True,port='5017')
###########################3







