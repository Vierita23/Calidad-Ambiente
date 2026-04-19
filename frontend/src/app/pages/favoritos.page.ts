// =============================================================================
// Archivo: pages/favoritos.page.ts
// Propósito: Lista productos marcados como favoritos (solo cliente).
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, computed, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';

import { FavoritosService } from '../core/favoritos.service';
import { ProductoService } from '../core/producto.service';
import { Producto } from '../models/producto';

@Component({
  selector: 'app-favoritos-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './favoritos.page.html',
  styleUrl: './favoritos.page.scss',
})
export class FavoritosPage {
  private readonly api = inject(ProductoService);
  private readonly fav = inject(FavoritosService);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);
  protected readonly todos = signal<Producto[]>([]);

  protected readonly favoritos = computed(() => {
    const set = new Set(this.fav.todosLosIds());
    return this.todos().filter((p) => set.has(p.id));
  });

  constructor() {
    this.api
      .listar(undefined, undefined, '-creado_en')
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (items) => {
          this.todos.set(items);
          this.cargando.set(false);
        },
        error: () => {
          this.error.set('No pudimos cargar el catálogo.');
          this.cargando.set(false);
        },
      });
  }

  protected trackPorId(_i: number, p: Producto): number {
    return p.id;
  }
}
