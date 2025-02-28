import { writable, get } from 'svelte/store'

export function storable(data: any) {
   const store = writable(data);
   const { subscribe, set, update } = store;
   const isBrowser = typeof window !== 'undefined';

   isBrowser &&
      localStorage.storable &&
      set(JSON.parse(localStorage.storable));

   return {
      subscribe,
      set: (n: any) => {
         isBrowser && (localStorage.storable = JSON.stringify(n));
         set(n);
      },
      update: (cb: Function) => {
         const updatedStore = cb(get(store));

         isBrowser && (localStorage.storable = JSON.stringify(updatedStore));
         set(updatedStore);
      }
   };
}