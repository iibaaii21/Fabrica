# Rootwork v2: qué ha cambiado (para el reenvío)

## Texto para la nota de reenvío (inglés, pegar tal cual)

Thanks for the feedback on the first version. Rootwork has been rebuilt with much more depth and polish:
- 6 worlds (Meadow, Orchard, Marsh, River Delta, Night Garden, Crystal Caves) with 150 hand-tuned gardens, unlocked with stars.
- A new mechanic in every world: fixed stones, pools that break the grid, and gardens with two and three springs.
- Interactive tutorial on the first gardens, plus an intro card for every new mechanic.
- New Daily Garden mode with a streak counter.
- Undo, hints you earn by playing, pause menu and settings (sound, music, vibration, reset progress).
- Much more juice: water flows tile by tile, bouncy rotations, flowers burst into bloom with particles and notes, a celebration with stars, generative ambient music and a living animated background for each world.
- Keyboard controls (arrows + space), mouse and touch. Tested at 60 fps on desktop and mobile.
- CrazyGames SDK v3 integrated: gameplayStart/Stop, happytime on world completion, midgame ads only between gardens (never before the 3rd garden, at most every 3 minutes) and an optional rewarded ad for hints. The game pauses and mutes during ads.
- English and Spanish (automatic).

## Comparación

| | v1 (rechazado) | v2 |
|---|---|---|
| Niveles | 300 iguales (solo cambiaba el tamaño) | 150 en 6 mundos, cada uno con su mecánica y su ambiente |
| Mecánicas | girar piezas | girar, piedras fijas, charcos (tableros irregulares), 2 y 3 manantiales |
| Progresión | desbloqueo lineal | estrellas que abren mundos, pistas que se ganan, mundo completado |
| Tutorial | texto fijo abajo | mano animada en el nivel 1, mensajes en los niveles 2-3, tarjeta por mundo |
| Menús | Play / Levels / Sound | Jugar (continúa), Mundos, Jardín del día, Ajustes, Pausa |
| Modo extra | — | Jardín del día con racha |
| Juice | partículas al ganar | agua que avanza en cadena, rebote, flores con estallido, gotas, temblor, estrellas animadas, música |
| SDK | adaptador mínimo | v3 completo (inicio y fin de partida, loading, happytime, midgame, rewarded, módulo de datos) |
| Controles | ratón y táctil | ratón, táctil, teclado y deshacer |
| Idiomas | inglés | inglés y español |

## Comprobado (20/11, Chromium sin interfaz)

- Los 150 niveles y el diario se generan en 25 ms en total; todos se resuelven sin error y tienen el número correcto de manantiales.
- Unos 60 fps en 1280×720 y en iPhone 13 emulado; 0 errores de consola.
- Tutorial probado con clics reales: el nivel 1 se gana con 1 movimiento y da 3 estrellas.
- **No probado** con el SDK real de CrazyGames: su dominio está bloqueado desde el servidor. El código solo llama al SDK si existe y protege cada llamada; sin SDK el juego funciona igual. Comprobarlo en la QA Tool de CrazyGames antes de enviar.
