// =============================================================================
// Archivo: main.ts
// Carpeta: frontend/src/
// Propósito: Bootstrap de la aplicación Angular (standalone).
// =============================================================================
import { bootstrapApplication } from '@angular/platform-browser';

import { appConfig } from './app/app.config';
import { App } from './app/app';

bootstrapApplication(App, appConfig).catch((err) => console.error(err));
