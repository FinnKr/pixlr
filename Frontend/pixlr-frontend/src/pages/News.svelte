<script lang="ts">
    import { marked } from 'marked';
    import { onMount } from "svelte";
    import { sdk, collections } from "../appwrite";
    import type { Models } from "appwrite";

    interface NewsEntry extends Models.Document {
        title: string,
        content: string
    }

    const LOAD_DOCUMENT_AMOUNT: number = 3;

    let news: NewsEntry[];
    let news_ids = [];

    let is_loading: boolean = true;

    onMount(async () => {
        news_ids = (await sdk.database.listDocuments(collections.news, [], LOAD_DOCUMENT_AMOUNT, 0, undefined, undefined, ['$id'],['DESC'])).documents;
        news = await getFullNews(news_ids);
        is_loading = false;
    });

    async function getFullNews(document_list: Models.Document[]): Promise<NewsEntry[]> {
        let news: NewsEntry[] = [];
        for (let document of document_list) {
            let news_entry: NewsEntry = await (sdk.database.getDocument(collections.news, document.$id));
            news.push(news_entry);
        }
        return news;
    }

    async function loadMore() {
        let new_news = await getFullNews((await sdk.database.listDocuments(collections.news, [], LOAD_DOCUMENT_AMOUNT, news.length, undefined,undefined,['$id'],['DESC'])).documents);
        news = news.concat(new_news);
    }
</script>

{#if !is_loading}
    <main>
        <h1 class="title">News</h1>
        {#if news}
            {#each news as news_entry (news_entry.$id)}
            <div class="card block">
                <header class="card-header">
                    <p class="card-header-title">
                        {news_entry.title}
                    </p>
                </header>
                <div class="card-content html-content">
                    {@html marked(news_entry.content)}
                </div>
            </div>
            {:else}
                <p>No news to display :(</p>
            {/each}
            {#if news.length == LOAD_DOCUMENT_AMOUNT}
                <p on:click={loadMore} class="load-more-btn">Load More</p>
            {/if}
        {/if}
    </main>
{:else}
    <progress class="progress is-large is-success" max="100">0%</progress>
{/if}

<style>
    .load-more-btn {
        cursor: pointer;
    }
</style>
