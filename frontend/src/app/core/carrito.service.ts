// =============================================================================
// Archivo: core/carrito.service.ts
// Propósito: Carrito demo en el cliente (localStorage + señales reactivas).
// =============================================================================
import { computed, Injectable, signal } from '@angular/core';

import { LineaCarrito } from '../models/linea-carrito';
import { Producto } from '../models/producto';

const STORAGE_KEY = 'dt-technology-cart-v1';

@Injectable({ providedIn: 'root' })
export class CarritoService {
  readonly lineas = signal<LineaCarrito[]>([]);

  /** Unidades totales (suma de cantidades). */
  readonly cantidadTotal = computed(() =>
    this.lineas().reduce((acc, l) => acc + l.cantidad, 0),
  );

  /** Importe total (asume precio numérico en string). */
  readonly importeTotal = computed(() =>
    this.lineas().reduce((acc, l) => acc + Number(l.producto.precio) * l.cantidad, 0),
  );

  constructor() {
    this.restaurarDesdeAlmacen();
  }

  /** Añade una unidad del producto (o incrementa si ya existe). */
  agregar(producto: Producto, unidades = 1): void {
    if (unidades < 1) {
      return;
    }
    this.lineas.update((lista) => {
      const idx = lista.findIndex((l) => l.producto.id === producto.id);
      if (idx === -1) {
        return [...lista, { producto, cantidad: unidades }];
      }
      const copia = [...lista];
      copia[idx] = { ...copia[idx], cantidad: copia[idx].cantidad + unidades };
      return copia;
    });
    this.persistir();
  }

  /** Quita una línea por id de producto. */
  quitar(productoId: number): void {
    this.lineas.update((lista) => lista.filter((l) => l.producto.id !== productoId));
    this.persistir();
  }

  vaciar(): void {
    this.lineas.set([]);
    this.persistir();
  }

  private persistir(): void {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.lineas()));
    } catch {
      /* ignorar quota / modo privado */
    }
  }

  private restaurarDesdeAlmacen(): void {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return;
      }
      const parsed = JSON.parse(raw) as LineaCarrito[];
      if (!Array.isArray(parsed)) {
        return;
      }
      const validas = parsed.filter(
        (x) =>
          x &&
          typeof x.cantidad === 'number' &&
          x.cantidad > 0 &&
          x.producto &&
          typeof x.producto.id === 'number' &&
          typeof x.producto.nombre === 'string',
      );
      this.lineas.set(validas);
    } catch {
      this.lineas.set([]);
    }
  }
}
