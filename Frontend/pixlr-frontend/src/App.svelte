<script lang="ts">
	import {Router, Route } from 'svelte-routing';
	import About from './pages/About.svelte';
	import Home from './pages/Home.svelte';
	import Login from "./pages/Login.svelte";
	import Navbar from "./components/Navbar.svelte";
	import Profile from './pages/Profile.svelte';
	export let url = '';
</script>

<Router url="{url}">
	<Navbar />
	<div class="container pt-2">
		<Route path="/"><Home /></Route>
		<Route path="about" component="{About}" />
		<Route path="login" component="{Login}" />
		<Route path="profile" component="{Profile}" />
	</div>
</Router>

