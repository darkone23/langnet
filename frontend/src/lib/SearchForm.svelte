<script lang="ts">
  import { goto } from "@mateothegreat/svelte5-router";
  console.log("you loaded my javascript!", import.meta.env.MODE);
  

  console.log("nice goto", goto)

  function handleFormSubmit(event) {
    const queryEndpoint = "";
    event.preventDefault();
    event.stopImmediatePropagation();
    console.log("nice js event", event);

    const formData = Object.fromEntries(new FormData(event.target));

    goto("/q", {
      language: formData["l"],
      search: formData["s"]
    })    
  }
  
</script>

<div class="search-controls">
  <form action={actionTarget} method="get" on:submit={handleFormSubmit}>
    <div>
      <label for="search-input">Enter your term: </label>
      <input id="search-input" type="text" name="s" required />
    </div>
    
    <div>
      <label for="lang-select">Select your lang: </label>
      <select id="lang-select" name="l" required>
        <option value="lat" selected>Latin</option>
        <option value="grk">Greek</option>
      </select>
    </div>

    <div>
      <button type="submit">Submit</button>
    </div>
  </form>
</div>
