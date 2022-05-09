<script lang="ts">
    export let comment_list;
</script>

<div class="content">
    {#each comment_list as comment}
        <div class="box comment-box">
            {comment.content}
        </div>
    {/each}
</div>

<style>
    .comment-box {
        padding: 0.5rem !important;
    }
    .comment-box:not(:last-child) {
        margin-bottom: 1rem !important;
    }
</style>
