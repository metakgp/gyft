<script lang="ts">
  import metakgpLogo from "$lib/assets/metakgp-logo.png";
  export let logoVisible: boolean = true;
</script>

{#if logoVisible}
  <div class="logo-container">
    <img src={metakgpLogo} alt="MetaKGP | IIT Kharagpur" />
  </div>
{/if}
<div>
  <h1>Get Your Freaking <span>Time - Table</span></h1>
</div>

<style>
  h1 {
    font-size: 2rem;
    line-height: 2.75rem;
    margin-bottom: 2rem;
  }
  h1 span {
    display: block;
    font-size: 3rem;
  }

  @media screen and (max-width: 900px) {
    h1 {
      font-size: 1.5rem;
      margin-bottom: 2.5rem;
    }
    h1 span {
      display: block;
      font-size: 2.5rem;
    }
    .logo-container {
      max-width: 100px;
      margin-inline: auto;
    }
    .logo-container img {
      width: 100%;
      display: block;
    }
  }
</style>
