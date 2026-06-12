document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    if (!form) {
        return;
    }

    const tipoComprobante = document.getElementById("tipo_comprobante_id");
    const fechaEmision = document.getElementById("fecha_emision");
    const clienteNombre = document.getElementById("cliente_nombre");
    const clienteDocumento = document.getElementById("cliente_documento");
    const clienteTelefono = document.getElementById("cliente_telefono");
    const productoServicio = document.getElementById("producto_servicio");
    const plan = document.getElementById("plan");
    const monto = document.getElementById("monto");
    const asesorVenta = document.getElementById("asesor_venta");
    const observacion = document.getElementById("observacion");

    form.addEventListener("submit", (event) => {
        limpiarErrores();

        let esValido = true;

        if (!tipoComprobante.value.trim()) {
            mostrarError(tipoComprobante, "Selecciona el tipo de comprobante");
            esValido = false;
        }

        if (!fechaEmision.value.trim()) {
            mostrarError(fechaEmision, "Selecciona la fecha de emisión");
            esValido = false;
        }

        if (!clienteNombre.value.trim()) {
            mostrarError(clienteNombre, "Ingresa el nombre del cliente");
            esValido = false;
        }

        if (!clienteDocumento.value.trim()) {
            mostrarError(clienteDocumento, "Ingresa el documento del cliente");
            esValido = false;
        } else if (!/^[0-9]{8,11}$/.test(clienteDocumento.value.trim())) {
            mostrarError(clienteDocumento, "El documento debe tener entre 8 y 11 números");
            esValido = false;
        }

        if (clienteTelefono.value.trim() && !/^[0-9]{9}$/.test(clienteTelefono.value.trim())) {
            mostrarError(clienteTelefono, "El teléfono debe tener 9 dígitos");
            esValido = false;
        }

        if (!productoServicio.value.trim()) {
            mostrarError(productoServicio, "Ingresa el producto o servicio");
            esValido = false;
        }

        if (!plan.value.trim()) {
            mostrarError(plan, "Ingresa el plan");
            esValido = false;
        }

        if (!monto.value.trim()) {
            mostrarError(monto, "Ingresa el monto");
            esValido = false;
        } else if (Number(monto.value) <= 0) {
            mostrarError(monto, "El monto debe ser mayor a 0");
            esValido = false;
        }

        if (asesorVenta.value.trim().length > 100) {
            mostrarError(asesorVenta, "El asesor no debe superar 100 caracteres");
            esValido = false;
        }

        if (observacion.value.trim().length > 250) {
            mostrarError(observacion, "La observación no debe superar 250 caracteres");
            esValido = false;
        }

        if (!esValido) {
            event.preventDefault();
        }
    });

    clienteTelefono.addEventListener("input", () => {
        clienteTelefono.value = clienteTelefono.value.replace(/\D/g, "").slice(0, 9);
    });

    clienteDocumento.addEventListener("input", () => {
        clienteDocumento.value = clienteDocumento.value.replace(/\D/g, "").slice(0, 11);
    });

    monto.addEventListener("input", () => {
        if (Number(monto.value) < 0) {
            monto.value = "";
        }
    });

    function mostrarError(campo, mensaje) {
        campo.classList.add("input-error");

        const error = document.createElement("small");
        error.className = "field-error";
        error.textContent = mensaje;

        campo.insertAdjacentElement("afterend", error);
    }

    function limpiarErrores() {
        const errores = document.querySelectorAll(".field-error");
        const campos = document.querySelectorAll(".input-error");

        errores.forEach((error) => error.remove());
        campos.forEach((campo) => campo.classList.remove("input-error"));
    }
});