<script>
  import "./styles.css";

  let circles = [
    {
      position: [10, 15],
      color: "box-shadow: 0 0 400px 140px rgba(0, 133, 255, 1)",
    },
    {
      position: [10, 90],
      color: "box-shadow: 0 0 100px 100px rgba(0, 255, 102, 0.72)",
    },
    { position: [40, 40], color: "box-shadow: 0 0 150px 100px #FFD447" },
    {
      position: [100, 10],
      color: "box-shadow: 0 0 250px 150px rgba(204, 0, 255, 0.75)",
    },
    {
      position: [80, 90],
      color: "box-shadow: 0 0 200px 80px rgba(204, 0, 255, 1)",
    },
  ];
</script>

<div class="app">
  <main>
    <div class="circle-container">
      {#each circles as circle}
        <div
          class="circle"
          style:top={circle.position[0] + "%"}
          style:left={circle.position[1] + "%"}
          style={circle.color}
        />
      {/each}
    </div>
    <slot />
  </main>
</div>

<style>
  main {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: stretch;
    align-items: stretch;
    padding: 1.5rem;
  }
  .circle {
    pointer-events: none;
    width: 0px;
    height: 0px;
    border-radius: 50%;
    position: absolute;
  }
</style>
