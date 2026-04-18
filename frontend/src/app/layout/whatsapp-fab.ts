// =============================================================================
// Archivo: layout/whatsapp-fab.ts
// Carpeta: frontend/src/app/layout/
// Propósito: Botón flotante global para contactar por WhatsApp desde cualquier ruta.
// =============================================================================
import { Component } from '@angular/core';

import { WHATSAPP_E164_DIGITS } from '../core/whatsapp.config';
import { abrirWhatsAppEnNuevaPestana, construirUrlWhatsApp } from '../core/whatsapp.util';

@Component({
  selector: 'app-whatsapp-fab',
  standalone: true,
  templateUrl: './whatsapp-fab.html',
  styleUrl: './whatsapp-fab.scss',
})
export class WhatsappFab {
  /** Texto corto para chats rápidos iniciados desde el botón flotante. */
  protected readonly mensajeRapido =
    'Hola, quiero información sobre productos disponibles en DT Technology.';

  /** URL lista para `aria-label` + `href` (accesible aunque falle JS). */
  protected readonly href = construirUrlWhatsApp(WHATSAPP_E164_DIGITS, this.mensajeRapido);

  /** Evita navegación “dura”: abrimos en pestaña nueva como en el formulario. */
  protected onClick(event: MouseEvent): void {
    event.preventDefault();
    abrirWhatsAppEnNuevaPestana(this.href);
  }
}
