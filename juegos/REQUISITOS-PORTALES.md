# Requisitos de los portales (CrazyGames y Poki): por qué rechazan y qué exigimos a cada juego

Investigado el 20/11/2026. Las páginas oficiales (docs.crazygames.com, developers.poki.com, sdk.poki.com) están bloqueadas desde el servidor de la fábrica. Lo de abajo viene de los fragmentos oficiales que devuelven los buscadores y de guías de terceros; cada punto indica de dónde sale. Revisarlo contra la documentación oficial cuando se pueda abrir.

## Por qué rechazan

| Motivo | Portal | Fuente |
|---|---|---|
| **Calidad insuficiente.** Mensaje típico: «The overall quality of the game does not yet meet the expectations of our platform». El equipo juega cada juego y comprueba que funciona, que tiene calidad y que es divertido. | CrazyGames | FAQ oficial (fragmento) y reseñas de desarrolladores |
| **Falta de originalidad.** Rechazan clones y *asset flips*. Poki además valora que el juego sea «único dentro de su categoría» y que «aporte algo nuevo». | Ambos | FAQ de CrazyGames y guía de calidad de Poki (fragmentos) |
| **Poco pulido** (*polish*): el segundo motivo más habitual tras la originalidad. Poki habla de «assets sin pulir, interfaz confusa, tema poco inspirado». | Ambos | Guías de terceros y Poki (fragmento) |
| **Texto ilegible** en el iframe 16:9 o con resolución normal (devicePixelRatio 1). | CrazyGames | Guía de terceros |
| **Temas inadecuados**, fuera de PEGI 12 o dirigidos a niños. | CrazyGames | FAQ oficial (fragmento) |
| **Uso indebido de propiedad intelectual** (portadas con imágenes sin derechos). | Ambos | Poki (fragmento) y guía de terceros |
| **IA:** se acepta un juego hecho con ayuda de IA si aporta valor. Se rechaza si se nota la IA (artefactos), si la propiedad no está clara o si la calidad es baja. | Poki | sdk.poki.com/working-with-ai (fragmento) y guía de terceros |

**Reenvíos:** CrazyGames solo reconsidera un juego rechazado si trae **mejoras claras**; si los cambios son pequeños, el resultado será el mismo. Poki tampoco lo reconsidera sin una «mejora significativa».

## Requisitos técnicos (CrazyGames)

- **Descarga inicial:** hasta 50 MB; hasta 20 MB para salir en la portada móvil. Total máximo 250 MB y 1500 archivos (página oficial *Technical*, fragmento).
- **Anuncios:** solo los del SDK. En el Basic Launch no hay anuncios aunque estén integrados (fragmento oficial).
- **Basic Launch:** el SDK no es obligatorio. **Full Launch:** integración completa (gameplay start/stop, anuncios por el SDK y módulos de datos y de usuario donde aplique) (guías de terceros).
- **SDK v3:**
  - Script `https://sdk.crazygames.com/crazygames-sdk-v3.js`; se inicializa con `await window.CrazyGames.SDK.init()`.
  - `SDK.game.gameplayStart()` / `gameplayStop()` al jugar y al pausar o ir a menús. `SDK.game.loadingStart()` / `loadingStop()` envuelven las cargas.
  - `SDK.game.happytime()` para logros, no en cada nivel.
  - `SDK.ad.requestAd('midgame' | 'rewarded', { adStarted, adFinished, adError })`; `adError` también salta si no hay anuncio.
  - Mientras se pide un anuncio, el juego debe pausarse, bloquear la entrada y silenciar el audio, y seguir si hay error.
  - `SDK.environment` puede valer `local`, `crazygames` o `disabled`.
  - Fuentes: fragmentos de la documentación oficial, extensión de Defold, GDevelop y plantillas públicas.
- No usar enlaces externos ni inicios de sesión externos. Clasificación PEGI 12.

## Lo que más pesa en la retención (Poki y guías)

- **Diversión en menos de 10 segundos.** Si menos del 50 % pasa del primer minuto, el problema está en el onboarding o en el juego (Poki y la guía de Defold).
- **Tutorial integrado** que enseñe la mecánica en los primeros 30-60 s (referencia: guías de calidad de Meta Instant Games, en las que se inspira CrazyGames).
- **Carga rápida.** Poki mide el tiempo de carga con su *Web Fit Test*.
- **Móvil desde el principio:** horizontal en escritorio y vertical en móvil.
- **Profundidad:** progresión, metas a medio plazo y motivo para volver (modo diario o rachas).

## Lista de comprobación de la fábrica (todo juego antes de enviarlo)

1. Mecánica conocida pero con **giro propio** visible en el primer minuto. Nada de clon 1:1 de un juego famoso.
2. **Tutorial jugable** en el primer nivel (mano o flecha y una frase). Cada mecánica nueva se presenta con una tarjeta.
3. **Progresión:** mundos o capítulos, estrellas o recompensas, desbloqueos y una meta visible.
4. **Menú pulido:** jugar o continuar, selector de niveles, ajustes (sonido, música, vibración, borrar progreso) y pausa.
5. **Guardado** automático (localStorage y, con SDK, módulo de datos).
6. **Juice:** animación con rebote, partículas, celebración, sonido en cada acción y música opcional.
7. **Modo extra** que invite a volver (diario con racha, contrarreloj o infinito).
8. **Rendimiento:** 60 fps en escritorio y en iPhone emulado, sin errores de consola, legible a 1280×720 y en vertical.
9. **SDK de CrazyGames** integrado y protegido: si el SDK no carga, el juego funciona igual.
10. Inglés por defecto y español automático. Sin enlaces externos en la versión de portales.
11. Imágenes (1920×1080, 800×1200, 800×800) y vídeos (16:9 y 2:3) del juego real, sin imágenes de terceros.

## Estado de los juegos

- **Rootwork v2 (20/11):** cumple los puntos 1-11. Detalles en `rootwork/CAMBIOS-V2.md`. Es el que se reenvía.
- Loomlines: la mecánica (unir parejas sin cruzar) es muy parecida a un juego móvil muy famoso. Riesgo alto de «poco original»; no reenviar sin un giro propio fuerte.
- Lumen Drift y Lunavault: juegos de un botón muy simples. Les falta progresión y profundidad; no reenviar tal cual.
