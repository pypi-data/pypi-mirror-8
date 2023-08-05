# -*- coding: utf-8 -*-
"""
    SMTP mailer.
"""
import smtplib
import socket
import threading

from .base import BaseMailer
from ..utils import sanitize_address, DNS_NAME


class SMTPMailer(BaseMailer):
    """A wrapper that manages the SMTP network connection.
    """

    def __init__(self, host='localhost', port=587, username=None, password=None,
                 use_tls=True, *args, **kwargs):
        """
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = bool(use_tls)
        self.connection = None
        self._lock = threading.RLock()
        super(SMTPMailer, self).__init__(*args, **kwargs)

    def open(self):
        """Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            # For performance, we use the cached FQDN for local_hostname.
            self.connection = smtplib.SMTP(self.host, self.port,
                                           local_hostname=DNS_NAME.get_fqdn())
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
        except:
            if not self.fail_silently:
                raise
        return True

    def close(self):
        """Closes the connection to the email server.
        """
        try:
            try:
                self.connection.quit()
            except socket.sslerror:
                # This happens when calling quit() on a TLS connection
                # sometimes.
                self.connection.close()
            except:
                if self.fail_silently:
                    return
                raise
        finally:
            self.connection = None

    def send_messages(self, *email_messages):
        """Sends one or more EmailMessage objects and returns the number of
        messages sent.
        """
        if not email_messages:
            return
        self._lock.acquire()
        try:
            new_conn_created = self.open()
            if not self.connection:
                # We failed silently on open().
                # Trying to send would be pointless.
                return
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
            if new_conn_created:
                self.close()
        finally:
            self._lock.release()
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending.
        """
        recipients = email_message.get_recipients()
        if not recipients:
            return False
        from_email = email_message.from_email or self.default_from
        from_email = sanitize_address(from_email, email_message.encoding)
        recipients = [
            sanitize_address(addr, email_message.encoding)
            for addr in recipients]
        try:
            self.connection.sendmail(from_email, recipients,
                                     email_message.as_string())
        except:
            if not self.fail_silently:
                raise
            return False
        return True
