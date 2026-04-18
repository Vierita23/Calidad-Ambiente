// =============================================================================
// Archivo: pages/contacto.page.ts
// Carpeta: frontend/src/app/pages/
// Propósito: Contacto + formulario que abre WhatsApp con el mensaje prellenado.
//
// Flujo:
// 1) El usuario completa nombre/mensaje (correo opcional).
// 2) Al enviar, construimos un texto y abrimos `wa.me` en una pestaña nueva.
// =============================================================================
import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { WHATSAPP_E164_DIGITS } from '../core/whatsapp.config';
import { abrirWhatsAppEnNuevaPestana, construirUrlWhatsApp } from '../core/whatsapp.util';

@Component({
  selector: 'app-contacto-page',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './contacto.page.html',
  styleUrl: './contacto.page.scss',
})
export class ContactoPage {
  /** Nombre del cliente (obligatorio para enviar). */
  protected nombre = '';

  /** Correo opcional (si existe, se incluye en el mensaje de WhatsApp). */
  protected correo = '';

  /** Mensaje del cliente (obligatorio para enviar). */
  protected mensaje = '';

  /** Evita doble clic mientras se abre WhatsApp. */
  protected readonly enviando = signal(false);

  /** Texto de ayuda / error simple (sin librerías de validación). */
  protected readonly aviso = signal<string | null>(null);

  /**
   * Construye el cuerpo del mensaje según el formato solicitado por negocio.
   * Si agregas campos nuevos, actualiza también la plantilla HTML.
   */
  private construirMensaje(): string {
    const lineas = ['Hola, quiero información.', `Nombre: ${this.nombre.trim()}`, `Mensaje: ${this.mensaje.trim()}`];
    if (this.correo.trim()) {
      lineas.splice(2, 0, `Correo: ${this.correo.trim()}`);
    }
    return lineas.join('\n');
  }

  /** Handler del submit del formulario. */
  protected enviarPorWhatsApp(): void {
    this.aviso.set(null);

    if (!this.nombre.trim() || !this.mensaje.trim()) {
      this.aviso.set('Por favor completa tu nombre y tu mensaje antes de enviar.');
      return;
    }

    this.enviando.set(true);
    try {
      const url = construirUrlWhatsApp(WHATSAPP_E164_DIGITS, this.construirMensaje());
      abrirWhatsAppEnNuevaPestana(url);
    } finally {
      // WhatsApp abre en otra pestaña; liberamos el estado casi de inmediato.
      this.enviando.set(false);
    }
  }
}
