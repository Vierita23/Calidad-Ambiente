// =============================================================================
// Archivo: core/toast.service.ts
// Propósito: Mensajes breves no intrusivos (éxito / info).
// =============================================================================
import { Injectable, signal } from '@angular/core';

export type ToastTipo = 'ok' | 'info';

export interface ToastMensaje {
  id: number;
  texto: string;
  tipo: ToastTipo;
}

@Injectable({ providedIn: 'root' })
export class ToastService {
  readonly mensajes = signal<ToastMensaje[]>([]);
  private seq = 0;

  exito(texto: string): void {
    this.mostrar(texto, 'ok');
  }

  info(texto: string): void {
    this.mostrar(texto, 'info');
  }

  private mostrar(texto: string, tipo: ToastTipo): void {
    const id = ++this.seq;
    this.mensajes.update((lista) => [...lista, { id, texto, tipo }]);
    window.setTimeout(() => this.quitar(id), 3400);
  }

  quitar(id: number): void {
    this.mensajes.update((lista) => lista.filter((m) => m.id !== id));
  }
}
