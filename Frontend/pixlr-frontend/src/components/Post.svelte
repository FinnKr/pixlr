<script lang="ts">
    import { onMount } from "svelte";
    import { sdk, collections, buckets } from "../appwrite";

    export let id;

    interface Post {
        title: string;
        user_id: string;
        image_id: string;
    }

    let post: Post;
    let image: URL;

    let loading: boolean = true;

    onMount(async () => {
        post = (await sdk.database.getDocument(
            collections.posts,
            id
        )) as unknown as Post;

        image = await sdk.storage.getFileView(buckets.post_images, post.image_id);
        loading = false;
    });
</script>

{#if !loading}
    <div class="card block">
        <header class="card-header">
            <p class="card-header-title">
                {post.title}
            </p>
          </header>
        <div class="card-image">
            <figure class="image is-square">
                <img
                    src={image.href}
                    alt={post.title}
                    style="image-rendering: pixelated;"
                />
            </figure>
        </div>
        <footer class="card-footer">
            <span class="icon is-large like-btn"><i class="fa-regular fa-heart fa-2x"></i></span>
            <span class="icon is-large cmnt-btn"><i class="fa-regular fa-comment fa-2x"></i></span>
          </footer>
    </div>
{:else}
    <progress class="progress is-large is-success" max="100">0%</progress>
{/if}

<style>
    .like-btn:hover {
        color: #d62828;
    }

    .cmnt-btn:hover {
        color: black;
    }
</style>
