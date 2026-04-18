// =============================================================================
// Archivo: pages/carrito.page.ts
// Propósito: Resumen del carrito demo (líneas, total, vaciar).
// =============================================================================
import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { CarritoService } from '../core/carrito.service';

@Component({
  selector: 'app-carrito-page',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './carrito.page.html',
  styleUrl: './carrito.page.scss',
})
export class CarritoPage {
  protected readonly carrito = inject(CarritoService);

  protected vaciar(): void {
    this.carrito.vaciar();
  }

  protected quitar(id: number): void {
    this.carrito.quitar(id);
  }
}
