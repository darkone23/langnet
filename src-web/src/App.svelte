<script lang="ts">

  import type { Route } from "@mateothegreat/svelte5-router";
  import { route, Router } from "@mateothegreat/svelte5-router";

  import Home from './Home.svelte';
  import SearchResults from './SearchResults.svelte';
  import About from './About.svelte';
  // import Dummy from './Dummy.svelte';

  const routes: Route[] = [
    {
      path: "/",
      component: Home
    },
    {
      path: "q",
      component: SearchResults,
    },
    {
      path: "about",
      component: About
    },
  ];
</script>

<div class="flex gap-2 px-4 mt-4">
  <a use:route href="/">Home</a>
  <a use:route href="/about">About</a>
</div>

<main class="flex flex-wrap items-center justify-between w-full px-4">

<Router basePath="/" {routes} />

</main>
