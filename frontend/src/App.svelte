<script lang="ts">

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

<div class="flex gap-2">
  <a use:route href="/">Home</a>
  <a use:route href="/about">About</a>
</div>

<Router base="/" {routes} />
