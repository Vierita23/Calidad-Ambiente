// =============================================================================
// Archivo: app.config.ts
// Carpeta: frontend/src/app/
// Propósito: Configuración de arranque de Angular (providers globales).
// Aquí habilitamos `HttpClient` para consumir el API Django.
// =============================================================================
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient(),
  ],
};
