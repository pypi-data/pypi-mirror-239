"""
Email module.

This module contains functions to send emails as well as generate reports
to send in the emails.

"""

import datetime
import logging
import smtplib

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from folioflex.portfolio import heatmap
from folioflex.portfolio.portfolio import Portfolio, Manager
from folioflex.utils import config_helper


# logging options https://docs.python.org/3/library/logging.html
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")

# provides the logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def send_email(message, subject, email_list, image_list=None):
    """Send summary of portfolios to email.

    Parameters
    ----------
    message : object
        Message to send in email
    subject : str
        Subject of email
    email_list : list
        Email addresses to send email to
    image_list : list
        Images to attach to email

    Returns
    ----------
    bool
        True if email was sent successfully, False otherwise.

    """
    # Check if SMTP values are set
    for key, value in config_helper.__dict__.items():
        if key.startswith("SMTP_") and not value:
            logger.warning(f"{key} is not set, email not sent")
            return False

    # Create the email
    email = MIMEMultipart()
    email["Subject"] = subject
    email["From"] = config_helper.SMTP_USERNAME
    email["To"] = ";".join(email_list)

    message = MIMEText(message, "html")
    email.attach(message)

    if image_list:
        for idx, image in enumerate(image_list, start=1):
            email_image = MIMEImage(image)
            email_image.add_header("Content-ID", f"image{idx}")
            email_image.add_header(
                "Content-Disposition", "attachment", filename=f"image{idx}.png"
            )
            email.attach(email_image)

    # Send the email
    try:
        with smtplib.SMTP(config_helper.SMTP_SERVER, config_helper.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(config_helper.SMTP_USERNAME, config_helper.SMTP_PASSWORD)
            smtp.send_message(email)
        logger.info("Email sent successfully")
        return True
    except smtplib.SMTPException as e:
        logger.warning(f"Error sending email: {e}")
        return False


def generate_report(
    email_list,
    heatmap_dict=None,
    heatmap_port=None,
    manager_dict=None,
    portfolio_dict=None,
):
    """Generate report of portfolio performance and send to email.

    Parameters
    ----------
    email_list : list
        Email addresses to send email to
    heatmap_dict : dict
        Market Heatmap dictionary to get values for
            see: folioflex.portfolio.heatmap.get_heatmap for more details
            Keys are:
            - lookback (optional)
    heatmap_port : dict
        Portfolio Heatmap dictionary to get values for
            see: folioflex.portfolio.heatmap.get_heatmap for more details
            Keys are:
            - config_path (optional)
            - portfolio (optional)
            - lookback (optional)
    manager_dict : dict
        Manager dictionary to get values for
            see: folioflex.portfolio.portfolio.Manager.get_summary for more details
            Keys are:
            - config_path
            - portfolios (optional)
            - date (optional)
            - lookbacks (optional)
    portfolio_dict : dict
        Portfolio dictionary to get values for
            see: folioflex.portfolio.portfolio.Portfolio.get_performance for more details
            Keys are:
            - config_path
            - portfolio
            - date (optional)
            - lookback (optional)

    Returns
    ----------
    bool
        True if email was sent successfully, False otherwise.
    """
    # building the email message

    today = datetime.date.today()
    subject = f"Summary as of {today}"
    message = f"Below is your financial summary as of {today}.<br><br>"
    image_list = []
    image_idx = 1

    if heatmap_dict is not None:
        lookback = heatmap_dict.get("lookback", None)

        heatmap_summary = heatmap.get_heatmap(lookback=lookback)
        # using plotly kaleido to convert to image into bytes then attach it to the email.
        image = heatmap_summary.to_image(format="png")
        image_list.append(image)

        message += (
            f"<p>Market Heatmap Summary</p>"
            f"<ul>"
            f"<li>lookback: {lookback}</li>"
            f"</ul>"
            f"<img src='cid:image{image_idx}' alt='heatmap market'/>" + "<br>"
        )

        image_idx += 1

    if heatmap_port is not None:
        config_path = heatmap_port.get("config_path", None)
        portfolio = heatmap_port.get("portfolio", None)
        lookback = heatmap_port.get("lookback", None)

        heatmap_summary = heatmap.get_heatmap(
            config_path=config_path, portfolio=portfolio, lookback=lookback
        )
        # using plotly kaleido to convert to image into bytes then attach it to the email.
        image = heatmap_summary.to_image(format="png")
        image_list.append(image)

        message += (
            f"<p>Portfolio Heatmap Summary</p>"
            f"<ul>"
            f"<li>portfolio: {portfolio}</li>"
            f"<li>lookback: {lookback}</li>"
            f"</ul>"
            f"<img src='cid:image{image_idx}' alt='heatmap portfolio'/>" + "<br>"
        )

        image_idx += 1

    if manager_dict is not None:
        config_path = manager_dict.get("config_path")
        portfolios = manager_dict.get("portfolios", None)
        date = manager_dict.get("date", None)
        lookbacks = manager_dict.get("lookbacks", None)

        manager_summary = Manager(
            config_path=config_path, portfolios=portfolios
        ).get_summary(date=date, lookbacks=lookbacks)

        message += (
            f"<p>Manager Summary</p>"
            f"<ul>"
            f"<li>lookbacks: {lookbacks}</li>"
            f"</ul><br>" + manager_summary.to_html() + "<br>"
        )

    if portfolio_dict is not None:
        config_path = portfolio_dict.get("config_path")
        portfolio = portfolio_dict.get("portfolio")
        date = portfolio_dict.get("date", None)
        lookback = portfolio_dict.get("lookback", None)

        portfolio_summary = Portfolio(
            config_path=config_path, portfolio=portfolio
        ).get_performance(date=date, lookback=lookback)

        # remove rows with 0 market value
        portfolio_summary = portfolio_summary[
            portfolio_summary["market_value"] != 0
        ].sort_values("market_value", ascending=False)

        message += (
            f"<p>Portfolio Summary</p>"
            f"<ul>"
            f"<li>portfolio: {portfolio}</li>"
            f"<li>lookback: {lookback}</li>"
            f"</ul><br>" + portfolio_summary.to_html() + "<br>"
        )

    return send_email(
        message, subject=subject, email_list=email_list, image_list=image_list
    )
