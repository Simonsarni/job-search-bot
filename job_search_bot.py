import urllib.request
import urllib.parse
import json
import csv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ============================================================
# CONFIGURACION - Editá estos valores antes de correr el bot
# ============================================================

# Tu email y contraseña de aplicación (ver instrucciones abajo)
MY_EMAIL = "tu_email@gmail.com"
MY_APP_PASSWORD = "tu_contraseña_de_aplicacion"  # No es tu contraseña normal de Gmail

# Qué trabajo buscar y dónde
SEARCH_QUERY = "software engineer intern"
SEARCH_LOCATION = "remote"
MAX_RESULTS = 10

# Archivo donde se guardan los resultados
CSV_FILE = "jobs_found.csv"

# ============================================================
# FUNCIONES
# ============================================================

def search_jobs(query, location, max_results):
    """
    Busca trabajos usando la API pública de Jooble.
    Retorna una lista de ofertas de trabajo.
    """
    print(f"\n🔍 Buscando '{query}' en '{location}'...")

    url = "https://jooble.org/api/"
    
    # Necesitás una API key gratis de jooble.org/api
    # Registrate en: https://jooble.org/api/about
    API_KEY = "TU_API_KEY_DE_JOOBLE"

    data = json.dumps({
        "keywords": query,
        "location": location,
        "resultonpage": max_results
    }).encode("utf-8")

    req = urllib.request.Request(
        url + API_KEY,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            jobs = result.get("jobs", [])
            print(f"✅ Se encontraron {len(jobs)} ofertas.")
            return jobs
    except Exception as e:
        print(f"❌ Error al buscar trabajos: {e}")
        return []


def save_to_csv(jobs, filename):
    """
    Guarda las ofertas encontradas en un archivo CSV.
    """
    if not jobs:
        print("⚠️  No hay trabajos para guardar.")
        return

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "company", "location", "salary", "date", "link"])

        # Solo escribe el header si el archivo es nuevo
        if not file_exists:
            writer.writeheader()

        for job in jobs:
            writer.writerow({
                "title": job.get("title", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "N/A"),
                "salary": job.get("salary", "Not specified"),
                "date": job.get("updated", datetime.today().strftime("%Y-%m-%d")),
                "link": job.get("link", "N/A")
            })

    print(f"💾 Resultados guardados en '{filename}'.")


def format_email_body(jobs):
    """
    Formatea el contenido del email con las ofertas encontradas.
    """
    today = datetime.today().strftime("%B %d, %Y")
    body = f"<h2>🤖 Job Search Bot — {today}</h2>"
    body += f"<p>Found <b>{len(jobs)}</b> new job listings for <b>{SEARCH_QUERY}</b> in <b>{SEARCH_LOCATION}</b>:</p>"
    body += "<hr>"

    for i, job in enumerate(jobs, 1):
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        location = job.get("location", "N/A")
        salary = job.get("salary", "Not specified")
        link = job.get("link", "#")

        body += f"""
        <div style="margin-bottom: 20px;">
            <h3>{i}. {title}</h3>
            <p>🏢 <b>Company:</b> {company}</p>
            <p>📍 <b>Location:</b> {location}</p>
            <p>💰 <b>Salary:</b> {salary}</p>
            <p><a href="{link}">🔗 View Job Listing</a></p>
        </div>
        <hr>
        """

    body += "<p><i>Sent automatically by your Job Search Bot 🤖</i></p>"
    return body


def send_email(jobs):
    """
    Manda un email con las ofertas encontradas.
    """
    if not jobs:
        print("⚠️  No hay trabajos para enviar por email.")
        return

    print("\n📧 Enviando email...")

    subject = f"🤖 Job Bot — {len(jobs)} new listings found ({datetime.today().strftime('%b %d')})"
    body = format_email_body(jobs)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MY_EMAIL, MY_APP_PASSWORD)
            server.sendmail(MY_EMAIL, MY_EMAIL, msg.as_string())
        print("✅ Email enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")


def run_bot():
    """
    Función principal — corre el bot completo.
    """
    print("=" * 50)
    print("🤖 JOB SEARCH BOT — Starting...")
    print("=" * 50)

    # 1. Buscar trabajos
    jobs = search_jobs(SEARCH_QUERY, SEARCH_LOCATION, MAX_RESULTS)

    if jobs:
        # 2. Guardar en CSV
        save_to_csv(jobs, CSV_FILE)

        # 3. Mandar email
        send_email(jobs)

        # 4. Mostrar resumen en consola
        print("\n📋 JOB LISTINGS FOUND:")
        print("-" * 50)
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job.get('title', 'N/A')} — {job.get('company', 'N/A')}")
            print(f"   📍 {job.get('location', 'N/A')} | 💰 {job.get('salary', 'Not specified')}")
            print(f"   🔗 {job.get('link', 'N/A')}\n")
    else:
        print("\n⚠️  No jobs found. Try changing the search query or location.")

    print("=" * 50)
    print("✅ Bot finished.")
    print("=" * 50)


# ============================================================
# CORRER EL BOT
# ============================================================
if __name__ == "__main__":
    run_bot()
