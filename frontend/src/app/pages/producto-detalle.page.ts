// =============================================================================
// Archivo: pages/producto-detalle.page.ts
// Propósito: Ficha del equipo + acción “Añadir al carrito”.
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, switchMap } from 'rxjs';

import { CarritoService } from '../core/carrito.service';
import { ProductoService } from '../core/producto.service';
import { Producto } from '../models/producto';

@Component({
  selector: 'app-producto-detalle-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './producto-detalle.page.html',
  styleUrl: './producto-detalle.page.scss',
})
export class ProductoDetallePage {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(ProductoService);
  private readonly carrito = inject(CarritoService);

  protected readonly producto = signal<Producto | null>(null);
  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);
  protected readonly feedback = signal<string | null>(null);

  constructor() {
    this.route.paramMap
      .pipe(
        map((pm) => Number(pm.get('id') ?? 'NaN')),
        switchMap((id) => {
          this.cargando.set(true);
          this.error.set(null);
          this.feedback.set(null);
          if (!Number.isFinite(id) || id < 1) {
            this.cargando.set(false);
            return of<{ ok: true; p: Producto } | { ok: false; mensaje: string }>({
              ok: false,
              mensaje: 'Producto no válido.',
            });
          }
          return this.api.obtener(id).pipe(
            map((p) => ({ ok: true as const, p })),
            catchError(() =>
              of<{ ok: true; p: Producto } | { ok: false; mensaje: string }>({
                ok: false,
                mensaje: 'No encontramos este equipo o el servidor no responde.',
              }),
            ),
          );
        }),
        takeUntilDestroyed(),
      )
      .subscribe((res) => {
        this.cargando.set(false);
        if (res.ok) {
          this.producto.set(res.p);
          this.error.set(null);
        } else {
          this.producto.set(null);
          this.error.set(res.mensaje);
        }
      });
  }

  protected anadirAlCarrito(): void {
    const p = this.producto();
    if (!p) {
      return;
    }
    this.carrito.agregar(p, 1);
    this.feedback.set('Producto añadido al carrito.');
    window.setTimeout(() => this.feedback.set(null), 2800);
  }
}
