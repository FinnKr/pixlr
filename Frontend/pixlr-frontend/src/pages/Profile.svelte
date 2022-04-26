<script lang="ts">
    import { onMount } from "svelte";
    import { Link, navigate } from "svelte-routing";
    import { sdk, collections } from "../appwrite";
    import Post from "../components/Post.svelte";
    import { Models, Query } from "appwrite";

    let account: Models.User<Models.Preferences>;
    let displayed_name: string = "";

    let posts: Models.Document[];

    onMount(async () => {
        try {
            account = await sdk.account.get();
            fetchPosts();
            displayed_name = account.name
                ? account.name
                : account.email.substring(
                      0,
                      account.email.indexOf("@") == -1
                          ? account.email.length
                          : account.email.indexOf("@")
                  );
        } catch (error) {
            navigate("/login");
        }
    });

    async function fetchPosts() {
        if (account) {
            let queries = [Query.equal("user_id", account.$id)];
            try {
                posts = (await sdk.database.listDocuments(collections.posts, queries, 10, 0, undefined, undefined, ['$id'],['DESC'])).documents;
            } catch (error) {
                console.error(error);
            }
        }
    }

    async function loadMore() {
        let queries = [Query.equal("user_id", account.$id)];
        posts = posts.concat((await sdk.database.listDocuments(collections.posts, queries, 10, posts.length, undefined,undefined,['$id'],['DESC'])).documents);
    }
</script>

{#if account}
    <h1 class="subtitle">Profile of {displayed_name}</h1>
    {#if posts}
        {#each posts as post (post.$id)}
            <Post id={post.$id} is_logged_in={true} can_delete={true} />
        {:else}
            <p><i>No posts created. Create one <Link to="/create-post">here</Link></i></p>
        {/each}
        {#if posts.length == 10}
            <p on:click={loadMore} class="load-more-btn">Load More</p>
        {/if}
    {:else}
        <progress class="progress is-large is-success" max="100">0%</progress>
    {/if}
{/if}
