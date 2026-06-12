from flask import Blueprint, render_template, request, redirect, url_for
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import random
import re
import smtplib

from konectaAD import (
    registrarUsuario,
    guardarCodigoValidacion,
    validarCodigoCorreo
)

load_dotenv()

registro_bp = Blueprint("registro", __name__)


# ══════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════

def correo_valido(correo):
    correo = correo.lower().strip()
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.match(patron, correo):
        return True

    return False


def generar_codigo():
    return str(random.randint(100000, 999999))


def enviar_codigo_correo(destinatario, codigo):
    remitente = os.getenv("MAIL_USER")
    password = os.getenv("MAIL_PASSWORD")

    if not remitente or not password:
        raise Exception("Falta configurar MAIL_USER y MAIL_PASSWORD en el archivo .env")

    mensaje = EmailMessage()
    mensaje["Subject"] = "Código de validación - Sistema Konecta"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario

    mensaje.set_content(f"""
Hola,

Tu código de validación es:

{codigo}

Ingresa este código para completar tu registro.

Sistema Konecta
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, password)
        smtp.send_message(mensaje)


# ══════════════════════════════════════════════
#  REGISTRO DE USUARIO
# ══════════════════════════════════════════════

@registro_bp.route("/registrar", methods=("GET", "POST"))
def registrar():
    error = None

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        correo = request.form.get("correo", "").strip()
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()
        celular = request.form.get("celular", "").strip()

        if not nombre or not correo or not usuario or not password:
            error = "Completa todos los campos obligatorios"
            return render_template("registrar.html", error=error)

        if not correo_valido(correo):
            error = "Ingresa un correo válido"
            return render_template("registrar.html", error=error)

        codigo = generar_codigo()

        exito_registro, mensaje_registro = registrarUsuario(
            nombre,
            correo,
            usuario,
            password,
            celular,
            1
        )

        if not exito_registro:
            error = mensaje_registro
            return render_template("registrar.html", error=error)

        try:
            exito_codigo, mensaje_codigo = guardarCodigoValidacion(correo, codigo)

            if not exito_codigo:
                error = mensaje_codigo
                return render_template("registrar.html", error=error)

            enviar_codigo_correo(correo, codigo)

        except Exception as error_correo:
            error = f"El usuario fue registrado, pero no se pudo enviar el correo: {error_correo}"
            return render_template("registrar.html", error=error)

        return redirect(url_for("registro.verificar_correo", correo=correo))

    return render_template("registrar.html", error=error)


# ══════════════════════════════════════════════
#  VALIDACIÓN DE CORREO
# ══════════════════════════════════════════════

@registro_bp.route("/verificar_correo", methods=("GET", "POST"))
def verificar_correo():
    correo = request.args.get("correo", "").strip()
    error = None

    if not correo:
        return redirect(url_for("registro.registrar"))

    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip()

        if not codigo:
            error = "Ingresa el código de validación"
            return render_template(
                "verificar_correo.html",
                correo=correo,
                error=error
            )

        exito = validarCodigoCorreo(correo, codigo)

        if exito:
            return redirect(url_for("registro.registro_exitoso"))

        error = "Código incorrecto. Inténtalo nuevamente"

    return render_template(
        "verificar_correo.html",
        correo=correo,
        error=error
    )


# ══════════════════════════════════════════════
#  REGISTRO EXITOSO
# ══════════════════════════════════════════════

@registro_bp.route("/registro_exitoso")
def registro_exitoso():
    return render_template("registro_exitoso.html")