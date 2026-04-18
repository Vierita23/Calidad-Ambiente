// =============================================================================
// Archivo: pages/catalogo.page.ts
// Carpeta: frontend/src/app/pages/
// Propósito: Muestra el catálogo consumiendo el API (`ProductoService`).
// También lee `?categoria=` desde la URL (enlaces del pie y compartir filtros).
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, computed, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ProductoService } from '../core/producto.service';
import { Producto } from '../models/producto';

@Component({
  selector: 'app-catalogo-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './catalogo.page.html',
  styleUrl: './catalogo.page.scss',
})
export class CatalogoPage {
  /** Servicio que encapsula el HTTP hacia Django. */
  private readonly productosApi = inject(ProductoService);

  /** Ruta actual (query params). */
  private readonly route = inject(ActivatedRoute);

  /** Permite cancelar la suscripción al destruir el componente. */
  private readonly destroyRef = inject(DestroyRef);

  /** Respuesta cruda del API (antes del filtro de texto `?q=`). */
  private readonly productosCrudos = signal<Producto[]>([]);

  /** Texto de búsqueda desde la URL (`?q=`). */
  protected readonly terminoBusqueda = signal('');

  /** Lista filtrada para la vista. */
  protected readonly productos = computed(() => {
    const items = this.productosCrudos();
    const q = this.terminoBusqueda().trim().toLowerCase();
    if (!q) {
      return items;
    }
    return items.filter((p) => {
      const nombre = p.nombre.toLowerCase();
      const desc = (p.descripcion ?? '').toLowerCase();
      const marca = (p.marca ?? '').toLowerCase();
      return nombre.includes(q) || desc.includes(q) || marca.includes(q);
    });
  });

  /** Indicador de carga para UX (evita “pantalla vacía” silenciosa). */
  protected readonly cargando = signal(true);

  /** Mensaje de error legible si falla la petición. */
  protected readonly error = signal<string | null>(null);

  /** Filtro activo (vacío = todas). */
  protected readonly filtro = signal<string>('');

  /** Categorías válidas en backend (debe coincidir con `Producto.Categoria`). */
  private static readonly categoriasValidas = new Set(['', 'celular', 'tablet', 'reloj', 'laptop']);

  /** Opciones del select (valor = código backend; texto = etiqueta humana). */
  protected readonly opcionesFiltro: Array<{ valor: string; etiqueta: string }> = [
    { valor: '', etiqueta: 'Todas las categorías' },
    { valor: 'celular', etiqueta: 'Celulares' },
    { valor: 'tablet', etiqueta: 'Tablets' },
    { valor: 'reloj', etiqueta: 'Relojes' },
    { valor: 'laptop', etiqueta: 'Laptops' },
  ];

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((pm) => {
      const raw = (pm.get('categoria') ?? '').trim();
      const next = CatalogoPage.categoriasValidas.has(raw) ? raw : '';
      this.filtro.set(next);
      this.terminoBusqueda.set((pm.get('q') ?? '').trim());
      this.refrescar();
    });
  }

  /** Disparado por el `<select>` del template. */
  protected onCambioFiltro(valor: string): void {
    this.filtro.set(valor);
    this.refrescar();
  }

  /** Consulta el backend y actualiza señales reactivas. */
  private refrescar(): void {
    this.cargando.set(true);
    this.error.set(null);

    const categoria = this.filtro();
    const filtro = categoria ? categoria : undefined;

    this.productosApi.listar(filtro).subscribe({
      next: (items) => {
        this.productosCrudos.set(items);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No pudimos cargar el catálogo. Verifica que el backend esté encendido.');
        this.cargando.set(false);
      },
    });
  }
}
