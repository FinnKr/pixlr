<script lang="ts">
    import { onMount } from "svelte";
    import { sdk, collections, buckets } from "../appwrite";
    import { Models, Query } from "appwrite";
    import { Link } from "svelte-routing";
    import CommentSection from "./CommentSection.svelte";

    export let id: string;
    export let is_logged_in: boolean;
    export let can_delete: boolean = false;

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

    let comment_count: number;

    let loading: boolean = true;

    let liking_process: boolean = false;

    let showNotLoggedInModal: boolean = false;
    let showCommentSectionModal: boolean = false;
    let showDeleteWarningModal: boolean = false;

    let comment_content: string = "";
    let is_commenting: boolean = false;
    let comment_list = null;

    let is_deleting: boolean = false;

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
        await getCommentCount();
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

    async function getCommentCount() {
        let queries = [Query.equal("post_id", post.$id)];
        comment_count = (
            await sdk.database.listDocuments(collections.comments, queries, 0)
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
        } else {
            showNotLoggedInModalF();
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

    async function hideModals() {
        showNotLoggedInModal = false;
        showCommentSectionModal = false;
        showDeleteWarningModal = false;
        document.documentElement.classList.remove("is-clipped");
    }

    async function showNotLoggedInModalF() {
        showNotLoggedInModal = true;
        document.documentElement.classList.add("is-clipped");
    }

    async function showCommentSectionModalF() {
        fetchComments();
        showCommentSectionModal = true;
        document.documentElement.classList.add("is-clipped");
    }

    async function showDeleteWarningModalF() {
        showDeleteWarningModal = true;
        document.documentElement.classList.add("is-clipped");
    }

    async function createComment() {
        if (comment_content && !is_commenting) {
            is_commenting = true;
            let response;
            try {
                let data = {
                    content: comment_content,
                    post_id: post.$id 
                };
                response = await sdk.functions.createExecution(
                    "create_comment",
                    JSON.stringify(data),
                    false
                );
            } catch (error) {
                console.error(error);
            }

            response = JSON.parse(response.stdout);
            if (response.statusCode > 299 || response.statusCode < 200) {
                console.error(response.error);
            }
            fetchComments();
            getCommentCount();
            comment_content = '';
        }
        is_commenting = false;
    }

    async function fetchComments() {
        comment_list = null;
        let comment_docs = [];
        let comments = [];
        let queries = [Query.equal("post_id", post.$id)];
        try {
            comment_docs = (await sdk.database.listDocuments(collections.comments, queries, 10, 0, undefined, undefined, ['$id'],['DESC'])).documents;
        } catch (error) {
            console.error(error);
        }
        for (let comment_doc of comment_docs){
            try {
                let comment = (await sdk.database.getDocument(collections.comments, comment_doc.$id));
                comments.push(comment);
            } catch (error) {}
        }
        comment_list = comments;
    }

    async function loadMoreComments() {
        let comment_docs = [];
        let comments = [];
        let queries = [Query.equal("post_id", post.$id)];
        try {
            comment_docs = (await sdk.database.listDocuments(collections.comments, queries, 10, comment_list.length, undefined,undefined,['$id'],['DESC'])).documents;
        } catch(error) {
            console.error(error);
        }
        for (let comment_doc of comment_docs){
            try {
                let comment = (await sdk.database.getDocument(collections.comments, comment_doc.$id));
                comments.push(comment);
            } catch (error) {}
        }
        comment_list = comment_list.concat(comments);
    }

    async function deletePost() {
        if (can_delete && !is_deleting) {
            is_deleting = true;
            let response;
            try {
                let data = {
                    post_id: post.$id
                };
                response = await sdk.functions.createExecution(
                    "delete_post",
                    JSON.stringify(data),
                    false
                );
            } catch (error) {
                console.error(error);
            }

            response = JSON.parse(response.stdout);
            if (response.statusCode > 299 || response.statusCode < 200) {
                console.error(response.error);
            }
            window.location.reload();
        }
        is_deleting = false;
    }
</script>

{#if showNotLoggedInModal}
    <div class="modal is-active">
        <div on:click={hideModals} class="modal-background" />
        <div class="modal-content">
            <div class="notification is-success has-text-centered">
                You need to be <Link to="/login"
                    ><strong>logged in</strong></Link
                > to like a post.
            </div>
        </div>
        <button
            on:click={hideModals}
            class="modal-close is-large"
            aria-label="close"
        />
    </div>
{/if}

{#if showDeleteWarningModal}
    <div class="modal is-active">
        <div on:click={hideModals} class="modal-background" />
        <div class="modal-content">
            <div class="notification is-danger has-text-centered">
                <p>Do you really want to delete this post?</p>
                <p class="mb-1">This cannot be undone!</p>
                <button on:click={deletePost} class="button is-danger is-light {is_deleting ? 'is-loading' : ''}">Delete Post</button>
            </div>
        </div>
        <button
            on:click={hideModals}
            class="modal-close is-large"
            aria-label="close"
        />
    </div>
{/if}

{#if showCommentSectionModal}
    <div class="modal is-active">
        <div on:click={hideModals} class="modal-background" />
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Comments</p>
                <button on:click={hideModals} class="delete" aria-label="close" />
            </header>
            <section class="modal-card-body">
                {#if comment_list != null}
                    {#if comment_list.length}
                        <CommentSection comment_list={comment_list} />
                        {#if comment_list.length == 10}
                            <span on:click={loadMoreComments} class="load-more-btn"><i>Load More</i></span>
                        {/if}
                    {:else}
                        <p>No comments</p>
                    {/if}
                {:else}
                    <progress class="progress is-large is-success" max="100">0%</progress>
                {/if}
            </section>
            {#if is_logged_in}
                <footer class="modal-card-foot">
                    <div class="container">
                        <textarea
                            bind:value={comment_content}
                            id="comment_input"
                            class="textarea is-success"
                            placeholder="Comment"
                            maxlength="255"
                        />
                        <button
                            on:click={createComment}
                            class="button {comment_content
                                ? 'is-success'
                                : ''} {is_commenting ? 'is-loading' : ''} mt-2"
                            disabled={!comment_content}>Create</button
                        >
                    </div>
                </footer>
            {/if}
        </div>
        <button
            on:click={hideModals}
            class="modal-close is-large"
            aria-label="close"
        />
    </div>
{/if}

{#if !loading}
    <div class="card block">
        <header class="card-header">
            <p class="card-header-title">
                {post.title}
            </p>
            {#if can_delete}
            <span on:click={showDeleteWarningModalF} class="icon is-small is-large" style="cursor: pointer;">
                <i class="das fa-solid fa-trash-can"></i>
            </span>
            {/if}
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
            <span
                on:click={showCommentSectionModalF}
                class="icon is-large cmnt-btn"
                ><i class="fa-regular fa-comment fa-2x" />
            </span>
            <p class="is-size-3">{comment_count}</p>
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
    .load-more-btn {
        cursor: pointer;
    }
</style>
