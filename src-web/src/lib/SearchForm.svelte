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
      // console.log('here are your params', params)

      goto("/q", params)    
    } else {
      console.warn("Unexpected event target", event.target)
    }

  }

  import { get } from 'svelte/store'
  import { storable } from './storable.js'

	const store = storable({
    term: '',
    checked: "lat",
  });

	let value = get(store)["term"];
  let langvalue = get(store)["checked"];

  function handleSearchChange() {
    store.update(function(data: any) {
      data["term"] = value;
      return data
    })
  }
  
  function handleLangChange() {
    store.update(function(data: any) {
      data["checked"] = langvalue;
      return data
    })
    
  }

  function clearSearchTerm(event: Event) {
    
    event.preventDefault();
    event.stopImmediatePropagation();

    store.update(function(data: any) {
      data["term"] = ""
      value = ""
      return data;
    })

  }

  const latRadio = {
    checked: langvalue == "lat"
  };

  const grcRadio = {
    checked: langvalue == "grc"
  };
  
  const sanRadio = {
    checked: langvalue == "san"
  };

</script>

<div class="search-controls">
  <form method="get"  on:submit={handleFormSubmit}>
    <div>
      <label for="search-input">Enter your term: </label>
      <input placeholder="search..." bind:value on:keyup={handleSearchChange} id="search-input" type="text" name="s" required />
    </div>
    
    <div>
      <label for="lang-select">Select your lang: </label>
      <input bind:group={langvalue} on:change={handleLangChange} type="radio" id="lat-radio" name="l" value="lat" required {...latRadio} />
      <label for="lat-radio">Latin</label>
      <input bind:group={langvalue} on:change={handleLangChange} type="radio" id="grc-radio" name="l" value="grc" required {...grcRadio}  />
      <label for="grc-radio">Greek</label>
      <input bind:group={langvalue} on:change={handleLangChange} type="radio" id="san-radio" name="l" value="san" required {...sanRadio}  />
      <label for="san-radio">Sanskrit</label>
    </div>

    <div class="mt-2">
        <button type="submit">
          <span class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 ">
            search
          </span>
        </button>
        <button on:click={clearSearchTerm}>
          <span class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-500 ">
            clear
          </span>
        </button>
    </div>
  </form>
</div>
