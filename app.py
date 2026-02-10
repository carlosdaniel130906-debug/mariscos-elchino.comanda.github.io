from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

menu = {
    "Tostada pulpo": 90,
    "Tostada pescado": 60,
    "Tostada camarón": 75,
    "Aguachile": 220,
    "Taco camarón": 65,
    "Taco pescado": 50,
    "Lisa frita": 150,
    "Caldo largo": 150,
    "Camarones empanizados": 180,
    "Pescado empanizado": 150,
    "Bebida": 30
}

mesas = {}
mesa_activa = None

@app.route("/", methods=["GET", "POST"])
def index():
    global mesa_activa

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "crear_mesa":
            nombre = request.form.get("nombre")
            if nombre and nombre not in mesas:
                mesas[nombre] = {"pedidos": [], "total": 0}
                mesa_activa = nombre

        elif accion == "agregar_pedido":
            platillo = request.form.get("platillo")
            if mesa_activa:
                precio = menu[platillo]
                mesas[mesa_activa]["pedidos"].append({
                    "nombre": platillo,
                    "precio": precio
                })
                mesas[mesa_activa]["total"] += precio

        elif accion == "borrar_pedido":
            mesa = request.form.get("mesa")
            index = int(request.form.get("index"))
            precio = mesas[mesa]["pedidos"][index]["precio"]
            mesas[mesa]["total"] -= precio
            mesas[mesa]["pedidos"].pop(index)

        elif accion == "cerrar_mesa":
            mesa = request.form.get("mesa")
            mesas.pop(mesa)
            if mesa_activa == mesa:
                mesa_activa = None

    return render_template(
        "menu.html",
        menu=menu,
        mesas=mesas,
        mesa_activa=mesa_activa
    )

if __name__ == "__main__":
    app.run(debug=True)
