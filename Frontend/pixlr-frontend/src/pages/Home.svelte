<script lang="ts">
    import { onMount } from "svelte";
    import { sdk, collections, isLoggedIn } from "../appwrite";
    import Post from "../components/Post.svelte";
    import type { Models } from "appwrite";

    let posts: Models.Document[];

    let is_loading: boolean = true;
    let is_logged_in: boolean;

    onMount(async () => {
        is_logged_in = await isLoggedIn();
        is_loading = false;
        posts = (await sdk.database.listDocuments(collections.posts, [], 10, 0, undefined, undefined, ['$id'],['DESC'])).documents;
    });

    async function loadMore() {
        posts = posts.concat((await sdk.database.listDocuments(collections.posts, [], 10, posts.length, undefined,undefined,['$id'],['DESC'])).documents);
    }
</script>

{#if !is_loading}
    <main>
        <h1 class="title">Global Feed</h1>
        {#if posts}
            {#each posts as post (post.$id)}
                <Post id={post.$id} is_logged_in={is_logged_in}/>
            {/each}
            <p on:click={loadMore} class="load-more-btn">Load More</p>
        {/if}
    </main>
{/if}

<style>
    .load-more-btn {
        cursor: pointer;
    }
</style>
