import { Appwrite } from "appwrite";

const collections = {
    posts: "posts",
    comments: "comments",
};

const sdk = new Appwrite();

sdk
    .setEndpoint('https://appwrite.berlin-fn.de/v1')
    .setProject('pixlr')
;

export { sdk, collections };