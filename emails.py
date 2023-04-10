import smtplib
import ssl
from email.utils import make_msgid
import mimetypes
from email.message import EmailMessage
from constants import MAIN_PATH

def send_emails(precio_medio, precio_min, precio_max, precio_historico_medio, dias):

    email_sender = ''
    email_password = ''
    email_receiver = ['']

    subject = "GALP Tucídides"

    body = """
    <html>
        <body>
            <p>Informe semanal de la gasolina en la estación Galp de calle Tucídides.</p>
            <p>Precio medio: {precio_medio}</p>
            <p>Precio mínimo: {precio_min}</p>
            <p>Precio máximo: {precio_max}</p>
            <p>Precio histórico medio: {precio_historico_medio}</p>
            <p>Día(s) más barato de la semana: {dias}</p>
            <p></p>
            <p>Comparación entre GALP Tucídides, GALP Hermann Hesse, Petroprix y Carrefour</p>
            <img src="cid:{image_comparison}">
            <p>*El precio de las estaciones de Galp se ha calculado restandole el 5% de cashback para el seguro de Mapfre y restándole los 10 cents de la promoción de Galp.</p>
            <p>*El precio de la estación de Carrefour se ha calculado restandole el 8% de cashback que te devuelven en la tarjeta Carrefour.</p>
        </body>
    </html>
    """

    body = body.replace('{precio_medio}', str(precio_medio))\
        .replace('{precio_min}', str(precio_min))\
        .replace('{precio_max}', str(precio_max))\
        .replace('{precio_historico_medio}', str(precio_historico_medio))\
        .replace('{dias}', dias)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # now create a Content-ID for the image
    image_comparison = make_msgid(domain='xyz.com')
    # if `domain` argument isn't provided, it will
    # use your computer's name

    # set an alternative html body
    em.add_alternative(body.format(image_comparison=image_comparison[1:-1]), subtype='html')
    # image_comparison looks like <long.random.number@xyz.com>
    # to use it as the img src, we don't need `<` or `>`
    # so we use [1:-1] to strip them off


    # now open the image and attach it to the email
    with open('{}/Results/comparison.jpg'.format(MAIN_PATH), 'rb') as img:

        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # attach it
        em.get_payload()[1].add_related(img.read(),
                                         maintype=maintype,
                                         subtype=subtype,
                                         cid=image_comparison)


    context = ssl.create_default_context()

    print("[INFO] Enviando email a {}".format(", ".join(email_receiver)))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        smtp.quit()
