import { Appwrite } from "appwrite";

const collections = {
    posts: "posts",
    comments: "comments",
    likes: "likes",
    news: "news"
};

const buckets = {
    post_images: "post_images"
};

const sdk = new Appwrite();

sdk
    .setEndpoint('https://appwrite.berlin-fn.de/v1')
    .setProject('pixlr')
    ;

async function isLoggedIn(): Promise<boolean> {
    try {
        await sdk.account.get();
        return true;
    } catch {
        return false;
    }
}

export { sdk, collections, buckets, isLoggedIn };