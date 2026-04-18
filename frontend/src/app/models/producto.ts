// =============================================================================
// Archivo: models/producto.ts
// Carpeta: frontend/src/app/models/
// Propósito: Tipos TypeScript que reflejan el JSON devuelto por Django REST.
// Nota: `precio` llega como string porque JSON no tiene tipo Decimal.
// =============================================================================

/** Códigos de categoría alineados con `Producto.Categoria` en el backend. */
export type CategoriaProducto = 'celular' | 'tablet' | 'reloj' | 'laptop';

/** Representación de un producto en el catálogo (respuesta del API). */
export interface Producto {
  id: number;
  nombre: string;
  /** Marca comercial (puede venir vacía o ausente en datos legacy). */
  marca?: string;
  categoria: CategoriaProducto;
  categoria_display: string;
  descripcion: string;
  precio: string;
  /** Código ISO (normalmente `USD` en este proyecto). */
  moneda?: string;
  imagen_url: string;
  creado_en: string;
}
