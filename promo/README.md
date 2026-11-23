# Video promocional — UP3 SGP PRO

`UP3_SGP_PRO_promo.mp4`: 1080×1920 (9:16), 30 fps, 20 s, H.264 + AAC 192 kbps, −14 LUFS. Listo para TikTok, Reels y Shorts. `portada.jpg` sirve de miniatura.

Las pantallas que se ven son la interfaz real de la app, pero **con datos ficticios**: ningún nombre, DNI ni causa de los internos aparece en el video.

## Guion

| Tiempo | Escena | Texto |
|---|---|---|
| 0–3 s | Contador 0→438 sobre grilla futurista, alerta roja con efecto glitch | «438 internos bajo control» / «Ni una fecha se te escapa.» |
| 3–7 s | El teléfono llega desde la profundidad, recorre el panel de inicio | «Toda la unidad, en tu bolsillo.» + 369 penados · 69 procesados · alertas |
| 7–13 s | 4 cortes rápidos con latigazos | 01 Alertas · 02 Búsqueda · 03 Ficha · 04 Egresos |
| 13–17 s | Carrusel 3D de 5 pantallas con rayos de luz y explosión de partículas | «Sin papeles. Sin planillas. Sin olvidos.» |
| 17–20 s | Logo, anillos de luz y CTA | «UP3 SGP PRO» · «Ingresá ahora →» |

La música es original, sintetizada a 120 BPM. Cada impacto, *whoosh*, clic de interfaz y campana cae justo en un corte o en una animación.

## Cómo regenerarlo (Node + Playwright, Python + NumPy, ffmpeg)

```bash
W=/ruta/de/trabajo; mkdir -p $W/shots; cp promo/src/* $W/
python3 $W/anon.py index.html $W/app_demo.html     # copia de la app con datos ficticios
node $W/shots.js $W                                 # capturas reales de la interfaz
node $W/render.js $W                                # 600 cuadros → video_noaudio.mp4
python3 $W/music.py $W/music.wav                    # banda sonora
ffmpeg -i $W/video_noaudio.mp4 -i $W/music.wav \
  -af "lowpass=f=16500:poles=2,volume=-2.5dB,aresample=192000,alimiter=limit=0.75:level=false:attack=1:release=50,aresample=48000" \
  -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart UP3_SGP_PRO_promo.mp4
```

Para cambiar textos o tiempos, editá `comp.html` (función `render(t)`). Para ver cuadros sueltos, usá `node preview.js $W 1.5,8,15`.
