<script lang="ts">
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import { sdk } from '../appwrite';
    import type { Models } from 'appwrite';

    let account: Models.User<Models.Preferences>;

    onMount(async() => {
        try {
            account = await sdk.account.get();
        } catch (error) {
            navigate("/login");
        }
    });
</script>

{#if account}
    <p>This is the profile from {account.name}</p>    
{/if}
