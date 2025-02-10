<script lang="ts">
  // let count: number = $state(0)
  // const increment = () => {
  //   count += 1
  // }
  // import { navigate } from "svelte-routing";
  import axios from 'axios';
  console.log("you loaded my javascript!")

  function handleFormSubmit(event) {
    const queryEndpoint = "";
    event.preventDefault();
    event.stopImmediatePropagation();
    console.log("nice event yo", event);
    axios.get(event.target.action)
      .then(function (response) {
        // handle success
        console.log("response", response);
      })
      .catch(function (error) {
        // handle error
        console.log("error", error);
      })
      .finally(function () {
        // always executed
      });
    
  }
  
</script>

<div class="search-controls">
  <form action="http://localhost:5000/api/q" method="get" on:submit={handleFormSubmit}>
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
