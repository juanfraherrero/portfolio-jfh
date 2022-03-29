from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    url_for
)
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint("portfolio",__name__,url_prefix="/")

@bp.route("/", methods=['GET'])
def index():
    return render_template("portfolio/index.html")

@bp.route("/mail", methods=["GET","POST"])
def mail():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get('mensaje')
        sendEmail(name,email,message)
        return render_template('portfolio/send_mail.html')
    
    return render_template( url_for('portfolio.index') )


def sendEmail(name, email,message):
    mi_email = 'juanfraherrero00@gmail.com'
    sg = sendgrid.SendGridAPIClient(api_key = current_app.config["SENDGRID_KEY"])

    from_email = Email(mi_email)
    to_email = To(mi_email, substitutions={
        "-name-":name,
        "-email-":email,
        "-message-":message,
    })

    html_content = """
        <p>Hola Juan Francisco, tienes un nuevo contacto desde a web:</p>
        <p>Nombre: -name- </p>
        <p>Correo: -email-</p>
        <p>Mensaje: -message-</p>
    """

    mail = Mail(from_email, to_email, 'Nuevo contacto desde la web', html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())