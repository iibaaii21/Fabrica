# Webs en Cloudflare Pages (publicadas el 23/11/2026)
- https://cellmate-plantillas.pages.dev  (sites/cellmate)
- https://calculadora-oposiciones.pages.dev  (sites/oposiciones)
- https://nimbloom.pages.dev  (sites/estudio)

Cada proyecto de Pages solo contiene un `_worker.js` que sirve los archivos de `sites/<web>/` desde la rama `claude/fabrica-ingresos-legales-9iymbg` de GitHub (raw), con su tipo de contenido y caché de 5 min en el HTML. **Cualquier push a sites/ se publica solo en unos minutos; no hace falta volver a desplegar.**

Solo hay que volver a desplegar si cambia `_worker.js`. El proxy reemplaza el Authorization, así que wrangler falla en la subida de assets: se despliega con la API directa (la clave de Cloudflare está guardada como secreto de red del entorno para api.cloudflare.com):
  curl -X POST https://api.cloudflare.com/client/v4/accounts/446f5a86a2192bf36f3393880ebe7af1/pages/projects/<proyecto>/deployments --form-string 'manifest={}' --form-string 'branch=main' -F "_worker.js=@herramientas/cloudflare/<web>/_worker.js;type=application/javascript+module"
