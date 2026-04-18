// =============================================================================
// Archivo: app.ts
// Carpeta: frontend/src/app/
// Propósito: Componente raíz (`<app-root>`) que define el layout global.
// =============================================================================
import { afterNextRender, Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { AppFooter } from './layout/app-footer';
import { AppHeader } from './layout/app-header';
import { WhatsappFab } from './layout/whatsapp-fab';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, AppHeader, AppFooter, WhatsappFab],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  /** Título interno del documento (útil si más adelante sincronizas con el router). */
  protected readonly title = signal('DT Technology');

  /** Intro breve con logo al cargar el sitio. */
  protected readonly splash = signal(true);

  constructor() {
    afterNextRender(() => {
      if (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        this.splash.set(false);
      }
    });
  }

  /**
   * Cierra la intro al terminar la animación del velo (2 s).
   * Se filtra por nombre para ignorar burbujeo de animaciones hijas.
   */
  protected onSplashAnimationEnd(event: AnimationEvent): void {
    if (event.target !== event.currentTarget || event.animationName !== 'splash-veil') {
      return;
    }
    this.splash.set(false);
  }
}
