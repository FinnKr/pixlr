<script lang="ts">
	import {Router, Route } from 'svelte-routing';
	import { globalHistory } from 'svelte-routing/src/history';
	import { onDestroy, onMount } from 'svelte';
	import About from './pages/About.svelte';
	import Home from './pages/Home.svelte';
	import Login from "./pages/Login.svelte";
	import Navbar from "./components/Navbar.svelte";
	import Profile from './pages/Profile.svelte';
	import CreatePost from './pages/CreatePost.svelte';
import Signup from './pages/Signup.svelte';

	export let url = '';

	let pathname = window.location.pathname;
	let unsub;

	onMount(() => {
		unsub = globalHistory.listen(({ location, action }) => {
			pathname = location.pathname;
		});
	});

	onDestroy(() => {
		unsub();
	});
</script>

<Router url={url}>
	<Navbar url={pathname}/>
	<div class="container pt-2">
		<div class="columns is-centered pt-5">
			<div class="column is-half">
				<Route path="/"><Home /></Route>
				<Route path="about" component="{About}" />
				<Route path="login" component="{Login}" />
				<Route path="profile" component="{Profile}" />
				<Route path="create-post" component="{CreatePost}" />
				<Route path="signup" component="{Signup}" />
			</div>
		</div>
	</div>
</Router>

