<script lang="ts">
  import { goto } from "@mateothegreat/svelte5-router";  
  function handleFormSubmit(event) {
    event.preventDefault();
    event.stopImmediatePropagation();

    const formData = Object.fromEntries(new FormData(event.target));

    goto("/q", {
      language: formData["l"],
      search: formData["s"]
    })    
  }
  
</script>

<div class="search-controls">
  <form method="get" on:submit={handleFormSubmit}>
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
        <button type="submit">
          <a class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 ">
            search
          </a>
        </button>
    </div>
  </form>
</div>
