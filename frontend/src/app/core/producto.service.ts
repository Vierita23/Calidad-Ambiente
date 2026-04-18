// =============================================================================
// Archivo: core/producto.service.ts
// Carpeta: frontend/src/app/core/
// Propósito: Centraliza las llamadas HTTP al endpoint `/api/productos/`.
//
// Por qué `/api`:
// - En `ng serve`, `proxy.conf.json` reenvía `/api` a `http://localhost:8000`.
// - En Docker, `nginx.conf` reenvía `/api` al servicio `backend`.
// =============================================================================
import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Producto } from '../models/producto';

@Injectable({ providedIn: 'root' })
export class ProductoService {
  /** Cliente HTTP inyectado (requiere `provideHttpClient()` en `app.config.ts`). */
  private readonly http = inject(HttpClient);

  /** Prefijo estable del API (ver comentario del archivo). */
  private readonly baseUrl = '/api';

  /**
   * Lista productos.
   * @param categoria filtro opcional (ej. `celular`) alineado con el backend.
   */
  listar(categoria?: string): Observable<Producto[]> {
    let params = new HttpParams();
    if (categoria) {
      params = params.set('categoria', categoria);
    }

    // Ojo: la URL termina en `/` para coincidir con el estilo de Django/DRF.
    return this.http.get<Producto[]>(`${this.baseUrl}/productos/`, { params });
  }

  /** Detalle de un producto (`GET /api/productos/{id}/`). */
  obtener(id: number): Observable<Producto> {
    return this.http.get<Producto>(`${this.baseUrl}/productos/${id}/`);
  }
}
