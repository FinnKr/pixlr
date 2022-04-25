<script lang="ts">
    import { onMount } from "svelte";
    import { sdk, collections, buckets } from "../appwrite";
    import { Models, Query } from "appwrite";

    export let id: string;
    export let is_logged_in: boolean;

    interface Post {
        $id: string;
        title: string;
        user_id: string;
        image_id: string;
    }

    let post: Post;
    let image: URL;

    let like_count: number;
    let is_liked: boolean = false;

    let loading: boolean = true;

    let liking_process: boolean = false;

    onMount(async () => {
        post = (await sdk.database.getDocument(
            collections.posts,
            id
        )) as unknown as Post;

        image = await sdk.storage.getFileView(
            buckets.post_images,
            post.image_id
        );
        await getLikes();
        if (is_logged_in) {
            await checkLikeStatus();
        }
        loading = false;
    });

    $: like_btn_el = `<i class="${
        is_liked ? "fa-solid" : "fa-regular"
    } fa-heart fa-2x" style="${is_liked ? "color: #d62828;" : ""}"/>`;

    async function checkLikeStatus() {
        console.log("Checked Status");
        if (is_logged_in) {
            let account: Models.User<Models.Preferences>;
            try {
                account = await sdk.account.get();
                let queries = [
                    Query.equal("user_id", account.$id),
                    Query.equal("post_id", post.$id),
                ];
                is_liked =
                    (
                        await sdk.database.listDocuments(
                            collections.likes,
                            queries
                        )
                    ).total > 0;
            } catch {
                is_liked = false;
            }
        }
    }

    async function getLikes() {
        let queries = [Query.equal("post_id", post.$id)];
        like_count = (
            await sdk.database.listDocuments(collections.likes, queries, 0)
        ).total;
    }

    async function like_post() {
        if (is_logged_in) {
            if (!is_liked) {
                console.log("Liked");

                like_count++;
                is_liked = true;

                if (!liking_process) {
                    liking_process = true;
                    let data = {
                        post_id: post.$id,
                    };

                    let response;
                    try {
                        response = await sdk.functions.createExecution(
                            "like_post",
                            JSON.stringify(data),
                            false
                        );
                    } catch (err) {
                        console.error(err);
                    }

                    response = JSON.parse(response.stdout);
                    if (
                        response.statusCode > 299 ||
                        response.statusCode < 200
                    ) {
                        console.error(response.error);
                    }
                    liking_process = false;
                }
                getLikes();
            } else {
                console.log("unliked");
                unlike_post();
            }
        }
    }

    async function unlike_post() {
        like_count--;
        is_liked = false;
        let data = {
            post_id: post.$id,
        };

        if (!liking_process) {
            liking_process = true;
            let response;
            try {
                response = await sdk.functions.createExecution(
                    "unlike_post",
                    JSON.stringify(data),
                    false
                );
            } catch (err) {
                console.error(err);
            }

            response = JSON.parse(response.stdout);
            if (response.statusCode > 299 || response.statusCode < 200) {
                console.error(response.error);
            }
            liking_process = false;
        }
        getLikes();
    }
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
            <span on:click={like_post} class="icon is-large like-btn">
                {@html like_btn_el}
            </span>
            <p class="is-size-3 mr-2">{like_count}</p>
            <span class="icon is-large cmnt-btn"
                ><i class="fa-regular fa-comment fa-2x" /></span
            >
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
