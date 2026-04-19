// =============================================================================
// Archivo: core/producto.service.ts
// Carpeta: frontend/src/app/core/
// Propósito: Centraliza las llamadas HTTP al endpoint `/api/productos/`.
// =============================================================================
import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Producto } from '../models/producto';

export type OrdenListado =
  | ''
  | '-creado_en'
  | 'precio'
  | '-precio'
  | 'nombre'
  | '-nombre'
  | 'id'
  | '-id';

@Injectable({ providedIn: 'root' })
export class ProductoService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/api';

  /**
   * Lista productos.
   * @param categoria filtro opcional (ej. `celular`)
   * @param q búsqueda en nombre, marca o descripción (API)
   * @param ordering orden Django (`-creado_en`, `precio`, …)
   */
  listar(categoria?: string, q?: string, ordering?: OrdenListado): Observable<Producto[]> {
    let params = new HttpParams();
    if (categoria) {
      params = params.set('categoria', categoria);
    }
    const t = (q ?? '').trim();
    if (t) {
      params = params.set('q', t);
    }
    const ord = (ordering ?? '').trim() as OrdenListado;
    if (ord) {
      params = params.set('ordering', ord);
    }

    return this.http.get<Producto[]>(`${this.baseUrl}/productos/`, { params });
  }

  obtener(id: number): Observable<Producto> {
    return this.http.get<Producto>(`${this.baseUrl}/productos/${id}/`);
  }
}
