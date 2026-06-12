function filtrarTabla() {
    const filtroEstado = document.getElementById("filtroEstado");
    const filtroPrioridad = document.getElementById("filtroPrioridad");
    const estadoBuscado = filtroEstado.value.toLowerCase().trim();
    const prioridadBuscada = filtroPrioridad.value.toLowerCase().trim();
    const filas = document.querySelectorAll("table tbody tr");
    
    filas.forEach((fila) => {
        if (fila.cells.length > 1) {
            
            const celdaPrioridad = fila.cells[3];
            const celdaEstado = fila.cells[5];    
            const textoPrioridad = celdaPrioridad ? celdaPrioridad.textContent.toLowerCase().trim() : "";
            const textoEstado = celdaEstado ? celdaEstado.textContent.toLowerCase().trim() : "";
            const coincideEstado = estadoBuscado === "" || textoEstado.includes(estadoBuscado);
            const coincidePrioridad = prioridadBuscada === "" || textoPrioridad.includes(prioridadBuscada);
            
            if (coincideEstado && coincidePrioridad) {
                fila.style.display = "";
            } else {
                fila.style.display = "none";
            }
        }
    });
}

function limpiarFiltros(event) {
    event.preventDefault();
    document.getElementById("filtroEstado").value = "";
    document.getElementById("filtroPrioridad").value = "";

    const filas = document.querySelectorAll("table tbody tr");
    filas.forEach((fila) => {
        fila.style.display = "";
    });
}