// =============================================================================
// Archivo: layout/app-toast.ts
// Propósito: Contenedor global de toasts (inyecta `ToastService`).
// =============================================================================
import { Component, inject } from '@angular/core';

import { ToastService } from '../core/toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  templateUrl: './app-toast.html',
  styleUrl: './app-toast.scss',
})
export class AppToast {
  protected readonly toast = inject(ToastService);
}
