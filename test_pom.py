from login_page import LoginPage # Importamos nuestra clase

def test_ejecucion_pom(driver): # <-- 1. Pedimos el driver como parámetro
    # ELIMINAMOS la línea: driver = webdriver.Chrome()
    
    driver.get("https://saucedemo.com")

    # Instanciamos la página 
    login = LoginPage(driver)

    # Caso de Uso: Login Fallido 
    login.ingresar_credenciales("locked_out_user", "secret_sauce") 
    login.click_login()

    mensaje = login.obtener_error()
    print(f"Resultado de la prueba: {mensaje}")
    
    # ELIMINAMOS la línea: driver.quit() (Pytest ya lo hace por ti en el conftest.py)