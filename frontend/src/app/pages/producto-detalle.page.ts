// =============================================================================
// Archivo: pages/producto-detalle.page.ts
// Propósito: Ficha del equipo + acción “Añadir al carrito” y favoritos.
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of, switchMap } from 'rxjs';

import { CarritoService } from '../core/carrito.service';
import { FavoritosService } from '../core/favoritos.service';
import { ProductoService } from '../core/producto.service';
import { ToastService } from '../core/toast.service';
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
  private readonly destroyRef = inject(DestroyRef);
  private readonly api = inject(ProductoService);
  private readonly carrito = inject(CarritoService);
  private readonly toast = inject(ToastService);
  protected readonly favoritos = inject(FavoritosService);

  protected readonly producto = signal<Producto | null>(null);
  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);

  constructor() {
    this.route.paramMap
      .pipe(
        map((pm) => Number(pm.get('id') ?? 'NaN')),
        switchMap((id) => {
          this.cargando.set(true);
          this.error.set(null);
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
        takeUntilDestroyed(this.destroyRef),
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
    this.toast.exito(`«${p.nombre}» añadido al carrito`);
  }

  protected toggleFavorito(): void {
    const p = this.producto();
    if (!p) {
      return;
    }
    const era = this.favoritos.tiene(p.id);
    this.favoritos.alternar(p.id);
    this.toast.exito(era ? `Quitaste «${p.nombre}» de favoritos` : `«${p.nombre}» guardado en favoritos`);
  }
}
