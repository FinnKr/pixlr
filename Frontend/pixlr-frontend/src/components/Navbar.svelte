<script lang="ts">
  import { onMount } from "svelte";
  import { Link, navigate, Router } from "svelte-routing";
  import { sdk } from "../appwrite";
  import type { Models } from "appwrite";

  export let url: string;

  let account: Models.User<Models.Preferences>;
  let logged_in: boolean = false;

  onMount(async () => {
    try {
      account = await sdk.account.get();
      logged_in = true;
    } catch{}
  });

  async function logout() {
    try {
      await sdk.account.deleteSession('current');
    } catch (error) {
      console.log("Error logging out");
    }
    account = undefined;
    logged_in = false;
    navigate("/login");
  }
</script>

<nav class="navbar" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="https://bulma.io">
      <img
        src="https://bulma.io/images/bulma-logo.png"
        width="112"
        height="28"
        alt="Pic"
      />
    </a>

    <Link
      to="/"
      role="button"
      class="navbar-burger"
      aria-label="menu"
      aria-expanded="false"
      data-target="navbarBasicExample"
    >
      <span aria-hidden="true" />
      <span aria-hidden="true" />
      <span aria-hidden="true" />
    </Link>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">
      <Link to="/" class="navbar-item {url == '/' ? 'has-text-weight-semibold' : ''}">Home</Link>

      <Link to="/" class="navbar-item">News</Link>

      <div class="navbar-item has-dropdown is-hoverable">
        <Link to="/" class="navbar-link">More</Link>

        <div class="navbar-dropdown">
          <Link to="/about" class="navbar-item {url == '/about' ? 'has-text-weight-semibold' : ''}">About</Link>
          <Link to="/" class="navbar-item">Donate</Link>
          <hr class="navbar-divider" />
          <a href="https://github.com/FinnKr/pixlr" class="navbar-item">GitHub Repository</a>
          <Link to="/" class="navbar-item">Report an issue</Link>
        </div>
      </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          {#if logged_in}
            {#if url != '/create-post'}
              <Link to="/create-post" class="button is-success">
                <strong>Create Post</strong>
              </Link>
            {/if}
            <button on:click={logout} class="button is-outlined is-success has-icons has-icons-right">
              <p>Log Out</p>
              <span class="icon is-small is-right">
                <i class="fas fa-arrow-right-from-bracket" />
              </span>
            </button>
            <Link to="/profile" class="button is-rounded has-text-weight-semibold  {url == '/profile' ? 'is-active' : ''}">{account.name.substring(0,1)}</Link>
          {:else}
            <Link to="/signup" class="button is-success">
              <strong>Sign up</strong>
            </Link>
            <Link to="/login" class="button is-light  {url == '/login' ? 'has-text-weight-semibold' : ''}">Log in</Link>
          {/if}
        </div>
      </div>
    </div>
  </div>
</nav>
