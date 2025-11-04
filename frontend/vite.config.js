import { defineConfig, loadEnv } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({mode}) => {
  let env = loadEnv(mode, process.cwd());
  let LANGNET_LOCAL = "http://localhost:5050"
  return {
    "plugins": [
      tailwindcss()
    ],
    "server": {
      "host": env.VITE_SERVER_HOST || "localhost",
      "port": Number(env.VITE_SERVER_PORT || 5173),
      "proxy": {
        "/api": LANGNET_LOCAL,
        "/q": LANGNET_LOCAL,
        "/htmx": LANGNET_LOCAL,
      },
      "allowedHosts": [
        "truenas-qemu-nixos.snake-dojo.ts.net"
      ]
    },
    "build": {
      "rollupOptions": {
        // ignore htmx eval warning
        "onwarn": (entry, next) => {
          if (entry.id && /htmx\.esm\.js$/.test(entry.id)) {
            return;
          } else {
            return next(entry);
          }
        }
      }
    }
  };
});
