// =============================================================================
// Archivo: core/whatsapp.config.ts
// Carpeta: frontend/src/app/core/
// Propósito: Centraliza el número de WhatsApp y la construcción de enlaces wa.me.
//
// IMPORTANTE (formato internacional):
// - `wa.me` requiere el número **sin** el símbolo `+` y **sin** ceros iniciales
//   del prefijo nacional.
// - El usuario entregó `0959247699`. Aquí asumimos Ecuador (+593): se elimina
//   el `0` inicial y queda `593959247699`.
// - Si tu línea es de otro país, cambia `WHATSAPP_E164_DIGITS` a tu E.164 sin `+`.
// =============================================================================

/**
 * Número en formato E.164 solo dígitos (sin `+`), usado por `https://wa.me/<...>`.
 *
 * El usuario indicó el número local `0959247699`. Aquí lo convertimos a internacional
 * asumiendo **Ecuador (+593)**: `0` inicial + `593` => `593959247699`.
 *
 * Si tu línea es de otro país, reemplaza este valor por el E.164 correcto.
 */
export const WHATSAPP_E164_DIGITS = '593959247699';
