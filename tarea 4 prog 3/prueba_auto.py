from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from jinja2 import Environment, FileSystemLoader

# Configuración inicial del navegador y directorio para las capturas de pantalla
driver = webdriver.Chrome()
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# funciones
def paso_iniciar_sesion():
    try:
        driver.get("https://www.netflix.com/login")
        driver.implicitly_wait(10)
        driver.save_screenshot("screenshots/paso1_iniciar_sesion.png")
        username_field = driver.find_element(By.NAME, "userLoginId")
        username_field.send_keys("correo de netflix, no la coloco aqui por terminos privados")
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("contraseña de netflix, no la coloco aqui por terminos privados")
        password_field.submit()
        driver.save_screenshot("screenshots/paso1_iniciar_sesion_submit.png")
        return "Inicio de sesión completado correctamente."
    except Exception as e:
        return f"Error al iniciar sesión: {e}"

def paso_mostrar_perfiles():
    try:
        perfil_icono = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "profile-icon")))
        perfil_icono.click()
        driver.save_screenshot("screenshots/paso2_mostrar_perfiles.png")
        return "Mostrar perfiles completado correctamente."
    except Exception as e:
        return f"Error al mostrar perfiles: {e}"

def paso_navegar_categoria():
    try:
        link_series = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/browse/genre/83']")))
        link_series.click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "slider-item")))
        driver.save_screenshot("screenshots/paso3_navegar_categoria.png")
        return "Navegar a la categoría de series completado correctamente."
    except Exception as e:
        return f"No se pudo navegar a la categoría 'Series': {e}"

def paso_seleccionar_serie():
    try:
        series_thumbnail = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "slider-item")))
        series_thumbnail.click()
        driver.save_screenshot("screenshots/paso4_seleccionar_serie.png")
        return "Seleccionar serie completado correctamente."
    except Exception as e:
        return f"Error al seleccionar la serie: {e}"

def paso_reproducir_serie():
    try:
        play_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, "primary-button")))
        play_button.click()
        driver.save_screenshot("screenshots/paso5_reproducir_serie.png")
        return "Reproducir serie completado correctamente."
    except Exception as e:
        return f"Error durante la reproducción de la serie: {e}"

# Ejecutar los pasos y recopilar resultados
results = {}
results[1] = paso_iniciar_sesion()
results[2] = paso_mostrar_perfiles()
results[3] = paso_navegar_categoria()
results[4] = paso_seleccionar_serie()
results[5] = paso_reproducir_serie()

# Generar el informe HTML
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("reportes/report_template.html")
html_content = template.render(results=results)


with open("reportes/netflix_automation_report.html", "w") as file:
    file.write(html_content)


driver.quit()
