<script lang="ts">
  import { goto } from "@mateothegreat/svelte5-router";  
  function handleFormSubmit(event: SubmitEvent) {
    event.preventDefault();
    event.stopImmediatePropagation();

    if (event.target instanceof HTMLFormElement) {
      const formData = Object.fromEntries(new FormData(event.target))

      const params = {
        language: "" + formData["l"],
        search: "" + formData["s"]
      }

      console.log('here are your params', params)

      goto("/q", params)    
    } else {
      console.warn("Unexpected event target", event.target)
    }

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
      <input type="radio" id="lat-radio" name="l" value="lat" required checked />
      <label for="lat-radio">Latin</label>
      <input type="radio" id="grc-radio" name="l" value="grc" required />
      <label for="grc-radio">Greek</label>
      <input type="radio" id="san-radio" name="l" value="san" required />
      <label for="san-radio">Sanskrit</label>
    </div>

    <div>
        <button type="submit">
          <span class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 ">
            search
          </span>
        </button>
    </div>
  </form>
</div>
