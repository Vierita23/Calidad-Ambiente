// =============================================================================
// Archivo: app.ts
// Carpeta: frontend/src/app/
// Propósito: Componente raíz (`<app-root>`) que define el layout global.
// =============================================================================
import { afterNextRender, Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Title } from '@angular/platform-browser';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';

import { AppFooter } from './layout/app-footer';
import { AppHeader } from './layout/app-header';
import { AppToast } from './layout/app-toast';
import { WhatsappFab } from './layout/whatsapp-fab';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, AppHeader, AppFooter, WhatsappFab, AppToast],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  /** Intro breve con logo al cargar el sitio. */
  protected readonly splash = signal(true);

  constructor() {
    const router = inject(Router);
    const docTitle = inject(Title);
    const destroyRef = inject(DestroyRef);

    const syncTitle = (): void => {
      let r = router.routerState.snapshot.root;
      while (r.firstChild) {
        r = r.firstChild;
      }
      const t = r.data['title'] as string | undefined;
      docTitle.setTitle(t ? `${t} · DT Technology` : 'DT Technology');
    };
    syncTitle();
    router.events
      .pipe(
        filter((e): e is NavigationEnd => e instanceof NavigationEnd),
        takeUntilDestroyed(destroyRef),
      )
      .subscribe(() => syncTitle());

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
