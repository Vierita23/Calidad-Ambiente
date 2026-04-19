// =============================================================================
// Archivo: pages/catalogo.page.ts
// Carpeta: frontend/src/app/pages/
// Propósito: Catálogo con filtros en URL, búsqueda y orden en el API.
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { FavoritosService } from '../core/favoritos.service';
import { OrdenListado, ProductoService } from '../core/producto.service';
import { ToastService } from '../core/toast.service';
import { Producto } from '../models/producto';

@Component({
  selector: 'app-catalogo-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './catalogo.page.html',
  styleUrl: './catalogo.page.scss',
})
export class CatalogoPage {
  private readonly productosApi = inject(ProductoService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  protected readonly favoritos = inject(FavoritosService);
  private readonly toast = inject(ToastService);

  protected readonly productos = signal<Producto[]>([]);
  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);
  protected readonly filtro = signal<string>('');
  protected readonly terminoBusqueda = signal('');
  protected readonly orden = signal<OrdenListado>('');

  private static readonly categoriasValidas = new Set(['', 'celular', 'tablet', 'reloj', 'laptop']);

  private static readonly ordenesValidos = new Set<OrdenListado>([
    '',
    '-creado_en',
    'precio',
    '-precio',
    'nombre',
    '-nombre',
    'id',
    '-id',
  ]);

  protected readonly opcionesFiltro: Array<{ valor: string; etiqueta: string }> = [
    { valor: '', etiqueta: 'Todas las categorías' },
    { valor: 'celular', etiqueta: 'Celulares' },
    { valor: 'tablet', etiqueta: 'Tablets' },
    { valor: 'reloj', etiqueta: 'Relojes' },
    { valor: 'laptop', etiqueta: 'Laptops' },
  ];

  protected readonly opcionesOrden: Array<{ valor: OrdenListado; etiqueta: string }> = [
    { valor: '', etiqueta: 'Orden por defecto' },
    { valor: '-creado_en', etiqueta: 'Más recientes' },
    { valor: '-precio', etiqueta: 'Mayor precio' },
    { valor: 'precio', etiqueta: 'Menor precio' },
    { valor: 'nombre', etiqueta: 'Nombre A–Z' },
    { valor: '-nombre', etiqueta: 'Nombre Z–A' },
  ];

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((pm) => {
      const rawCat = (pm.get('categoria') ?? '').trim();
      this.filtro.set(CatalogoPage.categoriasValidas.has(rawCat) ? rawCat : '');
      this.terminoBusqueda.set((pm.get('q') ?? '').trim());
      const rawOrd = (pm.get('orden') ?? '').trim() as OrdenListado;
      this.orden.set(CatalogoPage.ordenesValidos.has(rawOrd) ? rawOrd : '');
      this.refrescar();
    });
  }

  protected onCambioFiltro(valor: string): void {
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { categoria: valor || null },
      queryParamsHandling: 'merge',
    });
  }

  protected onCambioOrden(valor: string): void {
    const v = (valor || '') as OrdenListado;
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { orden: v || null },
      queryParamsHandling: 'merge',
    });
  }

  protected toggleFavorito(event: MouseEvent, id: number, nombre: string): void {
    event.preventDefault();
    event.stopPropagation();
    const era = this.favoritos.tiene(id);
    this.favoritos.alternar(id);
    this.toast.exito(era ? `Quitaste «${nombre}» de favoritos` : `«${nombre}» guardado en favoritos`);
  }

  private refrescar(): void {
    this.cargando.set(true);
    this.error.set(null);
    const cat = this.filtro();
    const q = this.terminoBusqueda();
    const ord = this.orden();
    this.productosApi.listar(cat || undefined, q || undefined, ord || undefined).subscribe({
      next: (items) => {
        this.productos.set(items);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No pudimos cargar el catálogo. Verifica que el backend esté encendido.');
        this.cargando.set(false);
      },
    });
  }
}
