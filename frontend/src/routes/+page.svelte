<script lang="ts">
  import Footer from "../components/Footer.svelte";
  import Header from "../components/Header.svelte";
  import HeroImg from "$lib/assets/hero-img.png";
  import Form from "../components/Form.svelte";
  import type { FormData } from "$lib/_types";

  let formData: FormData = {
    rollNo: null,
    password: null,
    securityAnswer: null,
    otp: null,
  };

  let securityQuestion: string | null = null;
</script>

<div id="wrapper">
  <main>
    <Form {securityQuestion} {formData} />
  </main>
  <aside>
    <img src={HeroImg} alt="." />
  </aside>
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

  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 2rem;
  }

  aside img {
    display: block;
    width: 100%;
    max-height: 600px;
    height: auto;
  }

  @media screen and (max-width: 900px) {
    aside {
      display: none;
    }
    main {
      padding: 0 0.5rem;
    }
    #wrapper {
      padding: 0.5rem;
    }
  }
</style>
