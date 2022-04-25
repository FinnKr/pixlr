<script lang="ts">
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { sdk } from "../appwrite";
    import type { Models } from "appwrite";

    let account: Models.User<Models.Preferences>;
    let displayed_name: string = "";

    onMount(async () => {
        try {
            account = await sdk.account.get();
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
</script>

{#if account}
    <p>This is the profile from {displayed_name}</p>
{/if}
