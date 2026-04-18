// =============================================================================
// Archivo: app.routes.ts
// Carpeta: frontend/src/app/
// Propósito: Rutas principales del sitio (carga perezosa con `loadComponent`).
// =============================================================================
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    loadComponent: () => import('./pages/inicio.page').then((m) => m.InicioPage),
  },
  {
    path: 'catalogo',
    loadComponent: () => import('./pages/catalogo.page').then((m) => m.CatalogoPage),
  },
  {
    path: 'producto/:id',
    loadComponent: () => import('./pages/producto-detalle.page').then((m) => m.ProductoDetallePage),
  },
  {
    path: 'carrito',
    loadComponent: () => import('./pages/carrito.page').then((m) => m.CarritoPage),
  },
  {
    path: 'tienda',
    loadComponent: () => import('./pages/tienda.page').then((m) => m.TiendaPage),
  },
  {
    path: 'contacto',
    loadComponent: () => import('./pages/contacto.page').then((m) => m.ContactoPage),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
