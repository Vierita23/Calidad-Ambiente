// =============================================================================
// Archivo: core/whatsapp.util.ts
// Carpeta: frontend/src/app/core/
// Propósito: Funciones puras para abrir WhatsApp Web / app con texto prellenado.
// =============================================================================

/**
 * Codifica un texto para usarlo de forma segura en querystring (`text=`).
 */
export function codificarTextoWhatsApp(texto: string): string {
  return encodeURIComponent(texto);
}

/**
 * Construye la URL oficial de apertura de chat (`wa.me`).
 *
 * @param digitosE164 Número internacional solo dígitos (ej. `593959247699`).
 * @param mensaje Texto opcional que aparecerá prellenado en el chat.
 */
export function construirUrlWhatsApp(digitosE164: string, mensaje?: string): string {
  const base = `https://wa.me/${digitosE164}`;
  if (!mensaje) {
    return base;
  }
  return `${base}?text=${codificarTextoWhatsApp(mensaje)}`;
}

/**
 * Abre WhatsApp en una nueva pestaña (mejor UX que reemplazar la página actual).
 */
export function abrirWhatsAppEnNuevaPestana(url: string): void {
  window.open(url, '_blank', 'noopener,noreferrer');
}
