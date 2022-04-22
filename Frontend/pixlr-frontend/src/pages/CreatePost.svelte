<script lang="ts">
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import { sdk } from '../appwrite';
    import type { Models } from 'appwrite';

    interface PixelColor {
        color: string
    }

    let account: Models.User<Models.Preferences>;
    let pixel_colors: PixelColor[] = Array<PixelColor>(32*32);
    let ready: boolean = false;
    let mouseButtonDown: boolean = false;

    onMount(async() => {
        try {
            account = await sdk.account.get();
            createPixelArray(32*32);
        } catch (error) {
            console.log(error)
            navigate("/login");
        }
    });
    function createPixelArray(size:number) {
        for (let i = 0; i < size; i++) {
            pixel_colors[i] = {color: i%2==0 ? "white": "black"};
        }
        ready = true;
    }
    function setColor(index: number) {
        if (mouseButtonDown){
            pixel_colors[index].color = "red";
        }
    }
    function mouseDown(){
        mouseButtonDown = true;
    }
    function mouseUp(){
        mouseButtonDown = false;
    }
</script>

<svelte:window on:mousedown|preventDefault="{mouseDown}" on:mouseup|preventDefault="{mouseUp}" />

{#if account}
        <h1>Create Post</h1>
        {#if ready}
            <table style="border-collapse: collapse; margin: auto; margin-top: 75px;">
                {#each Array(32) as _,i}
                    <tr>
                        {#each Array(32) as _,j}
                            <td on:mouseenter={()=>setColor(i*32+j)} style="background-color: {pixel_colors[i*32+j].color}"></td>
                        {/each}
                    </tr>
                {/each}
            </table>
        {/if}
{/if}

<style>
    td {
        width: 10px;
        height: 10px;
        padding: 0;
    }
</style>