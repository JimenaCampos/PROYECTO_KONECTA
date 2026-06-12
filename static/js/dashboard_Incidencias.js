// Captura automática de datos al cargar la interfaz
document.addEventListener("DOMContentLoaded", function() {
  const dataContainer = document.getElementById('data-dashboard-backend');
  
  if (dataContainer) {
    const proyeccion = JSON.parse(dataContainer.getAttribute('data-proyeccion'));
    const porTecnico = JSON.parse(dataContainer.getAttribute('data-tecnico'));
    const porTipo = JSON.parse(dataContainer.getAttribute('data-tipo'));

    inicializarDashboard(proyeccion, porTecnico, porTipo);
  }
});

// Función constructora de gráficos
function inicializarDashboard(proyeccionData, tecnicoData, tipoData) {
  // 1. Gráfico de Tendencia Lineal
  new Chart(document.getElementById('chartProyeccion'), {
    type: 'line',
    data: {
      labels: proyeccionData.map(p => p.periodo),
      datasets: [
        {
          label: 'Tickets Reales',
          data: proyeccionData.map(p => p.reales),
          borderColor: '#3b82f6',
          backgroundColor: 'transparent',
          tension: 0.2
        },
        {
          label: 'Proyección Lineal',
          data: proyeccionData.map(p => p.proyeccion),
          borderColor: '#ef4444',
          borderDash: [5, 5],
          backgroundColor: 'transparent',
          tension: 0
        }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  // 2. Gráfico de Técnicos
  new Chart(document.getElementById('chartTecnicos'), {
    type: 'bar',
    data: {
      labels: tecnicoData.map(t => t.nombre || 'Sin Asignar'),
      datasets: [{
        label: 'Tickets Asignados',
        data: tecnicoData.map(t => t.total_asignados),
        backgroundColor: '#3b82f6'
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  // 3. Gráfico por Tipo de Incidencia
  new Chart(document.getElementById('chartTipos'), {
    type: 'bar',
    data: {
      labels: tipoData.map(tp => tp.nombre_problema),
      datasets: [{
        label: 'Volumen de Incidentes',
        data: tipoData.map(tp => tp.cantidad),
        backgroundColor: '#10b981'
      }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });
}

// Funciones de Automatización de Reportes (Excel y PDF)
function exportarTablaExcel() {
  const table = document.getElementById('tabla-exportable-datos');
  const wb = XLSX.utils.table_to_book(table, { sheet: "Historial Reciente" });
  XLSX.writeFile(wb, "Reporte_Incidencias_Konecta.xlsx");
}

function exportarTablaPDF() {
  const element = document.getElementById('reporte-bloque-completo');
  const opt = {
    margin: 0.5,
    filename: 'Reporte_Analitico_Konecta.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  };
  html2pdf().set(opt).from(element).save();
}