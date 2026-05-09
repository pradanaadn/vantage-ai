<template>
  <header>
    <nav>
      <router-link to="/">Home</router-link>
    </nav>
  </header>
  <main>
    <router-view />
  </main>
</template>

<style>
#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  font-weight: normal;
}

header {
  line-height: 1.5;
  margin-bottom: 2rem;
}

nav {
  width: 100%;
  font-size: 1.2rem;
  text-align: center;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>
