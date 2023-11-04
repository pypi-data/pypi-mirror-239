# -*- coding: utf-8 -*-

import asyncio
import json
import socket

from asgiref.sync import async_to_sync, sync_to_async

from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator

# Mikäli pistoke-paketti ei ole käytössä, käytetään Djangon vakio-
# näkymäluokkaa. Tällöin metodi `async def websocket` ei ole ongelma,
# sillä sitä ei tunnisteta HTTP-verbin toteutukseksi.
try:
  from pistoke.nakyma import WebsocketNakyma
  from pistoke import WebsocketProtokolla
except ImportError:
  # pylint: disable=ungrouped-imports
  from django.views.generic import View as WebsocketNakyma
  WebsocketProtokolla = lambda x: x

from .celery import celery_app, celery_viestikanava


class Ilmoitukset(WebsocketNakyma):

  bootstrap_luokat = {
    'debug': 'alert-info',
    'info': 'alert-info',
    'success': 'alert-success',
    'warning': 'alert-warning',
    'error': 'alert-danger',
  }

  def _ilmoitus(self, ilmoitus):
    ''' Muodosta JSON-yhteensopiva sanoma ilmoituksen tiedoin. '''
    return {
      'level': ilmoitus.level,
      'message': ilmoitus.message,
      'tags': ' '.join((
        self.bootstrap_luokat.get(luokka, luokka)
        for luokka in ilmoitus.tags.split(' ')
      ))
    }
    # def _ilmoitus

  def get(self, request, *args, **kwargs):
    ''' Ajax-toteutus. Palauta JSON-sanoma kaikista ilmoituksista. '''
    # pylint: disable=unused-argument
    storage = messages.get_messages(request)
    return JsonResponse([
      self._ilmoitus(ilmoitus)
      for ilmoitus in storage
    ], safe=False)
    # def get

  @method_decorator(WebsocketProtokolla)
  async def websocket(self, request):
    '''
    Websocket-toteutus. Palauta ilmoituksia sitä mukaa, kun niitä tallennetaan.

    Vaatii django-pistoke-paketin asennuksen.
    '''
    async def laheta_ilmoitukset(signaali=None):
      ''' Lähetä kaikki olemassaolevat ilmoitukset selaimelle. '''
      # pylint: disable=unused-argument
      def hae_ilmoitukset():
        # pylint: disable=protected-access
        request.session._session_cache = request.session.load()
        request._messages = messages.storage.default_storage(request)
        for ilmoitus in request._messages:
          yield json.dumps(self._ilmoitus(ilmoitus))
        request._messages.update(None)
        request.session.save()
        # def hae_ilmoitukset
      for ilmoitus in await sync_to_async(lambda: list(hae_ilmoitukset()))():
        await request.send(ilmoitus)
        # for ilmoitus in await sync_to_async
      # async def laheta_ilmoitukset

    # Lähetä mahdolliset olemassaolevat ilmoitukset heti.
    await laheta_ilmoitukset()

    # Luo kanava Celery-signaalien kuunteluun.
    try:
      channel = celery_app.broker_connection().channel()
    except Exception:
      await request.send(json.dumps({'status': '500'}))
      raise

    # Luo rutiini Celery-viestien vastaanottoon taustalla.
    loop = asyncio.get_running_loop()
    receiver = celery_app.events.Receiver(
      channel=channel,
      handlers={
        celery_viestikanava(request.session.session_key):
        async_to_sync(laheta_ilmoitukset),
      }
    )

    # Aja taustalla Celery-kuuntelua, odota Websocket-yhteyden katkaisua.
    celery_paattyi = asyncio.Event()
    def celery_capture():
      try:
        receiver.capture()
      finally:
        celery_paattyi.set()
      # def celery_capture
    luku = loop.run_in_executor(None, celery_capture)

    async def odota_ja_katkaise():
      ''' Odota poikkeukseen (CancelledError) saakka. '''
      try:
        await celery_paattyi.wait()
      finally:
        receiver.should_stop = True

    # Kuuntele Celery-signaaleja, kunnes yhteys katkaistaan.
    await asyncio.gather(luku, odota_ja_katkaise())
    # async def websocket

  # class Ilmoitukset
