<script lang="ts">
    import { navigate } from "svelte-routing";
    import { sdk } from "../appwrite";
    import { onMount } from "svelte";

    let mail: string = "";
    let password: string = "";

    let is_logging_in: boolean = false;

    let is_not_logged_in: boolean = false;

    $: is_valid = mail && password;

    onMount(async () => {
        try {
            await sdk.account.get();
            navigate("/profile");
        } catch (error) {}
        is_not_logged_in = true;
    });

    async function login() {
        if (is_valid) {
            try {
                is_logging_in = true;
                await sdk.account.createSession(mail, password);
                is_logging_in = false;
                window.location.href = "/profile";
            } catch (error) {
                console.error("Wrong E-Mail or Password");
                is_logging_in = false;
            }
        }
    }
</script>

{#if is_not_logged_in}
    <div class="field">
        <label for="mail" class="label">E-Mail</label>
        <div class="control has-icons-left has-icons-right">
            <input
                bind:value={mail}
                id="mail"
                class="input"
                type="email"
                placeholder="E-Mail"
                required
            />
            <span class="icon is-small is-left">
                <i class="fas fa-envelope" />
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
                on:click={login}
                class="button {is_valid ? 'is-success' : ''} {is_logging_in
                    ? 'is-loading'
                    : ''}"
                disabled={!is_valid}>Submit</button
            >
        </div>
    </div>
{/if}
