<script lang="ts">
    import { navigate } from "svelte-routing";
    import { sdk } from "../appwrite";
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";

    let mail: string = "";
    let password: string = "";
    let password2: string = "";
    let username: string = "";

    let is_not_logged_in: boolean = false;

    let is_signing_up: boolean = false;

    let error_timeout_id: number;
    let show_error_message: boolean = false;
    let error_message: string = "";

    $: is_valid =
        mail && password && password2 && username && password == password2;

    onMount(async () => {
        try {
            await sdk.account.get();
            navigate("/profile");
        } catch (error) {}
        is_not_logged_in = true;
    });

    async function signUp() {
        if (is_valid) {
            try {
                is_signing_up = true;
                await sdk.account.create("unique()", mail, password, username);
                await sdk.account.createSession(mail, password);
                is_signing_up = false;
                window.location.href = "/profile";
            } catch (error) {
                error_message = error.message;
                is_valid = false;
                clearTimeout(error_timeout_id);
                show_error_message = true;
                error_timeout_id = window.setTimeout(
                    async () => (show_error_message = false),
                    3000
                );
                is_signing_up = false;
            }
        }
    }
</script>

{#if is_not_logged_in}
    {#if show_error_message}
        <div
            out:fade
            class="notification is-danger has-text-centered p-2 is-size-6"
        >
            {error_message}
        </div>
    {/if}
    <div class="field">
        <label for="new_mail" class="label">E-Mail</label>
        <div class="control has-icons-left has-icons-right">
            <input
                bind:value={mail}
                id="new_mail"
                class="input"
                type="email"
                placeholder="E-Mail"
                autocomplete="off"
                required
            />
            <span class="icon is-small is-left">
                <i class="fas fa-envelope" />
            </span>
        </div>
    </div>

    <div class="field">
        <label for="new_username" class="label">Username</label>
        <div class="control has-icons-left has-icons-right">
            <input
                bind:value={username}
                id="new_username"
                class="input"
                type="text"
                placeholder="Username"
                autocomplete="off"
                required
            />
            <span class="icon is-small is-left">
                <i class="fas fa-user" />
            </span>
        </div>
    </div>

    <div class="field">
        <label for="password" class="label">Password</label>
        <div class="control has-icons-left has-icons-right">
            <input
                bind:value={password}
                id="password"
                class="input"
                type="password"
                placeholder="Password"
                autocomplete="new-password"
                required
            />
            <span class="icon is-small is-left">
                <i class="fas fa-key" />
            </span>
        </div>
    </div>

    <div class="field">
        <label for="password2" class="label">Repeat Password</label>
        <div class="control has-icons-left has-icons-right">
            <input
                bind:value={password2}
                id="password2"
                class="input"
                type="password"
                placeholder="Repeat Password"
                autocomplete="new-password"
                required
            />
            <span class="icon is-small is-left">
                <i class="fas fa-key" />
            </span>
        </div>
    </div>

    <div class="field">
        <div class="control">
            <button
                on:click={signUp}
                class="button {is_valid ? 'is-success' : ''} {is_signing_up
                    ? 'is-loading'
                    : ''}"
                disabled={!is_valid}>Sign Up</button
            >
        </div>
    </div>
{/if}
