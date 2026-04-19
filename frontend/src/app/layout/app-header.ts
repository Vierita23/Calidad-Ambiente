// =============================================================================
// Archivo: layout/app-header.ts
// Carpeta: frontend/src/app/layout/
// Propósito: Cabecera global con búsqueda (envía al catálogo con `?q=`).
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

import { CarritoService } from '../core/carrito.service';
import { FavoritosService } from '../core/favoritos.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './app-header.html',
  styleUrl: './app-header.scss',
})
export class AppHeader {
  private readonly router = inject(Router);
  protected readonly carrito = inject(CarritoService);
  protected readonly favoritos = inject(FavoritosService);

  protected onBuscar(event: Event): void {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const raw = (new FormData(form).get('q') as string | null) ?? '';
    const q = raw.trim();
    this.router.navigate(['/catalogo'], { queryParams: q ? { q } : {} });
  }
}
