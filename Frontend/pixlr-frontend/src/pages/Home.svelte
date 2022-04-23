<script lang="ts">
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { sdk, collections } from "../appwrite";
    import Post from "../components/Post.svelte";
    import type { Models } from "appwrite";

    let posts: Models.Document[];

    onMount(async () => {
        posts = (await sdk.database.listDocuments(collections.posts, [], 10, 0, undefined, undefined, ['$id'],['DESC'])).documents;
    });

    async function loadMore() {
        posts = posts.concat((await sdk.database.listDocuments(collections.posts, [], 10, posts.length, undefined,undefined,['$id'],['DESC'])).documents);
    }
</script>

<main>
    <h1 class="title">Global Feed</h1>
    {#if posts}
        {#each posts as post (post.$id)}
            <Post id={post.$id} />
        {/each}
        <p on:click={loadMore} class="load-more-btn">Load More</p>
    {/if}
</main>

<style>
    .load-more-btn {
        cursor: pointer;
    }
</style>
