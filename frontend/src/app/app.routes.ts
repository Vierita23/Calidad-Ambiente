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
    data: { title: 'Inicio' },
    loadComponent: () => import('./pages/inicio.page').then((m) => m.InicioPage),
  },
  {
    path: 'catalogo',
    data: { title: 'Catálogo' },
    loadComponent: () => import('./pages/catalogo.page').then((m) => m.CatalogoPage),
  },
  {
    path: 'producto/:id',
    data: { title: 'Producto' },
    loadComponent: () => import('./pages/producto-detalle.page').then((m) => m.ProductoDetallePage),
  },
  {
    path: 'carrito',
    data: { title: 'Carrito' },
    loadComponent: () => import('./pages/carrito.page').then((m) => m.CarritoPage),
  },
  {
    path: 'favoritos',
    data: { title: 'Favoritos' },
    loadComponent: () => import('./pages/favoritos.page').then((m) => m.FavoritosPage),
  },
  {
    path: 'tienda',
    data: { title: 'La tienda' },
    loadComponent: () => import('./pages/tienda.page').then((m) => m.TiendaPage),
  },
  {
    path: 'contacto',
    data: { title: 'Contacto' },
    loadComponent: () => import('./pages/contacto.page').then((m) => m.ContactoPage),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
