<script lang="ts">
  import axios from 'axios';

  let { language, search } = Object.fromEntries(
    new URLSearchParams(
      window.location.search
    )
  )
  let result = $state({})

  let actionTarget = "/api/q";
  if (import.meta.env.MODE == "development") {
    actionTarget = "http://localhost:5000/api/q";
  }
  axios.get(actionTarget, {
    params: {
      l: language,
      s: search
    }
  }).then(function (response) {
      // handle success
      console.log("response", response);
      result = response.data
    })
    .catch(function (error) {
      // handle error
      console.log("error", error);
    })
    .finally(function () {
      // always executed
    });
</script>

<div>
  <p>
  {language}@{search}
  </p>
  <hr />
  <pre>{JSON.stringify(result, 0, 2)}
</div>
