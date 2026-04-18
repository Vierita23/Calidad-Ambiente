// =============================================================================
// Archivo: layout/app-footer.ts
// Carpeta: frontend/src/app/layout/
// Propósito: Pie de página corporativo (4 columnas) según diseño DT Technology.
// =============================================================================
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { WHATSAPP_E164_DIGITS } from '../core/whatsapp.config';
import { construirUrlWhatsApp } from '../core/whatsapp.util';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './app-footer.html',
  styleUrl: './app-footer.scss',
})
export class AppFooter {
  /** Año dinámico para la barra inferior de copyright. */
  protected readonly anio = new Date().getFullYear();

  /** Enlace directo a WhatsApp para la fila “Contáctanos” del pie. */
  protected readonly whatsappHref = construirUrlWhatsApp(
    WHATSAPP_E164_DIGITS,
    'Hola, quiero información desde la web de DT Technology.',
  );

  /** Redes: enlaces genéricos a las plataformas (reemplazar por perfiles oficiales cuando existan). */
  protected readonly redes = [
    { nombre: 'Facebook', href: 'https://www.facebook.com/', icono: 'fb' as const },
    { nombre: 'Instagram', href: 'https://www.instagram.com/', icono: 'ig' as const },
    { nombre: 'TikTok', href: 'https://www.tiktok.com/', icono: 'tt' as const },
    { nombre: 'YouTube', href: 'https://www.youtube.com/', icono: 'yt' as const },
  ];
}
