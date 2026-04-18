// =============================================================================
// Archivo: models/linea-carrito.ts
// Propósito: Línea del carrito en memoria (persistencia local opcional).
// =============================================================================
import { Producto } from './producto';

export interface LineaCarrito {
  producto: Producto;
  cantidad: number;
}
