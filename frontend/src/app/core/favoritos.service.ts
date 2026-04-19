// =============================================================================
// Archivo: core/favoritos.service.ts
// Propósito: Favoritos en cliente (localStorage) — demo sin cuenta de usuario.
// =============================================================================
import { computed, Injectable, signal } from '@angular/core';

const STORAGE_KEY = 'dt-technology-favoritos-v1';

@Injectable({ providedIn: 'root' })
export class FavoritosService {
  private readonly ids = signal<Set<number>>(new Set());

  /** Cantidad para badge en cabecera. */
  readonly cantidad = computed(() => this.ids().size);

  constructor() {
    this.restaurar();
  }

  tiene(id: number): boolean {
    return this.ids().has(id);
  }

  alternar(id: number): void {
    this.ids.update((s) => {
      const next = new Set(s);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
    this.persistir();
  }

  todosLosIds(): number[] {
    return [...this.ids()];
  }

  private persistir(): void {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...this.ids()]));
    } catch {
      /* ignorar */
    }
  }

  private restaurar(): void {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return;
      }
      const arr = JSON.parse(raw) as unknown;
      if (!Array.isArray(arr)) {
        return;
      }
      const nums = arr.filter((x): x is number => typeof x === 'number' && x > 0);
      this.ids.set(new Set(nums));
    } catch {
      this.ids.set(new Set());
    }
  }
}
