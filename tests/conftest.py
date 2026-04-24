import pytest
from selenium import webdriver
import os
from datetime import datetime

report_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(report_dir, exist_ok=True)

report_path = os.path.join(report_dir, "clinical_authority_report.html")

# Global array to hold test execution metrics in memory
test_results = []

@pytest.fixture(scope="function")
def driver():
    """Inicializa y devuelve una instancia limpia de Chrome para cada test."""
    
    options = Options()
    options.add_argument("--headless") # Ejecución sin ventana (obligatorio para GitHub)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook inyector a medida para nuestro Dashboard.
    Extraeremos y almacenaremos todo el contexto para luego generar el HTML de forma manual en lugar de usar pytest-html.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" or (report.when == "setup" and report.failed):
        # Obtain WebDriver safely if it was injected
        driver = item.funcargs.get('driver') if 'driver' in item.funcargs else None
        
        screenshot_b64 = None
        error_text = ""
        
        if report.failed:
            if hasattr(call, "excinfo") and call.excinfo:
                # Capture the precise AssertionError string
                error_text = str(call.excinfo.value).replace('\n', '<br/>')
            
            if driver:
                # Screen capture via Base64 logic
                screenshot_b64 = driver.get_screenshot_as_base64()

        # Append to our local test session array
        test_results.append({
            'name': item.name.replace("test_", "").replace("_", " ").title(),
            'duration': f"{report.duration:.2f}s",
            'status': report.outcome,
            'error_text': error_text,
            'screenshot': screenshot_b64
        })

def pytest_sessionfinish(session, exitstatus):
    """
    Se lanza cuando toda la sesión de pruebas acabó.
    Acá conectaremos nuestros resultados directamente en el HTML super-plantilla del usuario.
    """
    total = len(test_results)
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    skipped = sum(1 for r in test_results if r['status'] == 'skipped')
    
    pass_rate = round((passed / total * 100), 1) if total > 0 else 0

    rows_html = ""
    for idx, r in enumerate(test_results):
        st = r['status']
        if st == 'passed':
            badge = '<span class="px-3 py-1 bg-tertiary-container text-on-tertiary rounded-full text-[10px] font-bold uppercase tracking-wider shadow-sm">Pass</span>'
        elif st == 'failed':
            badge = '<span class="px-3 py-1 bg-error-container text-red-700 rounded-full text-[10px] font-bold uppercase tracking-wider shadow-sm">Fail</span>'
        else:
            badge = '<span class="px-3 py-1 bg-slate-200 text-slate-700 rounded-full text-[10px] font-bold uppercase tracking-wider shadow-sm">Skip</span>'
            
        # Fila principal de datos
        row = f'''
        <tr class="hover:bg-slate-50 transition-colors">
            <td class="px-6 py-4 font-mono text-sm text-blue-700 font-bold">{r['name']}</td>
            <td class="px-6 py-4 font-semibold text-slate-700">SauceDemo E2E Suite</td>
            <td class="px-6 py-4"><span class="px-2 py-1 bg-slate-200 text-slate-600 rounded text-[10px] font-bold uppercase">QA Node 1</span></td>
            <td class="px-6 py-4">{badge}</td>
            <td class="px-6 py-4 font-mono text-slate-500 text-xs">{r['duration']}</td>
            <td class="px-6 py-4 flex items-center gap-2">
                <div class="w-6 h-6 rounded-full bg-blue-100 text-[10px] flex items-center justify-center text-blue-800 font-bold border border-blue-200">SE</div>
                <span class="text-xs font-semibold text-slate-600">Selenium Bot</span>
            </td>
        </tr>
        '''
        rows_html += row
        
        # Bloque expansible en rojo exclusivo si algo falla (Insertando motivo y foto de Selenium)
        if st == 'failed':
            err_box = f'''
            <tr class="bg-red-50/50">
                <td colspan="6" class="p-0 border-b-2 border-red-200">
                    <details class="group cursor-pointer">
                        <summary class="flex items-center gap-2 text-red-700 font-bold uppercase text-[10px] hover:bg-red-100 transition-colors list-none outline-none px-6 py-3">
                            <span class="material-symbols-outlined transition-transform duration-300 group-open:rotate-180 text-sm">expand_more</span>
                            Ver Detalles y Captura de Pantalla
                        </summary>
                        <div class="px-8 pb-6 pt-4 border-t border-red-200/50 cursor-auto">
                            <div class="mb-4">
                                <span class="bg-red-100 text-red-700 px-3 py-1 rounded-md text-xs font-bold uppercase mb-2 inline-block shadow-sm">System Exception</span>
                                <p class="text-red-800 font-mono text-sm pl-3 py-1 border-l-4 border-red-400 bg-red-100/50">{r['error_text']}</p>
                            </div>
                            { f'<div class="rounded-xl overflow-hidden shadow-lg border-4 border-white inline-block mt-3"><img src="data:image/png;base64,{r["screenshot"]}" class="max-w-2xl" /></div>' if r['screenshot'] else '' }
                        </div>
                    </details>
                </td>
            </tr>
            '''
            rows_html += err_box

    # Lectura del HTML Dashboard base (que separamos antes del CSS)
    template_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'dashboard_template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Inyectar tags
    now_str = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
    html = html.replace('{{ FECHA_ACTUAL }}', now_str)
    html = html.replace('{{ TOTAL_TESTS }}', str(total))
    html = html.replace('{{ PASSED_TESTS }}', str(passed))
    html = html.replace('{{ FAILED_TESTS }}', str(failed))
    html = html.replace('{{ SKIPPED_TESTS }}', str(skipped))
    html = html.replace('{{ PASS_RATE }}', str(pass_rate))
    html = html.replace('{{ TEST_ROWS }}', rows_html)

    # Exportación Final Limpia
    report_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'clinical_authority_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"\\n\\n[Exito] Dashboard Clinical Authority inyectado desde Selenium con exito!")
    print(f"Reporte guardado en: {report_path}\\n")

    # [NUEVO] Abrir pestaña automáticamente en el navegador por defecto
    import webbrowser
    absolute_path = os.path.abspath(report_path)
    webbrowser.open(f"file:///{absolute_path}")
