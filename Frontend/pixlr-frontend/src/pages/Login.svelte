<script lang="ts">
    import { navigate } from 'svelte-routing';
    import { sdk } from '../appwrite';
    

    let mail: string = '';
    let password: string = '';

    $: is_valid = (mail && password)

    async function login() {
        if (is_valid) {
            try {
                await sdk.account.createSession(mail, password);
                navigate("/profile");
            } catch (error) {
                console.error('Wrong E-Mail or Password');
            }
        }
    }
</script>

<div class="field">
    <label for="mail" class="label">E-Mail</label>
    <div class="control has-icons-left has-icons-right">
        <input bind:value={mail} id="mail" class="input" type="email" placeholder="E-Mail" />
        <span class="icon is-small is-left">
            <i class="fas fa-envelope" />
        </span>
    </div>
</div>

<div class="field">
    <label for="password" class="label">Password</label>
    <div class="control has-icons-left has-icons-right">
        <input bind:value={password} id="password" class="input" type="password" placeholder="Password" />
        <span class="icon is-small is-left">
            <i class="fas fa-key" />
        </span>
    </div>
</div>

<!--div class="field">
    <div class="control">
        <label class="checkbox">
            <input type="checkbox" />
            I agree to the <a href="/">terms and conditions</a>
        </label>
    </div>
</div-->

<div class="field">
    <div class="control">
        <button on:click="{login}" class="button {is_valid ? 'is-success' : ''}" disabled={!is_valid}>Submit</button>
    </div>
</div>
