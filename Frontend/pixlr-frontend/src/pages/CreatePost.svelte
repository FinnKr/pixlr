<script lang="ts">
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { sdk } from "../appwrite";
    import type { Models } from "appwrite";
    import ColorPicker from "../components/ColorPicker.svelte";

    interface Position {
        x: number;
        y: number;
    }

    let is_creating: boolean = false;

    let post_title: string = "";

    let account: Models.User<Models.Preferences>;
    let mouseButtonDown: boolean = false;

    let editorCanvas;
    let editorCanvasContext;
    let hCanvas;
    let hCanvasContext;

    let last_pixel: Position = { x: -1, y: -1 };
    let currentColor: string = "#000000";

    $: is_valid = post_title && post_title.length;

    onMount(async () => {
        try {
            account = await sdk.account.get();
        } catch (error) {
            navigate("/login");
        }
    });

    function setEditorContext(node) {
        editorCanvasContext = node.getContext("2d");
    }

    function setHiddenContext(node) {
        hCanvasContext = node.getContext("2d");
    }

    async function mouseDown() {
        mouseButtonDown = true;
    }

    async function mouseUp() {
        mouseButtonDown = false;
    }

    function getMousePos(canvas, evt): Position {
        let rect = canvas.getBoundingClientRect();
        if (evt.type == "touchmove") {
            let touch = evt.touches[0] || evt.changedTouches[0];
            return {
                x: touch.clientX - rect.left,
                y: touch.clientY - rect.top,
            };
        }
        return {
            x: evt.clientX - rect.left,
            y: evt.clientY - rect.top,
        };
    }

    async function drawPixel(event) {
        if (mouseButtonDown || event.type == "touchmove") {
            let pos: Position = getMousePos(editorCanvas, event);
            let pixel: Position = {
                x: pos.x == 0 ? 0 : Math.ceil(pos.x / 10 - 1),
                y: pos.y == 0 ? 0 : Math.ceil(pos.y / 10 - 1),
            };
            if (last_pixel.x != pixel.x && last_pixel.y != pixel.y) {
                editorCanvasContext.fillStyle = currentColor;
                editorCanvasContext.fillRect(
                    pixel.x * 10,
                    pixel.y * 10,
                    10,
                    10
                );

                hCanvasContext.fillStyle = currentColor;
                hCanvasContext.fillRect(pixel.x, pixel.y, 1, 1);
            }
        }
    }

    async function createPost() {
        if (is_valid && !is_creating) {
            is_creating = true;
            let data = {
                title: post_title,
                image64: hCanvas.toDataURL(),
            };

            let response;
            try {
                response = await sdk.functions.createExecution(
                    "create_post",
                    JSON.stringify(data),
                    false
                );
            } catch (err) {}

            response = JSON.parse(response.stdout);
            if (response.statusCode > 299 || response.statusCode < 200) {
                //error
            }
            navigate("/profile");
        }
    }
</script>

<svelte:window on:mouseup={mouseUp} />

{#if account}
    <h1 class="title">Create Post</h1>
    <div class="is-flex editor-full-container-mobile">
        <div class="editorContainer mr-2 mobile-mb-2">
            <canvas
                use:setEditorContext
                bind:this={editorCanvas}
                on:mousemove={(event) => drawPixel(event)}
                on:touchmove|preventDefault={(event) => drawPixel(event)}
                on:mousedown={(event) => {
                    mouseDown();
                    drawPixel(event);
                }}
                width="320px"
                height="320px"
            />
        </div>
        <ColorPicker bind:value={currentColor} />
    </div>

    <div class="columns mt-2">
        <div class="column is-three-quarters">
            <label for="title_input" class="label">Title</label>
            <input
                bind:value={post_title}
                id="title_input"
                class="input mobile-sm-w"
                type="text"
                placeholder="Title"
                maxlength="100"
            />
        </div>
    </div>
    <button
        on:click={createPost}
        class="button {is_valid ? 'is-success' : ''} {is_creating
            ? 'is-loading'
            : ''}"
        disabled={!is_valid}>Create</button
    >

    <!-- Canvas with real 32x32 size for image generation -->
    <div class="is-hidden">
        <canvas
            use:setHiddenContext
            bind:this={hCanvas}
            width="32px"
            height="32px"
        />
    </div>
{/if}

<style>
    .editorContainer {
        border: 2px solid black;
        width: 324px;
        height: 324px;
    }

    @media only screen and (max-width: 768px) {
        .editor-full-container-mobile {
            flex-wrap: wrap;
        }
        .mobile-mb-2 {
            margin-bottom: 1rem;
        }
        .mobile-sm-w {
            width: 340px;
        }
    }
</style>
