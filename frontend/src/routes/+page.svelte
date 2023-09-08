<script>
  import Footer from "../components/Footer.svelte";
  import Header from "../components/Header.svelte";
</script>

<div id="wrapper">
  <main>
    <Header />
    <Footer />
  </main>
</div>

<style>
  #wrapper {
    height: 100%;
    width: 100%;
    border-radius: 10px;
    padding: 1rem;
    z-index: 20;
    border: 1px solid white;
    border-radius: 24px;
    border: 2px solid #fff;
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(106.5px);
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: space-evenly;
    gap: 2rem;
    overflow: auto;
  }
</style>
