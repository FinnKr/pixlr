<script lang="ts">
  import { Link } from "svelte-routing";
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
      <Link to="/" class="navbar-item">Home</Link>

      <Link to="/" class="navbar-item">Documentation</Link>

      <div class="navbar-item has-dropdown is-hoverable">
        <Link to="/" class="navbar-link">More</Link>

        <div class="navbar-dropdown">
          <Link to="/about" class="navbar-item">About</Link>
          <Link to="/" class="navbar-item">Donate</Link>
          <hr class="navbar-divider" />
          <Link to="/" class="navbar-item">Report an issue</Link>
        </div>
      </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <Link to="/" class="button is-success">
            <strong>Sign up</strong>
          </Link>
          <Link to="/login" class="button is-light">Log in</Link>
        </div>
      </div>
    </div>
  </div>
</nav>
