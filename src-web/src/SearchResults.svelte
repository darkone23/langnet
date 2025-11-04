<script lang="ts">
  import axios from 'axios';
  import SearchForm from './lib/SearchForm.svelte';

  console.log('you are loading searchform page')

  let { language, search } = Object.fromEntries(
    new URLSearchParams(
      window.location.search
    )
  )

  let status = $state("LOADING")
  let result = $state({})

  let actionTarget = "/api/q";
  if (import.meta.env.MODE == "development") {
    actionTarget = "http://localhost:5050/api/q";
  }
  axios.get(actionTarget, {
    params: {
      l: language,
      s: search
    }
  }).then(function (response) {
      // handle success
      // console.log("response", response);
      result = response.data;
      status = "OK";
    })
    .catch(function (error) {
      // handle error
      status = `${error.code}`;
      console.error(error.message, error)
      // console.log("error", error);
    })
</script>

<div>

  <SearchForm />

  <p>
  {language}@{search}::{status}
  </p>
  <hr />
  <pre>{JSON.stringify(result, null, 2)}</pre>
</div>
