import './style.css'

import Alpine, { type Alpine as AlpineT } from 'alpinejs';
import axios, { type AxiosInstance } from 'axios';
import htmx from 'htmx.org';

type Htmx = any;

class App {
  appNode: HTMLElement | null;
  rootNode: HTMLElement | null;

  alpine: AlpineT;
  htmx: Htmx;
  axios: AxiosInstance;

  constructor(window: globalThis.Window,  alpine: AlpineT, htmx: Htmx, axios: AxiosInstance) {
    // this.instance = axios.create();
    this.appNode = window.document.getElementById("app-target");
    this.rootNode = window.document.getElementById("app-root");

    this.alpine = alpine;
    this.axios = axios;
    this.htmx = htmx;

    (window as any).htmx = htmx;
    (window as any).Alpine = alpine;
    (window as any).axios = axios;
  }

  mount() {
    this.alpine.start();
    let appNode = this.appNode;
    let rootNode = this.rootNode;
    if (appNode && rootNode) {
      let appHtml = String(rootNode?.outerHTML);
      appNode.innerHTML = "";
      rootNode.innerHTML = "";
      appNode.classList.remove("hidden");
      this.htmx.swap(appNode, appHtml, {swapStyle: 'innerHTML'});
    }
  }
}

function mainfn(window: globalThis.Window, app: App) {
  // cast required for typescript global export
  (window as any).app = app;
  app.mount()
}

mainfn(window, new App(window, Alpine, htmx, axios.create()));
  

