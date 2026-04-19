// =============================================================================
// Archivo: pages/inicio.page.ts
// Carpeta: frontend/src/app/pages/
// Propósito: Inicio estilo tienda: categorías, novedades, ofertas, beneficios y WhatsApp.
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, computed, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';

import { WHATSAPP_E164_DIGITS } from '../core/whatsapp.config';
import { ProductoService } from '../core/producto.service';
import { construirUrlWhatsApp } from '../core/whatsapp.util';
import { Producto } from '../models/producto';

@Component({
  selector: 'app-inicio-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './inicio.page.html',
  styleUrl: './inicio.page.scss',
})
export class InicioPage {
  private readonly productosApi = inject(ProductoService);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly cargando = signal(true);
  protected readonly error = signal<string | null>(null);
  protected readonly ordenados = signal<Producto[]>([]);

  /** Tarjetas de acceso rápido (misma forma para plantilla tipada). */
  protected readonly categoriasInicio: Array<{
    link: readonly string[];
    queryParams: Record<string, string>;
    titulo: string;
    emoji: string;
  }> = [
    { link: ['/catalogo'], queryParams: { categoria: 'tablet' }, titulo: 'Tablets', emoji: '📱' },
    { link: ['/catalogo'], queryParams: { categoria: 'celular' }, titulo: 'Celulares', emoji: '📲' },
    { link: ['/catalogo'], queryParams: { categoria: 'reloj' }, titulo: 'Smartwatch', emoji: '⌚' },
    { link: ['/catalogo'], queryParams: { categoria: 'laptop' }, titulo: 'Laptops', emoji: '💻' },
    { link: ['/tienda'], queryParams: {}, titulo: 'La tienda', emoji: '🏪' },
  ];

  protected readonly recienLlegados = computed(() => this.ordenados().slice(0, 4));
  /** Segunda vitrina: solo si hay más modelos que en “Recién llegados”. */
  protected readonly ofertas = computed(() => {
    const s = this.ordenados();
    return s.length > 4 ? s.slice(4, 8) : [];
  });

  protected readonly waCotizar = construirUrlWhatsApp(
    WHATSAPP_E164_DIGITS,
    'Hola, quiero cotizar un modelo en DT Technology.'
  );

  constructor() {
    this.productosApi
      .listar(undefined, undefined, '-creado_en')
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (items) => {
          this.ordenados.set(items);
          this.cargando.set(false);
        },
        error: () => {
          this.error.set('No pudimos cargar las novedades. Verifica que el backend esté en marcha.');
          this.cargando.set(false);
        },
      });
  }

  protected trackPorId(_i: number, p: Producto): number {
    return p.id;
  }
}
